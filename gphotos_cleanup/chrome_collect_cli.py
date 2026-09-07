from __future__ import annotations

import argparse
import sys

from .chrome_collector import CdpError, collect_to_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.chrome_collect_cli")
    parser.add_argument("--serial", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--url", default="https://photos.google.com/")
    parser.add_argument("--max-scrolls", type=int, default=80)
    args = parser.parse_args(argv)
    try:
        collect_to_file(args.serial, args.output, args.url, args.max_scrolls)
    except OSError as error:
        print("error: Chrome DevTools is unavailable; unlock the phone and leave Google Photos open", file=sys.stderr)
        return 1
    except (CdpError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


raise SystemExit(main())
