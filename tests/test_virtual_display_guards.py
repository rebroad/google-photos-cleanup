import pytest

from gphotos_cleanup.chrome_collector import CdpError, collect, collect_to_file
from gphotos_cleanup.virtual_display import validate_cdp_endpoint


def test_cloud_collection_rejects_physical_chrome(tmp_path):
    with pytest.raises(CdpError, match="physical-device Chrome is disabled"):
        collect(serial="phone")
    with pytest.raises(CdpError, match="physical-device Chrome is disabled"):
        collect_to_file(str(tmp_path / "cloud.json"), serial="phone")


def test_cloud_collection_requires_virtual_endpoint(tmp_path):
    with pytest.raises(CdpError, match="virtual display"):
        collect()
    with pytest.raises(CdpError, match="virtual display"):
        collect_to_file(str(tmp_path / "cloud.json"))


@pytest.mark.parametrize("endpoint", [
    "http://192.168.1.10:9222",
    "https://127.0.0.1:9222",
    "http://127.0.0.1",
])
def test_cdp_endpoint_must_be_local_http_with_port(endpoint):
    with pytest.raises(ValueError):
        validate_cdp_endpoint(endpoint)


def test_cdp_endpoint_normalizes_trailing_slash():
    assert validate_cdp_endpoint("http://127.0.0.1:9222/") == "http://127.0.0.1:9222"


def test_corrupt_checkpoint_falls_back_to_final_output(tmp_path, monkeypatch):
    import json
    import gphotos_cleanup.chrome_collector as collector

    output = tmp_path / "cloud.json"
    output.write_text(json.dumps({"media_items": [], "scroll_count": 58, "scroll_top": 1234}))
    (tmp_path / "cloud.json.partial").write_text('{"interrupted":')
    captured = {}

    def fake_collect(*args):
        captured["args"] = args

    monkeypatch.setattr(collector, "_collect_to_file_endpoint", fake_collect)
    collector.collect_to_file(str(output), cdp_endpoint="http://127.0.0.1:9222")
    assert captured["args"][7:9] == (58, 1234)
