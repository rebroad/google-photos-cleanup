from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from .chrome_collector import CdpError, _WebSocket
from .headless_chrome_collector import headless_chrome
from .obscura_cdp_collector import _read_session_file


def _page_target(endpoint: str) -> dict[str, object]:
    with urllib.request.urlopen(f"{endpoint}/json/list", timeout=5) as response:
        targets = json.load(response)
    for target in targets:
        if (isinstance(target, dict) and target.get("type") == "page"
                and str(target.get("url", "")).startswith("https://photos.google.com")
                and isinstance(target.get("webSocketDebuggerUrl"), str)):
            return target
    raise CdpError("headless Chromium did not create a Google Photos page target")


def _expression(items: list[dict[str, str]]) -> str:
    encoded = json.dumps(items, separators=(",", ":"))
    return f"""
(async () => {{
  const input = {encoded};
  const hash = async (item) => {{
    try {{
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 2000);
      const response = await fetch(item.url, {{credentials: "include", signal: controller.signal}});
      clearTimeout(timer);
      if (!response.ok) return {{id: item.id, phash: null}};
      const bitmap = await createImageBitmap(await response.blob());
      const canvas = document.createElement("canvas");
      canvas.width = 16; canvas.height = 16;
      const context = canvas.getContext("2d", {{willReadFrequently: true}});
      context.drawImage(bitmap, 0, 0, 16, 16); bitmap.close();
      const pixels = context.getImageData(0, 0, 16, 16).data;
      const values = []; let total = 0;
      for (let i = 0; i < pixels.length; i += 4) {{
        const value = 0.299 * pixels[i] + 0.587 * pixels[i + 1] + 0.114 * pixels[i + 2];
        values.push(value); total += value;
      }}
      const average = total / values.length;
      return {{id: item.id, phash: values.map(value => value >= average ? "1" : "0").join("")}};
    }} catch (_) {{ return {{id: item.id, phash: null}}; }}
  }};
  const result = [];
  for (let i = 0; i < input.length; i += 8)
    result.push(...await Promise.all(input.slice(i, i + 8).map(hash)));
  return result;
}})()
"""


def collect(chrome: str, profile_dir: str, session_file: str, source: str,
            output: str, port: int = 9222, batch_size: int = 32) -> None:
    payload = json.loads(Path(source).read_text(encoding="utf-8"))
    records = payload.get("media_items", []) if isinstance(payload, dict) else payload
    jobs = [
        {"id": str(item["id"]), "url": str(item["source_url"])}
        for item in records if isinstance(item, dict) and item.get("id") and item.get("source_url")
    ]
    hashes: dict[str, str] = {}
    session = _read_session_file(session_file)
    with headless_chrome(chrome, profile_dir, port, "https://photos.google.com/") as endpoint:
        target = _page_target(endpoint)
        ws_url = str(target["webSocketDebuggerUrl"])
        parsed = urllib.parse.urlsplit(ws_url)
        ws = _WebSocket(ws_url, host_header=parsed.netloc, timeout=30)
        try:
            ws.call("Network.setCookies", {"cookies": session})
            ws.call("Page.navigate", {"url": "https://photos.google.com/"})
        finally:
            ws.close()
        time.sleep(5)
        target = _page_target(endpoint)
        ws_url = str(target["webSocketDebuggerUrl"])
        parsed = urllib.parse.urlsplit(ws_url)
        ws = _WebSocket(ws_url, host_header=parsed.netloc, timeout=30)
        try:
            for offset in range(0, len(jobs), max(1, batch_size)):
                result = ws.call("Runtime.evaluate", {
                    "expression": _expression(jobs[offset:offset + max(1, batch_size)]),
                    "awaitPromise": True, "returnByValue": True,
                })
                values = result.get("result", {}).get("result", {}).get("value", [])
                for item in values if isinstance(values, list) else []:
                    if isinstance(item, dict) and isinstance(item.get("phash"), str):
                        hashes[str(item["id"])] = item["phash"]
        finally:
            ws.close()
    output_items = []
    for item in records:
        if not isinstance(item, dict):
            continue
        copy = {key: value for key, value in item.items() if key != "source_url"}
        if str(item.get("id")) in hashes:
            copy["phash"] = hashes[str(item["id"])]
        output_items.append(copy)
    result = {key: value for key, value in payload.items() if key != "media_items"} if isinstance(payload, dict) else {}
    result["media_items"] = output_items
    Path(output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.cloud_fingerprint_cli")
    parser.add_argument("--chrome", required=True)
    parser.add_argument("--profile-dir", required=True)
    parser.add_argument("--session-file", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--port", type=int, default=9222)
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args(argv)
    try:
        collect(args.chrome, args.profile_dir, args.session_file, args.input, args.output, args.port, args.batch_size)
    except (CdpError, OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
