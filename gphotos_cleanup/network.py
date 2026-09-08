from __future__ import annotations

import json
import re
import shutil
import subprocess
from typing import Callable


def _termux_wifi() -> dict[str, object] | None:
    command = shutil.which("termux-wifi-connectioninfo")
    if not command:
        return None
    try:
        result = subprocess.run([command], text=True, capture_output=True, check=False, timeout=5)
        value = json.loads(result.stdout)
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) and value.get("supplicant_state") == "COMPLETED" else None


def _adb_connectivity(serial: str, runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> dict[str, object] | None:
    try:
        result = runner(["adb", "-s", serial, "shell", "dumpsys", "connectivity"], text=True, capture_output=True, check=False, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = result.stdout
    active = re.search(r"(?is)(?:mActiveNetwork|Active network).*?(?=\n\S|\Z)", text)
    block = active.group(0) if active else text[:12000]
    if "TRANSPORT_WIFI" in block:
        return {"transport": "wifi", "metered": "NET_CAPABILITY_NOT_METERED" not in block, "source": "adb:dumpsys connectivity"}
    if "TRANSPORT_CELLULAR" in block:
        return {"transport": "cellular", "metered": True, "source": "adb:dumpsys connectivity"}
    if "TRANSPORT_ETHERNET" in block:
        return {"transport": "ethernet", "metered": False, "source": "adb:dumpsys connectivity"}
    return None


def detect_connection(serial: str | None = None) -> dict[str, object]:
    """Return a conservative connection classification for transfer gating."""
    if serial:
        detected = _adb_connectivity(serial)
        if detected:
            return detected
    if _termux_wifi() is not None:
        return {"transport": "wifi", "metered": False, "source": "termux-wifi-connectioninfo"}
    return {"transport": "unknown", "metered": True, "source": "no reliable Android connectivity signal"}


def require_large_network_allowed(serial: str | None, allow: bool, allow_metered: bool) -> dict[str, object]:
    connection = detect_connection(serial)
    if not allow:
        raise ValueError("large network scan requires --allow-large-network")
    if connection["metered"] and not allow_metered:
        raise ValueError(f"large network scan blocked on {connection['transport']} ({connection['source']}); pass --allow-metered-network only after confirming the cost")
    return connection
