// Offline support for the installed app. The build stamps a new version into this file every time the
// app changes, which makes the browser install the new version and the page offer "Update ready".
const VERSION = '5edd519edef6';
const CORE = ['./', 'index.html', 'manifest.webmanifest', 'polygon-clipping.umd.min.js',
  'icons/icon-180.png', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/maskable-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open('v1-core-' + VERSION).then(c => c.addAll(CORE)));
});
self.addEventListener('message', e => { if (e.data === 'skip-waiting') self.skipWaiting(); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith('v1-core-') && k !== 'v1-core-' + VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin === location.origin) {
    // the app's own files come from this version's cache, so it opens offline
    e.respondWith(caches.open('v1-core-' + VERSION).then(c => c.match(req, { ignoreSearch: true })).then(hit => hit || fetch(req)));
  } else if (url.host === 'fonts.googleapis.com' || url.host === 'fonts.gstatic.com') {
    // fonts: use the saved copy right away and refresh it in the background
    e.respondWith(caches.open('v1-fonts').then(async c => {
      const hit = await c.match(req);
      const net = fetch(req).then(r => { if (r.ok || r.type === 'opaque') c.put(req, r.clone()); return r; }).catch(() => hit);
      return hit || net;
    }));
  }
});
