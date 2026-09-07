from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adb import Adb
from .fingerprint import fingerprint_adb, group_similar
from .ui import probe_inventory


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.probe_cli")
    sub = parser.add_subparsers(dest="command", required=True)
    backup = sub.add_parser("probe-backup")
    backup.add_argument("--serial", required=True)
    backup.add_argument("--inventory", required=True)
    backup.add_argument("--output", required=True)
    backup.add_argument("--limit", type=int)
    fingerprint = sub.add_parser("fingerprint")
    fingerprint.add_argument("--serial", required=True)
    fingerprint.add_argument("--inventory", required=True)
    fingerprint.add_argument("--output", required=True)
    args = parser.parse_args()
    inventory = json.loads(Path(args.inventory).read_text(encoding="utf-8"))["files"]
    if args.command == "probe-backup":
        value = {"serial": args.serial, "results": probe_inventory(Adb(args.serial), inventory, args.limit)}
    else:
        images = []
        for item in inventory:
            if str(item.get("extension", "")) in {".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif"}:
                copy = dict(item)
                copy["phash"] = fingerprint_adb(args.serial, str(item["path"]))
                images.append(copy)
        value = {"serial": args.serial, "images": images, "similar_groups": group_similar(images)}
    Path(args.output).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


raise SystemExit(main())
