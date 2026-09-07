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


def test_duplicate_groups_include_resized_same_kind_only():
    from gphotos_cleanup.photos import duplicate_groups

    groups = duplicate_groups([
        {"id": "image-1", "mime_type": "image/jpeg", "phash": "0" * 256},
        {"id": "image-2", "mime_type": "image/jpeg", "phash": "1" * 8 + "0" * 248},
        {"id": "video", "mime_type": "video/mp4", "phash": "0" * 256},
    ])
    assert len(groups) == 1
    assert {item["id"] for item in groups[0]["items"]} == {"image-1", "image-2"}


def test_duplicate_groups_use_exact_hash_without_perceptual_hash():
    from gphotos_cleanup.photos import duplicate_groups

    groups = duplicate_groups([
        {"id": "a", "mime_type": "video/mp4", "sha256": "ABC"},
        {"id": "b", "mime_type": "video/mp4", "sha256": "abc"},
    ])
    assert [item["id"] for item in groups[0]["items"]] == ["a", "b"]
