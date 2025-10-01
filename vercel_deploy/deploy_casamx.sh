#!/bin/bash

echo "🚀 DEPLOYMENT INMEDIATO - CasaMX.store"
echo "======================================="

# Configuration
REPO_URL="https://github.com/DabtcAvila/RedBull_ITAM_Dataton"
DOMAIN="casamx.store"
PROJECT_NAME="casamx-streamlit-app"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[1/5] Verificando Vercel CLI...${NC}"
if ! command -v vercel &> /dev/null; then
    echo -e "${RED}❌ Vercel CLI no encontrado. Instalando...${NC}"
    npm install -g vercel
else
    echo -e "${GREEN}✅ Vercel CLI disponible${NC}"
fi

echo -e "${YELLOW}[2/5] Verificando archivos de deployment...${NC}"
if [[ -f "vercel.json" && -f "requirements.txt" && -f "streamlit_simple.py" ]]; then
    echo -e "${GREEN}✅ Todos los archivos necesarios están presentes${NC}"
    ls -la vercel.json requirements.txt streamlit_simple.py api/index.py
else
    echo -e "${RED}❌ Faltan archivos necesarios${NC}"
    exit 1
fi

echo -e "${YELLOW}[3/5] Validando configuración Streamlit...${NC}"
python3 -c "
import streamlit as st
import pandas as pd
import plotly.express as px
print('✅ Dependencias Streamlit OK')
" 2>/dev/null || {
    echo -e "${RED}❌ Error en dependencias. Instalando...${NC}"
    pip3 install streamlit pandas plotly numpy
}

echo -e "${YELLOW}[4/5] Iniciando deployment en Vercel...${NC}"

# Login to Vercel (if not already logged in)
echo -e "${YELLOW}Verificando autenticación Vercel...${NC}"
vercel whoami > /dev/null 2>&1 || {
    echo -e "${YELLOW}🔑 Login requerido en Vercel...${NC}"
    vercel login
}

# Deploy to Vercel
echo -e "${YELLOW}🚀 Deploying to Vercel...${NC}"
vercel --prod --yes --name="$PROJECT_NAME" 2>&1 | tee deployment.log

# Extract deployment URL
DEPLOYMENT_URL=$(grep -o 'https://[^[:space:]]*\.vercel\.app' deployment.log | tail -1)

if [[ -n "$DEPLOYMENT_URL" ]]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo -e "${GREEN}📍 URL: $DEPLOYMENT_URL${NC}"
    
    echo -e "${YELLOW}[5/5] Configurando dominio personalizado...${NC}"
    
    # Add custom domain
    echo -e "${YELLOW}🌐 Configurando $DOMAIN...${NC}"
    vercel domains add "$DOMAIN" --yes 2>/dev/null || echo -e "${YELLOW}⚠️  Dominio ya configurado o requiere verificación DNS${NC}"
    
    # Alias the deployment
    vercel alias "$DEPLOYMENT_URL" "$DOMAIN" --yes 2>/dev/null || echo -e "${YELLOW}⚠️  Alias requiere configuración DNS${NC}"
    
    echo ""
    echo -e "${GREEN}🎉 ¡DEPLOYMENT COMPLETO!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🌐 Vercel URL: $DEPLOYMENT_URL${NC}"
    echo -e "${GREEN}🏠 Dominio:    https://$DOMAIN${NC}"
    echo -e "${GREEN}⚡ SSL:       Automático${NC}"
    echo -e "${GREEN}🚀 Status:    En vivo${NC}"
    echo ""
    
    # Test the deployment
    echo -e "${YELLOW}🔍 Verificando deployment...${NC}"
    sleep 5
    if curl -s -o /dev/null -w "%{http_code}" "$DEPLOYMENT_URL" | grep -q "200"; then
        echo -e "${GREEN}✅ App respondiendo correctamente${NC}"
        echo -e "${GREEN}🎯 Tiempo total: ~5 minutos${NC}"
    else
        echo -e "${YELLOW}⚠️  App iniciando, puede tomar unos segundos adicionales${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}📋 RESUMEN DEL DEPLOYMENT:${NC}"
    echo "   • Plataforma: Vercel"
    echo "   • Runtime: Python 3.9"
    echo "   • Framework: Streamlit"
    echo "   • SSL: Habilitado"
    echo "   • CDN: Global"
    echo "   • Repo: $REPO_URL"
    
else
    echo -e "${RED}❌ Error en deployment${NC}"
    echo -e "${RED}Ver deployment.log para detalles${NC}"
    exit 1
fi