#!/usr/bin/env python3
"""Build the installable web app in docs/ from map-designer.html.

map-designer.html is the one source for both the Claude artifact and the installed app.
Run this after changing it:  python3 tools/build_pwa.py
GitHub Pages serves docs/ at https://gamesbyaaron.github.io/Map-Maker-2/
"""
import hashlib, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, PWA, OUT = ROOT / 'map-designer.html', ROOT / 'pwa', ROOT / 'docs'
CDN = 'https://cdn.jsdelivr.net/npm/polygon-clipping@0.15.7/dist/polygon-clipping.umd.min.js'

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Block out FPS levels on a 1 m grid: rooms, doors, enemies, floors and simulated playthroughs.">
<meta name="theme-color" content="#fbfcfd" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#141b23" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Map Designer">
<style>
:root { color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
body { margin: 0; font: 14px system-ui, sans-serif; }
img { max-width: 100%; }
[hidden] { display: none !important; }
#pwa-update {
  position: fixed; z-index: 70; left: 50%; top: calc(env(safe-area-inset-top, 0px) + 10px); transform: translateX(-50%);
  border: 0; border-radius: 999px; padding: 10px 18px; background: var(--accent, #0d8a7c); color: var(--accent-fg, #fff);
  font: 600 14px var(--font-body, system-ui, sans-serif); box-shadow: 0 6px 24px rgba(0, 0, 0, .25); cursor: pointer; white-space: nowrap;
}
</style>
</head>
<body>
"""

TAIL = """
<button id="pwa-update" hidden>Update ready · Reload</button>
<script>
// installed app: offline support and the "Update ready" button
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').then(reg => {
      const offer = w => { const b = document.getElementById('pwa-update'); b.hidden = false; b.onclick = () => w.postMessage('skip-waiting'); };
      if (reg.waiting && navigator.serviceWorker.controller) offer(reg.waiting);
      reg.addEventListener('updatefound', () => {
        const w = reg.installing;
        if (w) w.addEventListener('statechange', () => { if (w.state === 'installed' && navigator.serviceWorker.controller) offer(w); });
      });
      document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') reg.update().catch(() => {}); });
    }).catch(() => {});
    let reloading = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => { if (!reloading) { reloading = true; location.reload(); } });
  });
}
</script>
</body>
</html>
"""

def main():
    app = SRC.read_text()
    assert CDN in app, 'polygon-clipping script tag not found'
    app = app.replace(CDN, 'polygon-clipping.umd.min.js')
    page = HEAD + app + TAIL
    if OUT.exists():
        for p in OUT.iterdir():
            if p.name != 'icons':
                p.unlink() if p.is_file() else shutil.rmtree(p)
    OUT.mkdir(exist_ok=True)
    (OUT / 'index.html').write_text(page)
    for name in ['manifest.webmanifest', 'polygon-clipping.umd.min.js', 'polygon-clipping.LICENSE.md']:
        shutil.copy(PWA / name, OUT / name)
    icons = OUT / 'icons'
    if icons.exists(): shutil.rmtree(icons)
    shutil.copytree(PWA / 'icons', icons)
    digest = hashlib.sha1()
    for p in sorted(OUT.rglob('*')):
        if p.is_file(): digest.update(p.read_bytes())
    digest.update((PWA / 'sw.js').read_bytes())
    version = digest.hexdigest()[:12]
    (OUT / 'sw.js').write_text((PWA / 'sw.js').read_text().replace('__VERSION__', version))
    (OUT / '.nojekyll').write_text('')
    print(f'built docs/ (version {version})')

if __name__ == '__main__':
    main()
