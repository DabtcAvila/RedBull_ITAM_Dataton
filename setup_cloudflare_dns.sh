#!/bin/bash

# 🌐 CLOUDFLARE DNS CONFIGURATION FOR CASAMX.APP
# Automatically configure DNS records for DigitalOcean VPS

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
DOMAIN="casamx.app"
ZONE_ID=""  # Will be detected automatically
CF_EMAIL=""
CF_API_TOKEN=""

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] ✅ $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] ❌ $1${NC}" >&2
    exit 1
}

info() {
    echo -e "${BLUE}[INFO] 📋 $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] ⚠️  $1${NC}"
}

# Get VPS IP
get_vps_ip() {
    if [[ -z "${VPS_IP:-}" ]]; then
        info "Detectando IP del VPS..."
        
        # Try to get IP from argument
        if [[ $# -gt 0 ]]; then
            VPS_IP="$1"
            log "IP proporcionada: $VPS_IP"
        else
            # Try to get current public IP (if running from VPS)
            if command -v curl >/dev/null 2>&1; then
                VPS_IP=$(curl -s ifconfig.me)
                log "IP detectada automáticamente: $VPS_IP"
            else
                error "No se pudo detectar la IP. Proporciona la IP como argumento: $0 YOUR_VPS_IP"
            fi
        fi
    fi
    
    # Validate IP format
    if [[ ! $VPS_IP =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        error "IP inválida: $VPS_IP"
    fi
}

# Get Cloudflare credentials
get_cloudflare_creds() {
    if [[ -z "$CF_API_TOKEN" ]]; then
        info "Configuración de Cloudflare requerida..."
        echo
        echo "🔑 Necesitas un API Token de Cloudflare:"
        echo "   1. Ve a: https://dash.cloudflare.com/profile/api-tokens"
        echo "   2. Click 'Create Token'"
        echo "   3. Usa template 'Edit zone DNS'"
        echo "   4. Selecciona zona: $DOMAIN"
        echo "   5. Copia el token generado"
        echo
        
        read -p "🔐 Ingresa tu Cloudflare API Token: " CF_API_TOKEN
        
        if [[ -z "$CF_API_TOKEN" ]]; then
            error "API Token requerido para continuar"
        fi
    fi
}

# Get Zone ID
get_zone_id() {
    info "Obteniendo Zone ID para $DOMAIN..."
    
    ZONE_ID=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=$DOMAIN" \
        -H "Authorization: Bearer $CF_API_TOKEN" \
        -H "Content-Type: application/json" | \
        jq -r '.result[0].id // empty')
    
    if [[ -z "$ZONE_ID" ]]; then
        error "No se pudo obtener Zone ID. Verifica que $DOMAIN esté en tu cuenta de Cloudflare"
    fi
    
    log "Zone ID obtenido: $ZONE_ID"
}

# Create or update DNS record
update_dns_record() {
    local name="$1"
    local content="$2"
    local display_name="$3"
    
    info "Configurando registro DNS: $display_name → $content"
    
    # Check if record exists
    local record_id=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?type=A&name=$name" \
        -H "Authorization: Bearer $CF_API_TOKEN" \
        -H "Content-Type: application/json" | \
        jq -r '.result[0].id // empty')
    
    local data="{\"type\":\"A\",\"name\":\"$name\",\"content\":\"$content\",\"ttl\":300}"
    
    if [[ -n "$record_id" ]]; then
        # Update existing record
        local response=$(curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$record_id" \
            -H "Authorization: Bearer $CF_API_TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data")
    else
        # Create new record
        local response=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
            -H "Authorization: Bearer $CF_API_TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    local success=$(echo "$response" | jq -r '.success')
    
    if [[ "$success" == "true" ]]; then
        log "✅ Registro DNS configurado: $display_name"
    else
        local errors=$(echo "$response" | jq -r '.errors[].message' 2>/dev/null | head -1)
        error "❌ Error configurando $display_name: $errors"
    fi
}

# Verify DNS propagation
verify_dns() {
    info "Verificando propagación DNS..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        info "Intento $attempt/$max_attempts - Verificando DNS..."
        
        # Check root domain
        local resolved_ip=$(dig +short @8.8.8.8 $DOMAIN A | head -1)
        
        if [[ "$resolved_ip" == "$VPS_IP" ]]; then
            log "✅ DNS propagado correctamente: $DOMAIN → $VPS_IP"
            break
        else
            if [[ $attempt -eq $max_attempts ]]; then
                warning "⚠️  DNS aún no ha propagado completamente"
                warning "   Esperado: $VPS_IP"
                warning "   Recibido: $resolved_ip"
                warning "   Esto puede tomar hasta 5 minutos más"
            else
                info "⏳ Esperando propagación DNS... (${attempt}0s)"
                sleep 10
            fi
        fi
        
        ((attempt++))
    done
}

# Main execution
main() {
    echo "🌐 CONFIGURACIÓN AUTOMÁTICA DE DNS - CASAMX.APP"
    echo "📅 Datatón ITAM 2025 - David Fernando Ávila Díaz"
    echo
    
    # Get VPS IP
    get_vps_ip "$@"
    
    # Get Cloudflare credentials
    get_cloudflare_creds
    
    # Check if jq is installed
    if ! command -v jq >/dev/null 2>&1; then
        info "Instalando jq para procesar JSON..."
        if command -v apt-get >/dev/null 2>&1; then
            apt-get update && apt-get install -y jq
        elif command -v brew >/dev/null 2>&1; then
            brew install jq
        else
            error "No se pudo instalar jq. Instálalo manualmente."
        fi
    fi
    
    # Get Zone ID
    get_zone_id
    
    # Configure DNS records
    update_dns_record "$DOMAIN" "$VPS_IP" "$DOMAIN"
    update_dns_record "www.$DOMAIN" "$VPS_IP" "www.$DOMAIN"
    
    # Verify DNS
    verify_dns
    
    echo
    log "🎉 ¡DNS CONFIGURADO EXITOSAMENTE!"
    echo
    echo "📋 REGISTROS DNS CONFIGURADOS:"
    echo "   • $DOMAIN → $VPS_IP"
    echo "   • www.$DOMAIN → $VPS_IP"
    echo
    echo "⏱️  PROPAGACIÓN:"
    echo "   • DNS puede tardar 1-5 minutos en propagar completamente"
    echo "   • Verifica en: https://dnschecker.org"
    echo
    echo "🔗 PRÓXIMOS PASOS:"
    echo "   1. Esperar 2-3 minutos para propagación completa"
    echo "   2. Ejecutar deployment en VPS:"
    echo "      ssh root@$VPS_IP"
    echo "      wget https://raw.githubusercontent.com/DabtcAvila/RedBull_ITAM_Dataton/main/deploy_casamx_vps_complete.sh"
    echo "      chmod +x deploy_casamx_vps_complete.sh"
    echo "      sudo ./deploy_casamx_vps_complete.sh"
    echo
    echo "🚀 RESULTADO FINAL: https://$DOMAIN funcionando en 15 minutos!"
}

# Check for help argument
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    echo "🌐 Configurador automático de DNS para CasaMX"
    echo
    echo "USAGE:"
    echo "  $0 [VPS_IP]"
    echo
    echo "EJEMPLOS:"
    echo "  $0 134.122.123.45"
    echo "  $0                    # Auto-detecta IP si se ejecuta desde VPS"
    echo
    echo "REQUISITOS:"
    echo "  • Dominio casamx.app en Cloudflare"
    echo "  • API Token de Cloudflare con permisos DNS"
    echo "  • jq instalado (se instala automáticamente)"
    exit 0
fi

# Execute main function
main "$@"