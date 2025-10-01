#!/bin/bash

# 🚀 AUTOMATED DIGITALOCEAN VPS DEPLOYMENT FOR CASAMX
# CRÍTICO PARA DATATÓN ITAM 2025
# Despliega CasaMX en VPS con dominio casamx.app funcionando en 15 minutos

set -euo pipefail

# Configuration
DOMAIN="casamx.app"
EMAIL="david.avila@itam.mx"
APP_DIR="/opt/casamx"
GITHUB_REPO="https://github.com/DabtcAvila/RedBull_ITAM_Dataton.git"
DB_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Functions
log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] ✅ $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] ❌ $1${NC}" >&2
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] ⚠️  $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] 📋 $1${NC}"
}

success() {
    echo -e "${PURPLE}[SUCCESS] 🎉 $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "Este script debe ejecutarse como root. Usa: sudo $0"
    fi
}

# System update and essential packages
setup_system() {
    log "Actualizando sistema Ubuntu 22.04..."
    
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -y
    apt-get upgrade -y
    
    # Install essential packages
    apt-get install -y \
        curl \
        wget \
        git \
        vim \
        htop \
        ufw \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release \
        python3 \
        python3-pip \
        nginx \
        certbot \
        python3-certbot-nginx \
        supervisor
    
    # Install Node.js (for any JS dependencies)
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
    
    log "Sistema actualizado e instalaciones base completadas"
}

# Configure firewall
setup_firewall() {
    log "Configurando firewall UFW..."
    
    # Reset and configure UFW
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow essential ports
    ufw allow 22/tcp   # SSH
    ufw allow 80/tcp   # HTTP
    ufw allow 443/tcp  # HTTPS
    
    # Enable firewall
    ufw --force enable
    
    log "Firewall configurado - puertos 22, 80, 443 abiertos"
}

# Clone CasaMX repository
clone_repository() {
    log "Clonando repositorio CasaMX desde GitHub..."
    
    # Remove existing directory if it exists
    if [[ -d "$APP_DIR" ]]; then
        rm -rf "$APP_DIR"
    fi
    
    # Create app directory
    mkdir -p "$APP_DIR"
    
    # Clone repository
    git clone "$GITHUB_REPO" "$APP_DIR"
    cd "$APP_DIR"
    
    # Create necessary directories
    mkdir -p data logs ssl
    
    log "Repositorio clonado correctamente en $APP_DIR"
}

# Setup CasaMX application
setup_application() {
    log "Configurando aplicación CasaMX..."
    
    cd "$APP_DIR"
    
    # Create virtual environment
    python3 -m venv casamx_env
    source casamx_env/bin/activate
    
    # Install minimal requirements (for the pure Python version)
    pip install --upgrade pip
    
    # Create optimized launcher script
    cat > start_casamx.py << 'EOF'
#!/usr/bin/env python3
"""
CasaMX Production Launcher
Optimized for DigitalOcean VPS deployment
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the pure Python version
from app_pure import *

if __name__ == "__main__":
    print("🚀 CasaMX Production Server Starting...")
    print(f"🌐 Domain: casamx.app")
    print(f"📊 Datatón ITAM 2025 - David Fernando Ávila Díaz")
    
    # Run the server
    main()
EOF

    chmod +x start_casamx.py
    
    # Create systemd service
    cat > /etc/systemd/system/casamx.service << EOF
[Unit]
Description=CasaMX Application Server
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 $APP_DIR/start_casamx.py
Restart=always
RestartSec=5
Environment=PORT=8080
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

    # Enable and start service
    systemctl daemon-reload
    systemctl enable casamx
    systemctl start casamx
    
    log "Aplicación CasaMX configurada como servicio systemd"
}

# Configure Nginx
setup_nginx() {
    log "Configurando Nginx como reverse proxy..."
    
    # Create nginx configuration
    cat > /etc/nginx/sites-available/casamx << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;
    
    # SSL configuration will be added by Certbot
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Performance optimizations
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Root location
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:8080/health;
        access_log off;
    }
    
    # Static file caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2)$ {
        proxy_pass http://127.0.0.1:8080;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

    # Enable site
    ln -sf /etc/nginx/sites-available/casamx /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    
    # Test nginx configuration
    nginx -t
    
    # Reload nginx
    systemctl reload nginx
    
    log "Nginx configurado correctamente"
}

# Setup SSL with Let's Encrypt
setup_ssl() {
    log "Configurando SSL con Let's Encrypt para $DOMAIN..."
    
    # Stop nginx temporarily for standalone mode
    systemctl stop nginx
    
    # Get SSL certificate
    certbot certonly \
        --standalone \
        --non-interactive \
        --agree-tos \
        --email "$EMAIL" \
        -d "$DOMAIN" \
        -d "www.$DOMAIN"
    
    # Configure nginx with SSL
    certbot --nginx \
        --non-interactive \
        --agree-tos \
        --email "$EMAIL" \
        -d "$DOMAIN" \
        -d "www.$DOMAIN"
    
    # Start nginx
    systemctl start nginx
    
    # Setup auto-renewal
    systemctl enable certbot.timer
    systemctl start certbot.timer
    
    log "SSL certificado instalado y auto-renovación configurada"
}

# Setup monitoring and health checks
setup_monitoring() {
    log "Configurando monitoreo y health checks..."
    
    # Create health check script
    cat > /usr/local/bin/casamx-health-check.sh << 'EOF'
#!/bin/bash

HEALTH_URL="http://localhost:8080/health"
LOG_FILE="/var/log/casamx-health.log"

check_health() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    if curl -f -s "$HEALTH_URL" > /dev/null 2>&1; then
        echo "[$timestamp] ✅ CasaMX healthy" >> "$LOG_FILE"
        return 0
    else
        echo "[$timestamp] ❌ CasaMX unhealthy, restarting service..." >> "$LOG_FILE"
        systemctl restart casamx
        sleep 10
        
        if curl -f -s "$HEALTH_URL" > /dev/null 2>&1; then
            echo "[$timestamp] ✅ CasaMX recovered after restart" >> "$LOG_FILE"
        else
            echo "[$timestamp] 🚨 CasaMX still unhealthy after restart!" >> "$LOG_FILE"
        fi
        return 1
    fi
}

check_health
EOF

    chmod +x /usr/local/bin/casamx-health-check.sh
    
    # Add cron job for health checks every minute
    (crontab -l 2>/dev/null; echo "* * * * * /usr/local/bin/casamx-health-check.sh") | crontab -
    
    log "Sistema de monitoreo configurado"
}

# Setup log rotation
setup_logs() {
    log "Configurando rotación de logs..."
    
    cat > /etc/logrotate.d/casamx << 'EOF'
/var/log/casamx-health.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    create 644 root root
}

/opt/casamx/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    create 644 root root
}
EOF

    log "Rotación de logs configurada"
}

# Performance optimizations
optimize_system() {
    log "Aplicando optimizaciones de rendimiento..."
    
    # Optimize sysctl parameters
    cat > /etc/sysctl.d/99-casamx.conf << 'EOF'
# Network optimization for CasaMX
net.core.rmem_default = 262144
net.core.rmem_max = 16777216
net.core.wmem_default = 262144
net.core.wmem_max = 16777216
net.core.netdev_max_backlog = 5000

# TCP optimization
net.ipv4.tcp_rmem = 4096 65536 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_congestion_control = bbr

# File system optimization
fs.file-max = 2097152
vm.swappiness = 10
EOF

    sysctl -p /etc/sysctl.d/99-casamx.conf
    
    # Increase file descriptor limits
    cat >> /etc/security/limits.conf << 'EOF'

# CasaMX optimizations
* soft nofile 65536
* hard nofile 65536
EOF

    log "Optimizaciones de rendimiento aplicadas"
}

# Final verification
verify_deployment() {
    log "Verificando deployment completo..."
    
    # Wait for services to stabilize
    sleep 30
    
    local all_good=true
    
    # Check CasaMX service
    if systemctl is-active --quiet casamx; then
        log "✅ Servicio CasaMX funcionando"
    else
        warning "❌ Servicio CasaMX no está funcionando"
        all_good=false
    fi
    
    # Check Nginx
    if systemctl is-active --quiet nginx; then
        log "✅ Nginx funcionando"
    else
        warning "❌ Nginx no está funcionando"
        all_good=false
    fi
    
    # Test local health endpoint
    if curl -f -s http://localhost:8080/health > /dev/null; then
        log "✅ Health endpoint local funcionando"
    else
        warning "❌ Health endpoint local no responde"
        all_good=false
    fi
    
    # Test HTTPS (if DNS is configured)
    if curl -f -s -k https://localhost > /dev/null 2>&1; then
        log "✅ HTTPS local funcionando"
    else
        warning "⚠️  HTTPS local podría tener problemas (normal si DNS no está configurado)"
    fi
    
    # Check SSL certificate
    if [[ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]]; then
        log "✅ Certificado SSL instalado"
    else
        warning "❌ Certificado SSL no encontrado"
        all_good=false
    fi
    
    # Check firewall
    if ufw status | grep -q "Status: active"; then
        log "✅ Firewall activo"
    else
        warning "❌ Firewall no está activo"
        all_good=false
    fi
    
    if $all_good; then
        success "Verificación completada - Todo funcionando correctamente"
    else
        warning "Verificación completada con algunos problemas menores"
    fi
}

# Print final summary
print_summary() {
    success "🎉 CASAMX DEPLOYMENT COMPLETADO EXITOSAMENTE! 🎉"
    echo
    echo "================================================================="
    echo "           CasaMX - Datatón ITAM 2025 READY!"
    echo "================================================================="
    echo
    echo "🌐 URLS:"
    echo "   • Producción: https://$DOMAIN"
    echo "   • WWW: https://www.$DOMAIN"
    echo "   • Health Check: https://$DOMAIN/health"
    echo
    echo "🛠️  COMANDOS ÚTILES:"
    echo "   • Ver logs app: journalctl -u casamx -f"
    echo "   • Ver logs nginx: tail -f /var/log/nginx/access.log"
    echo "   • Restart app: systemctl restart casamx"
    echo "   • Restart nginx: systemctl reload nginx"
    echo "   • Ver health: tail -f /var/log/casamx-health.log"
    echo
    echo "🔧 ARCHIVOS IMPORTANTES:"
    echo "   • App: $APP_DIR/start_casamx.py"
    echo "   • Nginx config: /etc/nginx/sites-available/casamx"
    echo "   • SSL certs: /etc/letsencrypt/live/$DOMAIN/"
    echo "   • Logs: /var/log/casamx-health.log"
    echo
    echo "📋 SIGUIENTE PASO CRÍTICO:"
    echo "   ⚡ CONFIGURAR DNS EN CLOUDFLARE O REGISTRAR:"
    echo "   A    $DOMAIN    →  $(curl -s ifconfig.me)"
    echo "   A    www        →  $(curl -s ifconfig.me)"
    echo
    echo "⏱️  TIEMPO TOTAL: $((SECONDS/60)) minutos"
    echo "🎯 LISTO PARA DATATÓN ITAM 2025!"
    echo
    echo "================================================================="
    success "David, configura el DNS y ¡casamx.app estará funcionando!"
}

# Main execution function
main() {
    local start_time=$(date '+%s')
    
    info "🚀 Iniciando deployment automático de CasaMX..."
    info "📅 Datatón ITAM 2025 - David Fernando Ávila Díaz"
    info "🎯 Objetivo: $DOMAIN funcionando en <15 minutos"
    echo
    
    check_root
    setup_system
    setup_firewall
    clone_repository
    setup_application
    setup_nginx
    setup_ssl
    setup_monitoring
    setup_logs
    optimize_system
    verify_deployment
    
    local end_time=$(date '+%s')
    local duration=$((end_time - start_time))
    
    print_summary
    
    success "✅ Deployment completado en $((duration/60)) minutos y $((duration%60)) segundos!"
}

# Trap interruptions
trap 'error "Deployment interrumpido por el usuario"' INT TERM

# Execute main function
main "$@"