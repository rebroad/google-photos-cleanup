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
