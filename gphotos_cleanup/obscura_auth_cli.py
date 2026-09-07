from __future__ import annotations

import argparse
import getpass
import json
import os
import shutil
import sys
import time
import urllib.request

from .obscura_cdp_collector import CdpError, _WebSocket, _wait_for_execution_context, obscura_server


def _defaults() -> tuple[str, str]:
    prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    candidates = [os.path.join(prefix, "tmp", "obscura-hpenvy-aarch64"), shutil.which("obscura")]
    binary = next((path for path in candidates if path and os.access(path, os.X_OK)), candidates[0])
    return binary, os.path.join(prefix, "tmp", "obscura-photos-profile")

def _evaluate(ws: _WebSocket, expression: str, session: str) -> object:
    response = ws.call("Runtime.evaluate", {"expression": expression, "returnByValue": True}, session)
    return response.get("result", {}).get("result", {}).get("value")


def _fill_and_click(ws: _WebSocket, session: str, selector: str, value: str, button: str) -> None:
    expression = (
        "(() => {"
        f"const field = document.querySelector({json.dumps(selector)});"
        "if (!field) return false;"
        "const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;"
        "setter.call(field, " + json.dumps(value) + ");"
        "field.dispatchEvent(new Event('input', {bubbles:true}));"
        "field.dispatchEvent(new Event('change', {bubbles:true}));"
        f"const next = document.querySelector({json.dumps(button)});"
        "if (!next) return false; next.click(); return true;"
        "})()"
    )
    if _evaluate(ws, expression, session) is not True:
        raise CdpError(f"Google login control not found: {selector} / {button}")


def authenticate(binary: str, storage_dir: str, port: int) -> None:
    login_url = "https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fphotos.google.com%2F&service=lh2"
    with obscura_server(binary, storage_dir, port):
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=8) as response:
            browser_url = str(json.load(response)["webSocketDebuggerUrl"])
        ws = _WebSocket(browser_url)
        try:
            target = ws.call("Target.createTarget", {"url": "about:blank"})
            target_id = target.get("result", {}).get("targetId")
            if not isinstance(target_id, str):
                raise CdpError("Obscura did not create a login target")
            attached = ws.call("Target.attachToTarget", {"targetId": target_id, "flatten": True})
            session = attached.get("result", {}).get("sessionId")
            if not isinstance(session, str):
                raise CdpError("Obscura did not attach the login target")
            ws.call("Page.enable", session=session)
            ws.call("Runtime.enable", session=session)
            ws.call("Page.navigate", {"url": login_url}, session=session)
            _wait_for_execution_context(ws, session)
            time.sleep(2)
            email = input("Google account email: ").strip()
            if not email:
                raise CdpError("An email address is required")
            _fill_and_click(ws, session, "input[type=email], input#identifierId, input[name=identifier]", email, "#identifierNext")
            time.sleep(2)
            password = getpass.getpass("Google account password (not saved): ")
            _fill_and_click(ws, session, "input[type=password], input[name=Passwd]", password, "#passwordNext, button[type=submit]")
            del password
            time.sleep(4)
            state = _evaluate(ws, "({url: location.href, title: document.title})", session)
            if isinstance(state, dict):
                print(f"Obscura login page: {state.get('title', '')}", file=sys.stderr)
            input("If Google requests a second factor, complete it through this headless session, then press Enter: ")
            ws.call("Page.navigate", {"url": "https://photos.google.com/"}, session=session)
            _wait_for_execution_context(ws, session)
            time.sleep(3)
            state = _evaluate(ws, "({url: location.href, title: document.title})", session)
            if not isinstance(state, dict) or not str(state.get("url", "")).startswith("https://photos.google.com/"):
                raise CdpError("Obscura did not finish an authenticated Google Photos session")
            print(f"Authenticated Obscura profile saved in {storage_dir}")
        finally:
            ws.close()


def main(argv: list[str] | None = None) -> int:
    default_binary, default_storage = _defaults()
    parser = argparse.ArgumentParser(prog="python -m gphotos_cleanup.obscura_auth_cli")
    parser.add_argument("--obscura", default=default_binary, help=f"Obscura binary (default: {default_binary})")
    parser.add_argument("--storage-dir", default=default_storage, help=f"Persistent profile directory (default: {default_storage})")
    parser.add_argument("--port", type=int, default=9333)
    args = parser.parse_args(argv)
    try:
        authenticate(args.obscura, args.storage_dir, args.port)
    except (CdpError, OSError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


raise SystemExit(main())
