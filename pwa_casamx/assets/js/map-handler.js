/**
 * CasaMX Interactive Map Handler
 * MapBox GL integration for neighborhood visualization
 * Version: 1.0.0
 */

class CasaMXMapHandler {
  constructor() {
    this.map = null;
    this.mapboxToken = 'pk.eyJ1IjoiY2FzYW14LWRlbW8iLCJhIjoiY2xtZGVtbzEyMDNkMDNrcGc4YjEyMzQ1NiJ9.demo'; // Demo token - replace with real one
    this.neighborhoods = [];
    this.markers = [];
    this.initialized = false;
    this.currentFilter = 'all';
    
    // Map style configuration
    this.mapStyle = {
      container: 'map',
      style: 'mapbox://styles/mapbox/dark-v11',
      center: [-99.1332, 19.4326], // CDMX center
      zoom: 10.5,
      pitch: 45,
      bearing: 0,
      minZoom: 9,
      maxZoom: 16
    };

    // Color scheme for different price ranges
    this.colorScheme = {
      luxury: '#e94560',     // Red for $50k+
      premium: '#0f3460',    // Blue for $30-50k
      standard: '#f39c12',   // Orange for $15-30k
      budget: '#48bb78'      // Green for <$15k
    };
  }

  /**
   * Initialize the interactive map
   */
  async initialize() {
    try {
      // Check if MapBox is available
      if (typeof mapboxgl === 'undefined') {
        console.warn('⚠️ MapBox GL not available, using fallback map');
        this.initializeFallbackMap();
        return false;
      }

      // Set access token (use demo mode if no token)
      mapboxgl.accessToken = this.mapboxToken;

      // Load neighborhood data
      await this.loadNeighborhoods();

      // Initialize map
      this.map = new mapboxgl.Map(this.mapStyle);

      // Add map controls
      this.addMapControls();

      // Set up map event listeners
      this.setupMapEvents();

      this.initialized = true;
      console.log('✅ Interactive map initialized successfully');
      return true;

    } catch (error) {
      console.error('❌ Failed to initialize map:', error);
      this.initializeFallbackMap();
      return false;
    }
  }

  /**
   * Load neighborhoods data
   */
  async loadNeighborhoods() {
    try {
      const response = await fetch('./assets/data/cdmx-neighborhoods.json');
      const data = await response.json();
      this.neighborhoods = data.neighborhoods;
      console.log('📍 Loaded', this.neighborhoods.length, 'neighborhoods for map');
    } catch (error) {
      console.error('❌ Failed to load neighborhoods:', error);
      throw error;
    }
  }

  /**
   * Add map controls (navigation, fullscreen, etc.)
   */
  addMapControls() {
    // Navigation controls
    this.map.addControl(new mapboxgl.NavigationControl({
      showCompass: true,
      showZoom: true,
      visualizePitch: true
    }), 'top-right');

    // Fullscreen control
    this.map.addControl(new mapboxgl.FullscreenControl(), 'top-right');

    // Geolocate control
    this.map.addControl(new mapboxgl.GeolocateControl({
      positionOptions: {
        enableHighAccuracy: true
      },
      trackUserLocation: true,
      showUserHeading: true
    }), 'top-right');

    // Scale control
    this.map.addControl(new mapboxgl.ScaleControl({
      maxWidth: 100,
      unit: 'metric'
    }), 'bottom-left');
  }

  /**
   * Setup map event listeners
   */
  setupMapEvents() {
    // Map loaded event
    this.map.on('load', () => {
      this.addNeighborhoodMarkers();
      this.addNeighborhoodClusters();
      this.addMapLayers();
    });

    // Map style loaded
    this.map.on('style.load', () => {
      console.log('🗺️ Map style loaded');
    });

    // Click events for interactivity
    this.map.on('click', 'neighborhoods-layer', (e) => {
      this.handleNeighborhoodClick(e);
    });

    // Mouse events for hover effects
    this.map.on('mouseenter', 'neighborhoods-layer', () => {
      this.map.getCanvas().style.cursor = 'pointer';
    });

    this.map.on('mouseleave', 'neighborhoods-layer', () => {
      this.map.getCanvas().style.cursor = '';
    });

    // Resize handler
    this.map.on('resize', () => {
      this.map.resize();
    });
  }

  /**
   * Add neighborhood markers to map
   */
  addNeighborhoodMarkers() {
    this.neighborhoods.forEach(neighborhood => {
      const priceCategory = this.getPriceCategory(neighborhood.price_range.average);
      const color = this.colorScheme[priceCategory];

      // Create custom marker element
      const markerElement = this.createMarkerElement(neighborhood, color);

      // Create popup content
      const popup = new mapboxgl.Popup({
        offset: 25,
        closeButton: true,
        closeOnClick: false,
        className: 'neighborhood-popup'
      }).setHTML(this.createPopupContent(neighborhood));

      // Create and add marker
      const marker = new mapboxgl.Marker({
        element: markerElement,
        anchor: 'bottom'
      })
        .setLngLat([neighborhood.coordinates.lng, neighborhood.coordinates.lat])
        .setPopup(popup)
        .addTo(this.map);

      this.markers.push({
        marker,
        neighborhood,
        priceCategory,
        visible: true
      });
    });

    console.log('📍 Added', this.markers.length, 'neighborhood markers');
  }

  /**
   * Create custom marker element
   */
  createMarkerElement(neighborhood, color) {
    const element = document.createElement('div');
    element.className = 'neighborhood-marker';
    element.style.cssText = `
      width: 40px;
      height: 40px;
      background: ${color};
      border: 3px solid white;
      border-radius: 50%;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      cursor: pointer;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      position: relative;
    `;

    // Add price indicator
    element.innerHTML = `
      <div style="color: white; font-weight: bold; font-size: 12px;">
        $${Math.round(neighborhood.price_range.average / 1000)}k
      </div>
    `;

    // Hover effects
    element.addEventListener('mouseenter', () => {
      element.style.transform = 'scale(1.2)';
      element.style.zIndex = '1000';
    });

    element.addEventListener('mouseleave', () => {
      element.style.transform = 'scale(1)';
      element.style.zIndex = '1';
    });

    return element;
  }

  /**
   * Create popup content for neighborhood
   */
  createPopupContent(neighborhood) {
    const priceRange = `$${neighborhood.price_range.min.toLocaleString()} - $${neighborhood.price_range.max.toLocaleString()}`;
    
    return `
      <div class="neighborhood-popup-content">
        <div class="popup-header">
          <h3>${neighborhood.name}</h3>
          <span class="popup-alcaldia">${neighborhood.alcaldia}</span>
        </div>
        
        <div class="popup-price">
          <strong>${priceRange} MXN/mes</strong>
        </div>
        
        <div class="popup-scores">
          <div class="score-item">
            <span class="score-label">🛡️ Seguridad</span>
            <div class="score-bar">
              <div class="score-fill" style="width: ${neighborhood.scores.security * 10}%"></div>
            </div>
            <span class="score-value">${neighborhood.scores.security}/10</span>
          </div>
          
          <div class="score-item">
            <span class="score-label">🚇 Transporte</span>
            <div class="score-bar">
              <div class="score-fill" style="width: ${neighborhood.scores.transport * 10}%"></div>
            </div>
            <span class="score-value">${neighborhood.scores.transport}/10</span>
          </div>
          
          <div class="score-item">
            <span class="score-label">🏪 Amenidades</span>
            <div class="score-bar">
              <div class="score-fill" style="width: ${neighborhood.scores.amenities * 10}%"></div>
            </div>
            <span class="score-value">${neighborhood.scores.amenities}/10</span>
          </div>
        </div>
        
        <div class="popup-features">
          <div class="feature-group">
            <strong>🚇 Metro:</strong>
            <span>${neighborhood.features.metro_stations.slice(0, 2).join(', ')}</span>
          </div>
          
          <div class="feature-group">
            <strong>🏥 Hospitales:</strong>
            <span>${neighborhood.features.hospitals.slice(0, 2).join(', ')}</span>
          </div>
          
          <div class="feature-group">
            <strong>🏫 Escuelas:</strong>
            <span>${neighborhood.features.schools.slice(0, 2).join(', ')}</span>
          </div>
        </div>
        
        <div class="popup-description">
          <p>${neighborhood.description}</p>
        </div>
        
        <div class="popup-tags">
          ${neighborhood.tags?.slice(0, 4).map(tag => 
            `<span class="tag">${tag.replace('_', ' ')}</span>`
          ).join('') || ''}
        </div>
      </div>
    `;
  }

  /**
   * Add neighborhood clustering for better performance
   */
  addNeighborhoodClusters() {
    // GeoJSON data for clustering
    const geojsonData = {
      type: 'FeatureCollection',
      features: this.neighborhoods.map(neighborhood => ({
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [neighborhood.coordinates.lng, neighborhood.coordinates.lat]
        },
        properties: {
          id: neighborhood.id,
          name: neighborhood.name,
          price_avg: neighborhood.price_range.average,
          security: neighborhood.scores.security,
          category: this.getPriceCategory(neighborhood.price_range.average)
        }
      }))
    };

    // Add source for clustering
    this.map.addSource('neighborhoods', {
      type: 'geojson',
      data: geojsonData,
      cluster: true,
      clusterMaxZoom: 14,
      clusterRadius: 50
    });

    // Add cluster circles
    this.map.addLayer({
      id: 'clusters',
      type: 'circle',
      source: 'neighborhoods',
      filter: ['has', 'point_count'],
      paint: {
        'circle-color': [
          'step',
          ['get', 'point_count'],
          this.colorScheme.budget,
          4,
          this.colorScheme.standard,
          8,
          this.colorScheme.premium
        ],
        'circle-radius': [
          'step',
          ['get', 'point_count'],
          20,
          4,
          25,
          8,
          30
        ],
        'circle-opacity': 0.8
      }
    });

    // Add cluster count labels
    this.map.addLayer({
      id: 'cluster-count',
      type: 'symbol',
      source: 'neighborhoods',
      filter: ['has', 'point_count'],
      layout: {
        'text-field': '{point_count_abbreviated}',
        'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
        'text-size': 12
      },
      paint: {
        'text-color': '#ffffff'
      }
    });
  }

  /**
   * Add additional map layers
   */
  addMapLayers() {
    // Add CDMX boundaries (simplified)
    this.map.addSource('cdmx-bounds', {
      type: 'geojson',
      data: {
        type: 'Feature',
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [-99.3654, 19.0489],
            [-98.9407, 19.0489],
            [-98.9407, 19.5925],
            [-99.3654, 19.5925],
            [-99.3654, 19.0489]
          ]]
        }
      }
    });

    this.map.addLayer({
      id: 'cdmx-bounds',
      type: 'line',
      source: 'cdmx-bounds',
      layout: {},
      paint: {
        'line-color': '#0f3460',
        'line-width': 2,
        'line-opacity': 0.6
      }
    });
  }

  /**
   * Handle neighborhood click events
   */
  handleNeighborhoodClick(e) {
    const features = this.map.queryRenderedFeatures(e.point, {
      layers: ['neighborhoods-layer']
    });

    if (features.length) {
      const neighborhoodId = features[0].properties.id;
      const neighborhood = this.neighborhoods.find(n => n.id === neighborhoodId);
      
      if (neighborhood) {
        this.showNeighborhoodDetails(neighborhood);
        this.flyToNeighborhood(neighborhood);
      }
    }
  }

  /**
   * Show detailed neighborhood information
   */
  showNeighborhoodDetails(neighborhood) {
    // Create detailed modal or sidebar
    console.log('🏠 Showing details for:', neighborhood.name);
    
    // You can implement a detailed view here
    // For now, just log the neighborhood data
  }

  /**
   * Fly to specific neighborhood
   */
  flyToNeighborhood(neighborhood) {
    this.map.flyTo({
      center: [neighborhood.coordinates.lng, neighborhood.coordinates.lat],
      zoom: 14,
      pitch: 60,
      bearing: 0,
      speed: 1.2,
      curve: 1.42
    });
  }

  /**
   * Filter neighborhoods on map
   */
  filterNeighborhoods(filterType, filterValue) {
    this.currentFilter = filterType;

    this.markers.forEach(markerData => {
      let shouldShow = true;

      switch (filterType) {
        case 'budget':
          shouldShow = markerData.neighborhood.price_range.average <= filterValue;
          break;
        case 'security':
          shouldShow = markerData.neighborhood.scores.security >= filterValue;
          break;
        case 'transport':
          shouldShow = markerData.neighborhood.scores.transport >= filterValue;
          break;
        case 'category':
          shouldShow = markerData.priceCategory === filterValue;
          break;
        case 'all':
        default:
          shouldShow = true;
          break;
      }

      // Show/hide marker
      if (shouldShow && !markerData.visible) {
        markerData.marker.addTo(this.map);
        markerData.visible = true;
      } else if (!shouldShow && markerData.visible) {
        markerData.marker.remove();
        markerData.visible = false;
      }
    });

    console.log('🔍 Filtered neighborhoods by', filterType, '- showing', 
                this.markers.filter(m => m.visible).length, 'of', this.markers.length);
  }

  /**
   * Highlight specific neighborhoods (e.g., search results)
   */
  highlightNeighborhoods(neighborhoodIds) {
    this.markers.forEach(markerData => {
      const isHighlighted = neighborhoodIds.includes(markerData.neighborhood.id);
      const element = markerData.marker.getElement();
      
      if (isHighlighted) {
        element.style.transform = 'scale(1.3)';
        element.style.boxShadow = '0 0 20px rgba(15, 52, 96, 0.8)';
        element.style.zIndex = '1000';
        element.style.border = '4px solid #f39c12';
      } else {
        element.style.transform = 'scale(1)';
        element.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
        element.style.zIndex = '1';
        element.style.border = '3px solid white';
      }
    });
  }

  /**
   * Clear all highlights
   */
  clearHighlights() {
    this.markers.forEach(markerData => {
      const element = markerData.marker.getElement();
      element.style.transform = 'scale(1)';
      element.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
      element.style.zIndex = '1';
      element.style.border = '3px solid white';
    });
  }

  /**
   * Get price category for color coding
   */
  getPriceCategory(avgPrice) {
    if (avgPrice >= 50000) return 'luxury';
    if (avgPrice >= 30000) return 'premium';
    if (avgPrice >= 15000) return 'standard';
    return 'budget';
  }

  /**
   * Fallback map implementation (for when MapBox is not available)
   */
  initializeFallbackMap() {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) return;

    mapContainer.innerHTML = `
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; background: var(--surface); color: var(--text-secondary); padding: 2rem; text-align: center;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🗺️</div>
        <h3 style="margin-bottom: 1rem; color: var(--text-primary);">Mapa Interactivo No Disponible</h3>
        <p style="margin-bottom: 2rem; max-width: 400px; line-height: 1.6;">
          El mapa interactivo requiere conexión a internet. Puedes usar la búsqueda y casos demo sin conexión.
        </p>
        <div class="neighborhood-list" style="width: 100%; max-width: 600px;">
          ${this.createNeighborhoodList()}
        </div>
      </div>
    `;
  }

  /**
   * Create simple neighborhood list for fallback
   */
  createNeighborhoodList() {
    if (!this.neighborhoods.length) return '';

    return `
      <h4 style="margin-bottom: 1rem; color: var(--text-primary);">Colonias Disponibles:</h4>
      <div style="display: grid; gap: 0.5rem; max-height: 300px; overflow-y: auto;">
        ${this.neighborhoods.map(n => `
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem; background: var(--surface-light); border-radius: 8px; border: 1px solid var(--border);">
            <div>
              <strong style="color: var(--text-primary);">${n.name}</strong>
              <small style="color: var(--text-muted); margin-left: 0.5rem;">${n.alcaldia}</small>
            </div>
            <div style="color: var(--primary-color); font-weight: 600;">
              $${n.price_range.average.toLocaleString()}
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  /**
   * Resize map (useful for responsive design)
   */
  resize() {
    if (this.map && this.initialized) {
      this.map.resize();
    }
  }

  /**
   * Destroy map instance
   */
  destroy() {
    if (this.map) {
      this.map.remove();
      this.map = null;
      this.initialized = false;
    }
  }
}

// Export for use in main app
window.CasaMXMapHandler = CasaMXMapHandler;