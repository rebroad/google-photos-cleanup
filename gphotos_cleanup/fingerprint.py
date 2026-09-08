from __future__ import annotations

import io
import shutil
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageOps

VIDEO_FRAME_SIZE = 16
VIDEO_FRAME_LIMIT = 12
VIDEO_EXTENSIONS = {".mp4", ".m4v", ".mov", ".3gp", ".mkv", ".webm", ".avi"}


def _average_hash_image(image: Image.Image, size: int = 16) -> str:
    image = ImageOps.fit(image.convert("L"), (size, size), method=Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    average = sum(pixels) / len(pixels)
    return "".join("1" if pixel >= average else "0" for pixel in pixels)


def average_hash(data: bytes, size: int = 16) -> str:
    return _average_hash_image(Image.open(io.BytesIO(data)), size)


def _video_hash(raw_frames: bytes, frame_size: int = VIDEO_FRAME_SIZE) -> str:
    stride = frame_size * frame_size
    frames = [raw_frames[offset:offset + stride] for offset in range(0, len(raw_frames), stride)]
    frames = [frame for frame in frames if len(frame) == stride][:VIDEO_FRAME_LIMIT]
    if not frames:
        raise ValueError("video produced no frames")
    columns, rows = 4, 3
    sheet = Image.new("L", (columns * frame_size, rows * frame_size), color=0)
    for index, frame in enumerate(frames):
        sheet.paste(Image.frombytes("L", (frame_size, frame_size), frame),
                    ((index % columns) * frame_size, (index // columns) * frame_size))
    return _average_hash_image(sheet)


def video_fingerprint_stream(stream) -> str:
    # MP4 metadata is commonly stored at EOF. Spool only this one media file
    # to the OS temporary directory so ffmpeg can seek; it is removed before
    # returning and is never part of the inventory or report.
    with tempfile.NamedTemporaryFile(prefix="gphotos-video-", suffix=".bin") as temporary:
        shutil.copyfileobj(stream, temporary)
        temporary.flush()
        command = [
            "ffmpeg", "-v", "error", "-i", temporary.name,
            "-vf", f"thumbnail={VIDEO_FRAME_LIMIT},scale={VIDEO_FRAME_SIZE}:{VIDEO_FRAME_SIZE},format=gray",
            "-frames:v", str(VIDEO_FRAME_LIMIT), "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1",
        ]
        result = subprocess.run(command, capture_output=True, check=False, timeout=120)
    if result.returncode != 0:
        detail = result.stderr.decode(errors="replace").strip()
        raise RuntimeError(detail or "ffmpeg could not decode video")
    return _video_hash(result.stdout)


def hamming(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right)) + abs(len(left) - len(right))


def fingerprint_file(path: str | Path) -> str:
    return average_hash(Path(path).read_bytes())


def fingerprint_adb(serial: str, path: str) -> str:
    data = subprocess.run(["adb", "-s", serial, "exec-out", "cat", path], capture_output=True, check=True).stdout
    return average_hash(data)


def fingerprint_adb_thumbnail(serial: str, media_id: str, kind: str) -> str:
    """Fingerprint a MediaStore thumbnail, never the original media file."""
    collection = "video" if kind == "video" else "images"
    uri = f"content://media/external/{collection}/thumbnails/{media_id}"
    result = subprocess.run(
        ["adb", "-s", serial, "exec-out", "content", "read", "--uri", uri],
        capture_output=True,
        check=True,
        timeout=30,
    )
    if not result.stdout:
        raise RuntimeError("MediaStore returned an empty thumbnail")
    return average_hash(result.stdout)


def video_fingerprint_adb(serial: str, path: str) -> str:
    adb = subprocess.Popen(["adb", "-s", serial, "exec-out", "cat", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert adb.stdout is not None
    try:
        fingerprint = video_fingerprint_stream(adb.stdout)
    finally:
        adb.stdout.close()
    stderr = adb.stderr.read() if adb.stderr is not None else b""
    status = adb.wait()
    if status != 0:
        raise RuntimeError(stderr.decode(errors="replace").strip() or f"adb failed with {status}")
    return fingerprint


def group_similar(items: list[dict[str, object]], threshold: int = 12) -> list[list[dict[str, object]]]:
    groups: list[list[dict[str, object]]] = []
    for item in items:
        digest = str(item.get("phash", ""))
        for group in groups:
            if hamming(digest, str(group[0].get("phash", ""))) <= threshold:
                group.append(item)
                break
        else:
            groups.append([item])
    return [group for group in groups if len(group) > 1]
