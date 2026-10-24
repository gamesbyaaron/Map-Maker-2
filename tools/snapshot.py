#!/usr/bin/env python3
"""Freeze the current build as a saved version that never changes:  python3 tools/snapshot.py v1

Copies docs/ into snapshots/<name>/ and makes it a separate app: its own name and grey icon, its own
saved maps (so newer versions can't touch them), and its own offline cache. build_pwa.py then publishes
it unchanged at https://gamesbyaaron.github.io/Map-Maker-2/<name>/
Run build_pwa.py first so docs/ holds the version you want to keep.
"""
import json, pathlib, re, shutil, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS, SNAPS = ROOT / 'docs', ROOT / 'snapshots'
GREY = (84, 94, 108)

def recolor(path):
    # the teal background turns grey; the white plan and the coloured dots stay
    img = Image.open(path).convert('RGBA')
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a and g > r + 40 and g > b:                       # teal-ish, including anti-aliased edges
                t = (g - r) / 125
                px[x, y] = tuple(round(c * t + w * (1 - t)) for c, w in zip(GREY, (r, g, b))) + (a,)
    img.save(path)

def main(name):
    assert re.fullmatch(r'v\d+', name), 'name it like v1, v2…'
    out = SNAPS / name
    assert not out.exists(), f'{out} already exists; saved versions are never overwritten'
    shutil.copytree(DOCS, out)
    label = name.upper().replace('V', 'v')

    page = (out / 'index.html').read_text()
    assert page.count("'mm2.") >= 10, 'storage keys not found'
    page = page.replace("'mm2.", f"'mm2{name}.")
    page = page.replace('<title>FPS Map Designer</title>', f'<title>FPS Map Designer {label}</title>')
    page = page.replace('<h1>FPS Map Designer</h1>', f'<h1>FPS Map Designer {label}</h1>')
    page = page.replace('content="Map Designer"', f'content="Map Designer {label}"')
    (out / 'index.html').write_text(page)

    m = json.loads((out / 'manifest.webmanifest').read_text())
    m['name'] = f'FPS Map Designer {label}'
    m['short_name'] = f'Map Designer {label}'
    (out / 'manifest.webmanifest').write_text(json.dumps(m, indent=2) + '\n')

    sw = (out / 'sw.js').read_text()
    assert sw.count("'core-'") == 4, 'cache names not found'
    (out / 'sw.js').write_text(sw.replace("'core-'", f"'{name}-core-'").replace("'fonts'", f"'{name}-fonts'"))

    for p in (out / 'icons').glob('*.png'): recolor(p)
    print(f'saved snapshots/{name}/')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'v1')
