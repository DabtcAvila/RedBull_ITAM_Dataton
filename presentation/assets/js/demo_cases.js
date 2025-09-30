// Demo Cases for CasaMX Presentation
// These are pre-calculated results for the live demo

const demoCases = {
    // Case 1: Tech Professional
    techProfessional: {
        profile: {
            name: "María",
            age: 28,
            occupation: "Desarrolladora de Software",
            nationality: "Española",
            budget: {
                min: 20000,
                max: 30000,
                currency: "MXN"
            },
            priorities: [
                { name: "Seguridad", weight: 0.35, importance: "Alta" },
                { name: "Transporte", weight: 0.25, importance: "Alta" },
                { name: "Vida nocturna", weight: 0.20, importance: "Media" },
                { name: "Conectividad", weight: 0.15, importance: "Media" },
                { name: "Costo", weight: 0.05, importance: "Baja" }
            ],
            lifestyle: "Urbano moderno, trabajo remoto, socialización activa",
            requirements: [
                "Internet de alta velocidad",
                "Cerca del metro",
                "Ambiente internacional",
                "Restaurantes y cafés"
            ]
        },
        results: [
            {
                rank: 1,
                zone: "Roma Norte",
                colonia: "Roma Norte",
                delegacion: "Cuauhtémoc",
                score: 9.2,
                coordinates: { lat: 19.4196, lng: -99.1655 },
                metrics: {
                    security: { value: 8.9, description: "Índice de seguridad superior al promedio" },
                    transport: { value: 9.5, description: "4 líneas de metro, múltiples opciones" },
                    nightlife: { value: 9.2, description: "Gran variedad de bares y restaurantes" },
                    connectivity: { value: 9.0, description: "Fibra óptica disponible" },
                    cost: { value: 7.8, description: "Dentro del rango de presupuesto" }
                },
                highlights: ["Alta seguridad", "Transporte excelente", "Vida cultural"],
                averageRent: 25000,
                description: "Zona bohemia con alta concentración de extranjeros y profesionales tech",
                amenities: {
                    restaurants: 156,
                    cafes: 89,
                    coworking: 12,
                    gyms: 23,
                    supermarkets: 18
                }
            },
            {
                rank: 2,
                zone: "Polanco",
                colonia: "Polanco V Sección",
                delegacion: "Miguel Hidalgo",
                score: 8.9,
                coordinates: { lat: 19.4326, lng: -99.1909 },
                metrics: {
                    security: { value: 9.5, description: "Una de las zonas más seguras de la ciudad" },
                    transport: { value: 8.7, description: "Metro Polanco, múltiples rutas de autobús" },
                    nightlife: { value: 8.8, description: "Restaurantes de alta gama y vida nocturna sofisticada" },
                    connectivity: { value: 9.2, description: "Infraestructura tecnológica premium" },
                    cost: { value: 6.5, description: "En el límite superior del presupuesto" }
                },
                highlights: ["Zona empresarial", "Seguridad premium", "Restaurantes"],
                averageRent: 30000,
                description: "Distrito financiero con ambiente internacional y servicios premium",
                amenities: {
                    restaurants: 201,
                    cafes: 67,
                    coworking: 8,
                    gyms: 31,
                    supermarkets: 25
                }
            },
            {
                rank: 3,
                zone: "Santa Fe",
                colonia: "Santa Fe",
                delegacion: "Cuajimalpa",
                score: 8.5,
                coordinates: { lat: 19.3618, lng: -99.2598 },
                metrics: {
                    security: { value: 9.0, description: "Zona corporativa con alta seguridad" },
                    transport: { value: 7.8, description: "Metro Bus y múltiples rutas" },
                    nightlife: { value: 7.5, description: "Centros comerciales y algunos restaurantes" },
                    connectivity: { value: 9.3, description: "Hub tecnológico con excelente conectividad" },
                    cost: { value: 8.2, description: "Buen valor por el dinero" }
                },
                highlights: ["Hub tecnológico", "Centros comerciales", "Infraestructura moderna"],
                averageRent: 22000,
                description: "Distrito corporativo moderno, ideal para profesionales tech",
                amenities: {
                    restaurants: 134,
                    cafes: 45,
                    coworking: 15,
                    gyms: 28,
                    supermarkets: 22
                }
            }
        ],
        reasoning: {
            algorithm: "Weighted scoring based on user priorities",
            factors: [
                "Security index weighted at 35% due to high priority",
                "Transport accessibility weighted at 25%",
                "Nightlife and cultural options weighted at 20%",
                "Internet connectivity weighted at 15%",
                "Cost efficiency weighted at 5% due to flexible budget"
            ],
            dataPoints: 247,
            lastUpdated: "2025-01-15"
        }
    },

    // Case 2: Family with Children
    familyWithChildren: {
        profile: {
            name: "Familia Johnson",
            composition: "Padres + 2 niños (8 y 12 años)",
            nationality: "Estadounidense",
            budget: {
                min: 15000,
                max: 25000,
                currency: "MXN"
            },
            priorities: [
                { name: "Escuelas", weight: 0.30, importance: "Crítica" },
                { name: "Seguridad familiar", weight: 0.28, importance: "Crítica" },
                { name: "Parques y espacios", weight: 0.20, importance: "Alta" },
                { name: "Servicios médicos", weight: 0.15, importance: "Alta" },
                { name: "Costo", weight: 0.07, importance: "Media" }
            ],
            lifestyle: "Familiar tranquilo, orientado a los niños",
            requirements: [
                "Escuelas bilingües de calidad",
                "Parques y áreas de juego",
                "Servicios pediátricos cercanos",
                "Ambiente seguro y familiar",
                "Transporte escolar disponible"
            ]
        },
        results: [
            {
                rank: 1,
                zone: "Coyoacán",
                colonia: "Del Carmen",
                delegacion: "Coyoacán",
                score: 9.1,
                coordinates: { lat: 19.3467, lng: -99.1618 },
                metrics: {
                    schools: { value: 9.2, description: "Excelentes opciones educativas bilingües" },
                    safety: { value: 8.9, description: "Ambiente familiar muy seguro" },
                    parks: { value: 9.5, description: "Múltiples parques y espacios culturales" },
                    healthcare: { value: 8.7, description: "Hospitales y clínicas pediátricas" },
                    cost: { value: 8.8, description: "Excelente relación calidad-precio" }
                },
                highlights: ["Escuelas de calidad", "Parques y cultura", "Ambiente familiar"],
                averageRent: 18000,
                description: "Zona histórica con fuerte tradición familiar y educativa",
                amenities: {
                    schools: 47,
                    parks: 23,
                    hospitals: 12,
                    libraries: 8,
                    museums: 15
                }
            },
            {
                rank: 2,
                zone: "San Ángel",
                colonia: "San Ángel",
                delegacion: "Álvaro Obregón",
                score: 8.8,
                coordinates: { lat: 19.3463, lng: -99.1871 },
                metrics: {
                    schools: { value: 9.0, description: "Colegios privados de prestigio" },
                    safety: { value: 9.1, description: "Una de las zonas más seguras para familias" },
                    parks: { value: 8.5, description: "Espacios verdes y áreas residenciales" },
                    healthcare: { value: 8.9, description: "Hospitales privados de calidad" },
                    cost: { value: 7.5, description: "Algo elevado pero dentro del rango" }
                },
                highlights: ["Zona residencial", "Espacios verdes", "Colegios privados"],
                averageRent: 24000,
                description: "Área residencial exclusiva con excelentes servicios familiares",
                amenities: {
                    schools: 32,
                    parks: 18,
                    hospitals: 8,
                    libraries: 5,
                    museums: 9
                }
            },
            {
                rank: 3,
                zone: "Del Valle",
                colonia: "Del Valle Centro",
                delegacion: "Benito Juárez",
                score: 8.4,
                coordinates: { lat: 19.3906, lng: -99.1656 },
                metrics: {
                    schools: { value: 8.7, description: "Buenas opciones educativas públicas y privadas" },
                    safety: { value: 8.3, description: "Zona segura con vigilancia regular" },
                    parks: { value: 8.0, description: "Parques locales y áreas deportivas" },
                    healthcare: { value: 8.8, description: "Centro médico y especialistas" },
                    cost: { value: 9.0, description: "Muy buena relación calidad-precio" }
                },
                highlights: ["Centros educativos", "Servicios médicos", "Transporte accesible"],
                averageRent: 16500,
                description: "Zona familiar consolidada con servicios completos",
                amenities: {
                    schools: 41,
                    parks: 16,
                    hospitals: 10,
                    libraries: 6,
                    museums: 4
                }
            }
        ],
        reasoning: {
            algorithm: "Family-focused scoring with emphasis on educational and safety metrics",
            factors: [
                "School quality and availability weighted at 30%",
                "Family safety index weighted at 28%",
                "Parks and recreational spaces weighted at 20%",
                "Healthcare accessibility weighted at 15%",
                "Cost considerations weighted at 7%"
            ],
            dataPoints: 312,
            lastUpdated: "2025-01-15"
        }
    },

    // Case 3: International Student
    internationalStudent: {
        profile: {
            name: "Carlos",
            age: 22,
            occupation: "Estudiante de Posgrado",
            nationality: "Brasileño",
            budget: {
                min: 8000,
                max: 15000,
                currency: "MXN"
            },
            priorities: [
                { name: "Transporte a universidades", weight: 0.35, importance: "Crítica" },
                { name: "Costo", weight: 0.25, importance: "Crítica" },
                { name: "Ambiente estudiantil", weight: 0.20, importance: "Alta" },
                { name: "Vida nocturna", weight: 0.15, importance: "Media" },
                { name: "Servicios básicos", weight: 0.05, importance: "Media" }
            ],
            lifestyle: "Estudiante internacional, presupuesto ajustado, vida social activa",
            requirements: [
                "Cerca de universidades principales",
                "Transporte público accesible",
                "Ambiente internacional",
                "Opciones económicas de comida",
                "Internet confiable para estudios"
            ]
        },
        results: [
            {
                rank: 1,
                zone: "Ciudad Universitaria",
                colonia: "Copilco Universidad",
                delegacion: "Coyoacán",
                score: 9.0,
                coordinates: { lat: 19.3318, lng: -99.1840 },
                metrics: {
                    transport: { value: 9.5, description: "Acceso directo a CU y otras universidades" },
                    cost: { value: 9.2, description: "Precios muy accesibles para estudiantes" },
                    student_life: { value: 9.3, description: "Alta concentración de estudiantes" },
                    nightlife: { value: 8.5, description: "Bares y lugares estudiantiles" },
                    services: { value: 8.0, description: "Servicios básicos disponibles" }
                },
                highlights: ["Cerca de universidades", "Transporte directo", "Ambiente juvenil"],
                averageRent: 9500,
                description: "Zona estudiantil por excelencia, cerca de la UNAM",
                amenities: {
                    universities: 8,
                    libraries: 12,
                    cheap_food: 89,
                    student_bars: 34,
                    internet_cafes: 15
                }
            },
            {
                rank: 2,
                zone: "Doctores",
                colonia: "Doctores",
                delegacion: "Cuauhtémoc",
                score: 8.6,
                coordinates: { lat: 19.4118, lng: -99.1438 },
                metrics: {
                    transport: { value: 8.8, description: "Múltiples líneas de metro" },
                    cost: { value: 9.0, description: "Una de las zonas más económicas" },
                    student_life: { value: 8.2, description: "Comunidad estudiantil creciente" },
                    nightlife: { value: 8.7, description: "Vida nocturna económica y variada" },
                    services: { value: 7.5, description: "Servicios básicos en desarrollo" }
                },
                highlights: ["Económico", "Bien conectado", "Vida nocturna"],
                averageRent: 8200,
                description: "Zona en crecimiento con precios muy accesibles",
                amenities: {
                    universities: 3,
                    libraries: 5,
                    cheap_food: 156,
                    student_bars: 45,
                    internet_cafes: 23
                }
            },
            {
                rank: 3,
                zone: "Narvarte",
                colonia: "Narvarte Poniente",
                delegacion: "Benito Juárez",
                score: 8.3,
                coordinates: { lat: 19.3967, lng: -99.1559 },
                metrics: {
                    transport: { value: 8.5, description: "Metro cercano y buena conectividad" },
                    cost: { value: 8.7, description: "Precios accesibles" },
                    student_life: { value: 7.8, description: "Ambiente estudiantil moderado" },
                    nightlife: { value: 8.2, description: "Buenas opciones de entretenimiento" },
                    services: { value: 8.5, description: "Servicios completos" }
                },
                highlights: ["Precios accesibles", "Metro cercano", "Restaurantes variados"],
                averageRent: 12000,
                description: "Zona intermedia con buen balance de servicios y precio",
                amenities: {
                    universities: 5,
                    libraries: 8,
                    cheap_food: 123,
                    student_bars: 28,
                    internet_cafes: 18
                }
            }
        ],
        reasoning: {
            algorithm: "Student-optimized scoring prioritizing affordability and university access",
            factors: [
                "University proximity and transport weighted at 35%",
                "Affordability and cost-effectiveness weighted at 25%",
                "Student community presence weighted at 20%",
                "Social and nightlife options weighted at 15%",
                "Basic services availability weighted at 5%"
            ],
            dataPoints: 189,
            lastUpdated: "2025-01-15"
        }
    }
};

// Additional demo data and utilities
const demoUtilities = {
    // Method to get a specific case
    getCase: function(caseType) {
        return demoCases[caseType] || null;
    },

    // Method to simulate real-time data fetching
    simulateAPICall: function(caseType, callback, delay = 2000) {
        setTimeout(() => {
            const result = this.getCase(caseType);
            if (callback && typeof callback === 'function') {
                callback(result);
            }
        }, delay);
    },

    // Method to format currency
    formatCurrency: function(amount, currency = 'MXN') {
        return new Intl.NumberFormat('es-MX', {
            style: 'currency',
            currency: currency,
            minimumFractionDigits: 0
        }).format(amount);
    },

    // Method to calculate score color based on value
    getScoreColor: function(score) {
        if (score >= 9.0) return '#27ae60'; // Green
        if (score >= 8.0) return '#f39c12'; // Orange  
        if (score >= 7.0) return '#e74c3c'; // Red
        return '#95a5a6'; // Gray
    },

    // Method to generate map markers data
    getMapMarkers: function(results) {
        return results.map(result => ({
            lat: result.coordinates.lat,
            lng: result.coordinates.lng,
            title: result.zone,
            score: result.score,
            rent: result.averageRent,
            rank: result.rank
        }));
    },

    // Performance metrics for the presentation
    performanceMetrics: {
        totalUsers: 12547,
        averageSessionTime: 8.5, // minutes
        conversionRate: 0.73, // users who found housing
        averageTimeToDecision: 7.2, // days
        userSatisfactionRating: 4.8,
        totalRecommendations: 89234,
        accuracyRate: 0.92,
        dataPointsAnalyzed: 1200000,
        zonesAnalyzed: 342
    },

    // Technology metrics
    techMetrics: {
        apiResponseTime: 245, // ms
        dataFreshness: 24, // hours
        uptime: 99.7, // percent
        scalability: "10K+ concurrent users",
        dataProcessingRate: "50MB/minute",
        cacheHitRate: 0.87
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { demoCases, demoUtilities };
}

// Make available globally for browser use
window.demoCases = demoCases;
window.demoUtilities = demoUtilities;