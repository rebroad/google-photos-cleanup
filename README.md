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

Collect from a supported signed-in Chrome session. The preferred mode uses
Chrome already signed in on the phone through ADB port forwarding. The tool does
not tap the screen, request your password, export cookies, or modify the phone:

~~~sh
python3 -m gphotos_cleanup.chrome_collect_cli \
  --serial SERIAL --output photos-raw.json
python -m gphotos_cleanup normalize --input photos-raw.json --output photos-normalized.json
~~~

The ADB mode opens photos.google.com in Chrome automatically, then uses Chrome
DevTools to inspect the rendered media and scroll the Photos timeline. This may
bring Chrome visibly to the foreground, but the collector performs no taps or
screen automation. ADB forwards a temporary local port and removes it when
collection finishes. Use --no-open if Chrome is already prepared and should not
be navigated.

When ADB/phone Chrome is unavailable, use any local Chrome-compatible browser
with a dedicated profile stored outside this repository and a local DevTools
endpoint. Authentication is performed once by the user in that browser; the
collector only uses the already-authenticated session afterward:

~~~sh
# Example browser setup; choose a profile path outside the repository.
chrome --remote-debugging-port=9222 \
  --user-data-dir="$PREFIX/tmp/google-photos-chrome-profile" \
  https://photos.google.com/
python3 -m gphotos_cleanup.chrome_collect_cli \
  --cdp-endpoint http://127.0.0.1:9222 --output photos-raw.json
~~~

The endpoint mode is headless from the collector's perspective: it performs no
screen automation. Keep profile directories, DevTools state, and reports under
$PREFIX/tmp on Termux (or /var/tmp on Linux), never in this public repo.
Obscura remains available as an experimental diagnostic collector, but Google
may reject its login flow before a password field is offered, so it is not the
primary authentication path.

Then compare and produce the review-only manifest:

~~~sh
python -m gphotos_cleanup match \
  --inventory /data/data/com.termux/files/usr/tmp/device-inventory-video.json \
  --photos photos-normalized.json --output matches.json
python -m gphotos_cleanup report --matches matches.json \
  --csv deletion-review.csv --manifest deletion-candidates.json
~~~
