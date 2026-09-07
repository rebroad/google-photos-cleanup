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
python -m gphotos_cleanup report --matches matches.json --csv report.csv \
  --manifest deletion-candidates.json
```

`photos.json` is the normalized output expected from a future authenticated
Google Photos adapter. A sample schema is shown in `gphotos_cleanup/photos.py`.

The inventory command uses `adb shell find` and `stat`; it does not copy the
phone's media to Termux. Hashing is opt-in and only hashes files remotely when
the device provides `sha256sum`.

The JSON manifest is review-only: every candidate has `action: "review_only"`,
and `deletion_performed` is always `false`. The tool has no delete operation.

For an authenticated Obscura session, collect and compare with:

```sh
python -m gphotos_cleanup.collect_cli \
  --obscura /path/to/obscura \
  --storage-dir "$PREFIX/tmp/obscura-photos-profile" \
  --output photos.json
python -m gphotos_cleanup normalize --input photos.json --output photos-normalized.json
python -m gphotos_cleanup match \
  --inventory /data/data/com.termux/files/usr/tmp/device-inventory-video.json \
  --photos photos-normalized.json --output matches.json
python -m gphotos_cleanup report --matches matches.json \
  --csv deletion-review.csv --manifest deletion-candidates.json
```


When Chrome on the phone is visibly signed in, the cookie-free CDP collector can
scroll the live session and write redacted cloud records:

```sh
python -m gphotos_cleanup.chrome_collect_cli \
  --serial 10.84.166.154:43021 \
  --output photos.json
```

This uses Chrome DevTools through ADB forwarding; it does not export cookies.
The phone must be unlocked and Google Photos must be signed in.
