#!/bin/bash
# CasaMX Deployment Verification Script - Datatón ITAM 2025
# Verifica que casamx.store esté funcionando correctamente

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuración
DOMAIN="casamx.store"
WWW_DOMAIN="www.casamx.store"
LOCAL_PORT="8503"
TUNNEL_ID="d198c64a-c169-42ce-9279-e0abdd0b71df"

echo -e "${BLUE}🔍 CasaMX Deployment Verification - Datatón ITAM 2025${NC}"
echo -e "${BLUE}====================================================${NC}"
echo ""

# Función para verificar URL
check_url() {
    local url=$1
    local description=$2
    local expected_status=${3:-200}
    
    echo -e "${CYAN}🌐 Verificando $description: $url${NC}"
    
    # Verificar conectividad básica
    local response=$(curl -s -w "%{http_code},%{time_total},%{ssl_verify_result}" -o /dev/null "$url" --max-time 10 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        local http_code=$(echo $response | cut -d',' -f1)
        local time_total=$(echo $response | cut -d',' -f2)
        local ssl_result=$(echo $response | cut -d',' -f3)
        
        if [ "$http_code" -eq "$expected_status" ]; then
            echo -e "${GREEN}   ✅ Status: $http_code (OK) - Tiempo: ${time_total}s${NC}"
            if [[ "$url" == https* ]]; then
                if [ "$ssl_result" -eq 0 ]; then
                    echo -e "${GREEN}   ✅ SSL: Válido${NC}"
                else
                    echo -e "${YELLOW}   ⚠️  SSL: Advertencia (código: $ssl_result)${NC}"
                fi
            fi
            return 0
        else
            echo -e "${RED}   ❌ Status: $http_code (Esperado: $expected_status)${NC}"
            return 1
        fi
    else
        echo -e "${RED}   ❌ No hay respuesta (timeout o error de conexión)${NC}"
        return 1
    fi
}

# Función para verificar DNS
check_dns() {
    local domain=$1
    local record_type=$2
    
    echo -e "${CYAN}🔍 Verificando DNS $record_type para $domain${NC}"
    
    local result=$(dig +short $record_type $domain 2>/dev/null)
    
    if [ ! -z "$result" ]; then
        echo -e "${GREEN}   ✅ $record_type records:${NC}"
        echo "$result" | while read line; do
            echo -e "${GREEN}      → $line${NC}"
        done
        return 0
    else
        echo -e "${RED}   ❌ No se encontraron records $record_type${NC}"
        return 1
    fi
}

# Función para verificar servicios locales
check_local_service() {
    echo -e "${CYAN}🏠 Verificando servicio local (puerto $LOCAL_PORT)${NC}"
    
    if lsof -Pi :$LOCAL_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${GREEN}   ✅ Puerto $LOCAL_PORT está en uso${NC}"
        local pid=$(lsof -Pi :$LOCAL_PORT -sTCP:LISTEN -t)
        local process=$(ps -p $pid -o comm= 2>/dev/null)
        echo -e "${GREEN}      → PID: $pid, Proceso: $process${NC}"
        
        # Verificar conectividad local
        if curl -s -f "http://localhost:$LOCAL_PORT" > /dev/null; then
            echo -e "${GREEN}   ✅ Servicio local respondiendo${NC}"
            return 0
        else
            echo -e "${YELLOW}   ⚠️  Puerto en uso pero servicio no responde${NC}"
            return 1
        fi
    else
        echo -e "${RED}   ❌ Puerto $LOCAL_PORT no está en uso${NC}"
        return 1
    fi
}

# Función para verificar tunnel
check_tunnel() {
    echo -e "${CYAN}🌐 Verificando Cloudflare Tunnel${NC}"
    
    if command -v cloudflared &> /dev/null; then
        echo -e "${GREEN}   ✅ cloudflared está instalado${NC}"
        
        # Verificar si el tunnel está corriendo
        local tunnel_info=$(cloudflared tunnel info $TUNNEL_ID 2>/dev/null)
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}   ✅ Tunnel encontrado${NC}"
            echo "$tunnel_info" | head -5 | while read line; do
                echo -e "${GREEN}      → $line${NC}"
            done
        else
            echo -e "${YELLOW}   ⚠️  No se puede obtener información del tunnel${NC}"
        fi
        
        # Verificar archivo de configuración
        if [ -f ~/.cloudflared/config.yml ]; then
            echo -e "${GREEN}   ✅ Archivo de configuración existe${NC}"
        else
            echo -e "${RED}   ❌ Archivo de configuración no encontrado${NC}"
        fi
    else
        echo -e "${RED}   ❌ cloudflared no está instalado${NC}"
        return 1
    fi
}

# Función para test de rendimiento
performance_test() {
    echo -e "${CYAN}📊 Test de rendimiento para $1${NC}"
    
    local url=$1
    local result=$(curl -w "@-" -o /dev/null -s "$url" <<'EOF'
     namelookup:  %{time_namelookup}s\n
        connect:  %{time_connect}s\n
     appconnect:  %{time_appconnect}s\n
    pretransfer:  %{time_pretransfer}s\n
       redirect:  %{time_redirect}s\n
  starttransfer:  %{time_starttransfer}s\n
                 ----------\n
          total:  %{time_total}s\n
EOF
)
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}   ✅ Tiempos de respuesta:${NC}"
        echo "$result" | while read line; do
            echo -e "${GREEN}      $line${NC}"
        done
    else
        echo -e "${RED}   ❌ No se pudo realizar el test de rendimiento${NC}"
    fi
}

# Función para verificar headers de seguridad
check_security_headers() {
    local url=$1
    
    echo -e "${CYAN}🔒 Verificando headers de seguridad para $url${NC}"
    
    local headers=$(curl -s -I "$url" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        # Verificar headers importantes
        if echo "$headers" | grep -q "strict-transport-security"; then
            echo -e "${GREEN}   ✅ HSTS habilitado${NC}"
        else
            echo -e "${YELLOW}   ⚠️  HSTS no detectado${NC}"
        fi
        
        if echo "$headers" | grep -q "x-content-type-options"; then
            echo -e "${GREEN}   ✅ X-Content-Type-Options presente${NC}"
        else
            echo -e "${YELLOW}   ⚠️  X-Content-Type-Options no detectado${NC}"
        fi
        
        if echo "$headers" | grep -q "cf-ray"; then
            echo -e "${GREEN}   ✅ Cloudflare activo (CF-Ray header presente)${NC}"
        else
            echo -e "${YELLOW}   ⚠️  Cloudflare headers no detectados${NC}"
        fi
    else
        echo -e "${RED}   ❌ No se pudieron obtener headers${NC}"
    fi
}

# INICIO DE VERIFICACIONES

echo -e "${YELLOW}🔍 1. VERIFICACIÓN DE SERVICIOS LOCALES${NC}"
echo "----------------------------------------"
check_local_service
echo ""

echo -e "${YELLOW}🌐 2. VERIFICACIÓN DE TUNNEL${NC}"
echo "------------------------------"
check_tunnel
echo ""

echo -e "${YELLOW}🔍 3. VERIFICACIÓN DE DNS${NC}"
echo "----------------------------"
check_dns $DOMAIN "A"
check_dns $DOMAIN "CNAME"
check_dns $WWW_DOMAIN "CNAME"
check_dns $DOMAIN "NS"
echo ""

echo -e "${YELLOW}🌐 4. VERIFICACIÓN DE CONECTIVIDAD WEB${NC}"
echo "----------------------------------------"
check_url "http://localhost:$LOCAL_PORT" "Servicio local"
check_url "https://$DOMAIN" "Dominio principal"
check_url "https://$WWW_DOMAIN" "Subdominio www"
echo ""

echo -e "${YELLOW}🔒 5. VERIFICACIÓN DE SEGURIDAD${NC}"
echo "--------------------------------"
check_security_headers "https://$DOMAIN"
echo ""

echo -e "${YELLOW}📊 6. TEST DE RENDIMIENTO${NC}"
echo "---------------------------"
performance_test "https://$DOMAIN"
echo ""

# VERIFICACIONES ADICIONALES

echo -e "${YELLOW}🔍 7. VERIFICACIONES ADICIONALES${NC}"
echo "----------------------------------"

# Verificar redirección HTTP a HTTPS
echo -e "${CYAN}🔄 Verificando redirección HTTP → HTTPS${NC}"
if curl -s -I "http://$DOMAIN" | grep -q "301\|302"; then
    echo -e "${GREEN}   ✅ Redirección HTTP → HTTPS configurada${NC}"
else
    echo -e "${YELLOW}   ⚠️  Redirección HTTP → HTTPS no detectada${NC}"
fi

# Verificar certificado SSL
echo -e "${CYAN}🔐 Verificando certificado SSL${NC}"
local ssl_info=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -subject -dates 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ Certificado SSL válido${NC}"
    echo "$ssl_info" | while read line; do
        echo -e "${GREEN}      → $line${NC}"
    done
else
    echo -e "${YELLOW}   ⚠️  No se pudo verificar el certificado SSL${NC}"
fi

echo ""

# RESUMEN FINAL
echo -e "${BLUE}📋 RESUMEN DE VERIFICACIÓN${NC}"
echo -e "${BLUE}============================${NC}"

# URLs de verificación externa
echo -e "${CYAN}🔗 Enlaces útiles para verificación manual:${NC}"
echo -e "   • DNS Global: https://dnschecker.org/#A/$DOMAIN"
echo -e "   • SSL Test: https://www.ssllabs.com/ssltest/analyze.html?d=$DOMAIN"
echo -e "   • Speed Test: https://www.webpagetest.org/"
echo -e "   • Uptime: https://uptime.is/$DOMAIN"

echo ""
echo -e "${GREEN}✅ Verificación completada para Datatón ITAM 2025${NC}"
echo -e "${BLUE}🚀 Si todo está verde, casamx.store está listo para la demo!${NC}"

# Script de monitoreo continuo (opcional)
read -p "¿Deseas ejecutar monitoreo continuo? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}📡 Iniciando monitoreo continuo (Ctrl+C para salir)...${NC}"
    while true; do
        echo -e "\n${BLUE}$(date): Verificando $DOMAIN...${NC}"
        if check_url "https://$DOMAIN" "Dominio principal" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ $DOMAIN funcionando${NC}"
        else
            echo -e "${RED}❌ $DOMAIN no responde${NC}"
        fi
        sleep 30
    done
fi