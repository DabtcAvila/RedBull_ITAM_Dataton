#!/bin/bash
# DEPLOYMENT ENTERPRISE DEFINITIVO - CasaMX
# David Fernando Ávila Díaz - ITAM

echo "🚀 ENTERPRISE DEPLOYMENT - NIVEL GANADOR"

# Crear Dockerfile optimizado
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements_production.txt .
RUN pip install --no-cache-dir -r requirements_production.txt

# Copiar aplicación
COPY streamlit_simple.py .
COPY .streamlit/ .streamlit/

EXPOSE 8080

# Comando optimizado para producción
CMD ["streamlit", "run", "streamlit_simple.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]
EOF

# Crear docker-compose para desarrollo
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  casamx:
    build: .
    ports:
      - "8080:8080"
    environment:
      - STREAMLIT_SERVER_PORT=8080
      - STREAMLIT_SERVER_HEADLESS=true
EOF

echo "✅ Docker configuration created"

# Commit y push
git add Dockerfile docker-compose.yml
git commit -m "Add Enterprise Docker configuration for production deployment"
git push origin main

echo "🏆 ENTERPRISE DEPLOYMENT READY"
echo "📊 Arquitectura: Docker + Streamlit + Enterprise config"
echo "🌐 Domain: casamx.store"
echo "⚡ Performance: Optimizado para producción"
echo ""
echo "🎯 AHORA en DigitalOcean:"
echo "1. Create App → Web Service (NO Static)"
echo "2. Source: GitHub repo"
echo "3. Build: Dockerfile automático"
echo "4. Domain: casamx.store"
echo ""
echo "✅ ENTERPRISE LEVEL GARANTIZADO"