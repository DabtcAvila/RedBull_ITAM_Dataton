/**
 * CasaMX PWA - Main Application
 * Enterprise-grade progressive web application for housing recommendations
 * Version: 1.0.0
 * Author: David Fernando Ávila Díaz
 */

class CasaMXApp {
  constructor() {
    this.currentView = 'search';
    this.recommendationEngine = new CasaMXRecommendationEngine();
    this.mapHandler = new CasaMXMapHandler();
    this.installPromptEvent = null;
    this.isOnline = navigator.onLine;
    this.currentSearch = null;
    this.demoCases = [];
    
    // UI Elements
    this.elements = {};
    
    // Initialize app
    this.init();
  }

  /**
   * Initialize the application
   */
  async init() {
    console.log('🚀 Initializing CasaMX PWA v1.0.0');
    
    // Show loading screen
    this.showLoadingScreen();
    
    try {
      // Cache DOM elements
      this.cacheElements();
      
      // Setup event listeners
      this.setupEventListeners();
      
      // Initialize core systems
      await this.initializeSystems();
      
      // Setup PWA functionality
      this.setupPWA();
      
      // Hide loading screen
      this.hideLoadingScreen();
      
      // Show install banner if appropriate
      this.checkInstallPrompt();
      
      console.log('✅ CasaMX PWA initialized successfully');
      
    } catch (error) {
      console.error('❌ Failed to initialize app:', error);
      this.showError('Error al inicializar la aplicación');
      this.hideLoadingScreen();
    }
  }

  /**
   * Cache frequently used DOM elements
   */
  cacheElements() {
    this.elements = {
      // Views
      views: document.querySelectorAll('.view'),
      searchView: document.getElementById('searchView'),
      resultsView: document.getElementById('resultsView'),
      demosView: document.getElementById('demosView'),
      mapView: document.getElementById('mapView'),
      aboutView: document.getElementById('aboutView'),
      
      // Navigation
      navButtons: document.querySelectorAll('.nav-btn'),
      bottomNavButtons: document.querySelectorAll('.bottom-nav-btn'),
      menuToggle: document.getElementById('menuToggle'),
      
      // Forms
      searchForm: document.getElementById('searchForm'),
      budgetInput: document.getElementById('budget'),
      budgetRange: document.getElementById('budgetRange'),
      searchBtn: document.getElementById('searchBtn'),
      backToSearch: document.getElementById('backToSearch'),
      
      // Priority sliders
      priorityInputs: document.querySelectorAll('.priority-range'),
      priorityValues: document.querySelectorAll('.priority-value'),
      
      // Results
      recommendationsList: document.getElementById('recommendationsList'),
      
      // Demo cases
      demoCases: document.getElementById('demoCases'),
      
      // Map
      mapFilter: document.getElementById('mapFilter'),
      
      // PWA
      installBanner: document.getElementById('installBanner'),
      installBtn: document.getElementById('installBtn'),
      dismissInstall: document.getElementById('dismissInstall'),
      
      // Loading
      loadingScreen: document.getElementById('loadingScreen'),
      
      // Offline
      offlineIndicator: document.getElementById('offlineIndicator'),
      
      // Toast
      toastContainer: document.getElementById('toastContainer')
    };
  }

  /**
   * Setup all event listeners
   */
  setupEventListeners() {
    // Navigation events
    this.elements.navButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const view = e.currentTarget.dataset.view;
        this.switchView(view);
      });
    });

    this.elements.bottomNavButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const view = e.currentTarget.dataset.view;
        this.switchView(view);
      });
    });

    // Form events
    this.elements.searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleSearch();
    });

    // Budget synchronization
    this.elements.budgetInput.addEventListener('input', (e) => {
      this.elements.budgetRange.value = e.target.value;
    });

    this.elements.budgetRange.addEventListener('input', (e) => {
      this.elements.budgetInput.value = e.target.value;
    });

    // Priority sliders
    this.elements.priorityInputs.forEach(input => {
      input.addEventListener('input', (e) => {
        const valueId = e.target.id.replace('Priority', 'Value');
        const valueElement = document.getElementById(valueId);
        if (valueElement) {
          valueElement.textContent = e.target.value;
        }
      });
    });

    // Back to search
    if (this.elements.backToSearch) {
      this.elements.backToSearch.addEventListener('click', () => {
        this.switchView('search');
      });
    }

    // Map filter
    if (this.elements.mapFilter) {
      this.elements.mapFilter.addEventListener('change', (e) => {
        this.handleMapFilter(e.target.value);
      });
    }

    // PWA Install
    if (this.elements.installBtn) {
      this.elements.installBtn.addEventListener('click', () => {
        this.installPWA();
      });
    }

    if (this.elements.dismissInstall) {
      this.elements.dismissInstall.addEventListener('click', () => {
        this.dismissInstallBanner();
      });
    }

    // Online/Offline events
    window.addEventListener('online', () => this.handleOnlineStatus(true));
    window.addEventListener('offline', () => this.handleOnlineStatus(false));

    // Window events
    window.addEventListener('resize', () => this.handleResize());
  }

  /**
   * Initialize core systems
   */
  async initializeSystems() {
    const tasks = [
      { name: 'Recommendation Engine', fn: () => this.recommendationEngine.initialize() },
      { name: 'Demo Cases', fn: () => this.loadDemoCases() },
      { name: 'Map Handler', fn: () => this.mapHandler.initialize() }
    ];

    for (const task of tasks) {
      try {
        await task.fn();
        console.log(`✅ ${task.name} initialized`);
      } catch (error) {
        console.warn(`⚠️ ${task.name} failed to initialize:`, error);
      }
    }
  }

  /**
   * Setup PWA functionality
   */
  setupPWA() {
    // PWA install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.installPromptEvent = e;
      this.showInstallBanner();
    });

    // Track installation
    window.addEventListener('appinstalled', () => {
      console.log('✅ PWA installed successfully');
      this.hideInstallBanner();
      this.showToast('¡CasaMX instalado! Ya puedes acceder desde tu pantalla de inicio.', 'success');
      
      // Track installation analytics
      this.trackEvent('pwa_installed');
    });

    // Service Worker updates
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        this.showToast('Nueva versión disponible. Recargando...', 'info');
        setTimeout(() => window.location.reload(), 2000);
      });
    }
  }

  /**
   * Show loading screen with progress
   */
  showLoadingScreen() {
    if (this.elements.loadingScreen) {
      this.elements.loadingScreen.classList.remove('hidden');
      
      // Animate loading progress
      const progress = this.elements.loadingScreen.querySelector('.loading-progress');
      if (progress) {
        progress.style.width = '0%';
        setTimeout(() => {
          progress.style.transition = 'width 2s ease';
          progress.style.width = '100%';
        }, 100);
      }
    }
  }

  /**
   * Hide loading screen
   */
  hideLoadingScreen() {
    setTimeout(() => {
      if (this.elements.loadingScreen) {
        this.elements.loadingScreen.classList.add('hidden');
      }
    }, 1000);
  }

  /**
   * Switch between app views
   */
  switchView(viewName) {
    if (this.currentView === viewName) return;

    console.log(`🔄 Switching to ${viewName} view`);

    // Hide current view
    this.elements.views.forEach(view => {
      view.classList.remove('active');
    });

    // Show new view
    const newView = document.getElementById(viewName + 'View');
    if (newView) {
      newView.classList.add('active');
      this.currentView = viewName;
    }

    // Update navigation
    this.updateNavigation(viewName);

    // Handle view-specific logic
    this.handleViewSwitch(viewName);

    // Track view change
    this.trackEvent('view_change', { view: viewName });
  }

  /**
   * Update navigation state
   */
  updateNavigation(activeView) {
    // Update main navigation
    this.elements.navButtons.forEach(btn => {
      if (btn.dataset.view === activeView) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // Update bottom navigation
    this.elements.bottomNavButtons.forEach(btn => {
      if (btn.dataset.view === activeView) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }

  /**
   * Handle view-specific initialization
   */
  handleViewSwitch(viewName) {
    switch (viewName) {
      case 'map':
        // Initialize map if not already done
        if (this.mapHandler && !this.mapHandler.initialized) {
          this.mapHandler.initialize();
        }
        // Resize map in case of layout changes
        setTimeout(() => {
          if (this.mapHandler.map) {
            this.mapHandler.resize();
          }
        }, 100);
        break;

      case 'demos':
        if (this.demoCases.length === 0) {
          this.loadDemoCases();
        }
        break;
    }
  }

  /**
   * Handle search form submission
   */
  async handleSearch() {
    const formData = this.collectFormData();
    const validation = this.recommendationEngine.validateUserInput(formData);

    if (!validation.isValid) {
      this.showValidationErrors(validation.errors);
      return;
    }

    this.showSearchLoading(true);

    try {
      console.log('🔍 Performing search with criteria:', formData);
      
      const recommendations = await this.recommendationEngine.getRecommendations(formData, 5);
      this.currentSearch = { formData, recommendations };
      
      this.displayRecommendations(recommendations);
      this.switchView('results');
      
      // Track successful search
      this.trackEvent('search_completed', {
        budget: formData.budget,
        family_size: formData.familySize,
        has_children: formData.hasChildren
      });

    } catch (error) {
      console.error('❌ Search failed:', error);
      this.showError('Error al realizar la búsqueda. Por favor intenta de nuevo.');
    } finally {
      this.showSearchLoading(false);
    }
  }

  /**
   * Collect form data
   */
  collectFormData() {
    const formData = new FormData(this.elements.searchForm);
    
    return {
      budget: parseInt(formData.get('budget')) || 25000,
      familySize: parseInt(formData.get('familySize')) || 2,
      hasChildren: formData.get('hasChildren') === 'true',
      country: formData.get('country') || 'mexico',
      priorities: {
        security: parseInt(formData.get('securityPriority')) || 8,
        transport: parseInt(formData.get('transportPriority')) || 7,
        amenities: parseInt(formData.get('amenitiesPriority')) || 6,
        education: parseInt(formData.get('educationPriority')) || 5,
        price: parseInt(formData.get('pricePriority')) || 7,
        entertainment: parseInt(formData.get('entertainmentPriority')) || 6
      }
    };
  }

  /**
   * Display search loading state
   */
  showSearchLoading(loading) {
    if (loading) {
      this.elements.searchBtn.classList.add('loading');
      this.elements.searchBtn.disabled = true;
    } else {
      this.elements.searchBtn.classList.remove('loading');
      this.elements.searchBtn.disabled = false;
    }
  }

  /**
   * Display recommendations
   */
  displayRecommendations(recommendations) {
    if (!recommendations.length) {
      this.elements.recommendationsList.innerHTML = `
        <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
          <div style="font-size: 3rem; margin-bottom: 1rem;">🏠</div>
          <h3>No se encontraron recomendaciones</h3>
          <p>Intenta ajustar tus criterios de búsqueda</p>
        </div>
      `;
      return;
    }

    const html = recommendations.map((rec, index) => {
      const n = rec.neighborhood;
      const matchPercent = Math.round(rec.score);
      const priceRange = `$${n.price_range.min.toLocaleString()} - $${n.price_range.max.toLocaleString()}`;
      
      return `
        <div class="recommendation-card" style="animation-delay: ${index * 0.1}s">
          <div class="recommendation-header">
            <div class="recommendation-info">
              <h3 class="recommendation-title">${n.name}</h3>
              <p class="recommendation-subtitle">${n.alcaldia} • ${priceRange} MXN/mes</p>
            </div>
            <div class="match-score">
              <span class="match-percentage">${matchPercent}%</span>
              <span class="match-label">Match</span>
            </div>
          </div>

          <div class="recommendation-description">
            <p>${n.description}</p>
          </div>

          <div class="recommendation-scores">
            ${this.createScoreBar('Seguridad', n.scores.security, '🛡️')}
            ${this.createScoreBar('Transporte', n.scores.transport, '🚇')}
            ${this.createScoreBar('Amenidades', n.scores.amenities, '🏪')}
            ${this.createScoreBar('Educación', n.scores.education, '🎓')}
          </div>

          <div class="recommendation-features">
            <div class="feature-list">
              <div class="feature-item">
                <strong>🚇 Metro:</strong> ${n.features.metro_stations.slice(0, 2).join(', ')}
              </div>
              <div class="feature-item">
                <strong>🏥 Hospitales:</strong> ${n.features.hospitals.slice(0, 1).join(', ')}
              </div>
              <div class="feature-item">
                <strong>🏫 Escuelas:</strong> ${n.features.schools.slice(0, 1).join(', ')}
              </div>
            </div>
          </div>

          <div class="recommendation-reasons">
            <h4>¿Por qué te recomendamos ${n.name}?</h4>
            <ul>
              ${rec.reasons.slice(0, 3).map(reason => `<li>${reason}</li>`).join('')}
            </ul>
          </div>

          <div class="recommendation-actions">
            <button class="btn btn-primary" onclick="app.viewOnMap('${n.id}')">
              🗺️ Ver en Mapa
            </button>
            <button class="btn btn-ghost" onclick="app.showNeighborhoodDetails('${n.id}')">
              ℹ️ Más Detalles
            </button>
          </div>
        </div>
      `;
    }).join('');

    this.elements.recommendationsList.innerHTML = html;
  }

  /**
   * Create score bar HTML
   */
  createScoreBar(label, score, icon) {
    const percentage = score * 10;
    return `
      <div class="score-row">
        <div class="score-label">
          <span class="score-icon">${icon}</span>
          <span>${label}</span>
        </div>
        <div class="score-bar-container">
          <div class="score-bar">
            <div class="score-fill" style="width: ${percentage}%"></div>
          </div>
          <span class="score-value">${score}/10</span>
        </div>
      </div>
    `;
  }

  /**
   * Load demo cases
   */
  async loadDemoCases() {
    try {
      const response = await fetch('./assets/data/demo-cases.json');
      const data = await response.json();
      this.demoCases = data.demo_cases;
      
      this.displayDemoCases();
      console.log('✅ Demo cases loaded:', this.demoCases.length);
      
    } catch (error) {
      console.error('❌ Failed to load demo cases:', error);
    }
  }

  /**
   * Display demo cases
   */
  displayDemoCases() {
    if (!this.demoCases.length) return;

    const html = this.demoCases.map((demo, index) => `
      <div class="demo-card" style="animation-delay: ${index * 0.2}s" onclick="app.runDemoCase('${demo.id}')">
        <div class="demo-header">
          <div class="demo-avatar">${demo.avatar}</div>
          <div class="demo-info">
            <h3>${demo.name}</h3>
            <p class="demo-country">${demo.country}</p>
          </div>
        </div>
        
        <div class="demo-description">
          <p>${demo.description}</p>
        </div>
        
        <div class="demo-budget">
          Presupuesto: $${demo.criteria.budget.toLocaleString()} MXN
        </div>
        
        <div class="demo-priorities">
          ${Object.entries(demo.criteria.priorities)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 3)
            .map(([key, value]) => `
              <span class="priority-badge">${this.formatPriorityName(key)}: ${value}/10</span>
            `).join('')}
        </div>
        
        <div class="demo-action">
          <button class="btn btn-primary">
            🎯 Ver Recomendaciones
          </button>
        </div>
      </div>
    `).join('');

    this.elements.demoCases.innerHTML = html;
  }

  /**
   * Run demo case
   */
  async runDemoCase(caseId) {
    try {
      console.log(`🎯 Running demo case: ${caseId}`);
      
      this.showToast('Calculando recomendaciones para el caso demo...', 'info');
      
      const result = await this.recommendationEngine.getDemoRecommendations(caseId);
      
      if (result) {
        this.currentSearch = {
          formData: result.case.criteria,
          recommendations: result.recommendations,
          isDemo: true,
          demoCase: result.case
        };
        
        this.displayRecommendations(result.recommendations);
        this.switchView('results');
        
        // Track demo case usage
        this.trackEvent('demo_case_run', { case_id: caseId });
      }
      
    } catch (error) {
      console.error('❌ Failed to run demo case:', error);
      this.showError('Error al ejecutar el caso demo');
    }
  }

  /**
   * View neighborhood on map
   */
  viewOnMap(neighborhoodId) {
    const neighborhood = this.recommendationEngine.getNeighborhoodById(neighborhoodId);
    if (neighborhood && this.mapHandler.initialized) {
      this.switchView('map');
      setTimeout(() => {
        this.mapHandler.flyToNeighborhood(neighborhood);
        this.mapHandler.highlightNeighborhoods([neighborhoodId]);
      }, 300);
    } else {
      this.showToast('Mapa no disponible en modo offline', 'warning');
    }
  }

  /**
   * Show neighborhood details
   */
  showNeighborhoodDetails(neighborhoodId) {
    const neighborhood = this.recommendationEngine.getNeighborhoodById(neighborhoodId);
    if (neighborhood) {
      // Create detailed modal/popup
      console.log('🏠 Showing details for:', neighborhood.name);
      // You could implement a modal here
    }
  }

  /**
   * Handle map filtering
   */
  handleMapFilter(filterValue) {
    if (!this.mapHandler.initialized) return;

    switch (filterValue) {
      case 'budget':
        this.mapHandler.filterNeighborhoods('budget', 30000);
        break;
      case 'security':
        this.mapHandler.filterNeighborhoods('security', 7.5);
        break;
      case 'transport':
        this.mapHandler.filterNeighborhoods('transport', 8.0);
        break;
      default:
        this.mapHandler.filterNeighborhoods('all');
        break;
    }
  }

  /**
   * Handle online/offline status
   */
  handleOnlineStatus(isOnline) {
    this.isOnline = isOnline;
    
    if (isOnline) {
      this.elements.offlineIndicator.classList.add('hidden');
      this.showToast('Conexión restaurada', 'success');
    } else {
      this.elements.offlineIndicator.classList.remove('hidden');
      this.showToast('Modo offline activado', 'warning');
    }
    
    console.log(`📡 Network status: ${isOnline ? 'online' : 'offline'}`);
  }

  /**
   * Handle window resize
   */
  handleResize() {
    if (this.mapHandler && this.mapHandler.initialized) {
      this.mapHandler.resize();
    }
  }

  /**
   * PWA Installation
   */
  async installPWA() {
    if (!this.installPromptEvent) {
      this.showToast('La instalación no está disponible', 'warning');
      return;
    }

    try {
      const result = await this.installPromptEvent.prompt();
      console.log('PWA install prompt result:', result);
      
      if (result.outcome === 'accepted') {
        this.showToast('Instalando CasaMX...', 'info');
      }
      
      this.installPromptEvent = null;
      this.hideInstallBanner();
      
    } catch (error) {
      console.error('❌ PWA installation failed:', error);
      this.showToast('Error al instalar la aplicación', 'error');
    }
  }

  /**
   * Show install banner
   */
  showInstallBanner() {
    if (this.elements.installBanner) {
      this.elements.installBanner.classList.remove('hidden');
    }
  }

  /**
   * Hide install banner
   */
  hideInstallBanner() {
    if (this.elements.installBanner) {
      this.elements.installBanner.classList.add('hidden');
    }
  }

  /**
   * Dismiss install banner
   */
  dismissInstallBanner() {
    this.hideInstallBanner();
    localStorage.setItem('installBannerDismissed', 'true');
  }

  /**
   * Check if install prompt should be shown
   */
  checkInstallPrompt() {
    const dismissed = localStorage.getItem('installBannerDismissed');
    if (!dismissed && this.installPromptEvent) {
      this.showInstallBanner();
    }
  }

  /**
   * Show toast notification
   */
  showToast(message, type = 'info', duration = 4000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      <div style="display: flex; align-items: center; gap: 0.5rem;">
        <span>${this.getToastIcon(type)}</span>
        <span>${message}</span>
      </div>
    `;

    this.elements.toastContainer.appendChild(toast);

    // Auto remove
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, duration);
  }

  /**
   * Get toast icon by type
   */
  getToastIcon(type) {
    const icons = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️'
    };
    return icons[type] || icons.info;
  }

  /**
   * Show validation errors
   */
  showValidationErrors(errors) {
    errors.forEach(error => {
      this.showToast(error, 'error', 6000);
    });
  }

  /**
   * Show error message
   */
  showError(message) {
    this.showToast(message, 'error');
  }

  /**
   * Format priority name for display
   */
  formatPriorityName(key) {
    const names = {
      security: 'Seguridad',
      transport: 'Transporte',
      amenities: 'Amenidades',
      education: 'Educación',
      price: 'Precio',
      entertainment: 'Entretenimiento'
    };
    return names[key] || key;
  }

  /**
   * Track analytics events
   */
  trackEvent(eventName, properties = {}) {
    console.log('📊 Event tracked:', eventName, properties);
    
    // In a real app, you'd send this to your analytics service
    // Example: gtag('event', eventName, properties);
  }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.app = new CasaMXApp();
});

// Make app globally available
window.CasaMXApp = CasaMXApp;