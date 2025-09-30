#!/bin/bash

# CasaMX - Script de instalación de dependencias
# Datatón ITAM 2025

echo "🏠 CasaMX - Instalación de dependencias"
echo "Datatón ITAM 2025"
echo "================================================="

# Obtener la ruta del directorio actual
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

echo "📁 Directorio del proyecto: $PROJECT_DIR"

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Creando entorno virtual..."
    python3 -m venv "$VENV_DIR"
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source "$VENV_DIR/bin/activate"

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias desde requirements.txt..."
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements.txt"
    echo "✅ Dependencias instaladas"
else
    echo "⚠️  No se encontró requirements.txt"
fi

# Crear estructura de directorios
echo "📁 Creando estructura de directorios..."
mkdir -p "$PROJECT_DIR/data"/{mock,processed,raw,geographic}
mkdir -p "$PROJECT_DIR/src"/{api,models,utils,visualization}
mkdir -p "$PROJECT_DIR"/{notebooks,config,logs,tests}

# Crear archivos __init__.py
touch "$PROJECT_DIR/src/__init__.py"
touch "$PROJECT_DIR/src/api/__init__.py"
touch "$PROJECT_DIR/src/models/__init__.py"
touch "$PROJECT_DIR/src/utils/__init__.py"
touch "$PROJECT_DIR/src/visualization/__init__.py"
touch "$PROJECT_DIR/tests/__init__.py"

echo "🎉 Instalación completada!"
echo "================================================="
echo "Para usar el proyecto:"
echo "1. source venv/bin/activate"
echo "2. python src/api/main.py"
echo "3. Abrir navegador en: http://localhost:8000"
echo ""
echo "Para desactivar el entorno virtual:"
echo "deactivate"