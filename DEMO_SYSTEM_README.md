# 🚀 CasaMX - Sistema de Casos Demo

Sistema de casos demo pre-cargados para presentaciones fluidas de **10 minutos** en el Datatón ITAM 2025.

## 🎯 Casos de Demo Implementados

### 1. 👩‍👧‍👦 CASO MARÍA (Familia Española)
- **Presupuesto:** $35,000 MXN
- **Familia:** 4 personas (pareja + 2 niños de 8 y 12 años)
- **País:** España 🇪🇸
- **Prioridades:** Seguridad (9), Escuelas (9), Transporte (7)
- **Trabajo:** Polanco
- **Resultado Esperado:** Del Valle o Coyoacán
- **Perfil:** Directora de Marketing, busca zonas seguras con buenas escuelas

### 2. 👨‍💻 CASO ALEX (Profesional Tech Italiano)
- **Presupuesto:** $25,000 MXN
- **Familia:** Soltero, 28 años
- **País:** Italia 🇮🇹
- **Prioridades:** Transporte (9), Vida nocturna (8), Precio (6)
- **Trabajo:** Roma Norte
- **Resultado Esperado:** Roma Norte o Condesa
- **Perfil:** Software Engineer, busca conveniencia y vida social

### 3. 👩‍🎓 CASO SOPHIE (Estudiante Francesa)
- **Presupuesto:** $15,000 MXN
- **Familia:** Soltera, 22 años
- **País:** Francia 🇫🇷
- **Prioridades:** Precio (9), Transporte (8), Amenidades (6)
- **Trabajo:** Centro (Universidad)
- **Resultado Esperado:** Narvarte o zonas económicas
- **Perfil:** Estudiante de intercambio, presupuesto ajustado

## 🎬 Cómo Usar para Presentación

### Inicio Rápido
```bash
./run_casamx_demo.sh
```

### Flujo de Demo (45-60 segundos por caso)
1. **Abrir aplicación** → Mostrar landing page
2. **Seleccionar caso demo** → Click en botón del caso
3. **Mostrar resultados instantáneos** → Sin llenar formularios
4. **Explicar análisis personalizado** → Insights específicos del caso
5. **Navegar por recomendaciones** → Mapas, scores, pros/contras
6. **Cambiar al siguiente caso** → Button "Probar otro caso"

### Timing de Presentación
- **Introducción:** 30 segundos
- **Caso María:** 2 minutos
- **Caso Alex:** 2 minutos  
- **Caso Sophie:** 2 minutos
- **Funcionalidades adicionales:** 2 minutos
- **Q&A y cierre:** 1.5 minutos
- **Total:** 10 minutos

## 📁 Archivos del Sistema

### Archivos Principales
- `demo_cases.py` - Lógica principal de casos demo
- `streamlit_app_fixed.py` - Aplicación principal integrada
- `run_casamx_demo.sh` - Script de inicio rápido
- `test_demo_cases.py` - Tests de verificación

### Funciones Clave
- `load_demo_case(case_name)` - Carga caso específico
- `show_demo_selector()` - Muestra botones de selección
- `show_demo_profile()` - Perfil en sidebar
- `enhance_results_with_demo_context()` - Análisis personalizado

## 🎨 Características del Demo

### ✅ Ventajas Implementadas
- **Instantáneo** - Sin formularios, resultados inmediatos
- **Personalizado** - Análisis específico para cada persona
- **Convincente** - Resultados diferentes y realistas para cada caso
- **Fluido** - Navegación sin interrupciones
- **Professional** - Interface pulida para presentaciones

### 🔧 Funcionalidades Demo
- **Casos pre-cargados** con perfiles completos
- **Sidebar informativos** mostrando configuración
- **Análisis específicos** para cada tipo de usuario
- **Métricas de éxito** personalizadas
- **Insights culturales** para expatriados
- **Botones específicos** para navegación de demo

## 🚀 Instrucciones de Presentación

### Preparación
1. Ejecutar `./run_casamx_demo.sh`
2. Verificar que se abre en `http://localhost:8501`
3. Preparar slides de introducción (opcional)

### Durante la Demo
1. **Mostrar landing page** → Explicar concepto general
2. **Caso María** → "Familia europea buscando seguridad"
3. **Caso Alex** → "Joven profesional, vida social activa"  
4. **Caso Sophie** → "Estudiante, presupuesto limitado"
5. **Mostrar personalización** → Salir de demo y mostrar formulario

### Tips de Presentación
- **Resaltar la velocidad** → "Resultados en menos de 60 segundos"
- **Explicar personalización** → Algoritmo aprende de preferencias
- **Mostrar mapas interactivos** → Navegación visual
- **Destacar insights culturales** → Fit para expatriados
- **Demostrar diferencias** → Cada caso tiene resultados únicos

## 🔍 Resolución de Problemas

### Si no funcionan los imports:
```bash
source casamx_env/bin/activate
pip install streamlit pandas plotly folium streamlit-folium
```

### Si no se muestran los casos:
- Verificar que `demo_cases.py` está en el directorio correcto
- Revisar que las funciones se importan correctamente
- Comprobar que no hay errores en la consola

### Para debug:
```bash
python test_demo_cases.py
```

## 📊 Métricas de Éxito

- ✅ Cada caso toma 45-60 segundos en mostrar
- ✅ Resultados convincentes y diferentes para cada persona
- ✅ Sin necesidad de llenar formularios manualmente
- ✅ Interface fluida sin interrupciones
- ✅ Análisis personalizado para cada tipo de usuario
- ✅ Navegación intuitiva entre casos

---

**Desarrollado para el Datatón ITAM 2025**  
**David Fernando Ávila Díaz**  
**CasaMX - Tu hogar ideal en México**