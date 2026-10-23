#!/usr/bin/env python3
"""Draw the app icons into pwa/icons/ (a floor plan with a player and an enemy on the app's teal)."""
import pathlib
from PIL import Image, ImageDraw

OUT = pathlib.Path(__file__).resolve().parent.parent / 'pwa' / 'icons'
TEAL, WHITE, RED, BLUE = (13, 138, 124), (255, 255, 255), (229, 72, 77), (10, 143, 240)

def glyph(d, size, scale, ox, oy):
    # the menu mark, drawn on a 64-unit grid
    P = lambda x, y: (ox + x * scale, oy + y * scale)
    w = max(2, round(3.2 * scale))
    d.polygon([P(8, 14), P(38, 14), P(38, 28), P(56, 28), P(56, 52), P(8, 52)], outline=WHITE, width=w)
    d.line([P(38, 28), P(38, 38)], fill=WHITE, width=w)
    d.line([P(22, 14), P(22, 28), P(8, 28)], fill=WHITE, width=w, joint='curve')
    for (x, y, c) in [(18, 41, BLUE), (46, 43, RED)]:
        r = 4.2 * scale
        cx, cy = P(x, y)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c, outline=WHITE, width=max(1, round(1.4 * scale)))

def icon(size, rounded, inset):
    big = size * 4
    img = Image.new('RGBA', (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded: d.rounded_rectangle([0, 0, big - 1, big - 1], radius=big * 0.22, fill=TEAL)
    else: d.rectangle([0, 0, big, big], fill=TEAL)
    span = big * (1 - 2 * inset)                       # glyph spans 48 of its 64 units
    scale = span / 48
    glyph(d, big, scale, big / 2 - 32 * scale, big / 2 - 33 * scale)
    return img.resize((size, size), Image.LANCZOS)

OUT.mkdir(parents=True, exist_ok=True)
icon(192, True, 0.14).save(OUT / 'icon-192.png')
icon(512, True, 0.14).save(OUT / 'icon-512.png')
icon(180, False, 0.16).save(OUT / 'icon-180.png')
icon(512, False, 0.24).save(OUT / 'maskable-512.png')   # Android crops these into circles and squircles
print('icons written')
