#!/bin/bash
# CasaMX Cloudflare Setup Script - Datatón ITAM 2025
# David Fernando Ávila Díaz

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Datos del proyecto
TUNNEL_ID="d198c64a-c169-42ce-9279-e0abdd0b71df"
TUNNEL_NAME="casamx-dataton"
DOMAIN="casamx.store"
LOCAL_PORT="8503"
PROJECT_DIR="/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton"

echo -e "${BLUE}🚀 CasaMX Cloudflare Setup - Datatón ITAM 2025${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""

# Función para verificar comandos
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ $1 no está instalado${NC}"
        return 1
    else
        echo -e "${GREEN}✅ $1 está disponible${NC}"
        return 0
    fi
}

# Función para verificar archivos
check_file() {
    if [ ! -f "$1" ]; then
        echo -e "${RED}❌ Archivo no encontrado: $1${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Archivo encontrado: $1${NC}"
        return 0
    fi
}

# 1. Verificar dependencias
echo -e "${YELLOW}📋 Verificando dependencias...${NC}"
check_command "cloudflared" || {
    echo -e "${YELLOW}📦 Instalando cloudflared...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install cloudflared
    else
        curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
        chmod +x cloudflared
        sudo mv cloudflared /usr/local/bin/
    fi
}

check_command "streamlit" || {
    echo -e "${RED}❌ Streamlit no está instalado. Activar entorno virtual primero.${NC}"
    exit 1
}

# 2. Verificar directorio del proyecto
echo -e "${YELLOW}📁 Verificando directorio del proyecto...${NC}"
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Directorio del proyecto no encontrado: $PROJECT_DIR${NC}"
    exit 1
fi
cd "$PROJECT_DIR"

# 3. Crear directorio de configuración Cloudflare
echo -e "${YELLOW}⚙️  Preparando configuración Cloudflare...${NC}"
mkdir -p ~/.cloudflared

# 4. Verificar autenticación con Cloudflare
echo -e "${YELLOW}🔐 Verificando autenticación Cloudflare...${NC}"
if ! cloudflared tunnel list &> /dev/null; then
    echo -e "${YELLOW}🔑 Necesitas autenticarte con Cloudflare...${NC}"
    echo -e "${BLUE}Se abrirá tu navegador para login...${NC}"
    cloudflared tunnel login
fi

# 5. Verificar si el tunnel existe
echo -e "${YELLOW}🌐 Verificando tunnel existente...${NC}"
if cloudflared tunnel list | grep -q "$TUNNEL_ID"; then
    echo -e "${GREEN}✅ Tunnel $TUNNEL_NAME encontrado${NC}"
else
    echo -e "${YELLOW}🆕 Creando nuevo tunnel...${NC}"
    cloudflared tunnel create "$TUNNEL_NAME"
fi

# 6. Crear archivo de configuración del tunnel
echo -e "${YELLOW}📝 Creando configuración del tunnel...${NC}"
cat > ~/.cloudflared/config.yml << EOF
tunnel: $TUNNEL_ID
credentials-file: ~/.cloudflared/$TUNNEL_ID.json

# Configuraciones del tunnel
no-autoupdate: true
retries: 5
grace-period: 30s

# Rutas de tráfico
ingress:
  # Dominio principal
  - hostname: $DOMAIN
    service: http://localhost:$LOCAL_PORT
    originRequest:
      httpHostHeader: localhost:$LOCAL_PORT
      
  # Subdominio www
  - hostname: www.$DOMAIN
    service: http://localhost:$LOCAL_PORT
    originRequest:
      httpHostHeader: localhost:$LOCAL_PORT
      
  # Catch-all (obligatorio)
  - service: http_status:404

# Logging
loglevel: info
logfile: ~/.cloudflared/tunnel.log
EOF

# 7. Verificar archivo de credenciales
echo -e "${YELLOW}🔑 Verificando credenciales del tunnel...${NC}"
CREDENTIALS_FILE="$HOME/.cloudflared/$TUNNEL_ID.json"
if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo -e "${RED}❌ Archivo de credenciales no encontrado: $CREDENTIALS_FILE${NC}"
    echo -e "${YELLOW}💡 Ejecuta: cloudflared tunnel login${NC}"
    exit 1
fi

# 8. Validar configuración
echo -e "${YELLOW}✅ Validando configuración...${NC}"
if cloudflared tunnel validate ~/.cloudflared/config.yml; then
    echo -e "${GREEN}✅ Configuración válida${NC}"
else
    echo -e "${RED}❌ Error en la configuración${NC}"
    exit 1
fi

# 9. Configurar DNS (opcional, manual recomendado)
echo -e "${YELLOW}🌍 Configuración DNS...${NC}"
echo -e "${BLUE}📋 Configuración manual requerida en Cloudflare Dashboard:${NC}"
echo ""
echo -e "${BLUE}DNS Records necesarios:${NC}"
echo -e "Type: CNAME | Name: @ | Content: $TUNNEL_ID.cfargotunnel.com | Proxy: ON"
echo -e "Type: CNAME | Name: www | Content: $TUNNEL_ID.cfargotunnel.com | Proxy: ON"
echo ""

# 10. Crear directorio de logs
mkdir -p logs

# 11. Resumen de configuración
echo -e "${GREEN}🎉 CONFIGURACIÓN COMPLETADA${NC}"
echo -e "${GREEN}==============================${NC}"
echo ""
echo -e "${BLUE}📊 Información del Tunnel:${NC}"
echo -e "ID: $TUNNEL_ID"
echo -e "Nombre: $TUNNEL_NAME"
echo -e "Dominio: $DOMAIN"
echo -e "Puerto local: $LOCAL_PORT"
echo ""
echo -e "${BLUE}📁 Archivos creados:${NC}"
echo -e "~/.cloudflared/config.yml"
echo -e "~/.cloudflared/tunnel.log (cuando ejecutes)"
echo ""
echo -e "${BLUE}🚀 Para iniciar CasaMX:${NC}"
echo -e "1. Activar entorno: source casamx_env/bin/activate"
echo -e "2. Ejecutar script: ./cloudflare/run_casamx_tunnel.sh"
echo ""
echo -e "${BLUE}🌐 URLs una vez funcionando:${NC}"
echo -e "- https://$DOMAIN"
echo -e "- https://www.$DOMAIN"
echo -e "- http://localhost:$LOCAL_PORT (local)"
echo ""
echo -e "${YELLOW}⚠️  SIGUIENTE PASO: Configurar DNS en Cloudflare Dashboard${NC}"
echo -e "${YELLOW}📖 Ver guía: cloudflare/01_GUIA_CLOUDFLARE_DASHBOARD.md${NC}"

# 12. Verificar información del tunnel
echo -e "${BLUE}🔍 Información del tunnel:${NC}"
cloudflared tunnel info "$TUNNEL_ID"