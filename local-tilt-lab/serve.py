#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from urllib.parse import urlsplit
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
MAP = json.loads((ROOT / "resource-map.json").read_text())

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlsplit(self.path)
        key = parsed.path or "/"
        if parsed.query:
            key += "?" + parsed.query
        if key == "/":
            return self._serve(ROOT / "index.html", "text/html")
        if parsed.path == "/favicon.ico":
            entry = MAP.get("/favicon.svg")
            return self._serve(ROOT / entry["file"], "image/svg+xml")
        entry = MAP.get(key) or MAP.get(parsed.path)
        if entry:
            return self._serve(ROOT / entry["file"], entry["content_type"])
        if parsed.path.startswith("/__local__/"):
            return self._serve(ASSETS / parsed.path.rsplit("/", 1)[-1], "application/octet-stream")
        self.send_error(404, "local resource not captured")

    def _serve(self, path: Path, content_type: str):
        try:
            data = path.read_bytes()
        except FileNotFoundError:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"http://{args.host}:{args.port}/", flush=True)
    server.serve_forever()

if __name__ == "__main__":
    main()
