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
            port: int = 9222) -> None:
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
        ws = _WebSocket(ws_url, host_header=parsed.netloc, timeout=15)
        try:
            ws.call("Network.setCookies", {"cookies": _read_session_file(session_file)})
            ws.call("Page.navigate", {"url": url})
        finally:
            ws.close()
        time.sleep(5)
        value = _collect_endpoint(endpoint, url, max_scrolls)
        from .obscura_collector import write_cloud_records
        write_cloud_records(value, output)
