from __future__ import annotations

import argparse
import os
import shutil
import sys

from .chrome_collector import CdpError
from .headless_chrome_collector import collect
from .network import require_large_network_allowed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.headless_chrome_collect_cli")
    parser.add_argument("--chrome", default=shutil.which("chromium") or shutil.which("google-chrome") or "chromium")
    parser.add_argument("--profile-dir", default="/var/tmp/google-photos-chrome-profile")
    parser.add_argument("--session-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--url", default="https://photos.google.com/")
    parser.add_argument("--max-scrolls", type=int, default=200, help="maximum scroll steps (large scans require --allow-large-network)")
    parser.add_argument("--chunk-scrolls", type=int, default=100)
    parser.add_argument("--skip-fingerprints", action="store_true")
    parser.add_argument("--allow-large-network", action="store_true", help="explicitly allow scans over 500 scrolls; check the active connection first")
    parser.add_argument("--allow-metered-network", action="store_true", help="explicitly override the cellular/unknown-network safety gate")
    parser.add_argument("--include-source-urls", action="store_true")
    parser.add_argument("--port", type=int, default=9222)
    args = parser.parse_args(argv)
    if args.max_scrolls > 500 and args.allow_large_network:
        try:
            connection = require_large_network_allowed(None, args.allow_large_network, args.allow_metered_network)
            print(f"network: {connection['transport']} ({connection['source']})", file=sys.stderr)
        except ValueError as error:
            parser.error(str(error))
    if args.max_scrolls > 500 and not args.allow_large_network:
        parser.error("scans over 500 scrolls may download substantial media; pass --allow-large-network after checking the connection")
    try:
        collect(args.chrome, args.profile_dir, args.session_file, args.output,
                args.url, args.max_scrolls, args.port, args.chunk_scrolls, not args.skip_fingerprints, args.include_source_urls or args.skip_fingerprints)
    except (CdpError, OSError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
