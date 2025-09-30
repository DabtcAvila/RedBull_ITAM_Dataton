#!/bin/bash
# CasaMX - Ejecutar Cloudflare Tunnel + Streamlit
# David Fernando Ávila Díaz - ITAM

echo "🚀 Iniciando CasaMX con Cloudflare Tunnel"

# Directorio del proyecto
PROJECT_DIR="/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton"
cd "$PROJECT_DIR"

# Activar entorno virtual
source casamx_env/bin/activate

echo "📡 Iniciando Streamlit en puerto 8502..."
# Ejecutar Streamlit en background
nohup streamlit run streamlit_app_fixed.py --server.port=8502 --server.headless=true > streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Esperar que Streamlit inicie
sleep 5

echo "🌐 Iniciando Cloudflare Tunnel..."
# Ejecutar tunnel
cloudflared tunnel run casamx-dataton &
TUNNEL_PID=$!

echo ""
echo "✅ CasaMX FUNCIONANDO!"
echo "🌐 URLs disponibles:"
echo "   - https://casamx.store"
echo "   - https://www.casamx.store"
echo "   - Local: http://localhost:8502"
echo ""
echo "📊 Logs:"
echo "   - Streamlit: tail -f streamlit.log"
echo "   - Tunnel: logs en terminal"
echo ""
echo "🛑 Para detener:"
echo "   kill $STREAMLIT_PID $TUNNEL_PID"

# Mantener script corriendo
wait