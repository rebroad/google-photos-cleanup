from __future__ import annotations

import argparse
import sys

from .obscura_cdp_collector import CdpError, collect_to_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.obscura_collect_cli")
    parser.add_argument("--obscura", required=True, help="path to the Obscura binary")
    parser.add_argument("--storage-dir", required=True)
    parser.add_argument("--port", type=int, default=9333)
    parser.add_argument("--output", required=True)
    parser.add_argument("--url", default="https://photos.google.com/")
    parser.add_argument("--max-scrolls", type=int, default=20000)
    parser.add_argument("--session-file", help="filtered Chrome session JSON outside the repository")
    args = parser.parse_args(argv)
    try:
        collect_to_file(
            args.obscura, args.storage_dir, args.output, args.url,
            args.max_scrolls, args.port, args.session_file,
        )
    except OSError as error:
        print("error: Obscura CDP server is unavailable", file=sys.stderr)
        return 1
    except (CdpError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


raise SystemExit(main())
