from __future__ import annotations

import argparse
import sys

from .chrome_collector import CdpError, collect_to_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.chrome_collect_cli")
    parser.add_argument("--serial", help="ADB serial for signed-in Chrome on the phone")
    parser.add_argument("--cdp-endpoint", help="local Chrome DevTools HTTP endpoint, e.g. http://127.0.0.1:9222")
    parser.add_argument("--output", required=True)
    parser.add_argument("--url", default="https://photos.google.com/")
    parser.add_argument("--max-scrolls", type=int, default=80)
    parser.add_argument("--no-open", action="store_true", help="do not open Google Photos through ADB before collecting")
    args = parser.parse_args(argv)
    try:
        if not args.serial and not args.cdp_endpoint:
            parser.error("one of --serial or --cdp-endpoint is required")
        collect_to_file(
            args.output, args.serial, args.url, args.max_scrolls,
            args.cdp_endpoint, not args.no_open,
        )
    except OSError as error:
        print("error: Chrome DevTools is unavailable; keep an authenticated Google Photos tab open", file=sys.stderr)
        return 1
    except (CdpError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


raise SystemExit(main())
