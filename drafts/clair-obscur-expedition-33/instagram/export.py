#!/usr/bin/env python3
"""Export every HTML file in slides/ to a same-named 1080x1350 PNG in export/.

Usage:  python3 export.py               # export all slides
        python3 export.py slide-05*     # export only slides matching the pattern(s)

Use this when you have hand-edited the HTML in slides/ and just want fresh PNGs.
(Careful: running build.py REGENERATES slides/*.html from its Python definitions,
overwriting hand edits — build.py is for authoring, export.py is for converting.)
Requires Google Chrome.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

patterns = sys.argv[1:] or ['*']
slides = sorted({f for p in patterns for f in (ROOT / 'slides').glob(f'{p}.html' if not p.endswith('.html') else p)})
if not slides:
    sys.exit(f'no slides match {patterns} in {ROOT / "slides"}')

(ROOT / 'export').mkdir(exist_ok=True)
for html in slides:
    out = ROOT / 'export' / f'{html.stem}.png'
    subprocess.run([CHROME, '--headless', f'--screenshot={out}',
                    '--window-size=1080,1350', '--hide-scrollbars',
                    '--force-device-scale-factor=1', '--disable-gpu',
                    str(html)],
                   check=True, capture_output=True)
    print(f'exported export/{out.name}')
print(f'{len(slides)} slide(s) exported')
