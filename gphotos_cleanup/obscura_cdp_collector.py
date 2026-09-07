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
    """The live Obscura DevTools session could not complete a command."""


class _WebSocket:
    def __init__(self, url: str, host_header: str | None = None, timeout: float = 120.0):
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "ws" or not parsed.hostname or not parsed.port:
            raise CdpError("Obscura returned an invalid DevTools WebSocket URL")
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
                raise CdpError("Obscura closed the DevTools handshake")
            header += block
        if b" 101 " not in header.split(b"\r\n", 1)[0]:
            raise CdpError("Obscura rejected the DevTools WebSocket handshake")
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
            raise CdpError("Obscura closed the DevTools connection")
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
                raise CdpError("Obscura truncated a DevTools frame")
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


def _obscura_page_websocket_url(port: int) -> tuple[str, str, str]:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=8) as response:
            targets = json.load(response)
        pages = [
            target for target in targets
            if isinstance(target, dict)
            and target.get("type") == "page"
            and isinstance(target.get("webSocketDebuggerUrl"), str)
        ]
        if not pages:
            raise ValueError("Obscura has no page target")
        target = pages[-1]
        url = str(target["webSocketDebuggerUrl"])
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "ws" or not parsed.path:
            raise ValueError("Obscura returned an invalid page WebSocket URL")
        return url, parsed.netloc, str(target.get("url", ""))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise CdpError("Obscura CDP server is unavailable") from error


@contextmanager
def obscura_server(binary: str, storage_dir: str, port: int) -> Iterator[int]:
    command = [binary, "serve", "--stealth", "--host", "127.0.0.1", "--port", str(port), "--storage-dir", storage_dir, "--quiet"]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)
    try:
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise CdpError("Obscura server exited before becoming ready")
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1):
                    yield port
                    return
            except OSError:
                time.sleep(0.1)
        raise CdpError("Obscura server did not become ready")
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

from .chrome_collector import EXTRACT_AND_SCROLL

def _wait_for_execution_context(ws: _WebSocket, session: str, attempts: int = 15) -> None:
    for attempt in range(attempts):
        try:
            ws.call("Runtime.evaluate", {"expression": "location.href", "returnByValue": True}, session=session)
            return
        except CdpError as error:
            if "execution context" not in str(error).lower() or attempt == attempts - 1:
                raise
            time.sleep(1)
            time.sleep(1)

def _read_session_file(session_file: str) -> list[dict[str, object]]:
    value = json.loads(open(session_file, encoding="utf-8").read())
    cookies = value.get("cookies") if isinstance(value, dict) else None
    if not isinstance(cookies, list) or not cookies:
        raise CdpError("session file contains no cookies")
    return [cookie for cookie in cookies if isinstance(cookie, dict)]


def collect(
    binary: str,
    storage_dir: str,
    url: str = "https://photos.google.com/",
    max_scrolls: int = 20000,
    port: int = 9333,
    session_file: str | None = None,
) -> dict[str, object]:
    with obscura_server(binary, storage_dir, port) as server_port:
        with urllib.request.urlopen(f"http://127.0.0.1:{server_port}/json/version", timeout=8) as response:
            browser_url = str(json.load(response)["webSocketDebuggerUrl"])
        ws = _WebSocket(browser_url)
        try:
            target = ws.call("Target.createTarget", {"url": "about:blank"})
            target_id = target.get("result", {}).get("targetId")
            if not isinstance(target_id, str):
                raise CdpError("Obscura did not create a page target")
            attached = ws.call("Target.attachToTarget", {"targetId": target_id, "flatten": True})
            session = attached.get("result", {}).get("sessionId")
            if not isinstance(session, str):
                raise CdpError("Obscura did not attach the page target")
            ws.call("Page.enable", session=session)
            ws.call("Runtime.enable", session=session)
            if session_file:
                ws.call(
                    "Network.setCookies",
                    {"cookies": _read_session_file(session_file)},
                    session=session,
                )
            ws.call("Page.navigate", {"url": url}, session=session)
            _wait_for_execution_context(ws, session)
            time.sleep(5)
            expression = EXTRACT_AND_SCROLL.replace("__MAX_SCROLLS__", str(max(1, min(max_scrolls, 20000))))
            result = ws.call("Runtime.evaluate", {"expression": expression, "awaitPromise": True, "returnByValue": True}, session=session)
            value = result.get("result", {}).get("result", {}).get("value")
            if not isinstance(value, dict):
                raise CdpError("Obscura returned no Photos extraction result")
            if not value.get("authenticated"):
                raise CdpError("Obscura is not authenticated to Google Photos")
            return value
        finally:
            ws.close()


def collect_to_file(
    binary: str,
    storage_dir: str,
    output: str,
    url: str = "https://photos.google.com/",
    max_scrolls: int = 20000,
    port: int = 9333,
    session_file: str | None = None,
) -> None:
    write_cloud_records(
        collect(binary, storage_dir, url, max_scrolls, port, session_file),
        output,
    )
