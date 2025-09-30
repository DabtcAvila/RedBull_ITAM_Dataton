#!/bin/bash

echo "🎬 Iniciando CasaMX Cinematográfico - Versión Jueces Datatón 🎬"
echo "=================================================="
echo "🚀 Configurando entorno optimizado..."

# Configurar variables de entorno para máximo rendimiento
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Configuraciones de rendimiento de Python
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

echo "✅ Variables de entorno configuradas"
echo "🎯 Lanzando aplicación cinematográfica..."
echo "📱 Accede desde: http://localhost:8501"
echo "🌍 Acceso remoto: http://0.0.0.0:8501"
echo "=================================================="

# Lanzar Streamlit con configuración optimizada
python -m streamlit run streamlit_app_cinematic.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.fileWatcherType none \
    --browser.gatherUsageStats false \
    --server.maxUploadSize 200 \
    --server.maxMessageSize 200 \
    --server.enableCORS false \
    --server.enableXsrfProtection false