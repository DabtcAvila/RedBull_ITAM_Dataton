#!/usr/bin/env python3
"""
CasaMX - Sistema de Casos Demo Pre-cargados
Datatón ITAM 2025 - David Fernando Ávila Díaz

Sistema para presentaciones fluidas de 10 minutos con casos pre-configurados.
"""

import streamlit as st

def load_demo_case(case_name):
    """
    Carga un caso demo específico y configura todos los parámetros necesarios
    
    Args:
        case_name (str): Nombre del caso ('maria', 'alex', 'sophie')
    """
    
    cases = {
        'maria': {
            'name': 'María González',
            'country': 'España 🇪🇸',
            'description': 'Familia española con niños - Busca seguridad y educación',
            'presupuesto': 38000,  # Updated for 2025
            'familia_size': 4,
            'tiene_hijos': True,
            'prioridad_seguridad': 9,  # Máxima prioridad
            'prioridad_transporte': 6,
            'prioridad_precio': 5,
            'prioridad_amenidades': 8,  # Escuelas importantes
            'trabajo_zona': 'Polanco',
            'estilo_vida': 'Familiar',
            'profile': {
                'age': '35 años',
                'occupation': 'Directora de Marketing Internacional',
                'family': 'Esposo + 2 niños (8 y 12 años)',
                'priorities': 'Seguridad máxima y escuelas bilingües de calidad',
                'expected_areas': 'Del Valle Centro o Coyoacán (zonas familiares seguras)',
                'story': 'María se mudó a México por trabajo. Su prioridad #1 es la seguridad de sus hijos y encontrar escuelas bilingües de calidad.'
            }
        },
        
        'alex': {
            'name': 'Alessandro Romano',
            'country': 'Italia 🇮🇹',
            'description': 'Joven profesional tech italiano - Busca networking y vida social',
            'presupuesto': 28000,  # Updated for 2025
            'familia_size': 1,
            'tiene_hijos': False,
            'prioridad_seguridad': 7,
            'prioridad_transporte': 9,  # Quiere caminar al trabajo
            'prioridad_precio': 6,
            'prioridad_amenidades': 9,  # Vida nocturna y restaurantes
            'trabajo_zona': 'Roma Norte',
            'estilo_vida': 'Joven profesional',
            'profile': {
                'age': '28 años',
                'occupation': 'Software Engineer en startup',
                'family': 'Soltero, busca comunidad de expatriados',
                'priorities': 'Conveniencia de transporte, vida nocturna vibrante y networking',
                'expected_areas': 'Roma Norte (ideal), Condesa o Hipódromo',
                'story': 'Alessandro trabaja en una startup tech en Roma Norte. Quiere vivir donde pueda caminar al trabajo y disfrutar la mejor vida nocturna de CDMX.'
            }
        },
        
        'sophie': {
            'name': 'Sophie Dubois',
            'country': 'Francia 🇫🇷',
            'description': 'Estudiante francesa de intercambio - Presupuesto limitado, máxima experiencia',
            'presupuesto': 18000,  # Updated for 2025 inflation
            'familia_size': 1,
            'tiene_hijos': False,
            'prioridad_seguridad': 6,  # Moderada
            'prioridad_transporte': 9,  # Esencial para estudiante
            'prioridad_precio': 9,  # Máxima prioridad
            'prioridad_amenidades': 7,  # Quiere vida cultural
            'trabajo_zona': 'Centro',  # Universidad/Centro de estudios
            'estilo_vida': 'Estudiante',
            'profile': {
                'age': '22 años',
                'occupation': 'Estudiante de Intercambio en UNAM/ITAM',
                'family': 'Soltera, busca experiencia auténtica mexicana',
                'priorities': 'Maximizar presupuesto limitado con excelente transporte público',
                'expected_areas': 'Doctores (muy económico), Narvarte o zonas cercanas a Ciudad Universitaria',
                'story': 'Sophie está en intercambio académico por 1 año. Con presupuesto de estudiante, necesita zona bien conectada que le permita explorar toda la ciudad.'
            }
        }
    }
    
    if case_name not in cases:
        st.error(f"Caso '{case_name}' no encontrado")
        return False
    
    case = cases[case_name]
    
    # Configurar todos los session_state necesarios
    st.session_state.demo_mode = True
    st.session_state.demo_case = case
    st.session_state.search_done = True
    
    # Configurar parámetros del formulario
    st.session_state.presupuesto = case['presupuesto']
    st.session_state.familia_size = case['familia_size']
    st.session_state.tiene_hijos = case['tiene_hijos']
    st.session_state.prioridad_seguridad = case['prioridad_seguridad']
    st.session_state.prioridad_transporte = case['prioridad_transporte']
    st.session_state.prioridad_precio = case['prioridad_precio']
    st.session_state.prioridad_amenidades = case['prioridad_amenidades']
    st.session_state.trabajo_zona = case['trabajo_zona']
    st.session_state.estilo_vida = case['estilo_vida']
    
    return True

def show_demo_selector():
    """
    Muestra los botones de selección de casos demo en la página principal
    """
    st.markdown("---")
    st.header("🚀 Casos Demo para Presentación")
    st.markdown("*Selecciona un caso para ver recomendaciones instantáneas - Perfect for 10-minute demos!*")
    
    # Mostrar tiempo estimado
    st.info("⏱️ **Cada caso toma 45-60 segundos** | 🎯 **Resultados instantáneos sin formularios** | 🌍 **3 perfiles internacionales únicos**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **👩‍👧‍👦 CASO MARÍA**
        - **País:** España 🇪🇸
        - **Familia:** 4 personas
        - **Presupuesto:** $35,000 MXN
        - **Prioridad:** Seguridad y escuelas
        - **Trabajo:** Polanco
        """)
        if st.button("🎯 Ver Caso María", key="maria_btn", type="primary"):
            if load_demo_case('maria'):
                st.rerun()
    
    with col2:
        st.markdown("""
        **👨‍💻 CASO ALEX**
        - **País:** Italia 🇮🇹
        - **Familia:** Soltero (28 años)
        - **Presupuesto:** $25,000 MXN
        - **Prioridad:** Transporte y vida nocturna
        - **Trabajo:** Roma Norte
        """)
        if st.button("🎯 Ver Caso Alex", key="alex_btn", type="primary"):
            if load_demo_case('alex'):
                st.rerun()
    
    with col3:
        st.markdown("""
        **👩‍🎓 CASO SOPHIE**
        - **País:** Francia 🇫🇷
        - **Familia:** Soltera (22 años)
        - **Presupuesto:** $15,000 MXN
        - **Prioridad:** Precio y transporte
        - **Trabajo:** Centro (Universidad)
        """)
        if st.button("🎯 Ver Caso Sophie", key="sophie_btn", type="primary"):
            if load_demo_case('sophie'):
                st.rerun()

def show_demo_profile():
    """
    Muestra el perfil del caso demo activo en la sidebar
    """
    if hasattr(st.session_state, 'demo_mode') and st.session_state.demo_mode:
        case = st.session_state.demo_case
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🎭 MODO DEMO")
        st.sidebar.success(f"**Caso Activo:** {case['name']}")
        
        st.sidebar.markdown(f"""
        **👤 Perfil:**
        - **Edad:** {case['profile']['age']}
        - **Ocupación:** {case['profile']['occupation']}
        - **Familia:** {case['profile']['family']}
        - **País:** {case['country']} 
        
        **🎯 Prioridades:**
        {case['profile']['priorities']}
        
        **📍 Zonas Esperadas:**
        {case['profile']['expected_areas']}
        """)
        
        if st.sidebar.button("🚪 Salir del Demo", key="exit_demo"):
            st.session_state.demo_mode = False
            st.session_state.search_done = False
            if 'demo_case' in st.session_state:
                del st.session_state.demo_case
            st.rerun()

def get_demo_insights(case_name):
    """
    Retorna insights específicos para cada caso demo
    
    Args:
        case_name (str): Nombre del caso
        
    Returns:
        dict: Insights del caso
    """
    
    insights = {
        'maria': {
            'key_finding': "Familia española prioriza seguridad y educación",
            'recommendation_reason': "Del Valle y Coyoacán ofrecen el equilibrio perfecto entre seguridad, proximidad a buenas escuelas y precio razonable para una familia de 4 personas.",
            'cultural_fit': "Las zonas recomendadas tienen una fuerte comunidad internacional y ambiente familiar.",
            'budget_analysis': "Con $35,000 MXN puede acceder a departamentos de 80-100m² en zonas seguras.",
            'commute_impact': "Desde Del Valle/Coyoacán a Polanco: 35-50 min en transporte público."
        },
        
        'alex': {
            'key_finding': "Profesional tech italiano busca conveniencia y vida social",
            'recommendation_reason': "Roma Norte y Condesa son perfectas para un joven profesional: excelente conectividad, vida nocturna vibrante y proximidad al trabajo.",
            'cultural_fit': "Ambas zonas tienen alta concentración de expatriados y profesionistas jóvenes.",
            'budget_analysis': "Con $25,000 MXN puede acceder a estudios o departamentos de 1 recámara en las mejores zonas.",
            'commute_impact': "Desde Roma Norte: caminando al trabajo. Excelente conectividad con toda la ciudad."
        },
        
        'sophie': {
            'key_finding': "Estudiante francesa necesita maximizar presupuesto limitado",
            'recommendation_reason': "Narvarte ofrece la mejor relación precio-calidad con excelente transporte público para llegar al Centro donde estudia.",
            'cultural_fit': "Zona con buena oferta cultural y muchos estudiantes internacionales.",
            'budget_analysis': "Con $15,000 MXN puede acceder a cuartos compartidos o estudios pequeños bien ubicados.",
            'commute_impact': "Desde Narvarte al Centro: 25 min en Metro línea 9 o metrobús."
        }
    }
    
    return insights.get(case_name, {})

def enhance_results_with_demo_context(top_recommendations, case_name):
    """
    Enriquece los resultados con contexto específico del caso demo
    
    Args:
        top_recommendations: DataFrame con las recomendaciones
        case_name: Nombre del caso activo
        
    Returns:
        dict: Contexto adicional para mostrar
    """
    
    insights = get_demo_insights(case_name)
    case = st.session_state.demo_case
    
    # Análisis específico basado en las recomendaciones obtenidas
    context = {
        'insights': insights,
        'case_profile': case['profile'],
        'success_metrics': {
            'budget_fit': "✅ Dentro del presupuesto" if top_recommendations.iloc[0]['precio_renta_m2'] * 50 <= case['presupuesto'] * 1.1 else "⚠️ Ligeramente sobre presupuesto",
            'commute_score': f"🚗 Tiempo de traslado promedio: {_calculate_avg_commute(top_recommendations, case['trabajo_zona'])} min",
            'priority_match': f"🎯 Match con prioridades: {_calculate_priority_match(top_recommendations, case)}%"
        }
    }
    
    return context

def _calculate_avg_commute(recommendations, trabajo_zona):
    """Calcula el tiempo promedio de traslado"""
    zona_key_map = {
        'Centro': 'tiempo_centro',
        'Polanco': 'tiempo_polanco',
        'Santa Fe': 'tiempo_santa_fe',
        'Roma Norte': 'tiempo_centro'  # Aproximación
    }
    
    key = zona_key_map.get(trabajo_zona, 'tiempo_centro')
    return int(recommendations[key].mean())

def _calculate_priority_match(recommendations, case):
    """Calcula qué tan bien matchean las recomendaciones con las prioridades"""
    top_rec = recommendations.iloc[0]
    
    # Obtener las prioridades más altas del usuario
    priorities = {
        'seguridad': case['prioridad_seguridad'],
        'transporte': case['prioridad_transporte'],
        'precio': case['prioridad_precio'],
        'amenidades': case['prioridad_amenidades']
    }
    
    # Obtener los scores de la recomendación top
    scores = {
        'seguridad': top_rec['score_seguridad'],
        'transporte': top_rec['score_transporte'],
        'precio': top_rec['score_precio'],
        'amenidades': top_rec['score_amenidades']
    }
    
    # Calcular match ponderado
    total_match = 0
    total_weight = 0
    
    for category, user_priority in priorities.items():
        weight = user_priority / 10.0
        match = (scores[category] / 100.0) * weight
        total_match += match
        total_weight += weight
    
    return int((total_match / total_weight) * 100)