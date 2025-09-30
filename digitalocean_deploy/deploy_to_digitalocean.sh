#!/bin/bash

# CasaMX DigitalOcean Enterprise Deployment Script
# Automatiza deployment completo en 30-45 minutos
# Para Datatón ITAM 2025

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="casamx.store"
EMAIL="tu-email@example.com"  # Cambiar por email real
APP_DIR="/opt/casamx"
GITHUB_REPO="https://github.com/tu-usuario/RedBull_ITAM_Dataton.git"  # Cambiar por repo real

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "Este script debe ejecutarse como root. Usa: sudo $0"
    fi
}

# System update and dependencies
setup_system() {
    log "Actualizando sistema y instalando dependencias..."
    
    # Update system
    apt update && apt upgrade -y
    
    # Install essential packages
    apt install -y \
        curl \
        wget \
        git \
        vim \
        htop \
        ufw \
        fail2ban \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
    
    log "Sistema actualizado correctamente"
}

# Install Docker
install_docker() {
    log "Instalando Docker y Docker Compose..."
    
    # Add Docker GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add Docker repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Start and enable Docker
    systemctl start docker
    systemctl enable docker
    
    # Add current user to docker group
    usermod -aG docker $USER
    
    # Install Docker Compose standalone
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    log "Docker instalado correctamente"
}

# Install Nginx
install_nginx() {
    log "Instalando y configurando Nginx..."
    
    apt install -y nginx
    systemctl start nginx
    systemctl enable nginx
    
    # Create nginx user if not exists
    if ! id nginx >/dev/null 2>&1; then
        useradd -r -s /bin/false nginx
    fi
    
    log "Nginx instalado correctamente"
}

# Setup firewall
setup_firewall() {
    log "Configurando firewall (UFW)..."
    
    # Reset UFW
    ufw --force reset
    
    # Default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH, HTTP, HTTPS
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    
    # Allow monitoring (internal only)
    ufw allow from 10.0.0.0/8 to any port 9090
    ufw allow from 127.0.0.1 to any port 3100
    
    # Enable firewall
    ufw --force enable
    
    log "Firewall configurado correctamente"
}

# Clone repository
clone_repository() {
    log "Clonando repositorio CasaMX..."
    
    if [[ -d "$APP_DIR" ]]; then
        warning "Directorio $APP_DIR ya existe, actualizando..."
        cd "$APP_DIR"
        git pull origin main
    else
        git clone "$GITHUB_REPO" "$APP_DIR"
        cd "$APP_DIR"
    fi
    
    # Copy deployment files
    if [[ -d "digitalocean_deploy" ]]; then
        cp -r digitalocean_deploy/* .
    fi
    
    log "Repositorio clonado correctamente"
}

# Setup SSL with Let's Encrypt
setup_ssl() {
    log "Configurando SSL con Let's Encrypt..."
    
    # Install Certbot
    apt install -y certbot python3-certbot-nginx
    
    # Stop nginx temporarily
    systemctl stop nginx
    
    # Get SSL certificate
    certbot certonly --standalone -d "$DOMAIN" -d "www.$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive
    
    # Create SSL config for nginx
    mkdir -p /etc/nginx/ssl
    
    # Generate Diffie-Hellman parameters
    openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
    
    # Setup auto-renewal
    systemctl enable certbot.timer
    systemctl start certbot.timer
    
    log "SSL configurado correctamente"
}

# Setup application
setup_application() {
    log "Configurando aplicación CasaMX..."
    
    cd "$APP_DIR"
    
    # Create required directories
    mkdir -p data logs ssl
    
    # Generate secret key
    SECRET_KEY=$(openssl rand -hex 32)
    
    # Create environment file
    cat > .env << EOF
ENV=production
SECRET_KEY=$SECRET_KEY
DATABASE_URL=sqlite:///data/casamx.db
REDIS_URL=redis://redis:6379
REDIS_PASSWORD=casamx$(openssl rand -hex 8)
DOMAIN=$DOMAIN
EMAIL=$EMAIL
EOF

    # Set permissions
    chown -R www-data:www-data data logs
    chmod -R 755 data logs
    
    log "Aplicación configurada correctamente"
}

# Build and start containers
start_application() {
    log "Construyendo y iniciando contenedores..."
    
    cd "$APP_DIR"
    
    # Build and start containers
    docker-compose up -d --build
    
    # Wait for containers to be healthy
    log "Esperando que los contenedores estén saludables..."
    sleep 30
    
    # Check container health
    for container in casamx-app casamx-redis; do
        if docker ps --filter "name=$container" --filter "status=running" | grep -q "$container"; then
            log "✅ $container está funcionando"
        else
            error "❌ $container no está funcionando correctamente"
        fi
    done
    
    log "Aplicación iniciada correctamente"
}

# Configure Nginx
configure_nginx() {
    log "Configurando Nginx como reverse proxy..."
    
    cd "$APP_DIR"
    
    # Copy nginx configuration
    cp nginx.conf /etc/nginx/nginx.conf
    
    # Test nginx configuration
    nginx -t
    
    # Start nginx
    systemctl start nginx
    systemctl reload nginx
    
    log "Nginx configurado correctamente"
}

# Setup monitoring
setup_monitoring() {
    log "Configurando sistema de monitoreo..."
    
    cd "$APP_DIR"
    
    # Create Prometheus config
    cat > prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'casamx'
    static_configs:
      - targets: ['casamx-app:8000']
  
  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:8080']

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
EOF

    # Create systemd service for health monitoring
    cat > /etc/systemd/system/casamx-monitor.service << 'EOF'
[Unit]
Description=CasaMX Health Monitor
After=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/casamx
ExecStart=/opt/casamx/scripts/health_monitor.sh
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF

    # Create health monitor script
    mkdir -p scripts
    cat > scripts/health_monitor.sh << 'EOF'
#!/bin/bash
while true; do
    if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "$(date): CasaMX health check failed, restarting containers..."
        cd /opt/casamx
        docker-compose restart casamx-app
    fi
    sleep 60
done
EOF

    chmod +x scripts/health_monitor.sh
    
    # Enable health monitoring
    systemctl enable casamx-monitor
    systemctl start casamx-monitor
    
    log "Monitoreo configurado correctamente"
}

# Setup log rotation
setup_logs() {
    log "Configurando rotación de logs..."
    
    cat > /etc/logrotate.d/casamx << 'EOF'
/opt/casamx/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    create 644 www-data www-data
    postrotate
        docker-compose -f /opt/casamx/docker-compose.yml restart casamx-app
    endscript
}
EOF

    log "Rotación de logs configurada"
}

# Performance optimizations
optimize_system() {
    log "Aplicando optimizaciones de rendimiento..."
    
    # Increase file descriptor limits
    cat >> /etc/security/limits.conf << 'EOF'
* soft nofile 65536
* hard nofile 65536
* soft nproc 65536
* hard nproc 65536
EOF

    # Optimize sysctl parameters
    cat > /etc/sysctl.d/99-casamx.conf << 'EOF'
# Network optimization
net.core.rmem_default = 262144
net.core.rmem_max = 16777216
net.core.wmem_default = 262144
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 65536 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_congestion_control = bbr

# File system
fs.file-max = 2097152
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
EOF

    sysctl -p /etc/sysctl.d/99-casamx.conf
    
    log "Optimizaciones aplicadas"
}

# Create backup script
setup_backup() {
    log "Configurando sistema de backup..."
    
    mkdir -p /opt/backups
    
    cat > /opt/backups/backup_casamx.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/opt/casamx"

# Create backup directory
mkdir -p "$BACKUP_DIR/$DATE"

# Backup database
cp "$APP_DIR/data/casamx.db" "$BACKUP_DIR/$DATE/"

# Backup configuration
tar -czf "$BACKUP_DIR/$DATE/config.tar.gz" -C "$APP_DIR" .env docker-compose.yml nginx.conf

# Backup logs (last 7 days)
find "$APP_DIR/logs" -name "*.log" -mtime -7 -exec cp {} "$BACKUP_DIR/$DATE/" \;

# Compress everything
tar -czf "$BACKUP_DIR/casamx_backup_$DATE.tar.gz" -C "$BACKUP_DIR" "$DATE"
rm -rf "$BACKUP_DIR/$DATE"

# Keep only last 7 backups
find "$BACKUP_DIR" -name "casamx_backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: casamx_backup_$DATE.tar.gz"
EOF

    chmod +x /opt/backups/backup_casamx.sh
    
    # Add cron job for daily backups
    (crontab -l 2>/dev/null; echo "0 2 * * * /opt/backups/backup_casamx.sh >> /var/log/casamx_backup.log 2>&1") | crontab -
    
    log "Sistema de backup configurado"
}

# Final verification
verify_deployment() {
    log "Verificando deployment..."
    
    # Wait for services to stabilize
    sleep 30
    
    # Test HTTP redirect
    if curl -I -s http://"$DOMAIN" | grep -q "301"; then
        log "✅ HTTP redirect funcionando"
    else
        warning "⚠️  HTTP redirect podría no estar funcionando"
    fi
    
    # Test HTTPS
    if curl -I -s https://"$DOMAIN" | grep -q "200"; then
        log "✅ HTTPS funcionando"
    else
        error "❌ HTTPS no está funcionando"
    fi
    
    # Test API
    if curl -s https://"$DOMAIN"/api/ | grep -q "CasaMX"; then
        log "✅ API funcionando"
    else
        warning "⚠️  API podría tener problemas"
    fi
    
    # Test SSL certificate
    if echo | openssl s_client -connect "$DOMAIN":443 2>/dev/null | grep -q "Verify return code: 0"; then
        log "✅ Certificado SSL válido"
    else
        warning "⚠️  Certificado SSL podría tener problemas"
    fi
    
    # Check Docker containers
    if docker ps | grep -q "casamx"; then
        log "✅ Contenedores Docker funcionando"
    else
        error "❌ Contenedores Docker no están funcionando"
    fi
    
    log "Verificación completada"
}

# Print final information
print_summary() {
    log "🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE! 🎉"
    echo
    echo "========================================"
    echo "  CasaMX - Deployment Summary"
    echo "========================================"
    echo
    echo "🌐 URL Principal: https://$DOMAIN"
    echo "🔧 API Endpoint: https://$DOMAIN/api"
    echo "📚 API Docs: https://$DOMAIN/api/docs"
    echo "📊 Monitoring: https://$DOMAIN:9090 (Prometheus)"
    echo
    echo "🔐 Credenciales:"
    echo "   - SSH: puerto 22"
    echo "   - Nginx status: http://localhost:8080/nginx_status"
    echo "   - App logs: docker logs -f casamx-app"
    echo
    echo "🛠️  Comandos útiles:"
    echo "   - Restart app: cd $APP_DIR && docker-compose restart"
    echo "   - View logs: docker-compose logs -f"
    echo "   - SSL renewal: certbot renew"
    echo "   - Backup: /opt/backups/backup_casamx.sh"
    echo
    echo "📈 Performance Test:"
    echo "   curl -w \"@curl-format.txt\" -s -o /dev/null https://$DOMAIN"
    echo
    echo "🚀 TIEMPO TOTAL: $(date)"
    echo "🎯 LISTO PARA EL DATATÓN ITAM 2025!"
}

# Main execution
main() {
    log "🚀 Iniciando deployment de CasaMX en DigitalOcean..."
    
    check_root
    setup_system
    install_docker
    install_nginx
    setup_firewall
    clone_repository
    setup_ssl
    setup_application
    start_application
    configure_nginx
    setup_monitoring
    setup_logs
    optimize_system
    setup_backup
    verify_deployment
    print_summary
    
    log "✅ Deployment completado exitosamente en $(date)!"
}

# Handle interruption
trap 'error "Deployment interrumpido por el usuario"' INT TERM

# Run main function
main "$@"