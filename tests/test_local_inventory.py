from PIL import Image

from gphotos_cleanup.local import inventory

def test_local_inventory_scans_media_without_adb(tmp_path):
    media = tmp_path / "DCIM"
    media.mkdir()
    Image.new("RGB", (12, 8), "red").save(media / "photo.jpg")
    (media / "note.txt").write_text("not media")
    (media / ".thumbnails").mkdir()
    Image.new("RGB", (12, 8), "blue").save(media / ".thumbnails" / "thumb.jpg")

    records = inventory([str(media)], hash_files=True, fingerprints=True)

    assert len(records) == 1
    assert records[0]["filename"] == "photo.jpg"
    assert len(records[0]["sha256"]) == 64
    assert records[0]["fingerprint_kind"] == "image"
