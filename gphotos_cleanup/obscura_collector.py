from __future__ import annotations

import hashlib
import concurrent.futures
import json
import subprocess
import urllib.parse
import urllib.request

from .fingerprint import average_hash, video_fingerprint_stream
from pathlib import Path


def _is_google_media_url(url: str) -> bool:
    host = urllib.parse.urlsplit(url).hostname or ""
    return (
        host == "googleusercontent.com"
        or host.endswith(".googleusercontent.com")
        or host == "usercontent.google.com"
        or host.endswith(".usercontent.google.com")
    )


EXTRACT = r"""
JSON.stringify({
  url: location.href,
  title: document.title,
  text: document.body ? document.body.innerText : '',
  media: Array.from(document.querySelectorAll('img,video')).map((node) => ({
    tag: node.tagName.toLowerCase(),
    src: node.currentSrc || node.src || '',
    alt: node.alt || '',
    width: node.naturalWidth || node.videoWidth || 0,
    height: node.naturalHeight || node.videoHeight || 0
  })).filter((item) => item.src)
})
"""


def collect(binary: str, storage_dir: str, url: str = "https://photos.google.com/", wait: int = 5) -> dict[str, object]:
    command = [binary, "fetch", url, "--storage-dir", storage_dir, "--wait", str(wait), "--eval", EXTRACT]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"obscura exited with {result.returncode}")
    try:
        value = json.loads(result.stdout)
        if isinstance(value, str):
            value = json.loads(value)
        if not isinstance(value, dict):
            raise ValueError("collector result was not an object")
        final_url = str(value.get("url", ""))
        if not final_url.startswith("https://photos.google.com/"):
            raise RuntimeError(
                "Google Photos session is not authenticated; "
                f"the browser landed on {final_url or 'an unknown URL'}"
            )
        return value
    except (json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"could not parse obscura output: {error}") from error


class _LimitedReader:
    def __init__(self, stream, limit: int):
        self.stream = stream
        self.limit = limit
        self.total = 0

    def read(self, size: int = -1) -> bytes:
        remaining = self.limit - self.total
        if remaining <= 0:
            return b""
        requested = remaining if size is None or size < 0 else min(size, remaining + 1)
        chunk = self.stream.read(requested)
        self.total += len(chunk)
        if self.total > self.limit:
            raise ValueError("remote media exceeds fingerprint limit")
        return chunk


def _media_phash(url: str, video: bool = False, cookie_header: str | None = None) -> str | None:
    if not _is_google_media_url(url):
        return None
    headers = {"User-Agent": "gphotos-cleanup/0.1"}
    if cookie_header:
        headers["Cookie"] = cookie_header
    request = urllib.request.Request(url, headers=headers)
    limit = 128 * 1024 * 1024 if video else 16 * 1024 * 1024
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            length = response.headers.get("Content-Length")
            if length and int(length) > limit:
                return None
            if video:
                return video_fingerprint_stream(_LimitedReader(response, limit))
            data = response.read(limit + 1)
        if len(data) > limit:
            return None
        return average_hash(data)
    except (OSError, ValueError, RuntimeError):
        return None


def write_cloud_records(value: dict[str, object], output: str, cookie_header: str | None = None, include_source_urls: bool = False, fingerprint_missing: bool = True) -> None:
    media = value.get("media", [])
    records = []
    fingerprint_jobs = []
    for item in media if isinstance(media, list) else []:
        if not isinstance(item, dict):
            continue
        src = str(item.get("src", ""))
        if not _is_google_media_url(src):
            continue
        video = item.get("kind", item.get("tag")) == "video"
        records.append({
            "id": "media:" + hashlib.sha256(src.encode("utf-8")).hexdigest(),
            "filename": str(item.get("alt", "")),
            "mime_type": "video/*" if video else "image/*",
            "width": item.get("width", 0),
            "height": item.get("height", 0),
            "source": "google-photos-dom",
        })
        if include_source_urls:
            records[-1]["source_url"] = src
        browser_phash = item.get("phash")
        if isinstance(browser_phash, str):
            records[-1]["phash"] = browser_phash
        elif fingerprint_missing:
            fingerprint_jobs.append((len(records) - 1, src, video))
    if fingerprint_jobs:
        # Video fingerprints require a temporary ffmpeg input file and can be
        # substantially larger than image thumbnails. Keep those downloads
        # deliberately narrow to avoid multiplying peak Termux disk use.
        workers = 2 if any(job[2] for job in fingerprint_jobs) else 8
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            hashes = executor.map(lambda job: _media_phash(job[1], video=job[2], cookie_header=cookie_header), fingerprint_jobs)
            for (index, _src, _video), phash in zip(fingerprint_jobs, hashes):
                if phash:
                    records[index]["phash"] = phash
    payload: dict[str, object] = {"media_items": records}
    for key in ("url", "title", "complete", "reached_end", "scroll_count", "scroll_height", "scroll_top"):
        if key in value:
            payload[key] = value[key]
    Path(output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
