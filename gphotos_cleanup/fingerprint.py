from __future__ import annotations

import io
import subprocess
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageOps


def average_hash(data: bytes, size: int = 16) -> str:
    image = Image.open(io.BytesIO(data)).convert("L")
    image = ImageOps.fit(image, (size, size), method=Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    average = sum(pixels) / len(pixels)
    return "".join("1" if pixel >= average else "0" for pixel in pixels)


def hamming(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right)) + abs(len(left) - len(right))


def fingerprint_file(path: str | Path) -> str:
    return average_hash(Path(path).read_bytes())


def fingerprint_adb(serial: str, path: str) -> str:
    data = subprocess.run(["adb", "-s", serial, "exec-out", "cat", path], capture_output=True, check=True).stdout
    return average_hash(data)


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
