# Google Photos Cleanup Reporter

Termux-native, report-only tooling for comparing media on an Android phone with
metadata obtained from Google Photos. The tool never deletes files.

## Status

The ADB inventory, supported Chrome/CDP collection, matching, JSON/CSV
reporting, and private-session feasibility probe are implemented. Cloud
collection reads the rendered Google Photos session through Chrome DevTools;
credentials are entered interactively; explicitly exported cookies are saved only to a 0600 file outside this repository.

## Usage

```sh
python -m gphotos_cleanup auth-probe --serial SERIAL
python -m gphotos_cleanup inventory --serial SERIAL --output inventory.json
# ADB-free scan of Termux-accessible shared storage:
python -m gphotos_cleanup inventory --local --hash --fingerprint --output inventory.json
python -m gphotos_cleanup list-cloud --input photos-raw.json --output google-photos-list.csv
python -m gphotos_cleanup match --inventory inventory.json --photos photos.json --output matches.json
python -m gphotos_cleanup report --matches matches.json --csv report.csv \
  --manifest deletion-candidates.json
```

`photos.json` is the normalized output expected from a future authenticated
Google Photos adapter. A sample schema is shown in `gphotos_cleanup/photos.py`.

The inventory command uses `adb shell find` and `stat`; it does not copy the
phone's media to Termux. On a device where Termux has Android shared-storage
permission, `inventory --local` scans `$HOME/storage/shared` directly and needs
no ADB. Hashing and perceptual fingerprints are opt-in; fingerprints cover
resized/recompressed images and video contact sheets.

The JSON manifest is review-only: every candidate has `action: "review_only"`,
and `deletion_performed` is always `false`. It also records duplicate groups
found on the device and in Google Photos. The tool has no delete operation.

Authenticate in a Chrome session hosted on an Android virtual display, then collect through Chrome DevTools. The physical phone screen is not used for collection, scrolling, or media inspection. The display-only scrcpy server fork is maintained separately; this repository does not vendor scrcpy, its client, SDL, FFmpeg, Gradle, or an Android SDK. Its server artifact must be built on the local ARM64 Termux host and pushed with `adb`; video capture, compression, windowing, and transport are disabled.

First export only the filtered Google authentication cookies through Chrome
DevTools. The session file is written with mode 0600 outside this repository:

~~~sh
python3 -m gphotos_cleanup.chrome_auth_cli
~~~

When the virtual Chrome DevTools endpoint is tunneled to Termux, export from
that endpoint instead:

~~~sh
python3 -m gphotos_cleanup.chrome_auth_cli \
  --cdp-endpoint http://127.0.0.1:19223
~~~

The protected session can then be used by the local headless Chromium build
(which avoids Android Chrome’s display/network path):

~~~sh
python3 -m gphotos_cleanup.headless_chrome_collect_cli \
  --chrome "$(command -v chromium-browser)" \
  --profile-dir "$PREFIX/tmp/google-photos-headless-profile" \
  --session-file "$PREFIX/tmp/google-photos-session.json" \
  --output "$PREFIX/tmp/photos-raw-headless.json" \
  --max-scrolls 7000 --chunk-scrolls 100 --allow-large-network
~~~

Then run the collector against the authenticated Chrome DevTools endpoint. It
discovers the real nested timeline scroller, waits for virtualized tiles to
render, and records whether the bottom was actually reached:

~~~sh
python3 -m gphotos_cleanup.chrome_collect_cli \
  --cdp-endpoint http://127.0.0.1:19223 \
  --no-open \
  --output "$PREFIX/tmp/photos-raw-chrome.json"
python -m gphotos_cleanup normalize \
  --input "$PREFIX/tmp/photos-raw-chrome.json" \
  --output "$PREFIX/tmp/photos-normalized.json"
python -m gphotos_cleanup list-cloud \
  --input "$PREFIX/tmp/photos-raw-chrome.json" \
  --output "$PREFIX/tmp/google-photos-list.csv"
~~~

Large scans are deliberately opt-in because scrolling Google Photos causes
Chrome on the device or the headless browser to fetch thumbnails. Check whether
the current connection is metered before adding `--allow-large-network`; without
it, collection is capped at 200 scrolls by default.

Do not treat a run as complete unless the raw JSON contains
"complete": true. The supported Google Photos Library API is restricted to
app-created media for new development, and the Picker API lists only media the
user explicitly selects, so neither is a complete personal-library source.
The headless rendered timeline is therefore used with an explicit end-of-list
check. Cloud perceptual enrichment downloads each selected thumbnail and is
also explicitly gated with `--allow-large-network`; it is never implicit.

Cloud collection and session export are virtual-display-only: provide the local
`--cdp-endpoint` (for example `http://127.0.0.1:19223`). Physical-device
Chrome is rejected so scrolling cannot touch the phone user’s display. Keep
the endpoint local and keep all session/profile data outside Git.

Then compare and produce the review-only manifest:

~~~sh
python -m gphotos_cleanup match \
  --inventory /data/data/com.termux/files/usr/tmp/device-inventory-video.json \
  --photos photos-normalized.json --output matches.json
python -m gphotos_cleanup report --matches matches.json \
  --csv deletion-review.csv --manifest deletion-candidates.json
~~~

## Transfer safety

Large scans classify the active connection automatically. On Termux, a completed
`termux-wifi-connectioninfo` result is treated as Wi-Fi; when a device serial is
provided, Android connectivity capabilities are checked first. Cellular and
unknown connections are treated as metered and block large scans unless both
`--allow-large-network` and `--allow-metered-network` are supplied.

Cloud fingerprints are derived from 256px Google thumbnail URLs and are capped
at 512 KiB per image. Original images and full-resolution videos are never
downloaded by the fingerprint path; videos use a rendered poster thumbnail when
one is available. Metadata-only collection remains the preferred first pass.
