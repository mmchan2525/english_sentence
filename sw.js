const CACHE_NAME = 'yuri-english-v1';
const STATIC_ASSETS = [
  './',
  './index.html',
  './avatar.png',
  './range_timestamps.js',
  './manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  event.respondWith(
    fetch(req)
      .then((networkRes) => {
        // Cache successful responses for offline use
        if (networkRes && networkRes.status === 200) {
          const resClone = networkRes.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(req, resClone);
          });
        }
        return networkRes;
      })
      .catch(() => {
        // Offline fallback
        return caches.match(req).then((cachedRes) => {
          if (cachedRes) return cachedRes;
          // Fallback to index.html for navigation requests
          if (req.mode === 'navigate') {
            return caches.match('./index.html');
          }
        });
      })
  );
});
