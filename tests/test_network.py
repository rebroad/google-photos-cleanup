from subprocess import CompletedProcess

import pytest

from gphotos_cleanup import network


def test_adb_wifi_detection_reads_active_capabilities():
    result = network._adb_connectivity(
        "serial",
        runner=lambda *args, **kwargs: CompletedProcess(
            args[0], 0, "mActiveNetwork: TRANSPORT_WIFI NET_CAPABILITY_NOT_METERED\n", ""
        ),
    )
    assert result == {
        "transport": "wifi",
        "metered": False,
        "source": "adb:dumpsys connectivity",
    }


def test_cellular_requires_explicit_metered_override(monkeypatch):
    monkeypatch.setattr(network, "detect_connection", lambda serial=None: {
        "transport": "cellular", "metered": True, "source": "test"
    })
    with pytest.raises(ValueError, match="allow-metered-network"):
        network.require_large_network_allowed("serial", True, False)


def test_thumbnail_url_is_small_google_media_url():
    from gphotos_cleanup.obscura_collector import _thumbnail_url

    assert _thumbnail_url("https://lh3.googleusercontent.com/a=w2048-h1536") == "https://lh3.googleusercontent.com/a=w256-h256"
