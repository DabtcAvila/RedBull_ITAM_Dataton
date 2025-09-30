#!/usr/bin/env python3
"""
ESTRATEGIA MVP 36 HORAS - DATATÓN ITAM 2025
CasaMX: Recomendador Inteligente de Zonas CDMX

David Fernando Ávila Díaz - ITAM
Plan de desarrollo optimizado para timeline crítico
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class MVP36HStrategy:
    """Estrategia completa para desarrollar MVP ganador en 36 horas"""
    
    # Timeline crítico
    total_hours: int = 36
    buffer_hours: int = 6  # Para imprevistos
    dev_hours: int = 30
    
    # Recursos disponibles
    has_developer_account: bool = True
    budget_domain: bool = True
    claude_code_access: bool = True
    
    # Prioridades (orden de desarrollo)
    development_phases: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        self.development_phases = [
            {
                "phase": "1. Datos Core (6h)",
                "hours": 6,
                "priority": "CRÍTICA",
                "deliverables": [
                    "Extracción datos INEGI (colonias, socioeconómicos)",
                    "Datos CDMX (seguridad, transporte básico)",
                    "Web scraping inmobiliario (precios promedio)",
                    "Dataset consolidado y limpio"
                ],
                "tools": ["pandas", "requests", "beautifulsoup4", "geopandas"],
                "risks": ["APIs con rate limits", "Web scraping bloqueado"],
                "mitigation": ["Usar datos pre-descargados", "Proxies rotativos"]
            },
            {
                "phase": "2. Algoritmo Recomendador (8h)",
                "hours": 8,
                "priority": "CRÍTICA",
                "deliverables": [
                    "Modelo de scoring multivariable",
                    "Sistema de pesos personalizables", 
                    "Algoritmo de ranking y filtrado",
                    "Validación con casos de prueba"
                ],
                "tools": ["scikit-learn", "numpy", "scipy"],
                "risks": ["Algoritmo poco explicable", "Performance lenta"],
                "mitigation": ["Modelo simple pero robusto", "Caching agresivo"]
            },
            {
                "phase": "3. Interfaz Web MVP (10h)",
                "hours": 10,
                "priority": "CRÍTICA",
                "deliverables": [
                    "App Streamlit con forms de entrada",
                    "Mapa interactivo con Folium",
                    "Dashboard de resultados", 
                    "Diseño responsive básico"
                ],
                "tools": ["streamlit", "folium", "plotly", "custom CSS"],
                "risks": ["Streamlit limitaciones", "Mapas lentos"],
                "mitigation": ["Streamlit Cloud deployment", "Mapas pre-renderizados"]
            },
            {
                "phase": "4. Deploy y Optimización (4h)",
                "hours": 4,
                "priority": "ALTA",
                "deliverables": [
                    "Deploy en Streamlit Cloud",
                    "Dominio personalizado",
                    "Testing con datos reales",
                    "Optimización performance"
                ],
                "tools": ["streamlit cloud", "custom domain", "monitoring"],
                "risks": ["Deploy fallando", "Performance issues"],
                "mitigation": ["Deploy local backup", "Caching estratégico"]
            },
            {
                "phase": "5. Presentación (2h)",
                "hours": 2,
                "priority": "MEDIA",
                "deliverables": [
                    "Slides de presentación",
                    "Demo cases preparados",
                    "Backup plans"
                ],
                "tools": ["reveal.js", "demo scenarios"],
                "risks": ["Poco tiempo para pulir"],
                "mitigation": ["Templates pre-hechos", "Demo automatizado"]
            }
        ]

class DatatonMVPManager:
    """Gestor del desarrollo MVP para el Datatón"""
    
    def __init__(self):
        self.strategy = MVP36HStrategy()
        self.current_phase = 0
        self.completed_deliverables = []
        
        # Stack tecnológico MVP
        self.tech_stack = self.define_mvp_tech_stack()
        
        # Datos críticos mínimos
        self.critical_data_sources = self.define_critical_data()
        
        # Features core vs nice-to-have
        self.feature_prioritization = self.define_feature_priority()
    
    def define_mvp_tech_stack(self) -> Dict[str, str]:
        """Stack tecnológico optimizado para velocidad"""
        return {
            # Backend & Data
            "data_processing": "pandas + numpy",
            "geospatial": "geopandas + shapely",
            "apis": "requests + aiohttp",
            "scraping": "beautifulsoup4 + selenium (solo si necesario)",
            "storage": "sqlite + parquet files",
            
            # ML & Algoritmos  
            "scoring": "numpy + scipy (sin ML complejo)",
            "optimization": "scipy.optimize",
            "clustering": "sklearn.cluster (opcional)",
            
            # Frontend
            "web_framework": "streamlit (velocidad de desarrollo)",
            "maps": "folium + streamlit-folium",
            "charts": "plotly express",
            "styling": "streamlit + custom CSS",
            
            # Deploy
            "hosting": "streamlit cloud (gratis y rápido)",
            "domain": "custom domain via CNAME",
            "monitoring": "streamlit analytics",
            
            # Backup
            "local_deploy": "python -m streamlit run",
            "containerization": "docker (si tiempo permite)"
        }
    
    def define_critical_data(self) -> Dict[str, Dict[str, Any]]:
        """Fuentes de datos críticas - mínimo viable"""
        return {
            "inegi_basic": {
                "priority": 1,
                "source": "INEGI Descarga Directa + API",
                "data": [
                    "Población por AGEB/Colonia",
                    "Nivel socioeconómico promedio", 
                    "Escolaridad promedio",
                    "Viviendas particulares habitadas"
                ],
                "format": "CSV + Excel",
                "processing_time": "2h"
            },
            "cdmx_seguridad": {
                "priority": 1,
                "source": "Datos Abiertos CDMX API",
                "data": [
                    "Carpetas de investigación por colonia",
                    "Incidencia delictiva mensual",
                    "Clasificación de delitos"
                ],
                "format": "JSON via API",
                "processing_time": "1h"
            },
            "transporte_basico": {
                "priority": 2,
                "source": "GTFS CDMX + OpenStreetMap",
                "data": [
                    "Estaciones de Metro cercanas",
                    "Paradas de Metrobús",
                    "Líneas de transporte principales"
                ],
                "format": "GTFS + OSM XML",
                "processing_time": "1.5h"
            },
            "precios_inmobiliarios": {
                "priority": 1,
                "source": "Web Scraping + Dataset públicos",
                "data": [
                    "Precio promedio m² renta",
                    "Precio promedio m² venta", 
                    "Tipo de propiedades disponibles"
                ],
                "format": "Web scraping + CSV",
                "processing_time": "2h"
            },
            "pois_basicos": {
                "priority": 3,
                "source": "OpenStreetMap + Google Places",
                "data": [
                    "Hospitales principales",
                    "Universidades",
                    "Centros comerciales",
                    "Parques importantes"
                ],
                "format": "API JSON",
                "processing_time": "1h"
            }
        }
    
    def define_feature_priority(self) -> Dict[str, List[str]]:
        """Priorización de features para MVP"""
        return {
            "must_have": [
                "Form de entrada con 5-7 campos clave",
                "Algoritmo de scoring básico pero sólido",
                "Mapa con 3-5 zonas recomendadas coloreadas",
                "Fichas básicas de cada zona recomendada",
                "Justificación simple del por qué de cada recomendación"
            ],
            "should_have": [
                "Filtros dinámicos en el mapa",
                "Comparación lado a lado de zonas",
                "Gráficas básicas de características",
                "Export de resultados (PDF básico)"
            ],
            "could_have": [
                "Personalización avanzada de pesos",
                "Historiales de búsqueda",
                "Integración con más APIs",
                "Animaciones y transiciones fancy"
            ],
            "wont_have": [
                "Sistema de usuarios/login",
                "Base de datos compleja",
                "Machine learning avanzado",
                "Mobile app nativa",
                "Integración con redes sociales"
            ]
        }
    
    def get_development_timeline(self) -> Dict[str, Any]:
        """Timeline detallado con hitos específicos"""
        start_time = datetime.now()
        timeline = {}
        
        current_time = start_time
        for phase in self.strategy.development_phases:
            phase_duration = timedelta(hours=phase["hours"])
            timeline[phase["phase"]] = {
                "start": current_time.strftime("%Y-%m-%d %H:%M"),
                "end": (current_time + phase_duration).strftime("%Y-%m-%d %H:%M"),
                "duration": phase["hours"],
                "deliverables": phase["deliverables"],
                "priority": phase["priority"]
            }
            current_time += phase_duration
        
        timeline["buffer_time"] = {
            "start": current_time.strftime("%Y-%m-%d %H:%M"),
            "end": (current_time + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"),
            "duration": 6,
            "purpose": "Imprevistos, pulido final, backup plans"
        }
        
        return timeline
    
    def generate_mvp_tasks(self) -> List[Dict[str, Any]]:
        """Genera tareas específicas priorizadas"""
        return [
            {
                "task_id": "mvp_data_001",
                "title": "Extraer y limpiar datos INEGI colonias CDMX",
                "priority": 1,
                "estimated_hours": 2,
                "deliverable": "Dataset limpio con indicadores socioeconómicos por colonia",
                "tools": ["pandas", "requests", "geopandas"],
                "validation": "150+ colonias con datos completos"
            },
            {
                "task_id": "mvp_data_002", 
                "title": "Integrar datos de seguridad CDMX por colonia",
                "priority": 1,
                "estimated_hours": 1,
                "deliverable": "Índice de seguridad por colonia",
                "tools": ["requests", "pandas"],
                "validation": "Score de seguridad normalizado 0-100"
            },
            {
                "task_id": "mvp_data_003",
                "title": "Web scraping precios inmobiliarios",
                "priority": 1,
                "estimated_hours": 2,
                "deliverable": "Precios promedio venta/renta por colonia",
                "tools": ["beautifulsoup4", "requests"],
                "validation": "Precios para 100+ colonias principales"
            },
            {
                "task_id": "mvp_algo_001",
                "title": "Implementar algoritmo de scoring multivariable",
                "priority": 1,
                "estimated_hours": 3,
                "deliverable": "Función que recibe preferencias y devuelve scores",
                "tools": ["numpy", "scipy"],
                "validation": "Scores coherentes y explicables"
            },
            {
                "task_id": "mvp_algo_002",
                "title": "Sistema de recomendación y ranking",
                "priority": 1,
                "estimated_hours": 2,
                "deliverable": "Top 3-5 zonas según perfil usuario",
                "tools": ["pandas", "numpy"],
                "validation": "Recomendaciones diversas y relevantes"
            },
            {
                "task_id": "mvp_web_001",
                "title": "Interfaz Streamlit con formulario de entrada",
                "priority": 1,
                "estimated_hours": 3,
                "deliverable": "Form funcional que captura preferencias",
                "tools": ["streamlit"],
                "validation": "UX intuitiva, validación de inputs"
            },
            {
                "task_id": "mvp_web_002",
                "title": "Mapa interactivo con zonas recomendadas",
                "priority": 1,
                "estimated_hours": 4,
                "deliverable": "Mapa Folium con markers/colores por score",
                "tools": ["folium", "streamlit-folium"],
                "validation": "Mapa responsive, tooltips informativos"
            },
            {
                "task_id": "mvp_web_003",
                "title": "Dashboard de resultados y fichas de zonas",
                "priority": 1,
                "estimated_hours": 2,
                "deliverable": "Presentación clara de recomendaciones",
                "tools": ["streamlit", "plotly"],
                "validation": "Info concisa y accionable para usuario"
            },
            {
                "task_id": "mvp_deploy_001",
                "title": "Deploy en Streamlit Cloud con dominio personalizado",
                "priority": 1,
                "estimated_hours": 2,
                "deliverable": "App funcionando en casamx.app",
                "tools": ["streamlit cloud", "DNS config"],
                "validation": "URL funcional, performance aceptable"
            },
            {
                "task_id": "mvp_present_001",
                "title": "Preparar demo y casos de prueba",
                "priority": 2,
                "estimated_hours": 1,
                "deliverable": "3 casos de uso diversos preparados",
                "tools": ["demo scenarios"],
                "validation": "Demos fluidas, narrativa clara"
            }
        ]

def main():
    """Función principal para mostrar la estrategia MVP"""
    
    print("⚡ ESTRATEGIA MVP 36 HORAS - DATATÓN ITAM 2025")
    print("🏆 CasaMX: Recomendador Inteligente de Zonas CDMX")
    print("👨‍💻 David Fernando Ávila Díaz - ITAM")
    print("=" * 70)
    
    mvp_manager = DatatonMVPManager()
    
    # Mostrar timeline
    print("\n⏰ TIMELINE DE DESARROLLO:")
    timeline = mvp_manager.get_development_timeline()
    for phase_name, phase_info in timeline.items():
        priority_emoji = "🔴" if phase_info.get("priority") == "CRÍTICA" else "🟡" if phase_info.get("priority") == "ALTA" else "🟢"
        print(f"   {priority_emoji} {phase_name}")
        print(f"      📅 {phase_info['start']} → {phase_info['end']} ({phase_info['duration']}h)")
        if "deliverables" in phase_info:
            print(f"      📋 {len(phase_info['deliverables'])} deliverables")
    
    # Mostrar stack tecnológico
    print(f"\n🛠️ STACK TECNOLÓGICO MVP:")
    tech_stack = mvp_manager.tech_stack
    for category, tools in tech_stack.items():
        print(f"   📦 {category}: {tools}")
    
    # Mostrar datos críticos
    print(f"\n📊 FUENTES DE DATOS CRÍTICAS:")
    for source_name, source_info in mvp_manager.critical_data_sources.items():
        priority_emoji = "🔴" if source_info["priority"] == 1 else "🟡" if source_info["priority"] == 2 else "🟢"
        print(f"   {priority_emoji} {source_info['source']} ({source_info['processing_time']})")
        print(f"      📋 {len(source_info['data'])} tipos de datos")
    
    # Mostrar features
    print(f"\n🎯 PRIORIZACIÓN DE FEATURES:")
    features = mvp_manager.feature_prioritization
    for category, feature_list in features.items():
        emoji = "🔴" if category == "must_have" else "🟡" if category == "should_have" else "🟢" if category == "could_have" else "❌"
        print(f"   {emoji} {category.upper()}: {len(feature_list)} features")
        for feature in feature_list[:2]:  # Mostrar solo las primeras 2
            print(f"      • {feature}")
        if len(feature_list) > 2:
            print(f"      • ... y {len(feature_list) - 2} más")
    
    # Mostrar tareas inmediatas
    print(f"\n📋 PRIMERAS 5 TAREAS CRÍTICAS:")
    tasks = mvp_manager.generate_mvp_tasks()
    for i, task in enumerate(tasks[:5], 1):
        priority_emoji = "🔴" if task["priority"] == 1 else "🟡"
        print(f"   {priority_emoji} {i}. {task['title']} ({task['estimated_hours']}h)")
        print(f"      🎯 {task['deliverable']}")
    
    print(f"\n🚀 NOMBRE DE APP PROPUESTO: CasaMX")
    print(f"🌐 DOMINIO SUGERIDO: casamx.app")
    print(f"💡 TAGLINE: 'Tu hogar ideal en México, personalizado para ti'")
    
    print(f"\n⚡ LISTO PARA EJECUTAR EN 36 HORAS")
    print(f"🏆 ESTRATEGIA OPTIMIZADA PARA GANAR EL DATATÓN")
    
    return mvp_manager

if __name__ == "__main__":
    mvp_manager = main()