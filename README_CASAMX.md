# 🏠 CasaMX - Sistema de Análisis de Vivienda para CDMX

**Desarrollado por:** David Fernando Ávila Díaz  
**Institución:** Instituto Tecnológico Autónomo de México (ITAM)  
**Carrera:** Ciencia de Datos  
**Proyecto:** Datatón ITAM 2025

---

## 🎯 Descripción General

CasaMX es un sistema inteligente de análisis de datos de vivienda diseñado específicamente para la Ciudad de México. El proyecto combina análisis de datos avanzado, APIs web, y visualizaciones interactivas para proporcionar insights sobre el mercado inmobiliario de la capital mexicana.

## 🚀 Instalación Rápida

### Opción 1: Setup Automático (Recomendado)

```bash
# Clonar o descargar el proyecto
cd "RedBull_ITAM_Dataton"

# Ejecutar el setup rápido
python3 setup_quick.py
```

### Opción 2: Con Entorno Virtual

```bash
# Ejecutar script de instalación
chmod +x install_dependencies.sh
./install_dependencies.sh

# Activar entorno virtual
source venv/bin/activate
```

### Opción 3: Manual

```bash
# Instalar dependencias críticas
pip3 install pandas numpy fastapi uvicorn plotly folium sqlite3

# Crear estructura
python3 setup_quick.py
```

## 📊 Datos Incluidos

### Dataset Mock Realista (20 Colonias de CDMX)

Colonias incluidas con datos completos:
- **Premium:** Polanco, Santa Fe, Pedregal de San Ángel
- **Alto:** Roma Norte, Condesa, Anzures, Hipódromo
- **Medio-Alto:** Del Valle, Coyoacán, San Ángel, Juárez
- **Medio:** Narvarte, Escandón, Álamos, Portales, Tlalpan
- **Accesible:** Doctores, Lindavista, Xochimilco, Magdalena Contreras

### Información por Colonia

```json
{
  "scores": {
    "seguridad": 8.5,
    "transporte": 9.0,
    "amenidades": 9.2,
    "precio": 5.8
  },
  "precios": {
    "renta_m2": 380,
    "venta_m2": 58000,
    "renta_1br": 18000,
    "renta_2br": 28000,
    "renta_3br": 42000
  },
  "servicios": {
    "hospitales": ["Hospital Español", "Hospital de la Mujer"],
    "escuelas": ["Colegio Franco Inglés", "UNAM"],
    "restaurantes": 380
  },
  "transporte": {
    "metro_cercano": "Insurgentes",
    "distancia_metro": 0.6,
    "metrobus": ["Línea 1", "Línea 3"]
  }
}
```

## 🛠️ Uso del Sistema

### 1. Iniciar API

```bash
# Desde el directorio del proyecto
python src/api/main.py

# O con activación de entorno virtual
source venv/bin/activate
python src/api/main.py
```

### 2. Acceder a la API

- **API:** http://localhost:8000
- **Documentación:** http://localhost:8000/docs
- **Endpoints principales:**
  - `GET /` - Estado de la API
  - `GET /colonias` - Todas las colonias
  - `GET /colonias/{id}` - Colonia específica
  - `GET /search` - Búsqueda con filtros

### 3. Ejemplos de Consultas

```bash
# Obtener todas las colonias
curl http://localhost:8000/colonias

# Buscar por alcaldía
curl "http://localhost:8000/search?alcaldia=Cuauhtémoc"

# Filtrar por seguridad mínima
curl "http://localhost:8000/search?min_seguridad=8.0"

# Filtrar por precio máximo de renta
curl "http://localhost:8000/search?max_precio_renta=400"
```

## 📁 Estructura del Proyecto

```
RedBull_ITAM_Dataton/
├── 🏠 CasaMX Core Files
│   ├── requirements.txt              # Dependencias Python
│   ├── dataset_mock_cdmx.json       # Datos de 20 colonias
│   ├── datos_geograficos_cdmx.json  # Coordenadas y mapas
│   ├── setup_quick.py               # Setup rápido
│   ├── setup_project.py             # Setup completo
│   └── install_dependencies.sh      # Script bash
│
├── 📊 Data/
│   ├── casamx.db                    # Base de datos SQLite
│   ├── mock/                        # Datos de prueba
│   ├── processed/                   # Datos procesados
│   └── raw/                         # Datos originales
│
├── 🔧 Source Code/
│   └── api/
│       └── main.py                  # FastAPI server
│
├── 📓 Notebooks/                    # Jupyter notebooks
├── ⚙️  Config/                      # Configuración
└── 📝 Tests/                       # Pruebas unitarias
```

## 🌟 Características Principales

### ✅ API RESTful Completa
- FastAPI con documentación automática
- Endpoints para consultas, filtros y búsquedas
- Validación automática de datos
- CORS habilitado para desarrollo

### ✅ Base de Datos Optimizada
- SQLite para portabilidad y velocidad
- Esquema normalizado para consultas eficientes
- Índices automáticos en campos clave
- 20 colonias con datos completos

### ✅ Datos Geográficos
- Coordenadas precisas de todas las colonias
- Información de alcaldías y códigos postales
- Datos de transporte público (Metro, Metrobús)
- Puntos de interés y rutas principales

### ✅ Análisis de Mercado
- Scores de seguridad, transporte y amenidades
- Precios de renta y venta por m²
- Información de propiedades (1BR, 2BR, 3BR)
- Análisis socioeconómico por zona

## 📈 Métricas y Scoring

### Sistema de Puntuación (1-10)

- **Seguridad:** Basado en índices de criminalidad y percepción
- **Transporte:** Accesibilidad a metro, metrobús y conectividad
- **Amenidades:** Hospitales, escuelas, parques, restaurantes
- **Precio:** Valor inverso (menor precio = mayor score)

### Rangos de Precios

| Nivel | Renta/m² | Venta/m² | Ejemplos |
|-------|----------|----------|----------|
| Premium | $500+ | $70k+ | Polanco, Santa Fe |
| Alto | $350-500 | $50-70k | Roma, Condesa |
| Medio-Alto | $280-350 | $40-50k | Del Valle, Coyoacán |
| Medio | $220-280 | $30-40k | Narvarte, Escandón |
| Accesible | <$220 | <$30k | Doctores, Xochimilco |

## 🔍 Casos de Uso

### Para Compradores
```python
# Buscar colonias seguras y bien conectadas
GET /search?min_seguridad=8.0&score_transporte=8.0

# Filtrar por presupuesto
GET /search?max_precio_renta=300
```

### Para Inversionistas
```python
# Análisis de ROI por colonia
GET /colonias/col_001  # Datos completos de Polanco

# Comparativa de precios
GET /search?alcaldia=Cuauhtémoc
```

### Para Analistas
```python
# Datos para machine learning
GET /colonias  # Dataset completo

# Análisis geográfico
datos_geograficos_cdmx.json  # Coordenadas y mapas
```

## 🚀 Desarrollo y Extensión

### Agregar Nuevas Colonias

```python
# En src/utils/data_loader.py
new_colonia = {
    "id": "col_021",
    "nombre": "Nueva Colonia",
    "coordenadas": {"lat": 19.4000, "lon": -99.1500},
    # ... más datos
}
```

### Nuevos Endpoints

```python
# En src/api/main.py
@app.get("/analytics/price-trends")
async def get_price_trends():
    # Análisis de tendencias de precios
    pass

@app.get("/recommendations/{user_profile}")  
async def get_recommendations(user_profile: str):
    # Sistema de recomendaciones
    pass
```

### Visualizaciones

```python
# Ejemplo con Plotly
import plotly.express as px

# Mapa de calor de precios
fig = px.scatter_mapbox(
    data_colonias, 
    lat="lat", 
    lon="lon",
    color="renta_m2",
    size="poblacion",
    mapbox_style="open-street-map"
)
```

## 🛡️ Consideraciones de Producción

### Seguridad
- Validación de entrada en todos los endpoints
- Límites de rate limiting (implementar con Redis)
- Autenticación JWT para endpoints sensibles

### Performance  
- Cache de consultas frecuentes con Redis
- Indexación de base de datos optimizada
- Paginación en endpoints que retornan listas

### Monitoring
- Logs estructurados con logging module
- Métricas de API con Prometheus
- Health checks en `/health`

## 📚 Recursos Adicionales

### Documentación
- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **ReDoc:** http://localhost:8000/redoc
- **Esquema OpenAPI:** http://localhost:8000/openapi.json

### Datasets
- `dataset_mock_cdmx.json` - 20 colonias completas
- `datos_geograficos_cdmx.json` - Mapas y coordenadas
- Base de datos SQLite en `data/casamx.db`

### Scripts Útiles
- `setup_quick.py` - Setup sin dependencias
- `setup_project.py` - Setup completo con venv
- `install_dependencies.sh` - Script bash de instalación

## 🤝 Contribución

### Para el Datatón

1. **Fork del proyecto** o trabaja directamente
2. **Crea nuevas features** en `src/`
3. **Agrega datos** en `data/mock/`
4. **Documenta cambios** en este README
5. **Prueba la API** con `/docs`

### Áreas de Mejora Sugeridas

- [ ] Scraping de datos reales de portales inmobiliarios
- [ ] Integración con APIs de mapas (Google Maps, Mapbox)
- [ ] Sistema de recomendaciones con ML
- [ ] Dashboard web interactivo
- [ ] Análisis predictivo de precios
- [ ] Integración con datos de INEGI

---

## 📞 Contacto y Soporte

**David Fernando Ávila Díaz**  
**Estudiante de Ciencia de Datos - ITAM**  
**Datatón ITAM 2025**

### Troubleshooting

**Error: Dependencias no instaladas**
```bash
# Solución: Usar entorno virtual
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

**Error: Puerto 8000 ocupado**
```bash
# Cambiar puerto en src/api/main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Error: Base de datos no encontrada**
```bash
# Ejecutar setup nuevamente
python3 setup_quick.py
```

---

*Sistema diseñado para el Datatón ITAM 2025 con enfoque en análisis de datos de vivienda en la Ciudad de México. Optimizado para desarrollo rápido y análisis profundo del mercado inmobiliario.*