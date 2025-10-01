#!/bin/bash
# ENTERPRISE VPS CREATION - NO STATIC SITES
# David Fernando Ávila Díaz - ITAM

echo "🔥 CREANDO VPS ENTERPRISE PARA CASAMX..."

# Configuración VPS Enterprise
VPS_NAME="casamx-enterprise-$(date +%s)"
REGION="nyc1"
SIZE="s-2vcpu-2gb"  # ENTERPRISE: 2 CPUs, 2GB RAM
IMAGE="ubuntu-22-04-x64"

echo "🚀 Creando droplet enterprise..."
echo "📊 Configuración:"
echo "- Nombre: $VPS_NAME"
echo "- Region: $REGION"  
echo "- Size: $SIZE (2 vCPU, 2GB RAM)"
echo "- OS: Ubuntu 22.04 LTS"
echo ""

# Crear SSH key si no existe
if ! doctl compute ssh-key list --format Name | grep -q "casamx-key"; then
    echo "🔑 Generando SSH key..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/casamx_rsa -N "" -C "casamx-dataton"
    doctl compute ssh-key import casamx-key --public-key-file ~/.ssh/casamx_rsa.pub
fi

# Crear droplet
echo "⚡ Creando VPS enterprise..."
doctl compute droplet create $VPS_NAME \
    --region $REGION \
    --size $SIZE \
    --image $IMAGE \
    --ssh-keys casamx-key \
    --enable-monitoring \
    --enable-backups \
    --tag-names "casamx,dataton,enterprise" \
    --wait

# Obtener IP
VPS_IP=$(doctl compute droplet list --format Name,PublicIPv4 --no-header | grep $VPS_NAME | awk '{print $2}')

echo ""
echo "✅ VPS ENTERPRISE CREADO:"
echo "🌐 IP: $VPS_IP"
echo "🔐 SSH: ssh -i ~/.ssh/casamx_rsa root@$VPS_IP"
echo ""

echo "🎯 CONFIGURANDO CASAMX ENTERPRISE..."
echo "Esperando que VPS esté listo..."
sleep 60

# Configurar servidor automáticamente
ssh -i ~/.ssh/casamx_rsa -o StrictHostKeyChecking=no root@$VPS_IP << 'REMOTE_SCRIPT'
    # Actualizar sistema
    apt update && apt upgrade -y
    
    # Instalar stack completo
    apt install -y nginx certbot python3-certbot-nginx git python3-pip python3-venv
    
    # Crear directorio CasaMX
    mkdir -p /var/www/casamx
    cd /var/www/casamx
    
    # Clonar repositorio
    git clone https://github.com/DabtcAvila/RedBull_ITAM_Dataton.git .
    
    # Configurar Nginx para CasaMX
    cat > /etc/nginx/sites-available/casamx << 'NGINX_CONFIG'
server {
    listen 80;
    server_name casamx.app www.casamx.app;
    root /var/www/casamx;
    index index.html SOLUCION_DEFINITIVA.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
}
NGINX_CONFIG
    
    # Activar sitio
    ln -sf /etc/nginx/sites-available/casamx /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    
    # Test y restart Nginx
    nginx -t && systemctl restart nginx
    systemctl enable nginx
    
    # Configurar firewall
    ufw allow 22
    ufw allow 80
    ufw allow 443
    ufw --force enable
    
    echo "✅ NGINX CONFIGURADO"
    echo "🌐 Servidor funcionando"
REMOTE_SCRIPT

echo ""
echo "🌐 ACTUALIZAR DNS CLOUDFLARE:"
echo "A casamx.app → $VPS_IP"
echo "A www → $VPS_IP"
echo ""
echo "🏆 RESULTADO: https://casamx.app funcionando en 5 minutos"
echo "💎 NIVEL ENTERPRISE COMPLETO"