from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from .chrome_collector import (
    CdpError,
    _WebSocket,
    _chrome_page_websocket_url,
    adb_chrome_forward,
    connected_adb_serial,
)


def _default_output() -> str:
    prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    return os.path.join(prefix, "tmp", "google-photos-session.json")


def _relevant_domain(domain: str) -> bool:
    host = domain.lstrip(".").lower()
    return (
        host == "google.com"
        or host.endswith(".google.com")
        or host == "google.co.uk"
        or host.endswith(".google.co.uk")
        or host.endswith(".googleusercontent.com")
        or host.endswith(".usercontent.google.com")
    )


def export_session(serial: str, output: str) -> int:
    with adb_chrome_forward(serial) as port:
        endpoint = f"http://127.0.0.1:{port}"
        return export_session_endpoint(endpoint, output)


def _any_page_websocket_url(endpoint: str) -> tuple[str, str]:
    with urllib.request.urlopen(endpoint.rstrip("/") + "/json/list", timeout=5) as response:
        targets = json.load(response)
    for target in targets:
        if (isinstance(target, dict) and target.get("type") == "page"
                and isinstance(target.get("webSocketDebuggerUrl"), str)):
            ws_url = str(target["webSocketDebuggerUrl"])
            parsed = urllib.parse.urlsplit(ws_url)
            if parsed.scheme == "ws" and parsed.netloc and parsed.path:
                return ws_url, parsed.netloc
    raise CdpError("Chrome returned no page target for cookie export")


def export_session_endpoint(endpoint: str, output: str) -> int:
    # Cookie export is deliberately explicit and filtered below. It does not
    # export passwords, local storage, or arbitrary browser profile files.
    ws_url, host_header = _any_page_websocket_url(endpoint)
    ws = _WebSocket(ws_url, host_header=host_header, timeout=15)
    try:
        result = ws.call("Network.getAllCookies")
    finally:
        ws.close()
    cookies = [
        cookie for cookie in result.get("result", {}).get("cookies", [])
        if isinstance(cookie, dict) and _relevant_domain(str(cookie.get("domain", "")))
    ]
    if not cookies:
        raise CdpError("Chrome returned no Google authentication cookies")
    output_path = Path(output).expanduser().resolve()
    if output_path.is_relative_to(Path.cwd().resolve()):
        raise CdpError("session output must be outside the repository")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "gphotos-cleanup/google-session/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cookies": cookies,
    }
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(output_path, flags, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
    finally:
        try:
            os.chmod(output_path, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass
    return len(cookies)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.chrome_auth_cli")
    parser.add_argument("--serial", help="ADB serial; omitted when exactly one device is connected")
    parser.add_argument("--cdp-endpoint", help="Chrome DevTools HTTP endpoint, e.g. http://127.0.0.1:19223")
    parser.add_argument("--output", default=_default_output())
    args = parser.parse_args(argv)
    try:
        if args.cdp_endpoint:
            count = export_session_endpoint(args.cdp_endpoint, args.output)
        else:
            serial = args.serial or connected_adb_serial()
            count = export_session(serial, args.output)
        print(f"Exported {count} filtered Google cookies to {args.output}")
        print("Cookie values are local authentication state; keep this file outside Git.", file=sys.stderr)
    except (CdpError, OSError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
