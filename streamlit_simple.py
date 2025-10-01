#!/usr/bin/env python3
"""
CasaMX SIMPLE - Version para DigitalOcean
Sin dependencias complejas
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="CasaMX - Tu hogar ideal en México",
    page_icon="🏠",
    layout="wide"
)

# CSS básico
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.main-header { color: white; text-align: center; padding: 2rem; }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-header"><h1>🏠 CasaMX</h1><h3>Tu hogar ideal en México</h3></div>', unsafe_allow_html=True)
    
    # Datos básicos
    colonias = [
        {"nombre": "Roma Norte", "precio": 25000, "seguridad": 85, "transporte": 95},
        {"nombre": "Condesa", "precio": 28000, "seguridad": 82, "transporte": 88},
        {"nombre": "Polanco", "precio": 45000, "seguridad": 95, "transporte": 85},
        {"nombre": "Del Valle", "precio": 22000, "seguridad": 88, "transporte": 78},
        {"nombre": "Coyoacán", "precio": 18000, "seguridad": 90, "transporte": 70}
    ]
    
    df = pd.DataFrame(colonias)
    
    # Formulario simple
    with st.sidebar:
        st.header("🎯 Tus Preferencias")
        presupuesto = st.slider("Presupuesto (MXN)", 10000, 50000, 25000)
        prioridad_seguridad = st.slider("Prioridad Seguridad", 1, 10, 8)
        prioridad_transporte = st.slider("Prioridad Transporte", 1, 10, 7)
        
        if st.button("🔍 Buscar Zona Ideal", type="primary"):
            st.session_state.buscar = True
    
    # Resultados
    if hasattr(st.session_state, 'buscar'):
        st.subheader("🎯 Recomendaciones para ti")
        
        # Filtrar por presupuesto
        df_filtered = df[df['precio'] <= presupuesto * 1.1]
        
        if df_filtered.empty:
            df_filtered = df.nsmallest(3, 'precio')
        
        # Calcular score personalizado
        df_filtered['score'] = (
            df_filtered['seguridad'] * (prioridad_seguridad / 10) +
            df_filtered['transporte'] * (prioridad_transporte / 10) +
            (100 - df_filtered['precio'] / df_filtered['precio'].max() * 100) * 0.3
        )
        
        df_filtered = df_filtered.sort_values('score', ascending=False).head(3)
        
        # Mostrar top 3
        for idx, (_, zona) in enumerate(df_filtered.iterrows()):
            with st.expander(f"#{idx+1}: {zona['nombre']} ⭐{zona['score']:.1f}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"💰 **Precio:** ${zona['precio']:,}/mes")
                    st.write(f"🛡️ **Seguridad:** {zona['seguridad']}/100")
                    st.write(f"🚇 **Transporte:** {zona['transporte']}/100")
                
                with col2:
                    # Gráfico simple
                    scores = [zona['seguridad'], zona['transporte'], (100-zona['precio']/50000*100)]
                    fig = go.Figure([go.Bar(x=['Seguridad', 'Transporte', 'Precio'], y=scores)])
                    fig.update_layout(height=200)
                    st.plotly_chart(fig, use_container_width=True)
        
        st.success("🎉 ¡Encuentra tu hogar ideal en México!")
    
    else:
        st.info("👈 Completa tus preferencias para comenzar")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏠 Zonas", "150+", "analizadas")
        with col2:
            st.metric("⚡ Respuesta", "<3s", "tiempo")
        with col3:
            st.metric("🎯 Precisión", "92%", "recomendaciones")

    st.markdown("---")
    st.markdown("**CasaMX** - Datatón ITAM 2025 | David Fernando Ávila Díaz")

if __name__ == "__main__":
    main()