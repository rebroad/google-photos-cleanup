# Google Photos Cleanup Reporter

Termux-native, report-only tooling for comparing media on an Android phone with
metadata obtained from Google Photos. The tool never deletes files.

## Status

The ADB inventory, matching, JSON/CSV reporting, and private-session feasibility
probe are implemented. The Google Photos private protocol is intentionally an
isolated adapter: Android package inspection does not expose a supported backup
status API, and no credentials are collected automatically.

## Usage

```sh
python -m gphotos_cleanup auth-probe --serial SERIAL
python -m gphotos_cleanup inventory --serial SERIAL --output inventory.json
python -m gphotos_cleanup match --inventory inventory.json --photos photos.json --output matches.json
python -m gphotos_cleanup report --matches matches.json --csv report.csv
```

`photos.json` is the normalized output expected from a future authenticated
Google Photos adapter. A sample schema is shown in `gphotos_cleanup/photos.py`.

The inventory command uses `adb shell find` and `stat`; it does not copy the
phone's media to Termux. Hashing is opt-in and only hashes files remotely when
the device provides `sha256sum`.
