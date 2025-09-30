#!/bin/bash
# 🚀 CasaMX - Ejecutar en VIVO para Datatón ITAM 2025
# David Fernando Ávila Díaz - ITAM

clear
echo "🏆 ====================================="
echo "🏠 CasaMX - Datatón ITAM 2025"
echo "👨‍💻 David Fernando Ávila Díaz"
echo "🌐 casamx.store"
echo "====================================="
echo ""

# Directorio del proyecto
PROJECT_DIR="/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton"
cd "$PROJECT_DIR"

echo "🔧 Activando entorno virtual..."
source casamx_env/bin/activate

echo "📡 Iniciando Streamlit CasaMX..."
# Ejecutar Streamlit en background
nohup streamlit run streamlit_app_fixed.py --server.port=8502 --server.headless=true > logs/streamlit_live.log 2>&1 &
STREAMLIT_PID=$!

# Esperar que Streamlit inicie completamente
sleep 8

echo "🌐 Iniciando Cloudflare Tunnel..."
echo "   Conectando casamx.store a tu aplicación..."

# Ejecutar tunnel
cloudflared tunnel run casamx-dataton-2025 &
TUNNEL_PID=$!

# Esperar conexión
sleep 5

echo ""
echo "✅ 🎉 ¡CASAMX EN VIVO! 🎉"
echo ""
echo "🌍 URLs PÚBLICAS:"
echo "   📱 https://casamx.store"
echo "   🖥️  https://www.casamx.store"
echo ""
echo "🏠 URLs LOCALES:"
echo "   💻 http://localhost:8502"
echo "   🔗 http://192.168.100.76:8502"
echo ""
echo "📊 MONITOREO:"
echo "   📈 Dashboard: https://dash.cloudflare.com"
echo "   📜 Logs Streamlit: tail -f logs/streamlit_live.log"
echo ""
echo "🎯 PARA EL DATATÓN:"
echo "   ✅ App funcionando 24/7 mientras laptop esté encendida"
echo "   ✅ Dominio profesional configurado"
echo "   ✅ HTTPS automático activado"
echo "   ✅ Listo para demo en vivo"
echo ""
echo "🛑 PARA DETENER:"
echo "   Ctrl+C o ejecutar: kill $STREAMLIT_PID $TUNNEL_PID"
echo ""
echo "⚡ Presiona Ctrl+C para detener el sistema..."

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo CasaMX..."
    kill $STREAMLIT_PID 2>/dev/null
    kill $TUNNEL_PID 2>/dev/null
    echo "✅ Sistema detenido correctamente"
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT SIGTERM

# Mantener script corriendo
wait