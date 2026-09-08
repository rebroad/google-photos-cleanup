from __future__ import annotations

import urllib.parse


def validate_cdp_endpoint(endpoint: str) -> str:
    """Validate the local DevTools bridge used by the virtual display."""
    parsed = urllib.parse.urlsplit(endpoint)
    try:
        port = parsed.port
    except ValueError as error:
        raise ValueError("--cdp-endpoint must contain a valid port") from error
    if parsed.scheme != "http" or not parsed.hostname or not port:
        raise ValueError("--cdp-endpoint must be an HTTP endpoint with a port")
    if parsed.hostname.lower() not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("--cdp-endpoint must point to a local virtual-display endpoint")
    return endpoint.rstrip("/")
