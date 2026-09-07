from gphotos_cleanup.photos import match


def test_perceptual_match_does_not_cross_image_video_types():
    phash = "0" * 256
    result = match(
        [{"path": "a.jpg", "filename": "a.jpg", "extension": ".jpg", "phash": phash}],
        [{"id": "video", "filename": "v.mp4", "mime_type": "video/*", "phash": phash}],
    )
    assert result[0]["confidence"] == "none"


def test_perceptual_match_accepts_video_copy():
    phash = "0" * 256
    result = match(
        [{"path": "a.mp4", "filename": "a.mp4", "extension": ".mp4", "phash": phash}],
        [{"id": "video", "filename": "v.mp4", "mime_type": "video/*", "phash": phash}],
    )
    assert result[0]["remote_ids"] == ["video"]
