// Presentation Control Script for CasaMX Demo
// Handles Reveal.js configuration and interactive elements

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize Reveal.js
    Reveal.initialize({
        hash: true,
        controls: true,
        progress: true,
        center: true,
        touch: true,
        loop: false,
        rtl: false,
        navigationMode: 'default',
        shuffle: false,
        fragments: true,
        fragmentInURL: false,
        embedded: false,
        help: true,
        showNotes: false,
        autoPlayMedia: null,
        preloadIframes: null,
        autoAnimate: true,
        autoAnimateMatcher: null,
        autoAnimateEasing: 'ease',
        autoAnimateDuration: 1.0,
        autoAnimateUnmatched: true,
        autoAnimateStyles: [
            'opacity',
            'color',
            'background-color',
            'padding',
            'font-size',
            'line-height',
            'letter-spacing',
            'border-width',
            'border-color',
            'border-radius',
            'outline',
            'outline-offset'
        ],

        // Transition style
        transition: 'slide',
        transitionSpeed: 'default',
        backgroundTransition: 'fade',

        // Parallax background
        parallaxBackgroundImage: '',
        parallaxBackgroundSize: '',
        parallaxBackgroundHorizontal: null,
        parallaxBackgroundVertical: null,

        // Display controls
        display: 'block',
        hideInactiveCursor: true,
        hideCursorTime: 5000,

        // Keyboard shortcuts
        keyboard: {
            13: 'next', // Enter
            32: 'next', // Space
            37: 'prev', // Left arrow
            39: 'next', // Right arrow
            38: 'prev', // Up arrow
            40: 'next'  // Down arrow
        },

        // Configure plugins
        plugins: [ 
            RevealMarkdown, 
            RevealHighlight, 
            RevealNotes 
        ]
    });

    // Presentation Control Object
    const PresentationController = {
        currentSlide: 0,
        totalSlides: 0,
        demoMode: false,
        autoAdvanceTimers: [],
        
        // Initialize presentation features
        init: function() {
            this.setupSlideCounter();
            this.setupAutoAdvance();
            this.setupDemoInteractivity();
            this.setupKeyboardShortcuts();
            this.setupProgressTracking();
            this.preloadDemoData();
            console.log('CasaMX Presentation Controller initialized');
        },

        // Setup slide counter
        setupSlideCounter: function() {
            const slides = document.querySelectorAll('.slides section');
            this.totalSlides = slides.length;
            
            Reveal.addEventListener('slidechanged', (event) => {
                this.currentSlide = event.indexh;
                this.updateProgressIndicator();
                this.handleSlideSpecificActions(event.currentSlide);
            });
        },

        // Setup auto-advance for demo slides
        setupAutoAdvance: function() {
            const demoSlides = [4, 5, 6]; // Demo slides indices
            
            Reveal.addEventListener('slidechanged', (event) => {
                // Clear existing timers
                this.clearAutoAdvanceTimers();
                
                // Set up auto-advance for demo slides if needed
                if (demoSlides.includes(event.indexh) && this.demoMode) {
                    this.setupDemoAutoAdvance(15000); // 15 seconds per demo slide
                }
            });
        },

        // Setup demo interactivity
        setupDemoInteractivity: function() {
            // Add click handlers for demo elements
            document.addEventListener('click', (event) => {
                if (event.target.matches('.rec-card')) {
                    this.highlightRecommendation(event.target);
                }
                
                if (event.target.matches('.metric-card')) {
                    this.showMetricDetails(event.target);
                }
            });

            // Add demo mode toggle
            this.createDemoModeToggle();
        },

        // Setup additional keyboard shortcuts
        setupKeyboardShortcuts: function() {
            document.addEventListener('keydown', (event) => {
                switch(event.key) {
                    case 'd':
                    case 'D':
                        this.toggleDemoMode();
                        break;
                    case 'r':
                    case 'R':
                        this.resetPresentation();
                        break;
                    case 'f':
                    case 'F':
                        if (!document.fullscreenElement) {
                            document.documentElement.requestFullscreen();
                        } else {
                            document.exitFullscreen();
                        }
                        break;
                    case 'h':
                    case 'H':
                        this.showHelpOverlay();
                        break;
                }
            });
        },

        // Setup progress tracking
        setupProgressTracking: function() {
            this.createProgressIndicator();
            
            // Track time spent on each slide
            this.slideStartTime = Date.now();
            Reveal.addEventListener('slidechanged', () => {
                const timeSpent = Date.now() - this.slideStartTime;
                console.log(`Time on slide: ${timeSpent / 1000}s`);
                this.slideStartTime = Date.now();
            });
        },

        // Preload demo data
        preloadDemoData: function() {
            if (typeof demoCases !== 'undefined') {
                console.log('Demo cases loaded successfully');
                this.demoData = demoCases;
            } else {
                console.warn('Demo cases not available');
            }
        },

        // Handle slide-specific actions
        handleSlideSpecificActions: function(slide) {
            const slideIndex = Reveal.getIndices().h;
            
            switch(slideIndex) {
                case 0: // Title slide
                    this.animateTitleElements();
                    break;
                case 1: // Problem slide
                    this.animateStatistics();
                    break;
                case 4:
                case 5:
                case 6: // Demo slides
                    this.loadDemoCase(slideIndex - 4);
                    break;
                case 7: // Results slide
                    this.animateMetrics();
                    break;
                case 8: // Technology slide
                    this.animateTechStack();
                    break;
            }
        },

        // Animate title elements
        animateTitleElements: function() {
            const elements = ['.main-title', '.subtitle', '.team-info', '.tech-badge'];
            elements.forEach((selector, index) => {
                const element = document.querySelector(selector);
                if (element) {
                    element.style.opacity = '0';
                    element.style.transform = 'translateY(30px)';
                    setTimeout(() => {
                        element.style.transition = 'all 0.6s ease-out';
                        element.style.opacity = '1';
                        element.style.transform = 'translateY(0)';
                    }, index * 200);
                }
            });
        },

        // Animate statistics
        animateStatistics: function() {
            const statNumbers = document.querySelectorAll('.stat-number');
            statNumbers.forEach((element, index) => {
                const finalValue = element.textContent;
                const numericValue = parseFloat(finalValue.replace(/[^0-9.]/g, ''));
                
                setTimeout(() => {
                    this.animateCounter(element, 0, numericValue, 1500, finalValue);
                }, index * 300);
            });
        },

        // Load specific demo case
        loadDemoCase: function(caseIndex) {
            if (!this.demoData) return;
            
            const cases = ['techProfessional', 'familyWithChildren', 'internationalStudent'];
            const caseKey = cases[caseIndex];
            const caseData = this.demoData[caseKey];
            
            if (caseData) {
                this.populateDemoSlide(caseData, caseIndex);
                this.highlightTopRecommendation();
            }
        },

        // Populate demo slide with data
        populateDemoSlide: function(caseData, caseIndex) {
            // This would be implemented to dynamically update the slide content
            // For now, content is static in HTML
            console.log(`Loading demo case ${caseIndex}:`, caseData.profile.name);
        },

        // Animate metrics
        animateMetrics: function() {
            const metricValues = document.querySelectorAll('.metric-value');
            metricValues.forEach((element, index) => {
                const value = element.textContent;
                const numericValue = parseFloat(value.replace(/[^0-9.]/g, ''));
                
                setTimeout(() => {
                    if (!isNaN(numericValue)) {
                        this.animateCounter(element, 0, numericValue, 2000, value);
                    }
                }, index * 200);
            });

            // Animate chart bars
            setTimeout(() => {
                const bars = document.querySelectorAll('.bar');
                bars.forEach((bar, index) => {
                    bar.style.height = '0%';
                    setTimeout(() => {
                        bar.style.transition = 'height 1s ease-out';
                        bar.style.height = bar.getAttribute('style').match(/height:\s*(\d+%)/)[1];
                    }, index * 300);
                });
            }, 1000);
        },

        // Animate tech stack
        animateTechStack: function() {
            const stackLayers = document.querySelectorAll('.stack-layer');
            stackLayers.forEach((layer, index) => {
                layer.style.opacity = '0';
                layer.style.transform = 'translateX(-30px)';
                setTimeout(() => {
                    layer.style.transition = 'all 0.5s ease-out';
                    layer.style.opacity = '1';
                    layer.style.transform = 'translateX(0)';
                }, index * 200);
            });
        },

        // Animate counter
        animateCounter: function(element, start, end, duration, finalText) {
            const startTime = Date.now();
            const isDecimal = finalText.includes('.');
            
            const updateCounter = () => {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const easeProgress = 1 - Math.pow(1 - progress, 3); // Ease out cubic
                
                const currentValue = start + (end - start) * easeProgress;
                
                if (isDecimal) {
                    element.textContent = currentValue.toFixed(1) + finalText.substring(finalText.indexOf('.') + 2);
                } else {
                    element.textContent = Math.floor(currentValue) + finalText.replace(/[0-9]/g, '');
                }
                
                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    element.textContent = finalText;
                }
            };
            
            updateCounter();
        },

        // Demo mode functionality
        toggleDemoMode: function() {
            this.demoMode = !this.demoMode;
            const indicator = document.querySelector('.demo-mode-indicator');
            if (indicator) {
                indicator.textContent = this.demoMode ? 'DEMO MODE: ON' : 'DEMO MODE: OFF';
                indicator.className = `demo-mode-indicator ${this.demoMode ? 'active' : ''}`;
            }
            console.log(`Demo mode: ${this.demoMode ? 'ON' : 'OFF'}`);
        },

        // Create demo mode toggle
        createDemoModeToggle: function() {
            const toggle = document.createElement('div');
            toggle.className = 'demo-mode-indicator';
            toggle.textContent = 'DEMO MODE: OFF';
            toggle.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                background: rgba(0,0,0,0.7);
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
                z-index: 1000;
                cursor: pointer;
                transition: background 0.3s;
            `;
            
            toggle.addEventListener('click', () => this.toggleDemoMode());
            document.body.appendChild(toggle);
        },

        // Create progress indicator
        createProgressIndicator: function() {
            const indicator = document.createElement('div');
            indicator.className = 'slide-progress';
            indicator.style.cssText = `
                position: fixed;
                bottom: 10px;
                left: 10px;
                background: rgba(0,0,0,0.7);
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
                z-index: 1000;
            `;
            
            document.body.appendChild(indicator);
        },

        // Update progress indicator
        updateProgressIndicator: function() {
            const indicator = document.querySelector('.slide-progress');
            if (indicator) {
                indicator.textContent = `${this.currentSlide + 1} / ${this.totalSlides}`;
            }
        },

        // Auto advance for demos
        setupDemoAutoAdvance: function(delay) {
            const timer = setTimeout(() => {
                if (this.demoMode) {
                    Reveal.next();
                }
            }, delay);
            
            this.autoAdvanceTimers.push(timer);
        },

        // Clear auto advance timers
        clearAutoAdvanceTimers: function() {
            this.autoAdvanceTimers.forEach(timer => clearTimeout(timer));
            this.autoAdvanceTimers = [];
        },

        // Highlight recommendation
        highlightRecommendation: function(element) {
            // Remove existing highlights
            document.querySelectorAll('.rec-card').forEach(card => {
                card.classList.remove('highlighted');
            });
            
            // Add highlight to clicked element
            element.classList.add('highlighted');
            
            // Show additional details if available
            this.showRecommendationDetails(element);
        },

        // Show recommendation details
        showRecommendationDetails: function(element) {
            const zone = element.querySelector('h4').textContent;
            console.log(`Selected recommendation: ${zone}`);
            
            // Could show a modal with more details
            // For now, just log to console
        },

        // Show metric details
        showMetricDetails: function(element) {
            const metric = element.querySelector('.metric-label').textContent;
            const value = element.querySelector('.metric-value').textContent;
            console.log(`Metric selected: ${metric} - ${value}`);
            
            // Could show detailed breakdown
            // For now, just add a visual indicator
            element.style.transform = 'scale(1.05)';
            setTimeout(() => {
                element.style.transform = 'scale(1)';
            }, 200);
        },

        // Highlight top recommendation
        highlightTopRecommendation: function() {
            setTimeout(() => {
                const topRec = document.querySelector('.rec-card');
                if (topRec) {
                    topRec.classList.add('pulse');
                    setTimeout(() => {
                        topRec.classList.remove('pulse');
                    }, 2000);
                }
            }, 1000);
        },

        // Reset presentation
        resetPresentation: function() {
            Reveal.slide(0);
            this.currentSlide = 0;
            this.clearAutoAdvanceTimers();
            console.log('Presentation reset to beginning');
        },

        // Show help overlay
        showHelpOverlay: function() {
            const existingOverlay = document.querySelector('.help-overlay');
            if (existingOverlay) {
                existingOverlay.remove();
                return;
            }
            
            const overlay = document.createElement('div');
            overlay.className = 'help-overlay';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                color: white;
                z-index: 2000;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Inter', sans-serif;
            `;
            
            overlay.innerHTML = `
                <div style="text-align: center; max-width: 600px; padding: 2rem;">
                    <h2>Keyboard Shortcuts</h2>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 2rem 0;">
                        <div><strong>Space/Enter/→</strong><br>Next slide</div>
                        <div><strong>←</strong><br>Previous slide</div>
                        <div><strong>D</strong><br>Toggle demo mode</div>
                        <div><strong>R</strong><br>Reset presentation</div>
                        <div><strong>F</strong><br>Toggle fullscreen</div>
                        <div><strong>H</strong><br>Toggle this help</div>
                    </div>
                    <p>Click anywhere to close</p>
                </div>
            `;
            
            overlay.addEventListener('click', () => overlay.remove());
            document.body.appendChild(overlay);
        }
    };

    // Add custom CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        .highlighted {
            box-shadow: 0 0 20px rgba(74, 144, 226, 0.6) !important;
            transform: scale(1.02) !important;
        }
        
        .pulse {
            animation: pulse 2s ease-in-out;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(74, 144, 226, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(74, 144, 226, 0); }
            100% { box-shadow: 0 0 0 0 rgba(74, 144, 226, 0); }
        }
        
        .demo-mode-indicator.active {
            background: rgba(39, 174, 96, 0.8) !important;
        }
        
        .slide-progress {
            font-family: monospace;
        }
    `;
    document.head.appendChild(style);

    // Initialize the presentation controller
    PresentationController.init();

    // Make controller available globally
    window.PresentationController = PresentationController;
    
    console.log('CasaMX Presentation Ready! Press H for keyboard shortcuts.');
});