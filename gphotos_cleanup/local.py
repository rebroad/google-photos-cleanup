from __future__ import annotations

import hashlib
from pathlib import Path

from .fingerprint import VIDEO_EXTENSIONS, fingerprint_file, video_fingerprint_stream

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif", ".avif"}
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

def inventory(roots: list[str], hash_files: bool = False, fingerprints: bool = False) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for root_name in roots:
        root = Path(root_name).expanduser().resolve()
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or "/.thumbnails/" in path.as_posix():
                continue
            extension = path.suffix.lower()
            if extension not in MEDIA_EXTENSIONS:
                continue
            stat = path.stat()
            item: dict[str, object] = {
                "path": str(path), "filename": path.name, "size": stat.st_size,
                "mtime": int(stat.st_mtime), "birthtime": getattr(stat, "st_birthtime", None),
                "extension": extension,
            }
            if hash_files:
                digest = hashlib.sha256()
                with path.open("rb") as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                        digest.update(chunk)
                item["sha256"] = digest.hexdigest()
            if fingerprints:
                if extension in IMAGE_EXTENSIONS:
                    item["phash"] = fingerprint_file(path)
                    item["fingerprint_kind"] = "image"
                else:
                    with path.open("rb") as stream:
                        item["phash"] = video_fingerprint_stream(stream)
                    item["fingerprint_kind"] = "video-contact-sheet"
            records.append(item)
    return records
