#!/usr/bin/env python3
"""
CasaMX - Recomendador Inteligente de Zonas CDMX
Datatón ITAM 2025 - David Fernando Ávila Díaz

VERSIÓN CINEMATOGRÁFICA MEJORADA - EFECTOS PREMIUM
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import folium
from folium import plugins
from streamlit_folium import st_folium
import time
import random
from demo_cases import load_demo_case, show_demo_selector, show_demo_profile, enhance_results_with_demo_context

# Configuración de página CINEMATOGRÁFICA
st.set_page_config(
    page_title="CasaMX - Tu hogar ideal en México",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ocultar elementos de Streamlit para look más profesional
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# CSS personalizado
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    .stSelectbox > div > div > select {
        background-color: #f0f2f6;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Ocultar header cuando está en landing page */
    .main .block-container {
        padding-top: 1rem;
    }
    
    /* Estilos para botones demo integrados con Streamlit */
    .stButton > button {
        width: 100%;
        height: auto;
        padding: 1rem;
        border-radius: 15px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Datos mock simplificados pero realistas
@st.cache_data
def load_mock_data():
    """Carga datos mock para la demo"""
    colonias = [
        {
            "colonia": "Roma Norte",
            "alcaldia": "Cuauhtémoc",
            "lat": 19.4149,
            "lon": -99.1625,
            "score_seguridad": 85,
            "score_transporte": 95,
            "score_amenidades": 90,
            "score_precio": 60,
            "precio_renta_m2": 650,
            "nivel_socioeconomico": 8,
            "pros": ["Excelente vida nocturna", "Muy bien conectado", "Gran diversidad cultural"],
            "contras": ["Precios elevados", "Ruido nocturno"],
            "tiempo_centro": 15,
            "tiempo_polanco": 25,
            "tiempo_santa_fe": 45
        },
        {
            "colonia": "Condesa",
            "alcaldia": "Cuauhtémoc",
            "lat": 19.4069,
            "lon": -99.1716,
            "score_seguridad": 82,
            "score_transporte": 88,
            "score_amenidades": 95,
            "score_precio": 55,
            "precio_renta_m2": 700,
            "nivel_socioeconomico": 8,
            "pros": ["Parques hermosos", "Ambiente bohemio", "Restaurantes increíbles"],
            "contras": ["Muy caro", "Tráfico intenso"],
            "tiempo_centro": 20,
            "tiempo_polanco": 30,
            "tiempo_santa_fe": 40
        },
        {
            "colonia": "Polanco",
            "alcaldia": "Miguel Hidalgo",
            "lat": 19.4338,
            "lon": -99.1929,
            "score_seguridad": 95,
            "score_transporte": 85,
            "score_amenidades": 100,
            "score_precio": 30,
            "precio_renta_m2": 900,
            "nivel_socioeconomico": 10,
            "pros": ["La zona más exclusiva", "Máxima seguridad", "Servicios de lujo"],
            "contras": ["Extremadamente caro", "Puede sentirse impersonal"],
            "tiempo_centro": 25,
            "tiempo_polanco": 0,
            "tiempo_santa_fe": 35
        },
        {
            "colonia": "Del Valle",
            "alcaldia": "Benito Juárez",
            "lat": 19.3895,
            "lon": -99.1649,
            "score_seguridad": 88,
            "score_transporte": 78,
            "score_amenidades": 85,
            "score_precio": 70,
            "precio_renta_m2": 480,
            "nivel_socioeconomico": 7,
            "pros": ["Excelente para familias", "Buen precio/calidad", "Zona tranquila"],
            "contras": ["Menos vida nocturna", "Metro no tan cerca"],
            "tiempo_centro": 30,
            "tiempo_polanco": 35,
            "tiempo_santa_fe": 50
        },
        {
            "colonia": "Coyoacán Centro",
            "alcaldia": "Coyoacán",
            "lat": 19.3467,
            "lon": -99.1618,
            "score_seguridad": 90,
            "score_transporte": 70,
            "score_amenidades": 88,
            "score_precio": 75,
            "precio_renta_m2": 420,
            "nivel_socioeconomico": 7,
            "pros": ["Ambiente cultural único", "Arquitectura colonial", "Muy seguro"],
            "contras": ["Lejos del centro", "Transporte limitado"],
            "tiempo_centro": 45,
            "tiempo_polanco": 50,
            "tiempo_santa_fe": 60
        },
        {
            "colonia": "Narvarte",
            "alcaldia": "Benito Juárez",
            "lat": 19.3962,
            "lon": -99.1508,
            "score_seguridad": 75,
            "score_transporte": 85,
            "score_amenidades": 80,
            "score_precio": 85,
            "precio_renta_m2": 380,
            "nivel_socioeconomico": 6,
            "pros": ["Muy buen precio", "Bien conectado", "Comercio local abundante"],
            "contras": ["Densidad alta", "Ruido de avenidas"],
            "tiempo_centro": 25,
            "tiempo_polanco": 40,
            "tiempo_santa_fe": 55
        }
    ]
    return pd.DataFrame(colonias)

def calculate_personalized_score(colonia_data, user_preferences):
    """Calcula score personalizado basado en preferencias"""
    weights = {
        'seguridad': user_preferences['prioridad_seguridad'] / 10.0,
        'transporte': user_preferences['prioridad_transporte'] / 10.0,
        'precio': user_preferences['prioridad_precio'] / 10.0,
        'amenidades': user_preferences['prioridad_amenidades'] / 10.0
    }
    
    # Normalizar pesos
    total_weight = sum(weights.values())
    weights = {k: v/total_weight for k, v in weights.items()}
    
    # Calcular score
    score = (
        colonia_data['score_seguridad'] * weights['seguridad'] +
        colonia_data['score_transporte'] * weights['transporte'] +
        colonia_data['score_precio'] * weights['precio'] +
        colonia_data['score_amenidades'] * weights['amenidades']
    )
    
    return score

def main():
    # Header solo cuando hay resultados
    if hasattr(st.session_state, 'search_done') and st.session_state.search_done:
        st.title("🏠 CasaMX - Resultados")
        st.subheader("Tu hogar ideal en México - Personalizado para ti")
        st.markdown("*Encuentra las mejores zonas de CDMX según tus necesidades*")
    
    # Sidebar - Formulario
    st.sidebar.header("🎯 Cuéntanos sobre ti")
    
    # Mostrar perfil demo si está activo
    show_demo_profile()
    
    # Usar valores del demo si está activo, sino valores por defecto del formulario
    if hasattr(st.session_state, 'demo_mode') and st.session_state.demo_mode:
        presupuesto = st.session_state.presupuesto
        familia_size = st.session_state.familia_size
        tiene_hijos = st.session_state.tiene_hijos
        prioridad_seguridad = st.session_state.prioridad_seguridad
        prioridad_transporte = st.session_state.prioridad_transporte
        prioridad_precio = st.session_state.prioridad_precio
        prioridad_amenidades = st.session_state.prioridad_amenidades
        trabajo_zona = st.session_state.trabajo_zona
        estilo_vida = st.session_state.estilo_vida
        
        # Mostrar formulario deshabilitado en modo demo
        st.sidebar.subheader("Información Básica (Demo)")
        st.sidebar.text_input("Presupuesto mensual", f"${presupuesto:,} MXN", disabled=True)
        st.sidebar.text_input("Tamaño de familia", f"{familia_size} personas", disabled=True)
        st.sidebar.text_input("¿Tienes hijos?", "Sí" if tiene_hijos else "No", disabled=True)
        
        st.sidebar.subheader("Prioridades Configuradas")
        st.sidebar.text_input("Seguridad", f"{prioridad_seguridad}/10", disabled=True)
        st.sidebar.text_input("Transporte", f"{prioridad_transporte}/10", disabled=True)
        st.sidebar.text_input("Precio", f"{prioridad_precio}/10", disabled=True)
        st.sidebar.text_input("Amenidades", f"{prioridad_amenidades}/10", disabled=True)
        
        st.sidebar.subheader("Preferencias Configuradas")
        st.sidebar.text_input("Zona de trabajo", trabajo_zona, disabled=True)
        st.sidebar.text_input("Estilo de vida", estilo_vida, disabled=True)
    else:
        # Formulario normal
        st.sidebar.subheader("Información Básica")
        presupuesto = st.sidebar.slider("Presupuesto mensual (MXN)", 5000, 50000, 20000, 1000)
        familia_size = st.sidebar.selectbox("Tamaño de familia", [1, 2, 3, 4, 5])
        tiene_hijos = st.sidebar.checkbox("¿Tienes hijos?")
        
        # Prioridades
        st.sidebar.subheader("Tus Prioridades (1-10)")
        prioridad_seguridad = st.sidebar.slider("Seguridad", 1, 10, 8)
        prioridad_transporte = st.sidebar.slider("Transporte público", 1, 10, 7)
        prioridad_precio = st.sidebar.slider("Precio accesible", 1, 10, 6)
        prioridad_amenidades = st.sidebar.slider("Servicios y amenidades", 1, 10, 7)
        
        # Preferencias
        st.sidebar.subheader("Preferencias")
        trabajo_zona = st.sidebar.selectbox("¿Dónde trabajas?", 
                                           ["Centro", "Polanco", "Santa Fe", "Roma Norte", "Otro"])
        estilo_vida = st.sidebar.selectbox("Tu estilo de vida", 
                                          ["Familiar", "Joven profesional", "Estudiante", "Retirado"])
    
    # Botón de búsqueda
    if st.sidebar.button("🔍 Buscar mi zona ideal", type="primary"):
        st.session_state.search_done = True
    
    # Contenido principal
    if hasattr(st.session_state, 'search_done') and st.session_state.search_done:
        
        # Cargar datos
        df = load_mock_data()
        
        # Crear preferencias del usuario
        user_preferences = {
            'presupuesto': presupuesto,
            'familia_size': familia_size,
            'tiene_hijos': tiene_hijos,
            'prioridad_seguridad': prioridad_seguridad,
            'prioridad_transporte': prioridad_transporte,
            'prioridad_precio': prioridad_precio,
            'prioridad_amenidades': prioridad_amenidades,
            'trabajo_zona': trabajo_zona,
            'estilo_vida': estilo_vida
        }
        
        # Calcular scores personalizados
        df['score_personalizado'] = df.apply(
            lambda x: calculate_personalized_score(x, user_preferences), axis=1
        )
        
        # Filtrar por presupuesto (estimando 50m² promedio)
        precio_maximo_m2 = presupuesto / 50
        df_filtered = df[df['precio_renta_m2'] <= precio_maximo_m2 * 1.2]  # 20% tolerancia
        
        if df_filtered.empty:
            st.warning("⚠️ No encontramos zonas dentro de tu presupuesto. Te mostramos las más cercanas:")
            df_filtered = df.nsmallest(3, 'precio_renta_m2')
        
        # Ordenar por score personalizado
        df_filtered = df_filtered.sort_values('score_personalizado', ascending=False)
        
        # Top 3 recomendaciones
        top_recommendations = df_filtered.head(3)
        
        # Mostrar resultados
        st.header("🎯 Tus 3 Zonas Recomendadas")
        
        # Métricas resumen
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏆 Mejor Match", 
                     top_recommendations.iloc[0]['colonia'],
                     f"{top_recommendations.iloc[0]['score_personalizado']:.1f}/100")
        with col2:
            avg_price = top_recommendations['precio_renta_m2'].mean() * 50  # 50m²
            st.metric("💰 Precio Promedio", f"${avg_price:,.0f}", "MXN/mes")
        with col3:
            st.metric("📊 Zonas Analizadas", len(df), "colonias CDMX")
        
        # Mostrar información específica del caso demo si está activo
        if hasattr(st.session_state, 'demo_mode') and st.session_state.demo_mode:
            case_name = None
            # Identificar el caso activo
            if st.session_state.demo_case['name'] == 'María González':
                case_name = 'maria'
            elif st.session_state.demo_case['name'] == 'Alessandro Romano':
                case_name = 'alex'
            elif st.session_state.demo_case['name'] == 'Sophie Dubois':
                case_name = 'sophie'
            
            if case_name:
                demo_context = enhance_results_with_demo_context(top_recommendations, case_name)
                
                st.markdown("---")
                st.subheader(f"📊 Análisis Específico para {st.session_state.demo_case['name']}")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.info(f"**Insight Clave:** {demo_context['insights']['key_finding']}")
                    st.markdown(f"**¿Por qué estas recomendaciones?** {demo_context['insights']['recommendation_reason']}")
                    st.markdown(f"**Fit Cultural:** {demo_context['insights']['cultural_fit']}")
                    
                with col2:
                    st.markdown("**📈 Métricas de Éxito:**")
                    for metric, value in demo_context['success_metrics'].items():
                        st.markdown(f"• {value}")
                    
                st.markdown(f"**💰 Análisis de Presupuesto:** {demo_context['insights']['budget_analysis']}")
                st.markdown(f"**🚗 Impacto del Commute:** {demo_context['insights']['commute_impact']}")
        
        # Mapa interactivo
        st.subheader("🗺️ Ubicación de Recomendaciones")
        
        # Crear mapa centrado en CDMX
        m = folium.Map(location=[19.4326, -99.1332], zoom_start=11)
        
        # Agregar marcadores para cada recomendación
        colors = ['red', 'orange', 'green']
        for idx, (_, colonia) in enumerate(top_recommendations.iterrows()):
            folium.Marker(
                location=[colonia['lat'], colonia['lon']],
                popup=f"""
                <b>{colonia['colonia']}</b><br>
                Score: {colonia['score_personalizado']:.1f}/100<br>
                Precio: ${colonia['precio_renta_m2'] * 50:,.0f}/mes<br>
                Seguridad: {colonia['score_seguridad']}/100
                """,
                tooltip=f"#{idx+1}: {colonia['colonia']}",
                icon=folium.Icon(color=colors[idx], icon='home')
            ).add_to(m)
        
        # Mostrar mapa
        st_folium(m, width=700, height=400)
        
        # Cards detalladas de recomendaciones
        st.subheader("📋 Detalles de Recomendaciones")
        
        for idx, (_, colonia) in enumerate(top_recommendations.iterrows()):
            with st.expander(f"#{idx+1}: {colonia['colonia']} - {colonia['alcaldia']} ⭐{colonia['score_personalizado']:.1f}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🏠 Información General**")
                    precio_estimado = colonia['precio_renta_m2'] * 50
                    st.write(f"💰 **Precio estimado:** ${precio_estimado:,.0f}/mes")
                    st.write(f"🏢 **Alcaldía:** {colonia['alcaldia']}")
                    st.write(f"📊 **Nivel socioeconómico:** {colonia['nivel_socioeconomico']}/10")
                    
                    # Tiempos de traslado
                    st.markdown("**🚗 Tiempos de Traslado**")
                    st.write(f"🏛️ Centro: {colonia['tiempo_centro']} min")
                    st.write(f"🏙️ Polanco: {colonia['tiempo_polanco']} min")
                    st.write(f"🏢 Santa Fe: {colonia['tiempo_santa_fe']} min")
                
                with col2:
                    st.markdown("**📊 Scores por Categoría**")
                    
                    # Gráfico de barras para scores
                    scores_data = {
                        'Seguridad': colonia['score_seguridad'],
                        'Transporte': colonia['score_transporte'],
                        'Amenidades': colonia['score_amenidades'],
                        'Precio': colonia['score_precio']
                    }
                    
                    fig = go.Figure([go.Bar(
                        x=list(scores_data.keys()),
                        y=list(scores_data.values()),
                        marker_color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
                    )])
                    fig.update_layout(height=300, yaxis_range=[0,100])
                    st.plotly_chart(fig, use_container_width=True)
                
                # Pros y contras
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown("**✅ Ventajas**")
                    for pro in colonia['pros']:
                        st.write(f"• {pro}")
                
                with col4:
                    st.markdown("**⚠️ Consideraciones**")
                    for contra in colonia['contras']:
                        st.write(f"• {contra}")
        
        # Gráfico comparativo
        st.subheader("📈 Comparación Visual")
        
        categories = ['score_seguridad', 'score_transporte', 'score_amenidades', 'score_precio']
        fig = go.Figure()
        
        for idx, (_, colonia) in enumerate(top_recommendations.iterrows()):
            fig.add_trace(go.Scatterpolar(
                r=[colonia[cat] for cat in categories],
                theta=['Seguridad', 'Transporte', 'Amenidades', 'Precio'],
                fill='toself',
                name=colonia['colonia'],
                line=dict(color=colors[idx])
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Call to action
        if hasattr(st.session_state, 'demo_mode') and st.session_state.demo_mode:
            st.success(f"🎉 ¡Demo completado! Recomendaciones para {st.session_state.demo_case['name']} generadas en menos de 60 segundos.")
        else:
            st.success("🎉 ¡Listo! Estas son nuestras recomendaciones personalizadas para ti.")
        
        if hasattr(st.session_state, 'demo_mode') and st.session_state.demo_mode:
            # Opciones específicas para modo demo
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🚀 Probar otro caso"):
                    st.session_state.demo_mode = False
                    st.session_state.search_done = False
                    if 'demo_case' in st.session_state:
                        del st.session_state.demo_case
                    st.rerun()
            with col2:
                if st.button("👤 Personalizar"):
                    st.session_state.demo_mode = False
                    st.session_state.search_done = False
                    if 'demo_case' in st.session_state:
                        del st.session_state.demo_case
                    st.info("👈 Ahora puedes personalizar tu búsqueda en la barra lateral")
                    st.rerun()
            with col3:
                if st.button("📊 Ver más detalles"):
                    st.info("Todos los detalles están desplegados arriba. Scroll hacia arriba para ver análisis completo.")
        else:
            # Opciones normales
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📧 Recibir por email"):
                    st.info("Funcionalidad próximamente")
            with col2:
                if st.button("📱 Compartir"):
                    st.info("Funcionalidad próximamente")  
            with col3:
                if st.button("🔄 Nueva búsqueda"):
                    st.session_state.search_done = False
                    st.rerun()
    
    else:
        # LANDING PAGE CINEMATOGRÁFICA
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
            
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            
            @keyframes countUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes slideInLeft {
                from { opacity: 0; transform: translateX(-50px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            @keyframes slideInRight {
                from { opacity: 0; transform: translateX(50px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            .hero-container {
                background: linear-gradient(135deg, 
                    #667eea 0%, 
                    #764ba2 25%, 
                    #f093fb 50%, 
                    #f5576c 75%, 
                    #4facfe 100%);
                background-size: 400% 400%;
                animation: gradientShift 8s ease infinite;
                padding: 4rem 2rem;
                text-align: center;
                border-radius: 20px;
                margin-bottom: 3rem;
                position: relative;
                overflow: hidden;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .hero-container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.1);
                backdrop-filter: blur(1px);
            }
            
            .hero-content {
                position: relative;
                z-index: 2;
            }
            
            .hero-title {
                font-family: 'Inter', sans-serif;
                font-size: 4rem;
                font-weight: 800;
                color: white;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                animation: fadeInUp 1s ease-out;
                line-height: 1.1;
            }
            
            .hero-subtitle {
                font-family: 'Inter', sans-serif;
                font-size: 1.5rem;
                font-weight: 300;
                color: rgba(255,255,255,0.9);
                margin-bottom: 2rem;
                animation: fadeInUp 1s ease-out 0.3s both;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            
            .stats-container {
                display: flex;
                justify-content: center;
                gap: 3rem;
                margin: 2rem 0;
                animation: fadeInUp 1s ease-out 0.6s both;
            }
            
            .stat-item {
                text-align: center;
                color: white;
            }
            
            .stat-number {
                font-family: 'Inter', sans-serif;
                font-size: 2.5rem;
                font-weight: 700;
                display: block;
                animation: countUp 1s ease-out 1s both;
            }
            
            .stat-label {
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                opacity: 0.8;
                font-weight: 400;
            }
            
            .demo-buttons-container {
                margin: 3rem 0;
                animation: fadeInUp 1s ease-out 0.9s both;
            }
            
            .demo-button {
                display: inline-block;
                margin: 0.5rem;
                padding: 1rem 2rem;
                background: linear-gradient(45deg, #FF6B6B, #FF8E53);
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-family: 'Inter', sans-serif;
                font-weight: 600;
                font-size: 1.1rem;
                border: none;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 8px 25px rgba(255,107,107,0.3);
            }
            
            .demo-button:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 35px rgba(255,107,107,0.4);
                animation: pulse 0.6s ease-in-out;
            }
            
            .demo-button:active {
                transform: translateY(-1px);
            }
            
            .features-section {
                margin: 4rem 0;
            }
            
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-top: 2rem;
            }
            
            .feature-card {
                background: white;
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                border: 1px solid rgba(0,0,0,0.05);
                position: relative;
                overflow: hidden;
            }
            
            .feature-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, #FF6B6B, #4FACFE);
            }
            
            .feature-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.15);
            }
            
            .feature-card:nth-child(1) {
                animation: slideInLeft 1s ease-out 1.2s both;
            }
            
            .feature-card:nth-child(2) {
                animation: fadeInUp 1s ease-out 1.4s both;
            }
            
            .feature-card:nth-child(3) {
                animation: slideInRight 1s ease-out 1.6s both;
            }
            
            .feature-icon {
                font-size: 3rem;
                margin-bottom: 1rem;
                display: block;
            }
            
            .feature-title {
                font-family: 'Inter', sans-serif;
                font-size: 1.4rem;
                font-weight: 700;
                color: #333;
                margin-bottom: 1rem;
            }
            
            .feature-description {
                font-family: 'Inter', sans-serif;
                color: #666;
                line-height: 1.6;
                font-size: 1rem;
            }
            
            .section-title {
                font-family: 'Inter', sans-serif;
                font-size: 2.5rem;
                font-weight: 700;
                text-align: center;
                color: #333;
                margin-bottom: 1rem;
                animation: fadeInUp 1s ease-out 0.8s both;
            }
            
            .section-subtitle {
                font-family: 'Inter', sans-serif;
                font-size: 1.2rem;
                text-align: center;
                color: #666;
                margin-bottom: 2rem;
                animation: fadeInUp 1s ease-out 1s both;
            }
            
            @media (max-width: 768px) {
                .hero-title {
                    font-size: 2.5rem;
                }
                
                .hero-subtitle {
                    font-size: 1.2rem;
                }
                
                .stats-container {
                    flex-direction: column;
                    gap: 1rem;
                }
                
                .demo-button {
                    display: block;
                    margin: 0.5rem auto;
                    width: 80%;
                    text-align: center;
                }
                
                .feature-card {
                    animation: fadeInUp 1s ease-out 0.5s both !important;
                }
            }
        </style>
        
        <!-- HERO SECTION -->
        <div class="hero-container">
            <div class="hero-content">
                <h1 class="hero-title">CasaMX</h1>
                <p class="hero-subtitle">
                    Tu hogar ideal en México está a un clic de distancia.<br>
                    IA personalizada para extranjeros que buscan el lugar perfecto para vivir.
                </p>
                
                <div class="stats-container">
                    <div class="stat-item">
                        <span class="stat-number">2.1M+</span>
                        <span class="stat-label">Extranjeros en México</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">150+</span>
                        <span class="stat-label">Zonas analizadas</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">&lt;3seg</span>
                        <span class="stat-label">Tiempo de respuesta</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # DEMO BUTTONS SECTION
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <h2 style="font-family: 'Inter', sans-serif; font-size: 2.2rem; font-weight: 700; color: #333; margin-bottom: 1rem;">
                ✨ Prueba una Demo Instantánea
            </h2>
            <p style="font-family: 'Inter', sans-serif; font-size: 1.1rem; color: #666; margin-bottom: 2rem;">
                Casos reales de extranjeros que encontraron su hogar ideal
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Crear botones demo con casos predefinidos
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👨‍👩‍👧‍👦 Demo: Familia con niños", 
                        key="demo_familia",
                        help="Caso: María (España) + 2 hijos, busca seguridad y escuelas"):
                # Configurar caso María España
                st.session_state.update({
                    'demo_case': 'familia',
                    'presupuesto': 25000,
                    'familia_size': 4,
                    'tiene_hijos': True,
                    'prioridad_seguridad': 10,
                    'prioridad_transporte': 7,
                    'prioridad_precio': 6,
                    'prioridad_amenidades': 9,
                    'trabajo_zona': 'Polanco',
                    'estilo_vida': 'Familiar',
                    'search_done': True
                })
                st.rerun()
        
        with col2:
            if st.button("💻 Demo: Joven profesional",
                        key="demo_profesional", 
                        help="Caso: Alex (Italia), tech, vida nocturna"):
                # Configurar caso Alex Italia
                st.session_state.update({
                    'demo_case': 'profesional',
                    'presupuesto': 18000,
                    'familia_size': 1,
                    'tiene_hijos': False,
                    'prioridad_seguridad': 7,
                    'prioridad_transporte': 9,
                    'prioridad_precio': 8,
                    'prioridad_amenidades': 10,
                    'trabajo_zona': 'Santa Fe',
                    'estilo_vida': 'Joven profesional',
                    'search_done': True
                })
                st.rerun()
        
        with col3:
            if st.button("🎓 Demo: Estudiante",
                        key="demo_estudiante",
                        help="Caso: Sophie (Francia), universidad, presupuesto ajustado"):
                # Configurar caso Sophie Francia  
                st.session_state.update({
                    'demo_case': 'estudiante',
                    'presupuesto': 12000,
                    'familia_size': 1,
                    'tiene_hijos': False,
                    'prioridad_seguridad': 8,
                    'prioridad_transporte': 10,
                    'prioridad_precio': 10,
                    'prioridad_amenidades': 6,
                    'trabajo_zona': 'Centro',
                    'estilo_vida': 'Estudiante',
                    'search_done': True
                })
                st.rerun()
        
        # FEATURES SECTION
        st.markdown("""
        <div class="features-section">
            <h2 class="section-title">¿Por qué elegir CasaMX?</h2>
            <p class="section-subtitle">Tecnología avanzada al servicio de tu nueva vida en México</p>
            
            <div class="features-grid">
                <div class="feature-card">
                    <span class="feature-icon">🤖</span>
                    <h3 class="feature-title">IA Personalizada</h3>
                    <p class="feature-description">
                        Algoritmo inteligente que aprende de tus preferencias específicas como extranjero. 
                        Considera cultura, idioma y necesidades únicas de adaptación.
                    </p>
                </div>
                
                <div class="feature-card">
                    <span class="feature-icon">📊</span>
                    <h3 class="feature-title">6 Fuentes de Datos</h3>
                    <p class="feature-description">
                        Información en tiempo real: seguridad, precios, transporte, servicios, 
                        calidad de vida y comunidad internacional.
                    </p>
                </div>
                
                <div class="feature-card">
                    <span class="feature-icon">🗺️</span>
                    <h3 class="feature-title">Mapas Interactivos</h3>
                    <p class="feature-description">
                        Visualización avanzada con análisis de proximidad, rutas optimizadas 
                        y puntos de interés relevantes para extranjeros.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # CALL TO ACTION ALTERNATIVO
        st.markdown("""
        <div style="text-align: center; margin: 4rem 0 2rem 0; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 20px;">
            <h3 style="font-family: 'Inter', sans-serif; font-size: 1.8rem; font-weight: 600; color: #333; margin-bottom: 1rem;">
                ¿Prefieres una búsqueda personalizada?
            </h3>
            <p style="font-family: 'Inter', sans-serif; font-size: 1.1rem; color: #666; margin-bottom: 1.5rem;">
                👈 Completa el formulario en la barra lateral para obtener recomendaciones 100% adaptadas a ti
            </p>
            <div style="font-size: 0.9rem; color: #888;">
                ⏱️ Toma menos de 2 minutos • 🎯 Resultados instantáneos • 🔒 Información privada
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("**CasaMX** - Datatón ITAM 2025 | Desarrollado por David Fernando Ávila Díaz")

if __name__ == "__main__":
    main()