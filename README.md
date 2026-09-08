# Google Photos Cleanup Reporter

Termux-native, report-only tooling for comparing media on an Android phone with
metadata obtained from Google Photos. The tool never deletes files.

## Status

The ADB inventory, supported Chrome/CDP collection, matching, JSON/CSV
reporting, and private-session feasibility probe are implemented. Cloud
collection reads the rendered Google Photos session through Chrome DevTools;
credentials and cookies are never collected automatically.

## Usage

```sh
python -m gphotos_cleanup auth-probe --serial SERIAL
python -m gphotos_cleanup inventory --serial SERIAL --output inventory.json
python -m gphotos_cleanup list-cloud --input photos-raw.json --output google-photos-list.csv
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
and `deletion_performed` is always `false`. It also records duplicate groups
found on the device and in Google Photos. The tool has no delete operation.

Authenticate in a Chrome session that is visible only through the approved
virtual-display workflow, then collect through Chrome DevTools. The physical
phone screen is not used for collection, scrolling, or media inspection. The
existing `flip7-virtual-display` helper can provide the Android virtual display
when Chrome authentication is needed.

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
  --max-scrolls 7000 --chunk-scrolls 100
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

Do not treat a run as complete unless the raw JSON contains
"complete": true. The supported Google Photos Library API is restricted to
app-created media for new development, and the Picker API lists only media the
user explicitly selects, so neither is a complete personal-library source.
The headless rendered timeline is therefore used with an explicit end-of-list
check.

The collector also supports `--serial` for a directly connected signed-in
Chrome, but the preferred setup is a CDP endpoint forwarded from the virtual
display. Keep the endpoint local and keep all session/profile data outside Git.

Then compare and produce the review-only manifest:

~~~sh
python -m gphotos_cleanup match \
  --inventory /data/data/com.termux/files/usr/tmp/device-inventory-video.json \
  --photos photos-normalized.json --output matches.json
python -m gphotos_cleanup report --matches matches.json \
  --csv deletion-review.csv --manifest deletion-candidates.json
~~~
