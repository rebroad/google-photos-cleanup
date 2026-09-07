from __future__ import annotations

import json
import subprocess
import urllib.request

from .fingerprint import average_hash
from pathlib import Path


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


def _photo_phash(url: str) -> str | None:
    if "googleusercontent.com/" not in url:
        return None
    request = urllib.request.Request(url, headers={"User-Agent": "gphotos-cleanup/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = response.read(16 * 1024 * 1024 + 1)
        if len(data) > 16 * 1024 * 1024:
            return None
        return average_hash(data)
    except (OSError, ValueError):
        return None


def write_cloud_records(value: dict[str, object], output: str) -> None:
    media = value.get("media", [])
    records = []
    for item in media if isinstance(media, list) else []:
        if not isinstance(item, dict):
            continue
        src = str(item.get("src", ""))
        if "googleusercontent.com/" not in src:
            continue
        record = {
            "id": src,
            "filename": str(item.get("alt", "")),
            "mime_type": "video/*" if item.get("tag") == "video" else "image/*",
            "width": item.get("width", 0),
            "height": item.get("height", 0),
            "source": "obscura-dom",
            "source_url": value.get("url"),
            "content_url": src,
        }
        if item.get("tag") != "video":
            phash = _photo_phash(src)
            if phash:
                record["phash"] = phash
        records.append(record)
    Path(output).write_text(json.dumps({"media_items": records}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
