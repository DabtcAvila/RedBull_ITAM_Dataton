// CasaMX Static App - Zero Dependencies JavaScript
class CasaMXApp {
    constructor() {
        this.data = window.CasaMXData;
        this.map = null;
        this.recommendations = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupPriorityRanges();
        this.loadDemoCases();
        console.log('✅ CasaMX App initialized with', this.data.neighborhoods.length, 'neighborhoods');
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Form submission
        document.getElementById('searchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSearch();
        });

        // Priority range updates
        document.querySelectorAll('.priority-range').forEach(range => {
            range.addEventListener('input', (e) => {
                const valueId = e.target.id.replace('Priority', 'Value');
                document.getElementById(valueId).textContent = e.target.value;
            });
        });
    }

    setupPriorityRanges() {
        // Initialize range displays
        document.querySelectorAll('.priority-range').forEach(range => {
            const valueId = range.id.replace('Priority', 'Value');
            document.getElementById(valueId).textContent = range.value;
        });
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');

        // Initialize map if switching to map tab
        if (tabName === 'map' && !this.map) {
            this.initializeMap();
        }
    }

    handleSearch() {
        const formData = new FormData(document.getElementById('searchForm'));
        
        const userPreferences = {
            budget: parseInt(formData.get('budget')),
            familySize: parseInt(formData.get('familySize')),
            hasChildren: formData.get('hasChildren') === 'true',
            country: formData.get('country'),
            priorities: {
                security: parseInt(document.getElementById('securityPriority').value),
                transport: parseInt(document.getElementById('transportPriority').value),
                amenities: parseInt(document.getElementById('amenitiesPriority').value),
                education: parseInt(document.getElementById('educationPriority').value),
                price: parseInt(document.getElementById('pricePriority').value),
                entertainment: parseInt(document.getElementById('entertainmentPriority').value)
            }
        };

        this.showLoading();
        
        // Simulate processing time for better UX
        setTimeout(() => {
            this.recommendations = this.calculateRecommendations(userPreferences);
            this.displayResults();
        }, 1500);
    }

    calculateRecommendations(userPrefs) {
        const recommendations = this.data.neighborhoods.map(neighborhood => {
            const score = this.calculateMatchScore(neighborhood, userPrefs);
            const reasons = this.generateReasons(neighborhood, score, userPrefs);
            
            return {
                neighborhood,
                score: score.total,
                breakdown: score.breakdown,
                reasons
            };
        });

        // Sort by score (highest first)
        recommendations.sort((a, b) => b.score - a.score);

        // Return top 5
        return recommendations.slice(0, 5);
    }

    calculateMatchScore(neighborhood, userPrefs) {
        const scores = {};
        
        // Budget compatibility (25% weight)
        scores.budget = this.calculateBudgetScore(neighborhood, userPrefs);
        
        // Security score (20% weight)
        scores.security = this.calculateSecurityScore(neighborhood, userPrefs);
        
        // Transport accessibility (15% weight)
        scores.transport = this.calculateTransportScore(neighborhood, userPrefs);
        
        // Amenities (15% weight)
        scores.amenities = neighborhood.scores.amenities / 10;
        
        // Education (10% weight, higher if has children)
        scores.education = neighborhood.scores.education / 10;
        const educationWeight = userPrefs.hasChildren ? 0.20 : 0.05;
        
        // Entertainment (10% weight)
        scores.entertainment = neighborhood.scores.entertainment / 10;
        
        // Demographics (5% weight)
        scores.demographics = this.calculateDemographicsScore(neighborhood, userPrefs);

        // Calculate weighted total
        let total = 0;
        total += scores.budget * 0.25;
        total += scores.security * 0.20;
        total += scores.transport * 0.15;
        total += scores.amenities * 0.15;
        total += scores.education * educationWeight;
        total += scores.entertainment * 0.10;
        total += scores.demographics * 0.05;

        // Apply bonuses/penalties
        const adjustments = this.calculateAdjustments(neighborhood, userPrefs);
        total += adjustments;

        // Convert to 0-100 scale
        total = Math.max(0, Math.min(100, total * 100));

        return {
            total: Math.round(total),
            breakdown: scores
        };
    }

    calculateBudgetScore(neighborhood, userPrefs) {
        const budget = userPrefs.budget;
        const { min, max, average } = neighborhood.price_range;

        if (budget >= min && budget <= max) {
            const distanceFromAverage = Math.abs(budget - average) / average;
            return Math.max(0.8, 1.0 - distanceFromAverage);
        }

        if (budget < min) {
            const shortfall = (min - budget) / min;
            return Math.max(0, 1.0 - shortfall * 2);
        }

        if (budget > max) {
            const excess = (budget - max) / max;
            return Math.max(0.3, 1.0 - excess * 0.5);
        }

        return 0.5;
    }

    calculateSecurityScore(neighborhood, userPrefs) {
        const baseScore = neighborhood.scores.security / 10;
        const priority = userPrefs.priorities.security / 10;
        
        // High priority users need high security neighborhoods
        if (priority >= 0.8 && baseScore < 0.7) {
            return baseScore * 0.6;
        }
        
        return baseScore;
    }

    calculateTransportScore(neighborhood, userPrefs) {
        const baseScore = neighborhood.scores.transport / 10;
        const metroBonus = neighborhood.features.metro_stations.length > 0 ? 0.1 : 0;
        return Math.min(1.0, baseScore + metroBonus);
    }

    calculateDemographicsScore(neighborhood, userPrefs) {
        let score = 0;
        let factors = 0;
        
        // Expat friendliness
        if (userPrefs.country !== 'mexico') {
            score += neighborhood.demographics.expat_friendly / 10;
            factors++;
        }
        
        // Family orientation
        if (userPrefs.hasChildren) {
            score += neighborhood.demographics.family_oriented / 10;
            factors++;
        } else if (userPrefs.familySize <= 2) {
            score += neighborhood.demographics.young_professional / 10;
            factors++;
        }
        
        return factors > 0 ? score / factors : 0.7;
    }

    calculateAdjustments(neighborhood, userPrefs) {
        let adjustments = 0;

        // Luxury zone bonus for high budget
        if (userPrefs.budget > 60000 && neighborhood.tags?.includes('luxury')) {
            adjustments += 0.05;
        }

        // Embassy zone bonus for internationals
        if (userPrefs.country !== 'mexico' && neighborhood.tags?.includes('embassy_zone')) {
            adjustments += 0.08;
        }

        // Young professional bonus
        if (userPrefs.familySize <= 2 && !userPrefs.hasChildren) {
            if (neighborhood.tags?.includes('hipster') || neighborhood.tags?.includes('nightlife')) {
                adjustments += 0.07;
            }
        }

        // Safety penalty for security-conscious users
        if (userPrefs.priorities.security >= 8 && neighborhood.scores.security < 7.5) {
            adjustments -= 0.15;
        }

        // Budget-friendly bonus
        if (userPrefs.budget < 20000 && neighborhood.tags?.includes('affordable')) {
            adjustments += 0.04;
        }

        return adjustments;
    }

    generateReasons(neighborhood, score, userPrefs) {
        const reasons = [];

        // Budget reasons
        if (score.breakdown.budget > 0.8) {
            reasons.push(`💰 Perfecto para tu presupuesto de $${userPrefs.budget.toLocaleString()}`);
        }

        // Security reasons
        if (score.breakdown.security > 0.8 && userPrefs.priorities.security >= 8) {
            reasons.push(`🛡️ Zona altamente segura (${neighborhood.safety_index}/100)`);
        }

        // Transport reasons
        if (score.breakdown.transport > 0.8) {
            const metros = neighborhood.features.metro_stations;
            reasons.push(`🚇 Excelente conectividad (${metros.length} estaciones de metro)`);
        }

        // Family reasons
        if (userPrefs.hasChildren && score.breakdown.education > 0.8) {
            reasons.push(`🎓 Excelentes escuelas para tus hijos`);
        }

        // Expat reasons
        if (userPrefs.country !== 'mexico' && neighborhood.demographics.expat_friendly > 8) {
            reasons.push(`🌍 Muy amigable para expatriados`);
        }

        // Lifestyle reasons
        if (!userPrefs.hasChildren && score.breakdown.entertainment > 0.8) {
            reasons.push(`🎭 Vida nocturna y entretenimiento vibrante`);
        }

        return reasons.slice(0, 4);
    }

    showLoading() {
        const resultsDiv = document.getElementById('results');
        resultsDiv.style.display = 'block';
        resultsDiv.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Analizando las mejores opciones para ti...</p>
            </div>
        `;
    }

    displayResults() {
        const resultsDiv = document.getElementById('results');
        const listDiv = document.getElementById('recommendationsList');
        
        listDiv.innerHTML = this.recommendations.map(rec => this.createResultCard(rec)).join('');
        resultsDiv.style.display = 'block';

        // Scroll to results
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
    }

    createResultCard(recommendation) {
        const { neighborhood, score, reasons } = recommendation;
        const priceRange = `$${neighborhood.price_range.min.toLocaleString()} - $${neighborhood.price_range.max.toLocaleString()}`;
        
        return `
            <div class="result-card">
                <div class="result-header">
                    <div class="result-title">${neighborhood.name}</div>
                    <div class="result-score">${score}% Match</div>
                </div>
                
                <div class="result-price">Rango: ${priceRange} MXN/mes</div>
                <div class="result-description">${neighborhood.description}</div>
                
                <div class="result-features">
                    ${neighborhood.tags.map(tag => `<span class="feature-tag">${this.formatTag(tag)}</span>`).join('')}
                </div>
                
                <div class="result-reasons">
                    <h4>¿Por qué es perfecto para ti?</h4>
                    ${reasons.map(reason => `<div class="reason">${reason}</div>`).join('')}
                </div>
                
                <div style="margin-top: 15px;">
                    <strong>📍 Alcaldía:</strong> ${neighborhood.alcaldia} | 
                    <strong>🏥 Hospitales:</strong> ${neighborhood.features.hospitals.length} |
                    <strong>🚇 Metro:</strong> ${neighborhood.features.metro_stations.join(', ')}
                </div>
            </div>
        `;
    }

    formatTag(tag) {
        const tagMap = {
            'luxury': 'Lujo',
            'affordable': 'Accesible',
            'hipster': 'Trendy',
            'cultural': 'Cultural',
            'business_district': 'Distrito Financiero',
            'historic': 'Histórico',
            'family_friendly': 'Familiar',
            'nightlife': 'Vida Nocturna',
            'walkable': 'Caminable',
            'embassy_zone': 'Zona Embajadas'
        };
        return tagMap[tag] || tag;
    }

    loadDemoCases() {
        const demoCasesDiv = document.getElementById('demoCases');
        
        demoCasesDiv.innerHTML = this.data.demo_cases.map(demoCase => `
            <div class="demo-card" onclick="app.runDemoCase('${demoCase.id}')">
                <div class="demo-title">${demoCase.name}</div>
                <div class="demo-profile">${demoCase.profile_description}</div>
                <div class="demo-criteria">
                    <div><strong>Presupuesto:</strong> $${demoCase.criteria.budget.toLocaleString()}/mes</div>
                    <div><strong>Familia:</strong> ${demoCase.criteria.family_size} persona${demoCase.criteria.family_size > 1 ? 's' : ''}</div>
                    <div><strong>Hijos:</strong> ${demoCase.criteria.has_children ? 'Sí' : 'No'}</div>
                    <div style="margin-top: 10px; font-size: 0.9em; color: #667eea;">
                        👆 Haz clic para ver recomendaciones
                    </div>
                </div>
            </div>
        `).join('');
    }

    runDemoCase(caseId) {
        const demoCase = this.data.demo_cases.find(c => c.id === caseId);
        if (!demoCase) return;

        // Convert demo case to user preferences
        const userPrefs = {
            budget: demoCase.criteria.budget,
            familySize: demoCase.criteria.family_size,
            hasChildren: demoCase.criteria.has_children,
            country: demoCase.nationality.toLowerCase().split(' ')[0],
            priorities: demoCase.criteria.priorities
        };

        // Calculate recommendations
        this.recommendations = this.calculateRecommendations(userPrefs);

        // Switch to results and display
        this.switchTab('search');
        setTimeout(() => {
            this.displayResults();
            
            // Add demo case info header
            const resultsDiv = document.getElementById('results');
            const demoHeader = document.createElement('div');
            demoHeader.style.cssText = 'background: #f0f4ff; padding: 20px; border-radius: 12px; margin-bottom: 20px;';
            demoHeader.innerHTML = `
                <h3 style="color: #667eea; margin-bottom: 10px;">📊 Caso Demo: ${demoCase.name}</h3>
                <p style="margin-bottom: 10px;">${demoCase.profile_description}</p>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <span><strong>Presupuesto:</strong> $${demoCase.criteria.budget.toLocaleString()}</span>
                    <span><strong>Familia:</strong> ${demoCase.criteria.family_size} persona${demoCase.criteria.family_size > 1 ? 's' : ''}</span>
                    <span><strong>Nacionalidad:</strong> ${demoCase.nationality}</span>
                </div>
            `;
            resultsDiv.insertBefore(demoHeader, resultsDiv.firstChild.nextSibling);
        }, 100);
    }

    initializeMap() {
        // Initialize Leaflet map
        this.map = L.map('leafletMap').setView([19.4326, -99.1332], 11);
        
        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);

        // Add neighborhood markers
        this.data.neighborhoods.forEach(neighborhood => {
            const marker = L.marker([neighborhood.coordinates.lat, neighborhood.coordinates.lng])
                .addTo(this.map);
            
            const priceRange = `$${neighborhood.price_range.min.toLocaleString()} - $${neighborhood.price_range.max.toLocaleString()}`;
            
            marker.bindPopup(`
                <div style="font-family: 'Inter', sans-serif;">
                    <h3 style="margin: 0 0 10px 0; color: #667eea;">${neighborhood.name}</h3>
                    <p style="margin: 5px 0;"><strong>Precio:</strong> ${priceRange}/mes</p>
                    <p style="margin: 5px 0;"><strong>Seguridad:</strong> ${neighborhood.safety_index}/100</p>
                    <p style="margin: 5px 0;"><strong>Metro:</strong> ${neighborhood.features.metro_stations.join(', ')}</p>
                    <p style="margin: 10px 0 0 0; font-size: 0.9em;">${neighborhood.description}</p>
                </div>
            `);
        });

        console.log('✅ Map initialized with', this.data.neighborhoods.length, 'markers');
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new CasaMXApp();
});