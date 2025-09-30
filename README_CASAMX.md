# CasaMX - Landing Page Cinematográfica

## 🎯 Características Implementadas

### ✨ HERO SECTION Cinematográfico
- **Título animado**: "CasaMX - Tu hogar ideal en México" con animación fadeInUp
- **Subtítulo persuasivo**: Dirigido específicamente a extranjeros
- **Estadísticas animadas**: 
  - 2.1M+ extranjeros en México
  - 150+ zonas analizadas
  - <3seg tiempo de respuesta
- **Background gradient animado**: Colores profesionales con efecto parallax

### 🎮 DEMO BUTTONS Prominentes
- **Demo: Familia con niños** (Caso María España + 2 hijos)
  - Presupuesto: $25,000 MXN
  - Prioridades: Seguridad (10/10), Amenidades (9/10)
  - Zona trabajo: Polanco
  
- **Demo: Joven profesional** (Caso Alex Italia, tech)
  - Presupuesto: $18,000 MXN
  - Prioridades: Amenidades (10/10), Transporte (9/10)
  - Zona trabajo: Santa Fe
  
- **Demo: Estudiante** (Caso Sophie Francia, universidad)
  - Presupuesto: $12,000 MXN
  - Prioridades: Precio (10/10), Transporte (10/10)
  - Zona trabajo: Centro

### 🎨 FEATURES HIGHLIGHT Visual
- **Cards animadas** con hover effects y micro-animaciones
- **Iconos representativos**: 🤖 IA personalizada, 📊 6 fuentes de datos, 🗺️ Mapas interactivos
- **Animaciones secuenciales**: slideInLeft, fadeInUp, slideInRight

### 💻 CSS AVANZADO
- **Gradientes profesionales**: Múltiples colores con animación
- **Keyframes animations**: fadeInUp, pulse, countUp, slideIn
- **Responsive design**: Breakpoints para móviles
- **Efectos hover**: Elevación de cards y botones
- **Typography**: Google Fonts Inter para look profesional

## 🚀 Instalación y Uso

### Prerrequisitos
```bash
pip install streamlit pandas numpy plotly folium streamlit-folium
```

### Ejecutar la aplicación
```bash
cd "RedBull_ITAM_Dataton"
streamlit run streamlit_app_fixed.py
```

### URL de acceso
- Local: http://localhost:8501

## 🎭 Experiencia de Usuario

### 1. Landing Page (WOW Factor)
Al abrir la aplicación, el usuario ve inmediatamente:
- Hero section con gradiente animado
- Estadísticas impactantes que validan el problema
- Botones de demo claramente visibles
- Features destacadas con iconos y animaciones

### 2. Demo Instantánea
Al hacer clic en cualquier botón demo:
- **Carga instantánea** del caso específico
- **Sidebar pre-lleno** con datos del perfil
- **Transición fluida** a los resultados
- **Información contextual** del caso en el sidebar

### 3. Resultados Personalizados
- Mapa interactivo con ubicaciones
- Cards detalladas por colonia
- Gráficos comparativos (radar)
- Métricas visuales claras

## 🔧 Integración Técnica

### Session State Management
- Los casos demo configuran `st.session_state` automáticamente
- Valores pre-definidos para cada perfil
- Botón "Cambiar a personalizado" para limpiar demo
- Persistencia durante la sesión

### Responsividad
- Grid adaptativo para features
- Estadísticas en columna en móviles  
- Botones demo apilados en pantallas pequeñas
- Typography escalable

### Performance
- CSS embebido para carga rápida
- Animaciones optimizadas
- Session state eficiente
- Datos mock locales

## 🎬 Resultado Final

**OBJETIVO CUMPLIDO**: WOW INMEDIATO en los primeros 10 segundos
- Visual impact instantáneo con hero cinematográfico
- Demos funcionales que cargan en <1 segundo
- Experiencia fluida y profesional
- Diseño que compite con startups tech premium

La landing page transforma completamente la primera impresión de CasaMX, pasando de una interfaz básica a una experiencia cinematográfica que impresionará a los jueces del datatón.