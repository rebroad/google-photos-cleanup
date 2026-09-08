from __future__ import annotations

import argparse
import sys

from .obscura_cdp_collector import CdpError, collect_to_file
from .network import require_large_network_allowed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.obscura_collect_cli")
    parser.add_argument("--obscura", required=True, help="path to the Obscura binary")
    parser.add_argument("--storage-dir", required=True)
    parser.add_argument("--port", type=int, default=9333)
    parser.add_argument("--output", required=True)
    parser.add_argument("--url", default="https://photos.google.com/")
    parser.add_argument("--max-scrolls", type=int, default=200, help="maximum scroll steps (large scans require --allow-large-network)")
    parser.add_argument("--session-file", help="filtered Chrome session JSON outside the repository")
    parser.add_argument("--allow-large-network", action="store_true", help="explicitly allow scans over 500 scrolls; check the active connection first")
    parser.add_argument("--allow-metered-network", action="store_true", help="explicitly override the cellular/unknown-network safety gate")
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
