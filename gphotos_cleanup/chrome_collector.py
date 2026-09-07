from __future__ import annotations

import base64
import json
import os
import socket
import struct
import subprocess
import urllib.parse
from contextlib import contextmanager
from typing import Iterator

from .obscura_collector import write_cloud_records


class CdpError(RuntimeError):
    """The live Chrome DevTools session could not complete a command."""


class _WebSocket:
    def __init__(self, url: str, timeout: float = 15.0):
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "ws" or not parsed.hostname or not parsed.port:
            raise CdpError("Chrome returned an invalid DevTools WebSocket URL")
        self.sock = socket.create_connection((parsed.hostname, parsed.port), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request = (
            f"GET {parsed.path or '/'} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port}\r\n"
            "Upgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n"
            "Origin: http://localhost\r\n\r\n"
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
        header = self.sock.recv(2)
        if len(header) != 2:
            raise CdpError("Chrome closed the DevTools connection")
        opcode = header[0] & 0x0F
        size = header[1] & 0x7F
        masked = bool(header[1] & 0x80)
        if size == 126:
            size = struct.unpack(">H", self.sock.recv(2))[0]
        elif size == 127:
            size = struct.unpack(">Q", self.sock.recv(8))[0]
        mask = self.sock.recv(4) if masked else b""
        payload = bytearray()
        while len(payload) < size:
            block = self.sock.recv(size - len(payload))
            if not block:
                raise CdpError("Chrome truncated a DevTools frame")
            payload.extend(block)
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


@contextmanager
def adb_chrome_forward(serial: str) -> Iterator[int]:
    probe = socket.socket()
    probe.bind(("127.0.0.1", 0))
    port = int(probe.getsockname()[1])
    probe.close()
    command = ["adb", "-s", serial, "forward", f"tcp:{port}", "localabstract:chrome_devtools_remote"]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise CdpError(result.stderr.strip() or "could not forward Chrome DevTools")
    try:
        yield port
    finally:
        subprocess.run(
            ["adb", "-s", serial, "forward", "--remove", f"tcp:{port}"],
            text=True,
            capture_output=True,
            check=False,
        )


EXTRACT_AND_SCROLL = r"""
(async () => {
  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
  const media = new Map();
  const collect = () => {
    for (const node of document.querySelectorAll('img,video')) {
      const src = node.currentSrc || node.src || '';
      if (!src) continue;
      media.set(src, {
        tag: node.tagName.toLowerCase(), src, alt: node.alt || '',
        width: node.naturalWidth || node.videoWidth || 0,
        height: node.naturalHeight || node.videoHeight || 0
      });
    }
  };
  const root = document.scrollingElement || document.documentElement;
  const candidates = [root, ...document.querySelectorAll('*')].filter((node) =>
    node && node.scrollHeight > node.clientHeight + 200 && node.clientHeight > 0
  );
  const scroller = candidates.sort((a, b) =>
    (b.scrollHeight - b.clientHeight) - (a.scrollHeight - a.clientHeight)
  )[0] || root;
  collect();
  let stagnant = 0;
  for (let index = 0; index < __MAX_SCROLLS__; index++) {
    const before = media.size;
    const next = Math.min(scroller.scrollTop + Math.max(600, scroller.clientHeight * 0.85),
                          scroller.scrollHeight - scroller.clientHeight);
    scroller.scrollTop = next;
    window.scrollTo(0, next);
    await delay(350);
    collect();
    stagnant = media.size === before ? stagnant + 1 : 0;
    if (next >= scroller.scrollHeight - scroller.clientHeight - 4 && stagnant >= 3) break;
  }
  const host = location.hostname;
  const text = document.body ? document.body.innerText : '';
  return {
    url: location.href,
    title: document.title,
    authenticated: host === 'photos.google.com' && !/sign[ -]?in|choose an account/i.test(text),
    media: Array.from(media.values())
  };
})()
"""


def collect(serial: str, url: str = "https://photos.google.com/", max_scrolls: int = 80) -> dict[str, object]:
    with adb_chrome_forward(serial) as port:
        try:
            ws = _WebSocket(f"ws://127.0.0.1:{port}/devtools/browser")
        except OSError as error:
            raise CdpError(
                "Chrome DevTools is unavailable; unlock the phone and leave Google Photos open"
            ) from error
        try:
            targets = ws.call("Target.getTargets").get("result", {}).get("targetInfos", [])
            pages = [target for target in targets if target.get("type") == "page"]
            if not pages:
                raise CdpError("Chrome has no debuggable page; unlock the phone and open Google Photos")
            target = next(
                (item for item in pages if urllib.parse.urlsplit(str(item.get("url", ""))).netloc == "photos.google.com"),
                pages[0],
            )
            attached = ws.call("Target.attachToTarget", {"targetId": target["targetId"], "flatten": True})
            session = str(attached.get("result", {}).get("sessionId", ""))
            if not session:
                raise CdpError("Chrome did not attach a Photos page")
            try:
                ws.call("Page.enable", session=session)
                ws.call("Runtime.enable", session=session)
                ws.call("Page.navigate", {"url": url}, session=session)
                expression = EXTRACT_AND_SCROLL.replace("__MAX_SCROLLS__", str(max(1, min(max_scrolls, 200))))
                result = ws.call(
                    "Runtime.evaluate",
                    {"expression": expression, "awaitPromise": True, "returnByValue": True},
                    session=session,
                )
                value = result.get("result", {}).get("result", {}).get("value")
                if not isinstance(value, dict):
                    raise CdpError("Chrome returned no Photos extraction result")
                if not value.get("authenticated"):
                    raise CdpError("Chrome is not authenticated to Google Photos; sign in visibly first")
                return value
            finally:
                ws.call("Target.detachFromTarget", {"sessionId": session})
        finally:
            ws.close()


def collect_to_file(serial: str, output: str, url: str = "https://photos.google.com/", max_scrolls: int = 80) -> None:
    value = collect(serial, url, max_scrolls)
    write_cloud_records(value, output)
