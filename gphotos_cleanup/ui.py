from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from pathlib import PurePosixPath

from .adb import Adb

VIEWER = "com.google.android.apps.photos/.pager.HostPhotoPagerActivity"

def _canonical(path: str) -> str:
    return path.replace("/sdcard/", "/storage/emulated/0/", 1)

def media_store_ids(adb: Adb) -> dict[str, str]:
    result: dict[str, str] = {}
    for collection in ("images/media", "video/media"):
        base = ["shell", "content", "query", "--uri", f"content://media/external/{collection}"]
        ids = adb.run(*base, "--projection", "_id").splitlines()
        paths = adb.run(*base, "--projection", "_data").splitlines()
        parsed_ids = [line.split("=", 1)[1] for line in ids if "_id=" in line]
        parsed_paths = [line.split("=", 1)[1] for line in paths if "_data=" in line]
        result.update({path: media_id for path, media_id in zip(parsed_paths, parsed_ids)})
    return result

def _center(bounds: str) -> tuple[int, int]:
    left_top, right_bottom = bounds.strip("[]").split("][")
    left, top = (int(part) for part in left_top.split(","))
    right, bottom = (int(part) for part in right_bottom.split(","))
    return (left + right) // 2, (top + bottom) // 2

def _dump(adb: Adb, name: str) -> ET.Element:
    remote = f"/sdcard/{name}.xml"
    adb.run("shell", "uiautomator", "dump", remote, check=False)
    return ET.fromstring(adb.run("shell", "cat", remote))

def probe_file(adb: Adb, path: str, media_id: str) -> dict[str, object]:
    video = PurePosixPath(path).suffix.lower() in {".mp4", ".mov", ".mkv", ".avi", ".3gp"}
    collection = "video/media" if video else "images/media"
    uri = f"content://media/external/{collection}/{media_id}"
    adb.run("shell", "am", "force-stop", "com.google.android.apps.photos", check=False)
    adb.run("shell", "am", "start", "-n", VIEWER, "-a", "android.intent.action.VIEW", "-d", uri, "-t", "video/*" if video else "image/*", check=False)
    time.sleep(3.0 if video else 1.2)
    if video:
        adb.run("shell", "input", "tap", "540", "1200")
        time.sleep(0.5)
    root = _dump(adb, "gphotos-cleanup-view")
    overflow = next((node for node in root.iter() if node.attrib.get("resource-id", "").endswith("action_bar_overflow")), None)
    if overflow is None:
        return {"path": path, "status": "viewer_not_ready", "evidence": []}
    adb.run("shell", "input", "tap", *map(str, _center(overflow.attrib["bounds"])))
    time.sleep(0.4)
    menu = _dump(adb, "gphotos-cleanup-menu")
    labels = [node.attrib.get("text", "") for node in menu.iter() if node.attrib.get("text")]
    backed_up = "Delete from device" in labels
    adb.run("shell", "input", "keyevent", "4", check=False)
    return {"path": path, "status": "backed_up" if backed_up else "not_confirmed", "evidence": [label for label in labels if label in {"Delete from device", "Download", "Delete from Google Photos"}], "labels": labels}

def probe_inventory(adb: Adb, files: list[dict[str, object]], limit: int | None = None) -> list[dict[str, object]]:
    index = media_store_ids(adb)
    results = []
    for item in files[:limit]:
        path = str(item["path"])
        media_id = index.get(_canonical(path))
        results.append(probe_file(adb, path, media_id) if media_id else {"path": path, "status": "not_in_mediastore", "evidence": []})
    return results
