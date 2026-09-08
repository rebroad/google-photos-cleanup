from __future__ import annotations

from gphotos_cleanup.chrome_collector import EXTRACT_AND_SCROLL, _WebSocket
from gphotos_cleanup.obscura_collector import _is_google_media_url
from gphotos_cleanup.chrome_auth_cli import _relevant_domain
from gphotos_cleanup import obscura_collector



class ChunkedSocket:
    def __init__(self, data: bytes, chunk_size: int = 1):
        self.data = data
        self.chunk_size = chunk_size

    def recv(self, size: int) -> bytes:
        if not self.data:
            return b""
        count = min(size, self.chunk_size, len(self.data))
        result, self.data = self.data[:count], self.data[count:]
        return result

    def sendall(self, data: bytes) -> None:
        pass

    def close(self) -> None:
        pass


def websocket_frame(payload: bytes, opcode: int = 1) -> bytes:
    size = len(payload)
    if size < 126:
        return bytes([0x80 | opcode, size]) + payload
    if size < 65536:
        return bytes([0x80 | opcode, 126]) + len(payload).to_bytes(2, "big") + payload
    return bytes([0x80 | opcode, 127]) + len(payload).to_bytes(8, "big") + payload


def test_websocket_reads_fragmented_header_and_payload():
    ws = object.__new__(_WebSocket)
    ws.sock = ChunkedSocket(websocket_frame(b"fragmented"), chunk_size=1)
    assert ws._receive_frame() == (1, b"fragmented")


def test_extractor_preserves_media_kind_and_checks_auth_after_scroll():
    assert "kind" in EXTRACT_AND_SCROLL
    assert "const text = document.body ? document.body.innerText : '';" in EXTRACT_AND_SCROLL
    assert "libraryMarker" in EXTRACT_AND_SCROLL
    assert "publicOverviewMarker" in EXTRACT_AND_SCROLL
    assert "libraryUrl" in EXTRACT_AND_SCROLL
    assert "timelineReady" in EXTRACT_AND_SCROLL
    assert "timeline_ready" in EXTRACT_AND_SCROLL
    assert "networkError" in EXTRACT_AND_SCROLL
    assert "googleusercontent" not in EXTRACT_AND_SCROLL
    assert "reached_end" in EXTRACT_AND_SCROLL



def test_extractor_does_not_include_cookie_or_password_apis():
    assert "Network.getAllCookies" not in EXTRACT_AND_SCROLL
    assert "document.cookie" not in EXTRACT_AND_SCROLL
    assert "password" not in EXTRACT_AND_SCROLL



def test_current_google_photos_media_hosts_are_allowed_without_allowing_arbitrary_hosts():
    assert _is_google_media_url("https://photos.fife.usercontent.google.com/pw/thumb")
    assert _is_google_media_url("https://lh3.googleusercontent.com/a")
    assert not _is_google_media_url("https://example.googleusercontent.com.evil.test/a")



def test_session_export_domain_filter_keeps_google_auth_hosts_only():
    assert _relevant_domain(".google.com")
    assert _relevant_domain("accounts.google.com")
    assert _relevant_domain("photos.fife.usercontent.google.com")
    assert not _relevant_domain("googleadservices.com")
    assert not _relevant_domain("example.test")


def test_cloud_video_fingerprint_runs_with_session_cookie(tmp_path, monkeypatch):
    monkeypatch.setattr(obscura_collector, "_media_phash", lambda url, video=False, cookie_header=None: "1" * 256 if video and cookie_header else None)
    output = tmp_path / "cloud.json"
    obscura_collector.write_cloud_records({"media": [{
        "kind": "video", "src": "https://lh3.googleusercontent.com/video",
        "alt": "clip.mp4", "width": 320, "height": 180,
    }]}, str(output), cookie_header="SID=filtered")
    item = __import__("json").loads(output.read_text())["media_items"][0]
    assert item["phash"] == "1" * 256
