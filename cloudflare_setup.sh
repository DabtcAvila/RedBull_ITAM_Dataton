#!/bin/bash
# CasaMX Cloudflare Tunnel Setup
# David Fernando Ávila Díaz - ITAM

echo "🚀 Configurando Cloudflare Tunnel para CasaMX"

# 1. Instalar cloudflared (si no está)
if ! command -v cloudflared &> /dev/null; then
    echo "📦 Instalando cloudflared..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install cloudflared
    else
        curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
        chmod +x cloudflared
        sudo mv cloudflared /usr/local/bin/
    fi
fi

# 2. Login a Cloudflare (abrirá browser)
echo "🔐 Autenticando con Cloudflare..."
cloudflared tunnel login

# 3. Crear tunnel para CasaMX
echo "🌐 Creando tunnel CasaMX..."
cloudflared tunnel create casamx-dataton

# 4. Crear archivo de configuración
echo "⚙️ Creando configuración..."
cat > ~/.cloudflared/config.yml << EOF
tunnel: casamx-dataton
credentials-file: ~/.cloudflared/casamx-dataton.json

ingress:
  - hostname: casamx.store
    service: http://localhost:8502
  - hostname: www.casamx.store
    service: http://localhost:8502
  - service: http_status:404
EOF

echo "✅ Tunnel configurado!"
echo ""
echo "🎯 SIGUIENTE PASO:"
echo "1. Ve a Cloudflare Dashboard → DNS"
echo "2. Añade tu dominio casamx.store (si no está)"
echo "3. Ejecuta: cloudflare_run_tunnel.sh"
echo ""
echo "🌐 Tu app estará en:"
echo "   - https://casamx.store"
echo "   - https://www.casamx.store"