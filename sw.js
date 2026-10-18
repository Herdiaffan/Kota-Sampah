const CACHE_NAME = 'kota-bersih-3d-v18-hd-lowram';
const CORE = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./assets/visual/app-icon.svg",
  "./assets/audio/area_sweep.ogg",
  "./assets/audio/city_ambience.ogg",
  "./assets/audio/city_theme.ogg",
  "./assets/audio/market_ambience.ogg",
  "./assets/audio/mission_complete.ogg",
  "./assets/audio/park_ambience.ogg",
  "./assets/audio/pickup.ogg",
  "./assets/audio/recycle.ogg",
  "./assets/audio/residential_ambience.ogg",
  "./assets/audio/river_ambience.ogg",
  "./assets/materials/city-atlas-1024.png",
  "./assets/materials/props-atlas-1024.png",
  "./assets/materials/waste-atlas-1024.png"
];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  // Keep HD atlases out of Cache Storage: LOW mode uses 1024; 2048/4096 are fetched only when selected.
  if (/\/assets\/materials\/[^/]+-atlas-(2048|4096)\.png$/.test(url.pathname)) {
    event.respondWith(fetch(event.request));
    return;
  }
  event.respondWith(caches.match(event.request).then(cached => {
    if (cached) return cached;
    return fetch(event.request).then(response => {
      if (response && response.ok) {
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
      }
      return response;
    }).catch(() => caches.match('./index.html'));
  }));
});
