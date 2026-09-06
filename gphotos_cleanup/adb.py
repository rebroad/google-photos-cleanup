from __future__ import annotations

import json
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class Adb:
    serial: str | None = None

    def run(self, *args: str, check: bool = True) -> str:
        command = ["adb"]
        if self.serial:
            command += ["-s", self.serial]
        command += list(args)
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        if check and result.returncode:
            raise RuntimeError(f"ADB failed ({result.returncode}): {result.stderr.strip()}")
        return result.stdout

    def shell(self, command: str, check: bool = True) -> str:
        return self.run("shell", command, check=check)

    def probe(self) -> dict[str, object]:
        state = self.run("get-state").strip()
        photos = self.run("shell", "dumpsys", "package", "com.google.android.apps.photos", check=False)
        version = "unknown"
        for line in photos.splitlines():
            if "versionName=" in line:
                version = line.split("versionName=", 1)[1].split()[0]
                break
        return {"serial": self.serial, "state": state, "photos_installed": "Package [com.google.android.apps.photos]" in photos, "photos_version": version}

    def inventory(self, roots: list[str], hash_files: bool = False) -> list[dict[str, object]]:
        root_expr = " ".join(shlex.quote(root) for root in roots)
        command = f"find {root_expr} -type f 2>/dev/null"
        paths = [line.strip() for line in self.shell(command).splitlines() if line.strip()]
        records: list[dict[str, object]] = []
        for path in paths:
            quoted = shlex.quote(path)
            stat = self.shell(f"stat -c '%s\t%Y\t%w\t%n' {quoted}", check=False).strip()
            parts = stat.split("\t", 3)
            if len(parts) != 4:
                continue
            size, mtime, birthtime, _ = parts
            suffix = PurePosixPath(path).suffix.lower()
            if suffix not in {".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif", ".mp4", ".mov", ".mkv", ".avi", ".3gp"}:
                continue
            record: dict[str, object] = {"path": path, "filename": PurePosixPath(path).name, "size": int(size), "mtime": int(mtime), "birthtime": birthtime, "extension": suffix}
            if hash_files:
                digest = self.shell(f"sha256sum {quoted}", check=False).split()
                if digest:
                    record["sha256"] = digest[0]
            records.append(record)
        return records

    def dump_json(self, value: object) -> str:
        return json.dumps(value, indent=2, sort_keys=True) + "\n"
