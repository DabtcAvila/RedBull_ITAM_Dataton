#!/bin/bash
# CasaMX Tunnel Runner - Datatón ITAM 2025
# Ejecuta Streamlit + Cloudflare Tunnel para casamx.store

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
TUNNEL_ID="d198c64a-c169-42ce-9279-e0abdd0b71df"
TUNNEL_NAME="casamx-dataton"
DOMAIN="casamx.store"
LOCAL_PORT="8503"
PROJECT_DIR="/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton"

echo -e "${BLUE}🚀 CasaMX Tunnel Runner - Datatón ITAM 2025${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Función para cleanup al salir
cleanup() {
    echo -e "\n${YELLOW}🛑 Deteniendo servicios...${NC}"
    
    # Matar Streamlit
    if [ ! -z "$STREAMLIT_PID" ]; then
        echo -e "${YELLOW}🔴 Deteniendo Streamlit (PID: $STREAMLIT_PID)${NC}"
        kill $STREAMLIT_PID 2>/dev/null
    fi
    
    # Matar tunnel
    if [ ! -z "$TUNNEL_PID" ]; then
        echo -e "${YELLOW}🔴 Deteniendo Tunnel (PID: $TUNNEL_PID)${NC}"
        kill $TUNNEL_PID 2>/dev/null
    fi
    
    # Cleanup PID files
    rm -f /tmp/casamx_streamlit.pid /tmp/casamx_tunnel.pid
    
    echo -e "${GREEN}✅ Servicios detenidos${NC}"
    exit 0
}

# Capturar señales para cleanup
trap cleanup SIGINT SIGTERM

# Verificar directorio del proyecto
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Directorio del proyecto no encontrado: $PROJECT_DIR${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

# Verificar entorno virtual
if [ ! -d "casamx_env" ]; then
    echo -e "${RED}❌ Entorno virtual no encontrado: casamx_env${NC}"
    echo -e "${YELLOW}💡 Ejecuta: python -m venv casamx_env && source casamx_env/bin/activate && pip install -r requirements.txt${NC}"
    exit 1
fi

# Activar entorno virtual
echo -e "${YELLOW}🐍 Activando entorno virtual...${NC}"
source casamx_env/bin/activate

# Verificar dependencias
if ! command -v streamlit &> /dev/null; then
    echo -e "${RED}❌ Streamlit no encontrado en el entorno virtual${NC}"
    echo -e "${YELLOW}💡 Instala dependencias: pip install -r requirements.txt${NC}"
    exit 1
fi

if ! command -v cloudflared &> /dev/null; then
    echo -e "${RED}❌ cloudflared no encontrado${NC}"
    echo -e "${YELLOW}💡 Instala cloudflared: brew install cloudflared${NC}"
    exit 1
fi

# Verificar configuración del tunnel
if [ ! -f ~/.cloudflared/config.yml ]; then
    echo -e "${RED}❌ Configuración del tunnel no encontrada${NC}"
    echo -e "${YELLOW}💡 Ejecuta: ./cloudflare/setup_casamx_cloudflare.sh${NC}"
    exit 1
fi

# Verificar app principal
APP_FILE="streamlit_app.py"
if [ ! -f "$APP_FILE" ]; then
    # Buscar archivos alternativos
    if [ -f "streamlit_app_fixed.py" ]; then
        APP_FILE="streamlit_app_fixed.py"
    elif [ -f "main_integration_system.py" ]; then
        APP_FILE="main_integration_system.py"
    else
        echo -e "${RED}❌ Archivo de aplicación no encontrado${NC}"
        ls -la *.py | head -5
        exit 1
    fi
fi

echo -e "${GREEN}✅ Usando aplicación: $APP_FILE${NC}"

# Verificar que el puerto esté libre
if lsof -Pi :$LOCAL_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Puerto $LOCAL_PORT ocupado, liberando...${NC}"
    PID=$(lsof -Pi :$LOCAL_PORT -sTCP:LISTEN -t)
    kill $PID 2>/dev/null
    sleep 2
fi

# Crear directorio de logs
mkdir -p logs

echo -e "${YELLOW}📡 Iniciando Streamlit en puerto $LOCAL_PORT...${NC}"

# Ejecutar Streamlit en background con logs
nohup streamlit run "$APP_FILE" \
    --server.port=$LOCAL_PORT \
    --server.headless=true \
    --server.address=0.0.0.0 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    > logs/streamlit_tunnel.log 2>&1 &
    
STREAMLIT_PID=$!

# Guardar PID para cleanup
echo $STREAMLIT_PID > /tmp/casamx_streamlit.pid

echo -e "${BLUE}🌱 Streamlit PID: $STREAMLIT_PID${NC}"

# Esperar que Streamlit inicie
echo -e "${YELLOW}⏳ Esperando que Streamlit inicie...${NC}"
sleep 8

# Verificar que Streamlit esté corriendo
if ! kill -0 $STREAMLIT_PID 2>/dev/null; then
    echo -e "${RED}❌ Streamlit falló al iniciar${NC}"
    echo -e "${YELLOW}📋 Últimos logs:${NC}"
    tail -20 logs/streamlit_tunnel.log
    exit 1
fi

# Verificar conectividad local
if curl -s -f "http://localhost:$LOCAL_PORT" > /dev/null; then
    echo -e "${GREEN}✅ Streamlit corriendo en http://localhost:$LOCAL_PORT${NC}"
else
    echo -e "${YELLOW}⚠️  Streamlit iniciando, puede tardar unos segundos más...${NC}"
fi

echo -e "${YELLOW}🌐 Iniciando Cloudflare Tunnel...${NC}"

# Ejecutar tunnel
cloudflared tunnel run "$TUNNEL_ID" &
TUNNEL_PID=$!

# Guardar PID para cleanup
echo $TUNNEL_PID > /tmp/casamx_tunnel.pid

echo -e "${BLUE}🌍 Tunnel PID: $TUNNEL_PID${NC}"

# Esperar que el tunnel se conecte
echo -e "${YELLOW}⏳ Estableciendo conexión del tunnel...${NC}"
sleep 5

echo ""
echo -e "${GREEN}🎉 CasaMX FUNCIONANDO!${NC}"
echo -e "${GREEN}========================${NC}"
echo ""
echo -e "${BLUE}🌐 URLs disponibles:${NC}"
echo -e "   • https://$DOMAIN"
echo -e "   • https://www.$DOMAIN"
echo -e "   • http://localhost:$LOCAL_PORT (local)"
echo ""
echo -e "${BLUE}📊 Monitoreo:${NC}"
echo -e "   • Streamlit logs: tail -f logs/streamlit_tunnel.log"
echo -e "   • Tunnel logs: tail -f ~/.cloudflared/tunnel.log"
echo -e "   • Status: cloudflared tunnel info $TUNNEL_ID"
echo ""
echo -e "${BLUE}🔗 Herramientas útiles:${NC}"
echo -e "   • DNS Checker: https://dnschecker.org/"
echo -e "   • SSL Test: https://www.ssllabs.com/ssltest/"
echo -e "   • Speed Test: https://www.webpagetest.org/"
echo ""
echo -e "${YELLOW}🛑 Para detener: Ctrl+C${NC}"
echo ""

# Mostrar información del tunnel
echo -e "${BLUE}📋 Información del tunnel:${NC}"
cloudflared tunnel info "$TUNNEL_ID" 2>/dev/null || echo -e "${YELLOW}⚠️  Información del tunnel no disponible (normal al iniciar)${NC}"

echo ""
echo -e "${GREEN}🚀 Sistema listo para Datatón ITAM 2025!${NC}"

# Mantener script corriendo y mostrar logs
echo -e "${BLUE}📡 Mostrando logs del tunnel (Ctrl+C para salir):${NC}"
echo -e "${BLUE}================================================${NC}"

# Esperar a que ambos procesos terminen
wait