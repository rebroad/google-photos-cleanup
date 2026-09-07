from __future__ import annotations

import argparse
import os
import shutil
import sys

from .chrome_collector import CdpError
from .headless_chrome_collector import collect


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.headless_chrome_collect_cli")
    parser.add_argument("--chrome", default=shutil.which("chromium") or shutil.which("google-chrome") or "chromium")
    parser.add_argument("--profile-dir", default="/var/tmp/google-photos-chrome-profile")
    parser.add_argument("--session-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--url", default="https://photos.google.com/")
    parser.add_argument("--max-scrolls", type=int, default=20000)
    parser.add_argument("--chunk-scrolls", type=int, default=100)
    parser.add_argument("--port", type=int, default=9222)
    args = parser.parse_args(argv)
    try:
        collect(args.chrome, args.profile_dir, args.session_file, args.output,
                args.url, args.max_scrolls, args.port, args.chunk_scrolls)
    except (CdpError, OSError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
