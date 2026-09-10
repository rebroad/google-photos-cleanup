# Cheeky Phone local copy

Captured from https://lozknowles.com/cheeky-phone.html through Chrome on the
Android virtual display.

Run a local server from the repository root:

    python -m http.server 8766 --directory local-cheeky-phone

Open http://127.0.0.1:8766/ in a browser. The copy includes the page, six
JavaScript modules, CSS, and the 533 KB George recording.

## Speech/audio behavior

There are two voice paths:

- Device voice: the app reads the selected SpeechSynthesisVoice with a
  SpeechSynthesisUtterance. It uses the selected locale, defaults to en-GB,
  and sets rate to 0.92. The browser/OS supplies the actual voice; the app
  cancels older utterances and applies a 20-second timeout.
- George recording: the app fetches assets/cheeky-george.mp3, decodes it
  with AudioContext.decodeAudioData, and plays named time slices from
  cheeky-clips.js. Underwater playback routes through high-/low-pass filters,
  a short delay/echo, and a 2.6 Hz modulation for the muffled warble. Above
  water the clip is routed directly.

The app also uses Web Audio for bubbles and pauses/cancels speech when muted,
hidden, stopped, or superseded. Captions remain available if audio or device
speech is unavailable.
