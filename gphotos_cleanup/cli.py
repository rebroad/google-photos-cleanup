from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
import sys
from pathlib import Path

from .adb import Adb
from .fingerprint import VIDEO_EXTENSIONS, fingerprint_adb, video_fingerprint_adb
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
    inventory.add_argument("--fingerprint", action="store_true", help="compute perceptual image fingerprints over ADB")
    inventory.add_argument("--output", required=True)
    normalize_cmd = sub.add_parser("normalize", help="normalize adapter JSON")
    normalize_cmd.add_argument("--input", required=True)
    normalize_cmd.add_argument("--output", required=True)
    matcher = sub.add_parser("match", help="match inventory against normalized Photos metadata")
    matcher.add_argument("--inventory", required=True)
    matcher.add_argument("--photos", required=True)
    matcher.add_argument("--output", required=True)
    report = sub.add_parser("report", help="write review CSV and optional deletion-candidate manifest")
    report.add_argument("--matches", required=True)
    report.add_argument("--csv", required=True)
    report.add_argument("--manifest", help="write a JSON review-only deletion-candidate manifest")
    args = parser.parse_args(argv)
    try:
        if args.command == "auth-probe":
            print(json.dumps(Adb(args.serial).probe(), indent=2, sort_keys=True))
        elif args.command == "inventory":
            serial = args.serial
            if args.fingerprint and not serial:
                devices = [line.split()[0] for line in Adb().run("devices").splitlines() if line.endswith("\tdevice")]
                if len(devices) != 1:
                    raise RuntimeError("--fingerprint requires --serial when ADB does not have exactly one device")
                serial = devices[0]
            files = Adb(serial).inventory(args.root, args.hash)
            if args.fingerprint:
                for item in files:
                    extension = str(item.get("extension", "")).lower()
                    if extension in {".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif"}:
                        try:
                            item["phash"] = fingerprint_adb(serial, str(item["path"]))
                            item["fingerprint_kind"] = "image"
                        except (OSError, RuntimeError):
                            item["phash_error"] = True
                    elif extension in VIDEO_EXTENSIONS:
                        try:
                            item["phash"] = video_fingerprint_adb(serial, str(item["path"]))
                            item["fingerprint_kind"] = "video-contact-sheet"
                        except (OSError, RuntimeError, ValueError):
                            item["phash_error"] = True
            _write(args.output, {"serial": serial, "roots": args.root, "files": files})
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
            if args.manifest:
                candidates = [
                    {
                        "path": item.get("path"),
                        "filename": item.get("filename"),
                        "confidence": item.get("confidence"),
                        "evidence": item.get("evidence", []),
                        "remote_ids": item.get("remote_ids", []),
                        "remote_urls": item.get("remote_urls", []),
                        "action": "review_only",
                    }
                    for item in matches
                    if item.get("confidence") not in (None, "none") and item.get("remote_ids")
                ]
                _write(args.manifest, {
                    "schema": "gphotos-cleanup/deletion-candidates/v1",
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "deletion_performed": False,
                    "candidates": candidates,
                })
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0
