from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import datetime, timezone
import sys
from pathlib import Path

from .adb import Adb
from .fingerprint import VIDEO_EXTENSIONS, fingerprint_adb, fingerprint_adb_thumbnail, video_fingerprint_adb
from .local import inventory as local_inventory
from .photos import duplicate_groups, match, normalize


def _write(path: str, value: object) -> None:
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gphotos-cleanup")
    sub = parser.add_subparsers(dest="command", required=True)
    probe = sub.add_parser("auth-probe", help="check ADB and Google Photos availability")
    probe.add_argument("--serial")
    inventory = sub.add_parser("inventory", help="inventory media on the phone")
    inventory.add_argument("--serial")
    inventory.add_argument("--local", action="store_true", help="scan Termux-accessible shared storage without ADB")
    inventory.add_argument("--local-root", action="append", help="local media root; repeatable (defaults to Termux shared storage)")
    inventory.add_argument("--root", action="append", default=["/sdcard/DCIM", "/sdcard/Pictures", "/sdcard/Movies"])
    inventory.add_argument("--hash", action="store_true")
    inventory.add_argument("--fingerprint", action="store_true", help="compute perceptual fingerprints from Android thumbnails")
    inventory.add_argument("--full-fingerprint", action="store_true", help="explicitly read original media for fingerprints")
    inventory.add_argument("--output", required=True)
    list_cloud = sub.add_parser("list-cloud", help="write a reviewable CSV of collected Google Photos items")
    list_cloud.add_argument("--input", required=True)
    list_cloud.add_argument("--output", required=True)
    normalize_cmd = sub.add_parser("normalize", help="normalize adapter JSON")
    normalize_cmd.add_argument("--input", required=True)
    normalize_cmd.add_argument("--output", required=True)
    matcher = sub.add_parser("match", help="match inventory against normalized Photos metadata")
    matcher.add_argument("--inventory", required=True)
    matcher.add_argument("--photos", required=True)
    matcher.add_argument("--output", required=True)
    matcher.add_argument("--phash-threshold", type=int, default=24)
    report = sub.add_parser("report", help="write review CSV and optional deletion-candidate manifest")
    report.add_argument("--matches", required=True)
    report.add_argument("--csv", required=True)
    report.add_argument("--manifest", help="write a JSON review-only deletion-candidate manifest")
    args = parser.parse_args(argv)
    try:
        if args.command == "auth-probe":
            print(json.dumps(Adb(args.serial).probe(), indent=2, sort_keys=True))
        elif args.command == "inventory":
            if args.local and args.serial:
                raise ValueError("--local and --serial are mutually exclusive")
            if args.local:
                prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
                shared = Path.home() / "storage" / "shared"
                roots = args.local_root or [
                    str(shared / "DCIM"), str(shared / "Pictures"), str(shared / "Movies"),
                ]
                files = local_inventory(roots, args.hash, args.fingerprint)
                _write(args.output, {"serial": None, "local": True, "roots": roots, "files": files})
                return 0
            serial = args.serial
            if args.fingerprint and not serial:
                devices = [line.split()[0] for line in Adb().run("devices").splitlines() if line.endswith("\tdevice")]
                if len(devices) != 1:
                    raise RuntimeError("--fingerprint requires --serial when ADB does not have exactly one device")
                serial = devices[0]
            files = Adb(serial).inventory(args.root, args.hash)
            if args.fingerprint:
                thumbnail_ids = None if args.full_fingerprint else Adb(serial).thumbnail_ids()
                for item in files:
                    extension = str(item.get("extension", "")).lower()
                    if extension in {".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif"}:
                        try:
                            if thumbnail_ids is None:
                                item["phash"] = fingerprint_adb(serial, str(item["path"]))
                            else:
                                media_id, kind = thumbnail_ids[str(item["path"])]
                                item["phash"] = fingerprint_adb_thumbnail(serial, media_id, kind)
                            item["fingerprint_kind"] = "image-thumbnail" if thumbnail_ids is not None else "image"
                        except (OSError, RuntimeError, KeyError):
                            item["phash_error"] = True
                    elif extension in VIDEO_EXTENSIONS:
                        try:
                            if thumbnail_ids is None:
                                item["phash"] = video_fingerprint_adb(serial, str(item["path"]))
                                item["fingerprint_kind"] = "video-contact-sheet"
                            else:
                                media_id, kind = thumbnail_ids[str(item["path"])]
                                item["phash"] = fingerprint_adb_thumbnail(serial, media_id, kind)
                                item["fingerprint_kind"] = "video-thumbnail"
                        except (OSError, RuntimeError, ValueError, KeyError):
                            item["phash_error"] = True
            _write(args.output, {"serial": serial, "roots": args.root, "files": files})
        elif args.command == "list-cloud":
            source = json.loads(Path(args.input).read_text(encoding="utf-8"))
            items = source.get("media_items", source) if isinstance(source, dict) else source
            if not isinstance(items, list):
                raise ValueError("cloud input must contain a media_items list")
            fields = ["id", "filename", "mime_type", "width", "height", "phash", "source"]
            with Path(args.output).open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                for item in items:
                    if isinstance(item, dict):
                        writer.writerow({field: item.get(field, "") for field in fields})
        elif args.command == "normalize":
            source = json.loads(Path(args.input).read_text(encoding="utf-8"))
            _write(args.output, normalize(source["media_items"] if isinstance(source, dict) and "media_items" in source else source))
        elif args.command == "match":
            inventory = json.loads(Path(args.inventory).read_text(encoding="utf-8"))["files"]
            photos = json.loads(Path(args.photos).read_text(encoding="utf-8"))
            matches = match(inventory, photos, tolerance_seconds=172800)
            _write(args.output, {
                "matches": matches,
                "device_duplicate_groups": duplicate_groups(inventory, args.phash_threshold),
                "google_photos_duplicate_groups": duplicate_groups(photos, args.phash_threshold),
            })
        elif args.command == "report":
            report_input = json.loads(Path(args.matches).read_text(encoding="utf-8"))
            matches = report_input.get("matches", report_input) if isinstance(report_input, dict) else report_input
            if not isinstance(matches, list):
                raise ValueError("matches input must contain a matches list")
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
                    "schema": "gphotos-cleanup/deletion-candidates/v2",
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "deletion_performed": False,
                    "candidates": candidates,
                    "device_duplicate_groups": report_input.get("device_duplicate_groups", []) if isinstance(report_input, dict) else [],
                    "google_photos_duplicate_groups": report_input.get("google_photos_duplicate_groups", []) if isinstance(report_input, dict) else [],
                })
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0
