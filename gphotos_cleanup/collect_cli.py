from __future__ import annotations

import argparse

from .obscura_collector import collect, write_cloud_records


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.collect_cli")
    parser.add_argument("--obscura", required=True)
    parser.add_argument("--storage-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--url", default="https://photos.google.com/")
    parser.add_argument("--wait", type=int, default=5)
    args = parser.parse_args()
    write_cloud_records(collect(args.obscura, args.storage_dir, args.url, args.wait), args.output)
    return 0


raise SystemExit(main())
