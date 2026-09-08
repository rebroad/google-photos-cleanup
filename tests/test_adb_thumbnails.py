from gphotos_cleanup.adb import Adb


def test_thumbnail_ids_normalize_android_storage_paths(monkeypatch):
    rows = (
        "Row: 0 _id=12, _data=/storage/emulated/0/DCIM/Camera/a.jpg\n"
        "Row: 1 _id=13, _data=/storage/emulated/0/DCIM/Camera/b.mp4\n"
    )
    monkeypatch.setattr(Adb, "shell", lambda self, command, check=True: rows)

    assert Adb("serial").thumbnail_ids() == {
        "/sdcard/DCIM/Camera/a.jpg": ("12", "image"),
        "/sdcard/DCIM/Camera/b.mp4": ("13", "video"),
    }
