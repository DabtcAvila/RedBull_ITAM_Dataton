// CasaMX PWA Service Worker
// Enterprise-grade offline functionality
// Version: 1.0.0

const CACHE_NAME = 'casamx-v1.0.0';
const STATIC_CACHE = 'casamx-static-v1.0.0';
const DYNAMIC_CACHE = 'casamx-dynamic-v1.0.0';

// Core files that MUST be cached for offline functionality
const CORE_CACHE_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  '/assets/css/styles.css',
  '/assets/js/app.js',
  '/assets/js/recommendation-engine.js',
  '/assets/js/map-handler.js',
  '/assets/data/cdmx-neighborhoods.json',
  '/assets/data/demo-cases.json',
  '/assets/images/logo.svg',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// MapBox and external resources
const EXTERNAL_RESOURCES = [
  'https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js',
  'https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
];

// Install event - cache core files
self.addEventListener('install', (event) => {
  console.log('[SW] Installing CasaMX Service Worker v1.0.0');
  
  event.waitUntil(
    Promise.all([
      // Cache core files
      caches.open(STATIC_CACHE).then((cache) => {
        console.log('[SW] Caching core files');
        return cache.addAll(CORE_CACHE_FILES);
      }),
      // Cache external resources
      caches.open(DYNAMIC_CACHE).then((cache) => {
        console.log('[SW] Caching external resources');
        return cache.addAll(EXTERNAL_RESOURCES.map(url => new Request(url, {mode: 'cors'})));
      })
    ])
  );
  
  // Force activation
  self.skipWaiting();
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating CasaMX Service Worker v1.0.0');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  
  // Take control immediately
  self.clients.claim();
});

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Handle different types of requests
  if (request.method === 'GET') {
    if (url.origin === location.origin) {
      // Same origin - cache first strategy
      event.respondWith(cacheFirstStrategy(request));
    } else if (url.host.includes('mapbox.com')) {
      // MapBox API - network first with cache fallback
      event.respondWith(networkFirstStrategy(request));
    } else if (url.host.includes('googleapis.com')) {
      // Google Fonts - cache first
      event.respondWith(cacheFirstStrategy(request));
    } else {
      // Other external resources - network first
      event.respondWith(networkFirstStrategy(request));
    }
  }
});

// Cache-first strategy for static assets
async function cacheFirstStrategy(request) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Cache-first failed:', error);
    return new Response('Offline - Recurso no disponible', { 
      status: 503,
      headers: { 'Content-Type': 'text/plain' }
    });
  }
}

// Network-first strategy for API calls
async function networkFirstStrategy(request) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed, trying cache:', error);
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline page for navigation requests
    if (request.destination === 'document') {
      return caches.match('/');
    }
    
    return new Response('Offline', { status: 503 });
  }
}

// Background sync for form submissions
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'search-request') {
    event.waitUntil(processOfflineSearches());
  }
});

// Process searches that were made offline
async function processOfflineSearches() {
  try {
    // Get pending searches from IndexedDB
    const pendingSearches = await getPendingSearches();
    
    for (const search of pendingSearches) {
      try {
        // Process search when back online
        const result = await processSearch(search);
        await removePendingSearch(search.id);
        
        // Notify app about completed search
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
          client.postMessage({
            type: 'SEARCH_COMPLETED',
            searchId: search.id,
            result: result
          });
        });
      } catch (error) {
        console.log('[SW] Failed to process offline search:', error);
      }
    }
  } catch (error) {
    console.log('[SW] Background sync failed:', error);
  }
}

// Push notification handler (for future features)
self.addEventListener('push', (event) => {
  console.log('[SW] Push received');
  
  const options = {
    body: event.data ? event.data.text() : 'Nueva recomendación disponible',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      url: '/'
    },
    actions: [
      {
        action: 'view',
        title: 'Ver Recomendación',
        icon: '/icons/icon-72x72.png'
      },
      {
        action: 'close',
        title: 'Cerrar'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('CasaMX', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'view' || !event.action) {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Helper functions for IndexedDB operations (placeholder for offline storage)
async function getPendingSearches() {
  // Implementation would use IndexedDB
  return [];
}

async function removePendingSearch(searchId) {
  // Implementation would use IndexedDB
  return true;
}

async function processSearch(searchData) {
  // Implementation would process the search locally or sync with server
  return {};
}

// Performance monitoring
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: '1.0.0' });
  }
});

console.log('[SW] CasaMX Service Worker v1.0.0 loaded successfully');