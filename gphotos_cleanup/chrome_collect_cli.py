from __future__ import annotations

import argparse
import sys

from .chrome_collector import CdpError, collect_to_file
from .network import require_large_network_allowed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.chrome_collect_cli")
    parser.add_argument("--cdp-endpoint", help="local Chrome DevTools HTTP endpoint, e.g. http://127.0.0.1:9222")
    parser.add_argument("--output", required=True)
    parser.add_argument("--url", default="https://photos.google.com/")
    parser.add_argument("--max-scrolls", type=int, default=200, help="maximum scroll steps (large scans require --allow-large-network)")
    parser.add_argument("--chunk-scrolls", type=int, default=100, help="scrolls per resumable DevTools evaluation")
    parser.add_argument("--allow-large-network", action="store_true", help="explicitly allow scans over 500 scrolls; check the active connection first")
    parser.add_argument("--allow-metered-network", action="store_true", help="explicitly override the cellular/unknown-network safety gate")
    args = parser.parse_args(argv)
    if not args.cdp_endpoint:
        parser.error("cloud collection requires the virtual display --cdp-endpoint")
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
            args.output, url=args.url, max_scrolls=args.max_scrolls,
            cdp_endpoint=args.cdp_endpoint, chunk_scrolls=args.chunk_scrolls,
        )
    except OSError as error:
        print("error: Chrome DevTools is unavailable; keep an authenticated Google Photos tab open", file=sys.stderr)
        return 1
    except (CdpError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


raise SystemExit(main())
