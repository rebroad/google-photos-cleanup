from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from .adb import Adb
from .photos import match, normalize


def _write(path: str, value: object) -> None:
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gphotos-cleanup")
    sub = parser.add_subparsers(dest="command", required=True)
    probe = sub.add_parser("auth-probe", help="check ADB and Google Photos availability")
    probe.add_argument("--serial")
    inventory = sub.add_parser("inventory", help="inventory media on the phone")
    inventory.add_argument("--serial")
    inventory.add_argument("--root", action="append", default=["/sdcard/DCIM", "/sdcard/Pictures", "/sdcard/Movies"])
    inventory.add_argument("--hash", action="store_true")
    inventory.add_argument("--output", required=True)
    normalize_cmd = sub.add_parser("normalize", help="normalize adapter JSON")
    normalize_cmd.add_argument("--input", required=True)
    normalize_cmd.add_argument("--output", required=True)
    matcher = sub.add_parser("match", help="match inventory against normalized Photos metadata")
    matcher.add_argument("--inventory", required=True)
    matcher.add_argument("--photos", required=True)
    matcher.add_argument("--output", required=True)
    report = sub.add_parser("report", help="write a review CSV")
    report.add_argument("--matches", required=True)
    report.add_argument("--csv", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "auth-probe":
            print(json.dumps(Adb(args.serial).probe(), indent=2, sort_keys=True))
        elif args.command == "inventory":
            _write(args.output, {"serial": args.serial, "roots": args.root, "files": Adb(args.serial).inventory(args.root, args.hash)})
        elif args.command == "normalize":
            source = json.loads(Path(args.input).read_text(encoding="utf-8"))
            _write(args.output, normalize(source["media_items"] if isinstance(source, dict) and "media_items" in source else source))
        elif args.command == "match":
            inventory = json.loads(Path(args.inventory).read_text(encoding="utf-8"))["files"]
            photos = json.loads(Path(args.photos).read_text(encoding="utf-8"))
            _write(args.output, match(inventory, photos))
        elif args.command == "report":
            matches = json.loads(Path(args.matches).read_text(encoding="utf-8"))
            with Path(args.csv).open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["path", "filename", "confidence", "evidence", "remote_ids", "remote_urls"])
                writer.writeheader()
                for item in matches:
                    row = dict(item)
                    row["evidence"] = ",".join(row["evidence"])
                    row["remote_ids"] = ",".join(str(value) for value in row["remote_ids"])
                    row["remote_urls"] = ",".join(str(value) for value in row["remote_urls"])
                    writer.writerow(row)
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0
