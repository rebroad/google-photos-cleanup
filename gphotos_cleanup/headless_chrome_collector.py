from __future__ import annotations

import subprocess
import time
import json
import urllib.parse
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .chrome_collector import CdpError, _WebSocket, _collect_endpoint
from .obscura_cdp_collector import _read_session_file


@contextmanager
def headless_chrome(chrome: str, profile_dir: str, port: int, url: str) -> Iterator[str]:
    profile = Path(profile_dir).expanduser().resolve()
    if profile.is_relative_to(Path.cwd().resolve()):
        raise CdpError("headless Chrome profile must be outside the repository")
    profile.mkdir(parents=True, exist_ok=True)
    process = subprocess.Popen([
        chrome, "--headless=new", "--disable-gpu", "--no-first-run",
        "--no-default-browser-check", f"--remote-debugging-port={port}",
        f"--user-data-dir={profile}", url,
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    endpoint = f"http://127.0.0.1:{port}"
    try:
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise CdpError("headless Chromium exited before becoming ready")
            try:
                with urllib.request.urlopen(f"{endpoint}/json/version", timeout=1):
                    yield endpoint
                    return
            except OSError:
                time.sleep(0.2)
        raise CdpError("headless Chromium did not expose DevTools")
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def collect(chrome: str, profile_dir: str, session_file: str, output: str,
            url: str = "https://photos.google.com/", max_scrolls: int = 20000,
            port: int = 9222, chunk_scrolls: int = 100, fingerprint: bool = True,
            include_source_urls: bool = False) -> None:
    session = _read_session_file(session_file)
    cookie_header = "; ".join(f"{item['name']}={item['value']}" for item in session)
    merged: dict[str, dict[str, object]] = {}
    total_scrolls = 0
    start_scroll_top = 0
    final_value: dict[str, object] = {}
    complete = False
    checkpoint = Path(output + ".partial")
    if checkpoint.exists():
        saved = json.loads(checkpoint.read_text(encoding="utf-8"))
        if isinstance(saved, dict):
            total_scrolls = int(saved.get("scroll_count", 0))
            start_scroll_top = int(saved.get("scroll_top", 0))
            complete = bool(saved.get("complete", False))
            final_value = saved
            for item in saved.get("media", []):
                if isinstance(item, dict) and item.get("src"):
                    merged[str(item["src"])] = item
    while total_scrolls < max(1, max_scrolls):
        chunk = min(max(1, chunk_scrolls), max(1, max_scrolls) - total_scrolls)
        previous_start = start_scroll_top
        for attempt in range(3):
            try:
                with headless_chrome(chrome, profile_dir, port, url) as endpoint:
                    with urllib.request.urlopen(f"{endpoint}/json/list", timeout=5) as response:
                        targets = json.load(response)
                    pages = [
                        target for target in targets
                        if isinstance(target, dict)
                        and target.get("type") == "page"
                        and str(target.get("url", "")).startswith("https://photos.google.com")
                        and isinstance(target.get("webSocketDebuggerUrl"), str)
                    ]
                    if not pages:
                        raise CdpError("headless Chromium did not create a Google Photos page target")
                    target = pages[0]
                    ws_url = str(target["webSocketDebuggerUrl"])
                    parsed = urllib.parse.urlsplit(ws_url)
                    ws = _WebSocket(ws_url, host_header=parsed.netloc, timeout=45)
                    try:
                        ws.call("Network.setCookies", {"cookies": session})
                        ws.call("Page.navigate", {"url": url})
                    finally:
                        ws.close()
                    time.sleep(5)
                    final_value = _collect_endpoint(endpoint, url, chunk, start_scroll_top, fingerprint)
                break
            except (CdpError, OSError, RuntimeError, ValueError):
                if attempt == 2:
                    checkpoint.write_text(json.dumps({
                        **final_value,
                        "media": list(merged.values()),
                        "scroll_count": total_scrolls,
                        "scroll_top": start_scroll_top,
                        "complete": False,
                    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                    raise
                time.sleep(2)
        for item in final_value.get("media", []):
            if isinstance(item, dict) and item.get("src"):
                merged[str(item["src"])] = item
        progressed = int(final_value.get("scroll_count", 0))
        total_scrolls += progressed
        complete = bool(final_value.get("complete"))
        start_scroll_top = int(final_value.get("scroll_top", start_scroll_top))
        if complete:
            break
        if progressed <= 0 or start_scroll_top <= previous_start:
            raise CdpError("Google Photos scroll position did not advance between headless chunks")
        checkpoint.write_text(json.dumps({
            **final_value,
            "media": list(merged.values()),
            "scroll_count": total_scrolls,
            "scroll_top": start_scroll_top,
            "complete": False,
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    final_value["media"] = list(merged.values())
    final_value["scroll_count"] = total_scrolls
    final_value["complete"] = complete
    final_value["reached_end"] = complete
    from .obscura_collector import write_cloud_records
    write_cloud_records(final_value, output, cookie_header=cookie_header, include_source_urls=include_source_urls)
