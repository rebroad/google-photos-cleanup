from __future__ import annotations

import base64
import json
import os
import socket
import struct
import time
import subprocess
import urllib.parse
import urllib.request
from contextlib import contextmanager
from typing import Iterator

from .obscura_collector import write_cloud_records


class CdpError(RuntimeError):
    """The live Chrome DevTools session could not complete a command."""


class _WebSocket:
    def __init__(self, url: str, host_header: str | None = None, timeout: float = 120.0):
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "ws" or not parsed.hostname or not parsed.port:
            raise CdpError("Chrome returned an invalid DevTools WebSocket URL")
        self.sock = socket.create_connection((parsed.hostname, parsed.port), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request = (
            f"GET {parsed.path or '/'} HTTP/1.1\r\n"
            f"Host: {host_header or f'{parsed.hostname}:{parsed.port}'}\r\n"
            "Upgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        ).encode()
        self.sock.sendall(request)
        header = b""
        while b"\r\n\r\n" not in header:
            block = self.sock.recv(4096)
            if not block:
                raise CdpError("Chrome closed the DevTools handshake")
            header += block
        if b" 101 " not in header.split(b"\r\n", 1)[0]:
            raise CdpError("Chrome rejected the DevTools WebSocket handshake")
        self.next_id = 0

    def close(self) -> None:
        self.sock.close()

    def _send_frame(self, opcode: int, payload: bytes) -> None:
        mask = os.urandom(4)
        size = len(payload)
        if size < 126:
            header = bytes([0x80 | opcode, 0x80 | size])
        elif size < 65536:
            header = bytes([0x80 | opcode, 0x80 | 126]) + struct.pack(">H", size)
        else:
            header = bytes([0x80 | opcode, 0x80 | 127]) + struct.pack(">Q", size)
        masked = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def _receive_frame(self) -> tuple[int, bytes]:
        def receive_exact(size: int) -> bytes:
            data = bytearray()
            while len(data) < size:
                block = self.sock.recv(size - len(data))
                if not block:
                    raise CdpError("Chrome closed the DevTools connection")
                data.extend(block)
            return bytes(data)

        header = receive_exact(2)
        opcode = header[0] & 0x0F
        size = header[1] & 0x7F
        masked = bool(header[1] & 0x80)
        if size == 126:
            size = struct.unpack(">H", receive_exact(2))[0]
        elif size == 127:
            size = struct.unpack(">Q", receive_exact(8))[0]
        mask = receive_exact(4) if masked else b""
        payload = bytearray(receive_exact(size))
        if masked:
            payload = bytearray(value ^ mask[index % 4] for index, value in enumerate(payload))
        return opcode, bytes(payload)

    def call(self, method: str, params: dict[str, object] | None = None, session: str | None = None) -> dict[str, object]:
        self.next_id += 1
        request: dict[str, object] = {"id": self.next_id, "method": method}
        if params is not None:
            request["params"] = params
        if session:
            request["sessionId"] = session
        self._send_frame(1, json.dumps(request, separators=(",", ":")).encode())
        while True:
            opcode, payload = self._receive_frame()
            if opcode == 9:
                self._send_frame(10, payload)
                continue
            if opcode != 1:
                continue
            message = json.loads(payload)
            if message.get("id") != self.next_id:
                continue
            if "error" in message:
                raise CdpError(str(message["error"]))
            return message


def _chrome_page_websocket_url(endpoint: str, attempts: int = 2) -> tuple[str, str, str]:
    endpoint = endpoint.rstrip("/")
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            targets = None
            for path in ("/json/list", "/json"):
                try:
                    with urllib.request.urlopen(f"{endpoint}{path}", timeout=2) as response:
                        targets = json.load(response)
                    break
                except (OSError, json.JSONDecodeError):
                    continue
            if not isinstance(targets, list):
                raise ValueError("Chrome returned no DevTools target list")
            pages = [
                target for target in targets
                if isinstance(target, dict)
                and target.get("type") == "page"
                and urllib.parse.urlsplit(str(target.get("url", ""))).netloc == "photos.google.com"
                and isinstance(target.get("webSocketDebuggerUrl"), str)
            ]
            if not pages:
                raise ValueError("Chrome has no Google Photos page target")
            root_pages = [
                page for page in pages
                if str(page.get("url", "")).rstrip("/") == "https://photos.google.com"
            ]
            candidates = root_pages or pages
            responsive: list[tuple[int, dict[str, object], str, str]] = []
            for target in candidates:
                url = str(target["webSocketDebuggerUrl"])
                parsed = urllib.parse.urlsplit(url)
                if parsed.scheme != "ws" or not parsed.path:
                    continue
                probe = None
                try:
                    probe = _WebSocket(url, host_header=parsed.netloc, timeout=3)
                    result = probe.call("Runtime.evaluate", {
                        "expression": "JSON.stringify({href: location.href, media: document.querySelectorAll('img,video').length})",
                        "returnByValue": True,
                    })
                    value = result.get("result", {}).get("result", {}).get("value")
                    details = json.loads(value) if isinstance(value, str) else {}
                    if details.get("href") != str(target.get("url", "")):
                        continue
                    responsive.append((int(details.get("media", 0)), target, url, parsed.netloc))
                except (CdpError, OSError, TimeoutError, ValueError, TypeError, json.JSONDecodeError):
                    continue
                finally:
                    if probe is not None:
                        probe.close()
            if responsive:
                _, target, url, host = max(responsive, key=lambda item: item[0])
                keep_id = str(target.get("id", target.get("targetId", "")))
                for extra in pages:
                    extra_id = str(extra.get("id", extra.get("targetId", "")))
                    if extra_id and extra_id != keep_id:
                        try:
                            with urllib.request.urlopen(
                                f"{endpoint}/json/close/{urllib.parse.quote(extra_id, safe='')}",
                                timeout=2,
                            ):
                                pass
                        except OSError:
                            pass
                return url, host, str(target.get("url", ""))
            raise ValueError("Google Photos targets are not ready for DevTools commands")
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(0.5)
    raise CdpError(
        "Chrome DevTools is unavailable; keep an authenticated Google Photos tab open "
        "or provide a dedicated CDP endpoint"
    ) from last_error


def connected_adb_serial() -> str:
    try:
        result = subprocess.run(
            ["adb", "devices"],
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )
    except subprocess.TimeoutExpired as error:
        raise CdpError("timed out listing ADB devices") from error
    if result.returncode:
        raise CdpError(result.stderr.strip() or "could not list ADB devices")
    devices = [
        line.split()[0]
        for line in result.stdout.splitlines()
        if len(line.split()) == 2 and line.split()[1] == "device"
    ]
    if len(devices) != 1:
        if not devices:
            raise CdpError("no ADB device is connected; provide --serial or use --cdp-endpoint")
        raise CdpError("multiple ADB devices are connected; provide --serial explicitly")
    return devices[0]


def adb_open_google_photos(serial: str, url: str) -> None:
    try:
        result = subprocess.run(
            [
                "adb", "-s", serial, "shell", "am", "start",
                "-a", "android.intent.action.VIEW",
                "-d", url,
                "-p", "com.android.chrome",
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=15,
        )
    except subprocess.TimeoutExpired as error:
        raise CdpError("timed out opening Google Photos in Chrome through ADB") from error
    if result.returncode:
        raise CdpError(result.stderr.strip() or "could not open Google Photos in Chrome")


@contextmanager
def adb_chrome_forward(serial: str) -> Iterator[int]:
    command = ["adb", "-s", serial, "forward", "tcp:0", "localabstract:chrome_devtools_remote"]
    try:
        result = subprocess.run(command, text=True, capture_output=True, check=False, timeout=15)
    except subprocess.TimeoutExpired as error:
        raise CdpError("timed out forwarding Chrome DevTools through ADB") from error
    if result.returncode:
        raise CdpError(result.stderr.strip() or "could not forward Chrome DevTools")
    try:
        port = int(result.stdout.strip())
    except ValueError as error:
        raise CdpError("ADB did not return the allocated Chrome DevTools port") from error
    try:
        yield port
    finally:
        subprocess.run(
            ["adb", "-s", serial, "forward", "--remove", f"tcp:{port}"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )


EXTRACT_AND_SCROLL = r"""
(async () => {
  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
  const media = new Map();
  const collect = () => {
    const nodes = [...document.querySelectorAll("img,video,div.qs41qe,div[class*=\"qs41qe\"]")];
    for (const node of nodes) {
      const tag = node.tagName.toLowerCase();
      const rect = node.getBoundingClientRect();
      if (!node.currentSrc && !node.src &&
          (rect.width < 50 || rect.height < 50)) continue;
      const style = getComputedStyle(node);
      const background = style.backgroundImage || "";
      const backgroundMatch = background.match(/url\(["\x27]?([^"\x27)]+)["\x27]?\)/);
      const src = node.currentSrc || node.src ||
        (backgroundMatch ? backgroundMatch[1] : "");
      if (!src) continue;
      const label = [node.alt, node.getAttribute("aria-label"), node.title,
        node.parentElement && node.parentElement.getAttribute("aria-label")]
        .filter(Boolean).join(" ");
      const kind = tag === "video" || /\bvideo\b|play/i.test(label)
        ? "video" : "image";
      media.set(src, {
        tag, kind, src, alt: node.alt || label,
        width: node.naturalWidth || node.videoWidth || 0,
        height: node.naturalHeight || node.videoHeight || 0
      });
    }
  };
  const root = document.scrollingElement || document.documentElement;
  const scrollables = [root, ...document.querySelectorAll('*')]
    .filter(node => node.scrollHeight > node.clientHeight + 100);
  const scroller = scrollables.reduce(
    (best, node) => (node.scrollHeight - node.clientHeight) >
      (best.scrollHeight - best.clientHeight) ? node : best,
    root
  );
  scroller.scrollTop = Math.min(__START_SCROLL_TOP__, Math.max(0, scroller.scrollHeight - scroller.clientHeight));
  await delay(500);
  collect();
  let stagnant = 0;
  let reachedEnd = false;
  let scrollCount = 0;
  for (let index = 0; index < __MAX_SCROLLS__; index++) {
    const before = media.size;
    const maximum = Math.max(0, scroller.scrollHeight - scroller.clientHeight);
    const step = Math.max(1800, scroller.clientHeight * 2.5);
    const next = Math.min(scroller.scrollTop + step, maximum);
    scroller.scrollTop = next;
    await delay(200);
    collect();
    scrollCount = index + 1;
    stagnant = media.size === before ? stagnant + 1 : 0;
    if (next >= maximum - 4 && stagnant >= 5) {
      reachedEnd = true;
      break;
    }
  }
  if (__FINGERPRINT__) {
  const hashImage = async (item) => {
    if (item.kind !== "image") return null;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 2000);
    try {
      const response = await fetch(item.src, {credentials: "include", signal: controller.signal});
      clearTimeout(timer);
      if (!response.ok) return null;
      const bitmap = await createImageBitmap(await response.blob());
      const canvas = document.createElement("canvas");
      canvas.width = 16;
      canvas.height = 16;
      const context = canvas.getContext("2d", {willReadFrequently: true});
      context.drawImage(bitmap, 0, 0, 16, 16);
      bitmap.close();
      const pixels = context.getImageData(0, 0, 16, 16).data;
      const values = [];
      let total = 0;
      for (let index = 0; index < pixels.length; index += 4) {
        const gray = 0.299 * pixels[index] + 0.587 * pixels[index + 1] +
          0.114 * pixels[index + 2];
        values.push(gray);
        total += gray;
      }
      const average = total / values.length;
      item.phash = values.map(value => value >= average ? "1" : "0").join("");
      return item.phash;
    } catch (_) {
      return null;
    }
  };
  const candidates = Array.from(media.values()).filter(item => item.kind === "image" && !item.phash);
  for (let index = 0; index < candidates.length; index += 8) {
    await Promise.all(candidates.slice(index, index + 8).map(hashImage));
  }
  }
  const text = document.body ? document.body.innerText : '';
  const host = location.hostname;
  return {
    url: location.href,
    title: document.title,
    authenticated: host === 'photos.google.com' && !/sign[ -]?in|choose an account/i.test(text),
    media: Array.from(media.values()),
    complete: reachedEnd,
    reached_end: reachedEnd,
    scroll_count: scrollCount,
    scroll_height: scroller.scrollHeight,
    scroll_top: scroller.scrollTop
  };
})()
"""


def _wait_for_execution_context(ws: _WebSocket, attempts: int = 15) -> None:
    for attempt in range(attempts):
        try:
            ws.call("Runtime.evaluate", {"expression": "location.href", "returnByValue": True})
            return
        except CdpError as error:
            if "execution context" not in str(error).lower() or attempt == attempts - 1:
                raise
            time.sleep(1)


def collect(
    serial: str | None = None,
    url: str = "https://photos.google.com/",
    max_scrolls: int = 20000,
    cdp_endpoint: str | None = None,
    open_chrome: bool = True,
) -> dict[str, object]:
    if cdp_endpoint:
        return _collect_endpoint(cdp_endpoint, url, max_scrolls)
    if not serial:
        raise CdpError("provide --serial for phone Chrome or --cdp-endpoint for local Chrome")
    with adb_chrome_forward(serial) as port:
        endpoint = f"http://127.0.0.1:{port}"
        if open_chrome:
            try:
                _chrome_page_websocket_url(endpoint)
            except CdpError:
                adb_open_google_photos(serial, url)
                time.sleep(3)
        return _collect_endpoint(endpoint, url, max_scrolls)


def _collect_endpoint(endpoint: str, url: str, max_scrolls: int, start_scroll_top: int = 0, fingerprint: bool = True) -> dict[str, object]:
    ws_url, host_header, current_url = _chrome_page_websocket_url(endpoint)
    ws = _WebSocket(ws_url, host_header=host_header)
    try:
        if current_url.rstrip("/") != url.rstrip("/"):
            ws.call("Page.navigate", {"url": url})
        expression = EXTRACT_AND_SCROLL.replace("__MAX_SCROLLS__", str(max(1, min(max_scrolls, 20000)))).replace("__START_SCROLL_TOP__", str(max(0, start_scroll_top))).replace("__FINGERPRINT__", "true" if fingerprint else "false")
        result = ws.call(
            "Runtime.evaluate",
            {"expression": expression, "awaitPromise": True, "returnByValue": True},
        )
        value = result.get("result", {}).get("result", {}).get("value")
        if not isinstance(value, dict):
            raise CdpError("Chrome returned no Photos extraction result")
        if not value.get("authenticated"):
            raise CdpError("Chrome is not authenticated to Google Photos; sign in with Chrome first")
        return value
    finally:
        ws.close()


def collect_to_file(
    output: str,
    serial: str | None = None,
    url: str = "https://photos.google.com/",
    max_scrolls: int = 20000,
    cdp_endpoint: str | None = None,
    open_chrome: bool = True,
) -> None:
    value = collect(serial, url, max_scrolls, cdp_endpoint, open_chrome)
    write_cloud_records(value, output)
