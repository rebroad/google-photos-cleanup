from __future__ import annotations

import base64
import json
import os
import socket
import struct
import time
import urllib.parse
import urllib.request
from pathlib import Path

from .obscura_collector import write_cloud_records
from .virtual_display import validate_cdp_endpoint


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
                    # Keep unrelated Chrome tabs intact. Only collapse duplicate
                    # Google Photos pages, as collection should not disrupt the
                    # user's other browsing session.
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


EXTRACT_AND_SCROLL = r"""
(async () => {
  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
  const media = new Map();
  await delay(2000);
  const collect = () => {
    const nodes = [...document.querySelectorAll("img,video,div.qs41qe,div[class*=\"qs41qe\"],div[class*=\"RY3tic\"]")];
    for (const node of nodes) {
      const tag = node.tagName.toLowerCase();
      const rect = node.getBoundingClientRect();
      // Hidden preload images and shell icons often retain a Google URL but
      // are not timeline tiles. Only accept media occupying a real tile-sized
      // rectangle in the rendered viewport.
      if (rect.width < 50 || rect.height < 50) continue;
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
        height: node.naturalHeight || node.videoHeight || 0,
        poster: node.poster || ''
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
  await delay(250);
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
    scroller.dispatchEvent(new Event("scroll", {bubbles: true}));
    // Google Photos virtualizes the timeline and needs time to fetch/render
    // the next batch before its tile backgrounds become observable.
    await delay(1000);
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
      const thumbnail = /=[^/?]*$/.test(item.src)
        ? item.src.replace(/=[^/?]*$/, "=w256-h256")
        : item.src + "=w256-h256";
      const response = await fetch(thumbnail, {credentials: "include", signal: controller.signal});
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
  const libraryMarker = /Search your photos and albums|Create and add photos|Photos library/i.test(text);
  const publicOverviewMarker = /Get the app|A safe home for your life's memories|Edit, organise, search and back up your photos/i.test(text);
  const networkError = /can't connect|no internet connection|ERR_NAME_NOT_RESOLVED|ERR_INTERNET_DISCONNECTED/i.test(text);
  const libraryUrl = host === 'photos.google.com' &&
    /^\/(?:u\/\d+\/)?$/.test(location.pathname);
  // A signed-in shell can briefly contain the library labels while the real
  // virtualized timeline is still loading (or while an account-login iframe
  // is present). Do not let that state become a successful empty inventory.
  const timelineReady = scroller.scrollHeight > 10000 && media.size > 0;
  return {
    url: location.href,
    title: document.title,
    authenticated: libraryUrl && libraryMarker && !publicOverviewMarker && !/sign[ -]?in|choose an account/i.test(text),
    network_error: networkError,
    timeline_ready: timelineReady,
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
    if serial:
        raise CdpError("physical-device Chrome is disabled; use the virtual display --cdp-endpoint")
    if not cdp_endpoint:
        raise CdpError("cloud collection requires the virtual display --cdp-endpoint")
    return _collect_endpoint(validate_cdp_endpoint(cdp_endpoint), url, max_scrolls)



def _reload_endpoint(endpoint: str, url: str) -> None:
    ws_url, host_header, _current_url = _chrome_page_websocket_url(endpoint)
    ws = _WebSocket(ws_url, host_header=host_header)
    try:
        ws.call("Page.reload", {"ignoreCache": True})
    except CdpError as error:
        if "navigated or closed" not in str(error).lower():
            raise
    finally:
        ws.close()
    time.sleep(3)


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
            if value.get("network_error"):
                raise CdpError("Chrome cannot resolve or reach Google Photos; fix the virtual device network before collecting")
            raise CdpError("Chrome is not authenticated to Google Photos; sign in with Chrome first")
        if not value.get("timeline_ready"):
            raise CdpError("Google Photos timeline is not ready; wait for the library to load and retry")
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
    chunk_scrolls: int = 100,
    fingerprint: bool = True,
) -> None:
    """Collect in bounded, resumable browser evaluations."""
    if serial:
        raise CdpError("physical-device Chrome is disabled; use the virtual display --cdp-endpoint")
    if not cdp_endpoint:
        raise CdpError("cloud collection requires the virtual display --cdp-endpoint")
    checkpoint = Path(output + ".partial")
    merged: dict[str, dict[str, object]] = {}
    total_scrolls = 0
    start_scroll_top = 0
    final_value: dict[str, object] = {}
    if checkpoint.exists() or Path(output).exists():
        try:
            saved = json.loads(checkpoint.read_text(encoding="utf-8")) if checkpoint.exists() else json.loads(Path(output).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            saved = json.loads(Path(output).read_text(encoding="utf-8")) if Path(output).exists() else {}
        if isinstance(saved, dict):
            total_scrolls = int(saved.get("scroll_count", 0))
            start_scroll_top = int(saved.get("scroll_top", 0))
            final_value = saved
            saved_items = saved.get("media", saved.get("media_items", []))
            for item in saved_items:
                if isinstance(item, dict) and item.get("src"):
                    merged[str(item["src"])] = item
    _collect_to_file_endpoint(
        validate_cdp_endpoint(cdp_endpoint), url, max_scrolls, chunk_scrolls,
        fingerprint,
        output, checkpoint, merged, total_scrolls, start_scroll_top, final_value,
    )


def _collect_to_file_endpoint(
    endpoint: str, url: str, max_scrolls: int, chunk_scrolls: int, fingerprint: bool, output: str,
    checkpoint: Path, merged: dict[str, dict[str, object]], total_scrolls: int,
    start_scroll_top: int, final_value: dict[str, object],
) -> None:
    limit = max(1, min(max_scrolls, 20000))
    chunk_limit = max(1, min(chunk_scrolls, 500))
    complete = bool(final_value.get("complete", False))
    chunks_since_reload = 0
    while total_scrolls < limit and not complete:
        previous_start = start_scroll_top
        chunk = min(chunk_limit, limit - total_scrolls)
        value = _collect_endpoint(endpoint, url, chunk, start_scroll_top, fingerprint=fingerprint)
        final_value = value
        for item in value.get("media", []):
            if isinstance(item, dict) and item.get("src"):
                merged[str(item["src"])] = item
        progressed = int(value.get("scroll_count", 0))
        total_scrolls += progressed
        start_scroll_top = int(value.get("scroll_top", start_scroll_top))
        complete = bool(value.get("complete"))
        checkpoint_tmp = checkpoint.with_name(checkpoint.name + ".tmp")
        checkpoint_tmp.write_text(json.dumps({
            **value, "media": list(merged.values()),
            "scroll_count": total_scrolls, "scroll_top": start_scroll_top,
            "complete": complete,
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(checkpoint_tmp, checkpoint)
        chunks_since_reload += 1
        if chunks_since_reload >= 10 and not complete:
            _reload_endpoint(endpoint, url)
            chunks_since_reload = 0
        if complete:
            break
        if progressed <= 0 or start_scroll_top <= previous_start:
            raise CdpError("Google Photos scroll position did not advance between chunks")
    final_value["media"] = list(merged.values())
    final_value["scroll_count"] = total_scrolls
    final_value["scroll_top"] = start_scroll_top
    final_value["complete"] = complete
    final_value["reached_end"] = complete
    write_cloud_records(final_value, output, fingerprint_missing=fingerprint)
