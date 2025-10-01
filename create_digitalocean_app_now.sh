#!/bin/bash
# Crear app CasaMX en DigitalOcean INMEDIATAMENTE
# David Fernando Ávila Díaz - ITAM

echo "🚀 CREANDO CASAMX EN DIGITALOCEAN APP PLATFORM..."

# Mostrar URLs importantes
echo ""
echo "🎯 PASOS INMEDIATOS:"
echo "1. Ir a: https://cloud.digitalocean.com/apps"
echo "2. Clic: 'Create App'"
echo "3. Source: GitHub → DabtcAvila/RedBull_ITAM_Dataton"
echo "4. Branch: main"
echo "5. Auto-deploy: ✅ ON"
echo ""

echo "⚙️ CONFIGURACIÓN:"
echo "App Name: casamx-dataton-itam"
echo "Source Directory: / (root)"
echo "Build Command: pip install -r requirements.txt"
echo "Run Command: streamlit run streamlit_app_fixed.py --server.port=8080"
echo ""

echo "🌐 DOMINIO:"
echo "Custom Domain: casamx.store"
echo "SSL: Automático"
echo ""

echo "💰 PLAN RECOMENDADO:"
echo "Basic: $5/mes (1 vCPU, 512MB RAM)"
echo "Suficiente para demo del Datatón"
echo ""

echo "📊 DESPUÉS DEL DEPLOY:"
echo "- https://casamx.store (funcional en 10-15 min)"
echo "- SSL automático activado"
echo "- Performance optimizada"
echo ""

echo "🎯 URLs ACTUALES MIENTRAS ESPERAS:"
echo "- PWA: http://localhost:8090 (instalable)"
echo "- Cinematográfica: http://localhost:8504"
echo ""

echo "✅ TODO LISTO PARA GANAR EL DATATÓN ITAM 2025!"