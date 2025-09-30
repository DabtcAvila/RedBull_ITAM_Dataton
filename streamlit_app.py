#!/usr/bin/env python3
"""
CASAMX - APLICACIÓN STREAMLIT COMPLETA
Datatón ITAM 2025 - Sistema de Recomendaciones de Vivienda CDMX

David Fernando Ávila Díaz - ITAM
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from datetime import datetime
import json
from typing import Dict, List, Any
import base64
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
from recommendation_engine import (
    IntelligentRecommendationEngine, 
    UserProfile, 
    ZoneRecommendation
)

# ==================== CONFIGURACIÓN DE PÁGINA ====================
st.set_page_config(
    page_title="CasaMX - Encuentra tu hogar ideal en CDMX",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS PERSONALIZADO ====================
def load_custom_css():
    """Carga estilos CSS personalizados para diseño profesional"""
    st.markdown("""
    <style>
    /* Tema principal */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header personalizado */
    .custom-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .custom-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .custom-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Cards de recomendaciones */
    .recommendation-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .recommendation-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .card-subtitle {
        color: #7f8c8d;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    .score-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .score-detail {
        display: inline-block;
        margin-right: 1rem;
        padding: 0.2rem 0.6rem;
        background: #f8f9fa;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    /* Pros y contras */
    .pros-list {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    
    .contras-list {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
    }
    
    .pros-list h4, .contras-list h4 {
        margin-top: 0;
        color: #155724;
    }
    
    .contras-list h4 {
        color: #721c24;
    }
    
    /* Métricas personalizadas */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        text-align: center;
        border: 1px solid #e9ecef;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Botones personalizados */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Mapa container */
    .map-container {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Alertas personalizadas */
    .custom-alert {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .alert-success {
        background-color: #d4edda;
        border-color: #28a745;
        color: #155724;
    }
    
    .alert-info {
        background-color: #cce7ff;
        border-color: #007bff;
        color: #004085;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }
    
    /* Loader */
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== DATOS MOCK ====================
@st.cache_data
def load_mock_zones_data():
    """Carga datos mock de zonas CDMX para demo"""
    zones_data = [
        {
            'colonia': 'Roma Norte',
            'alcaldia': 'Cuauhtémoc',
            'lat': 19.4149,
            'lon': -99.1625,
            'precio_m2_renta_pesos': 350,
            'precio_m2_venta_pesos': 45000,
            'indice_seguridad': 82,
            'score_conectividad': 95,
            'score_amenidades': 88,
            'tiempo_centro_min': 15,
            'tiempo_polanco_min': 20,
            'tiempo_santa_fe_min': 35,
            'tiempo_roma_norte_min': 5,
            'tiempo_insurgentes_sur_min': 25,
            'parques_1km': 4,
            'restaurantes_1km': 45,
            'hospitales_1km': 3,
            'escuelas_primarias_1km': 6,
            'supermercados_1km': 8,
            'bancos_1km': 12,
            'estaciones_metro_1km': 2,
            'nivel_ruido': 6,
            'densidad_poblacional': 6500,
            'calidad_aire_promedio': 65,
            'vida_nocturna_score': 90,
            'nivel_socioeconomico': 8,
            'score_general': 85
        },
        {
            'colonia': 'Condesa',
            'alcaldia': 'Cuauhtémoc',
            'lat': 19.4084,
            'lon': -99.1712,
            'precio_m2_renta_pesos': 380,
            'precio_m2_venta_pesos': 48000,
            'indice_seguridad': 80,
            'score_conectividad': 88,
            'score_amenidades': 92,
            'tiempo_centro_min': 18,
            'tiempo_polanco_min': 22,
            'tiempo_santa_fe_min': 38,
            'tiempo_roma_norte_min': 8,
            'tiempo_insurgentes_sur_min': 20,
            'parques_1km': 6,
            'restaurantes_1km': 50,
            'hospitales_1km': 2,
            'escuelas_primarias_1km': 5,
            'supermercados_1km': 7,
            'bancos_1km': 10,
            'estaciones_metro_1km': 1,
            'nivel_ruido': 5,
            'densidad_poblacional': 5800,
            'calidad_aire_promedio': 68,
            'vida_nocturna_score': 95,
            'nivel_socioeconomico': 9,
            'score_general': 88
        },
        {
            'colonia': 'Polanco',
            'alcaldia': 'Miguel Hidalgo',
            'lat': 19.4338,
            'lon': -99.1929,
            'precio_m2_renta_pesos': 500,
            'precio_m2_venta_pesos': 65000,
            'indice_seguridad': 95,
            'score_conectividad': 85,
            'score_amenidades': 95,
            'tiempo_centro_min': 25,
            'tiempo_polanco_min': 5,
            'tiempo_santa_fe_min': 30,
            'tiempo_roma_norte_min': 20,
            'tiempo_insurgentes_sur_min': 35,
            'parques_1km': 3,
            'restaurantes_1km': 60,
            'hospitales_1km': 4,
            'escuelas_primarias_1km': 8,
            'supermercados_1km': 12,
            'bancos_1km': 15,
            'estaciones_metro_1km': 1,
            'nivel_ruido': 4,
            'densidad_poblacional': 4200,
            'calidad_aire_promedio': 72,
            'vida_nocturna_score': 85,
            'nivel_socioeconomico': 10,
            'score_general': 92
        },
        {
            'colonia': 'Del Valle',
            'alcaldia': 'Benito Juárez',
            'lat': 19.3729,
            'lon': -99.1619,
            'precio_m2_renta_pesos': 320,
            'precio_m2_venta_pesos': 42000,
            'indice_seguridad': 88,
            'score_conectividad': 90,
            'score_amenidades': 85,
            'tiempo_centro_min': 20,
            'tiempo_polanco_min': 25,
            'tiempo_santa_fe_min': 40,
            'tiempo_roma_norte_min': 15,
            'tiempo_insurgentes_sur_min': 10,
            'parques_1km': 5,
            'restaurantes_1km': 35,
            'hospitales_1km': 5,
            'escuelas_primarias_1km': 10,
            'supermercados_1km': 9,
            'bancos_1km': 11,
            'estaciones_metro_1km': 3,
            'nivel_ruido': 5,
            'densidad_poblacional': 7200,
            'calidad_aire_promedio': 70,
            'vida_nocturna_score': 70,
            'nivel_socioeconomico': 8,
            'score_general': 82
        },
        {
            'colonia': 'San Ángel',
            'alcaldia': 'Álvaro Obregón',
            'lat': 19.3467,
            'lon': -99.1881,
            'precio_m2_renta_pesos': 300,
            'precio_m2_venta_pesos': 38000,
            'indice_seguridad': 92,
            'score_conectividad': 70,
            'score_amenidades': 80,
            'tiempo_centro_min': 35,
            'tiempo_polanco_min': 30,
            'tiempo_santa_fe_min': 25,
            'tiempo_roma_norte_min': 25,
            'tiempo_insurgentes_sur_min': 15,
            'parques_1km': 8,
            'restaurantes_1km': 25,
            'hospitales_1km': 3,
            'escuelas_primarias_1km': 7,
            'supermercados_1km': 6,
            'bancos_1km': 8,
            'estaciones_metro_1km': 0,
            'nivel_ruido': 3,
            'densidad_poblacional': 3500,
            'calidad_aire_promedio': 78,
            'vida_nocturna_score': 45,
            'nivel_socioeconomico': 9,
            'score_general': 78
        },
        {
            'colonia': 'Coyoacán Centro',
            'alcaldia': 'Coyoacán',
            'lat': 19.3496,
            'lon': -99.1617,
            'precio_m2_renta_pesos': 280,
            'precio_m2_venta_pesos': 35000,
            'indice_seguridad': 85,
            'score_conectividad': 75,
            'score_amenidades': 78,
            'tiempo_centro_min': 30,
            'tiempo_polanco_min': 35,
            'tiempo_santa_fe_min': 45,
            'tiempo_roma_norte_min': 20,
            'tiempo_insurgentes_sur_min': 12,
            'parques_1km': 7,
            'restaurantes_1km': 30,
            'hospitales_1km': 2,
            'escuelas_primarias_1km': 8,
            'supermercados_1km': 7,
            'bancos_1km': 9,
            'estaciones_metro_1km': 1,
            'nivel_ruido': 4,
            'densidad_poblacional': 4800,
            'calidad_aire_promedio': 75,
            'vida_nocturna_score': 60,
            'nivel_socioeconomico': 7,
            'score_general': 75
        },
        {
            'colonia': 'Narvarte',
            'alcaldia': 'Benito Juárez',
            'lat': 19.3890,
            'lon': -99.1496,
            'precio_m2_renta_pesos': 250,
            'precio_m2_venta_pesos': 32000,
            'indice_seguridad': 78,
            'score_conectividad': 88,
            'score_amenidades': 82,
            'tiempo_centro_min': 18,
            'tiempo_polanco_min': 28,
            'tiempo_santa_fe_min': 42,
            'tiempo_roma_norte_min': 12,
            'tiempo_insurgentes_sur_min': 8,
            'parques_1km': 3,
            'restaurantes_1km': 28,
            'hospitales_1km': 4,
            'escuelas_primarias_1km': 9,
            'supermercados_1km': 8,
            'bancos_1km': 10,
            'estaciones_metro_1km': 2,
            'nivel_ruido': 6,
            'densidad_poblacional': 8500,
            'calidad_aire_promedio': 62,
            'vida_nocturna_score': 65,
            'nivel_socioeconomico': 6,
            'score_general': 72
        },
        {
            'colonia': 'Escandón',
            'alcaldia': 'Miguel Hidalgo',
            'lat': 19.4015,
            'lon': -99.1815,
            'precio_m2_renta_pesos': 240,
            'precio_m2_venta_pesos': 30000,
            'indice_seguridad': 75,
            'score_conectividad': 85,
            'score_amenidades': 75,
            'tiempo_centro_min': 22,
            'tiempo_polanco_min': 15,
            'tiempo_santa_fe_min': 25,
            'tiempo_roma_norte_min': 10,
            'tiempo_insurgentes_sur_min': 20,
            'parques_1km': 2,
            'restaurantes_1km': 20,
            'hospitales_1km': 2,
            'escuelas_primarias_1km': 6,
            'supermercados_1km': 6,
            'bancos_1km': 7,
            'estaciones_metro_1km': 1,
            'nivel_ruido': 7,
            'densidad_poblacional': 9200,
            'calidad_aire_promedio': 58,
            'vida_nocturna_score': 55,
            'nivel_socioeconomico': 5,
            'score_general': 68
        }
    ]
    return zones_data

# ==================== FUNCIONES AUXILIARES ====================
def create_user_profile_from_form(form_data: Dict[str, Any]) -> UserProfile:
    """Convierte datos del formulario en UserProfile"""
    # Mapear prioridades texto a números
    priority_mapping = {
        'Muy Bajo': 2,
        'Bajo': 4,
        'Medio': 6,
        'Alto': 8,
        'Muy Alto': 10
    }
    
    return UserProfile(
        presupuesto_max_renta=form_data['presupuesto_renta'],
        tamano_familia=form_data['tamaño_familia'],
        tiene_hijos=form_data['tiene_hijos'],
        edades_hijos=form_data.get('edades_hijos', []),
        prioridad_seguridad=priority_mapping[form_data['prioridad_seguridad']],
        prioridad_transporte=priority_mapping[form_data['prioridad_transporte']],
        prioridad_precio=priority_mapping[form_data['prioridad_precio']],
        ubicacion_trabajo=form_data['ubicación_trabajo'],
        estilo_vida=form_data['estilo_vida'],
        prefiere_zonas_tranquilas=form_data.get('prefiere_tranquilo', True),
        tiempo_max_trabajo_min=form_data.get('tiempo_max_trabajo', 45)
    )

def get_score_color(score: float) -> str:
    """Retorna color basado en score"""
    if score >= 85:
        return '#28a745'  # Verde
    elif score >= 70:
        return '#17a2b8'  # Azul
    elif score >= 55:
        return '#ffc107'  # Amarillo
    else:
        return '#dc3545'  # Rojo

def create_folium_map(recommendations: List[ZoneRecommendation], zones_data: List[Dict]) -> folium.Map:
    """Crea mapa interactivo con Folium"""
    # Centro del mapa en CDMX
    center_lat, center_lon = 19.4326, -99.1332
    
    # Crear mapa
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Mapear colonias a datos geográficos
    colonia_to_coords = {zone['colonia']: (zone['lat'], zone['lon']) for zone in zones_data}
    
    # Agregar markers para recomendaciones
    for i, rec in enumerate(recommendations):
        if rec.colonia in colonia_to_coords:
            lat, lon = colonia_to_coords[rec.colonia]
            
            # Color basado en ranking
            if i == 0:
                color = 'red'
                icon = '1'
            elif i == 1:
                color = 'orange'
                icon = '2'
            elif i == 2:
                color = 'yellow'
                icon = '3'
            else:
                color = 'blue'
                icon = str(i + 1)
            
            # Popup con información detallada
            popup_html = f"""
            <div style="width: 300px;">
                <h4>#{rec.ranking} {rec.colonia}</h4>
                <p><strong>Alcaldía:</strong> {rec.alcaldia}</p>
                <p><strong>Score:</strong> {rec.score_personalizado:.1f}/100</p>
                <p><strong>Renta estimada:</strong> ${rec.precio_renta_estimado:,}/mes</p>
                <hr>
                <p><strong>Seguridad:</strong> {rec.score_seguridad:.0f}/100</p>
                <p><strong>Transporte:</strong> {rec.score_transporte:.0f}/100</p>
                <p><strong>Precio:</strong> {rec.score_precio:.0f}/100</p>
                <hr>
                <p><strong>Principales razones:</strong></p>
                <ul>
                {"".join([f"<li>{razon}</li>" for razon in rec.razones_principales])}
                </ul>
            </div>
            """
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=f"#{rec.ranking} {rec.colonia}",
                icon=folium.Icon(
                    color=color,
                    icon_color='white',
                    icon='home',
                    prefix='fa'
                )
            ).add_to(m)
    
    return m

def display_recommendation_card(rec: ZoneRecommendation, rank: int):
    """Muestra card de recomendación"""
    with st.container():
        st.markdown(f"""
        <div class="recommendation-card">
            <div class="card-title">
                #{rank} {rec.colonia}
                <span class="score-badge">{rec.score_personalizado:.1f}/100</span>
            </div>
            <div class="card-subtitle">
                {rec.alcaldia} • Renta estimada: ${rec.precio_renta_estimado:,}/mes
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas en columnas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="score-detail">
                🛡️ Seguridad: {rec.score_seguridad:.0f}/100
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="score-detail">
                🚊 Transporte: {rec.score_transporte:.0f}/100
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="score-detail">
                💰 Precio: {rec.score_precio:.0f}/100
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="score-detail">
                🏪 Amenidades: {rec.score_amenidades:.0f}/100
            </div>
            """, unsafe_allow_html=True)
        
        # Expandir para ver detalles
        with st.expander(f"Ver detalles de {rec.colonia}"):
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("""
                <div class="pros-list">
                    <h4>✅ Ventajas</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for pro in rec.pros:
                    st.write(f"• {pro}")
            
            with col_right:
                st.markdown("""
                <div class="contras-list">
                    <h4>⚠️ Consideraciones</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for contra in rec.contras:
                    st.write(f"• {contra}")
            
            # Razones principales
            st.markdown("### 🎯 Por qué te recomendamos esta zona:")
            for razon in rec.razones_principales:
                st.info(f"💡 {razon}")

def generate_pdf_report(recommendations: List[ZoneRecommendation], user_profile: UserProfile) -> bytes:
    """Genera reporte PDF básico"""
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Título
    title = Paragraph("CasaMX - Reporte de Recomendaciones", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Información del usuario
    user_info = f"""
    <b>Perfil del Usuario:</b><br/>
    • Presupuesto: ${user_profile.presupuesto_max_renta:,}/mes<br/>
    • Tamaño familia: {user_profile.tamano_familia} personas<br/>
    • Ubicación trabajo: {user_profile.ubicacion_trabajo}<br/>
    • Estilo de vida: {user_profile.estilo_vida}<br/>
    """
    story.append(Paragraph(user_info, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Recomendaciones
    for i, rec in enumerate(recommendations, 1):
        rec_text = f"""
        <b>#{i} {rec.colonia}</b><br/>
        Alcaldía: {rec.alcaldia}<br/>
        Score: {rec.score_personalizado:.1f}/100<br/>
        Renta estimada: ${rec.precio_renta_estimado:,}/mes<br/>
        <br/>
        """
        story.append(Paragraph(rec_text, styles['Normal']))
        story.append(Spacer(1, 6))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# ==================== INTERFAZ PRINCIPAL ====================
def main():
    """Función principal de la aplicación Streamlit"""
    
    # Cargar CSS personalizado
    load_custom_css()
    
    # Header personalizado
    st.markdown("""
    <div class="custom-header">
        <h1>🏠 CasaMX</h1>
        <p>Encuentra tu hogar ideal en Ciudad de México</p>
        <p><small>Datatón ITAM 2025 • Algoritmo Inteligente de Recomendaciones</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar engine y datos
    if 'engine' not in st.session_state:
        st.session_state.engine = IntelligentRecommendationEngine()
        st.session_state.zones_data = load_mock_zones_data()
    
    # ==================== SIDEBAR - FORMULARIO ====================
    with st.sidebar:
        st.markdown("## 📝 Cuéntanos sobre ti")
        
        with st.form("user_profile_form"):
            st.markdown("### 💰 Presupuesto")
            presupuesto_renta = st.slider(
                "Presupuesto mensual para renta (MXN)",
                min_value=5000,
                max_value=100000,
                value=25000,
                step=2500,
                help="Incluye renta + gastos estimados"
            )
            
            st.markdown("### 👥 Familia")
            tamaño_familia = st.selectbox(
                "Tamaño de la familia",
                options=[1, 2, 3, 4, 5, 6],
                index=1,
                help="Número total de personas que vivirán en el hogar"
            )
            
            tiene_hijos = st.checkbox("Tengo hijos")
            
            edades_hijos = []
            if tiene_hijos:
                num_hijos = st.number_input("Número de hijos", min_value=1, max_value=5, value=1)
                edades_hijos = []
                for i in range(num_hijos):
                    edad = st.number_input(f"Edad del hijo {i+1}", min_value=0, max_value=25, value=8, key=f"hijo_{i}")
                    edades_hijos.append(edad)
            
            st.markdown("### 🎯 Prioridades")
            prioridad_seguridad = st.selectbox(
                "Importancia de la seguridad",
                options=['Muy Bajo', 'Bajo', 'Medio', 'Alto', 'Muy Alto'],
                index=3,
                help="Qué tan importante es para ti vivir en una zona segura"
            )
            
            prioridad_transporte = st.selectbox(
                "Importancia del transporte",
                options=['Muy Bajo', 'Bajo', 'Medio', 'Alto', 'Muy Alto'],
                index=3,
                help="Acceso a transporte público y conectividad"
            )
            
            prioridad_precio = st.selectbox(
                "Importancia del precio",
                options=['Muy Bajo', 'Bajo', 'Medio', 'Alto', 'Muy Alto'],
                index=2,
                help="Qué tan sensible eres al precio/presupuesto"
            )
            
            st.markdown("### 🏢 Trabajo y Estilo")
            ubicación_trabajo = st.selectbox(
                "Ubicación de tu trabajo",
                options=['Centro', 'Polanco', 'Santa Fe', 'Roma Norte', 'Insurgentes Sur'],
                index=1,
                help="Zona donde trabajas o necesitas desplazarte frecuentemente"
            )
            
            estilo_vida = st.selectbox(
                "Tu estilo de vida",
                options=['familiar', 'joven_profesional', 'retirado', 'estudiante'],
                index=0,
                format_func=lambda x: {
                    'familiar': '👨‍👩‍👧‍👦 Familiar',
                    'joven_profesional': '💼 Joven Profesional', 
                    'retirado': '🏌️ Retirado',
                    'estudiante': '🎓 Estudiante'
                }[x],
                help="Selecciona el estilo que mejor te describe"
            )
            
            st.markdown("### ⚙️ Preferencias Adicionales")
            prefiere_tranquilo = st.checkbox("Prefiero zonas tranquilas", value=True)
            tiempo_max_trabajo = st.slider(
                "Tiempo máximo aceptable al trabajo (minutos)",
                min_value=15,
                max_value=90,
                value=45,
                step=5
            )
            
            # Botón de envío
            submitted = st.form_submit_button("🔍 Buscar mi hogar ideal", use_container_width=True)
    
    # ==================== ÁREA PRINCIPAL ====================
    if submitted:
        # Crear perfil de usuario
        form_data = {
            'presupuesto_renta': presupuesto_renta,
            'tamaño_familia': tamaño_familia,
            'tiene_hijos': tiene_hijos,
            'edades_hijos': edades_hijos,
            'prioridad_seguridad': prioridad_seguridad,
            'prioridad_transporte': prioridad_transporte,
            'prioridad_precio': prioridad_precio,
            'ubicación_trabajo': ubicación_trabajo,
            'estilo_vida': estilo_vida,
            'prefiere_tranquilo': prefiere_tranquilo,
            'tiempo_max_trabajo': tiempo_max_trabajo
        }
        
        user_profile = create_user_profile_from_form(form_data)
        
        # Mostrar loading
        with st.spinner('🧠 Analizando las mejores opciones para ti...'):
            # Generar recomendaciones
            recommendations = st.session_state.engine.generate_recommendations(
                st.session_state.zones_data, 
                user_profile, 
                num_recommendations=5
            )
        
        # Guardar en session state
        st.session_state.recommendations = recommendations
        st.session_state.user_profile = user_profile
        
        # Mostrar alerta de éxito
        st.markdown("""
        <div class="custom-alert alert-success">
            ✅ ¡Listo! Hemos encontrado las mejores opciones para ti basadas en tus preferencias.
        </div>
        """, unsafe_allow_html=True)
        
        # ==================== MÉTRICAS RESUMEN ====================
        st.markdown("## 📊 Resumen de Análisis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-container">
                <div class="metric-value">5</div>
                <div class="metric-label">Zonas Analizadas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_score = sum(r.score_personalizado for r in recommendations) / len(recommendations)
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{avg_score:.1f}</div>
                <div class="metric-label">Score Promedio</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_price = sum(r.precio_renta_estimado for r in recommendations) / len(recommendations)
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">${avg_price:,.0f}</div>
                <div class="metric-label">Renta Promedio</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            match_percent = (recommendations[0].score_personalizado / 100) * 100
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{match_percent:.0f}%</div>
                <div class="metric-label">Mejor Match</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ==================== MAPA INTERACTIVO ====================
        st.markdown("## 🗺️ Mapa de Recomendaciones")
        
        # Crear y mostrar mapa
        folium_map = create_folium_map(recommendations, st.session_state.zones_data)
        
        with st.container():
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            map_data = st_folium(folium_map, width=700, height=400)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ==================== RECOMENDACIONES DETALLADAS ====================
        st.markdown("## 🏆 Tus Recomendaciones Personalizadas")
        
        # Tabs para diferentes vistas
        tab1, tab2, tab3 = st.tabs(["📋 Lista Detallada", "📊 Comparación", "💾 Exportar"])
        
        with tab1:
            for i, rec in enumerate(recommendations):
                display_recommendation_card(rec, i + 1)
                if i < len(recommendations) - 1:
                    st.divider()
        
        with tab2:
            # Crear dataframe para comparación
            df_comparison = pd.DataFrame([
                {
                    'Ranking': f"#{i+1}",
                    'Colonia': rec.colonia,
                    'Score Total': rec.score_personalizado,
                    'Seguridad': rec.score_seguridad,
                    'Transporte': rec.score_transporte,
                    'Precio': rec.score_precio,
                    'Renta Est.': f"${rec.precio_renta_estimado:,}"
                }
                for i, rec in enumerate(recommendations)
            ])
            
            st.dataframe(df_comparison, use_container_width=True)
            
            # Gráfico de radar para top 3
            if len(recommendations) >= 3:
                categories = ['Seguridad', 'Transporte', 'Precio', 'Amenidades', 'Calidad Vida']
                
                fig = go.Figure()
                
                for i, rec in enumerate(recommendations[:3]):
                    values = [
                        rec.score_seguridad,
                        rec.score_transporte, 
                        rec.score_precio,
                        rec.score_amenidades,
                        rec.score_calidad_vida
                    ]
                    
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself',
                        name=f"#{i+1} {rec.colonia}",
                        line_color=f"rgba({102 + i*50}, {126 + i*30}, {234 - i*40}, 0.8)"
                    ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    title="Comparación Top 3 Recomendaciones",
                    showlegend=True,
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("### 📄 Descargar Reporte")
            st.info("Genera un reporte PDF con tus recomendaciones personalizadas.")
            
            if st.button("📥 Generar PDF", use_container_width=True):
                try:
                    pdf_bytes = generate_pdf_report(recommendations, user_profile)
                    
                    st.download_button(
                        label="⬇️ Descargar Reporte PDF",
                        data=pdf_bytes,
                        file_name=f"CasaMX_Recomendaciones_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.success("✅ Reporte generado exitosamente!")
                    
                except Exception as e:
                    st.error(f"Error generando PDF: {e}")
                    st.info("💡 Tip: Puedes usar la función de imprimir de tu navegador como alternativa.")
            
            # Export a JSON
            st.markdown("### 📊 Datos en JSON")
            recommendations_dict = [
                {
                    'ranking': i+1,
                    'colonia': rec.colonia,
                    'alcaldia': rec.alcaldia,
                    'score_personalizado': rec.score_personalizado,
                    'precio_renta_estimado': rec.precio_renta_estimado,
                    'razones_principales': rec.razones_principales,
                    'pros': rec.pros,
                    'contras': rec.contras
                }
                for i, rec in enumerate(recommendations)
            ]
            
            json_str = json.dumps(recommendations_dict, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="📁 Descargar JSON",
                data=json_str,
                file_name=f"casamx_recomendaciones_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    else:
        # ==================== PÁGINA INICIAL ====================
        st.markdown("""
        <div class="custom-alert alert-info">
            👋 ¡Bienvenido a CasaMX! 
            Completa el formulario en la barra lateral para obtener recomendaciones personalizadas 
            de las mejores zonas para vivir en Ciudad de México.
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar información del sistema
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🧠 Algoritmo Inteligente
            
            - **Personalización total** basada en tus preferencias
            - **5 categorías de análisis**: Seguridad, Transporte, Precio, Amenidades, Calidad de vida
            - **4 perfiles de estilo de vida** con ajustes automáticos
            - **Scoring dinámico** que se adapta a tu perfil
            """)
        
        with col2:
            st.markdown("""
            ### 📊 Datos y Análisis
            
            - **8+ zonas de CDMX** con datos detallados
            - **15+ indicadores** por zona analizados
            - **Mapa interactivo** con visualización
            - **Explicaciones automáticas** de cada recomendación
            """)
        
        # Mapa demo
        st.markdown("### 🗺️ Vista Previa del Mapa")
        demo_map = folium.Map(location=[19.4326, -99.1332], zoom_start=11)
        
        # Agregar algunos markers de ejemplo
        sample_zones = [
            {"name": "Roma Norte", "lat": 19.4149, "lon": -99.1625, "color": "red"},
            {"name": "Condesa", "lat": 19.4084, "lon": -99.1712, "color": "blue"},
            {"name": "Polanco", "lat": 19.4338, "lon": -99.1929, "color": "green"},
        ]
        
        for zone in sample_zones:
            folium.Marker(
                location=[zone["lat"], zone["lon"]],
                popup=zone["name"],
                tooltip=zone["name"],
                icon=folium.Icon(color=zone["color"], icon='home', prefix='fa')
            ).add_to(demo_map)
        
        st_folium(demo_map, width=700, height=300)
    
    # ==================== FOOTER ====================
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; margin-top: 2rem;">
        🏆 <strong>CasaMX</strong> • Datatón ITAM 2025 • 
        Desarrollado por David Fernando Ávila Díaz<br>
        <small>Algoritmo Inteligente de Recomendaciones Inmobiliarias • CDMX</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()