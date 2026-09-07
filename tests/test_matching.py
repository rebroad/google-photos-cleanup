from gphotos_cleanup.photos import match, normalize


def test_exact_hash_is_high_confidence():
    result = match([{"path": "/sdcard/DCIM/a.jpg", "filename": "a.jpg", "sha256": "ABC", "mtime": 0}], [{"id": "g1", "filename": "a.jpg", "sha256": "abc"}])
    assert result[0]["confidence"] == "high"
    assert result[0]["remote_ids"] == ["g1"]


def test_filename_only_remains_review():
    result = match([{"path": "/sdcard/DCIM/a.jpg", "filename": "a.jpg", "size": 3, "mtime": 0}], [{"id": "g1", "filename": "a.jpg"}])
    assert result[0]["confidence"] == "review"


def test_normalize_discards_sensitive_unknown_fields():
    result = normalize([{"id": "g1", "filename": "a.jpg", "baseUrl": "secret", "token": "secret"}])
    assert "baseUrl" not in result[0]
    assert "token" not in result[0]
    assert result[0]["basename"] == "a.jpg"



def test_perceptual_hash_matches_resized_or_recompressed_copy():
    local_hash = "0" * 256
    remote_hash = "1" * 8 + "0" * 248
    result = match(
        [{"path": "/sdcard/DCIM/a.jpg", "filename": "a.jpg", "phash": local_hash}],
        [{"id": "g1", "filename": "different-name.jpg", "phash": remote_hash}],
    )
    assert result[0]["confidence"] == "review"
    assert result[0]["evidence"] == ["perceptual_hash"]
    assert result[0]["remote_ids"] == ["g1"]
