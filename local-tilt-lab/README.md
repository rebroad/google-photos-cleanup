# Tilt Lab local copy

Captured from the requested page through virtual-display Chrome. It contains the
loaded React/Three/Rapier application resources and does not contact the
original host.

Run:

    cd local-tilt-lab
    python serve.py --port 8765

Then open http://127.0.0.1:8765/ in a browser. The app is interactive:
drag bodies, pour with a press, use the shape controls, and adjust gravity and
bounce. The original Google Fonts were cross-origin browser resources and were
removed; system font fallbacks keep the copy offline/self-contained.
