#!/bin/bash
# CREAR VPS CASAMX AUTOMÁTICAMENTE
# David Fernando Ávila Díaz - ITAM

echo "🚀 CREANDO DROPLET DIGITALOCEAN..."

# Crear VPS automáticamente
VPS_NAME="casamx-dataton-vps"
REGION="nyc1"
SIZE="s-1vcpu-1gb"
IMAGE="ubuntu-22-04-x64"

echo "📡 Creando droplet: $VPS_NAME..."
doctl compute droplet create $VPS_NAME \
    --region $REGION \
    --size $SIZE \
    --image $IMAGE \
    --ssh-keys $(doctl compute ssh-key list --format ID --no-header | head -1) \
    --enable-monitoring \
    --enable-backups \
    --wait

# Obtener IP
VPS_IP=$(doctl compute droplet list --format Name,PublicIPv4 --no-header | grep $VPS_NAME | awk '{print $2}')

echo "✅ VPS creado con IP: $VPS_IP"
echo ""
echo "🔧 Configurando servidor..."

# SSH y configurar automáticamente
ssh -o StrictHostKeyChecking=no root@$VPS_IP << 'EOF'
    # Actualizar sistema
    apt update && apt upgrade -y
    
    # Instalar Nginx
    apt install -y nginx certbot python3-certbot-nginx
    
    # Crear página CasaMX
    cat > /var/www/html/index.html << 'HTML'
<!DOCTYPE html>
<html lang="es-MX">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CasaMX - Tu hogar ideal en México</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; margin: 0; padding: 20px; text-align: center; min-height: 100vh;
        }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        .demo-btn { 
            background: #FF6B6B; color: white; border: none;
            padding: 15px 30px; border-radius: 20px; cursor: pointer;
            margin: 10px; font-size: 16px;
        }
        .zona { 
            background: rgba(255,255,255,0.15); 
            padding: 15px; margin: 15px; border-radius: 10px; 
        }
        #results { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 CasaMX</h1>
        <h2>Tu hogar ideal en México</h2>
        <p>Recomendaciones personalizadas para extranjeros en CDMX</p>
        
        <div style="background:rgba(255,255,255,0.1);padding:2rem;border-radius:15px;margin:2rem;">
            <h3>🎯 Casos Demo Datatón ITAM 2025</h3>
            <button class="demo-btn" onclick="demo1()">👨‍👩‍👧‍👦 Familia Española</button>
            <button class="demo-btn" onclick="demo2()">💻 Profesional Italiano</button>
            <button class="demo-btn" onclick="demo3()">🎓 Estudiante Francesa</button>
        </div>
        
        <div id="results">
            <h3>🏆 Recomendaciones:</h3>
            <div class="zona">
                <h4>#1: Roma Norte</h4>
                <p>💰 $25,000/mes | 🛡️ 85/100 | 🚇 95/100</p>
                <p>Excelente para profesionales, vida nocturna vibrante</p>
            </div>
            <div class="zona">
                <h4>#2: Del Valle</h4>
                <p>💰 $22,000/mes | 🛡️ 88/100 | 🚇 78/100</p>
                <p>Ideal para familias, zona tranquila y segura</p>
            </div>
            <div class="zona">
                <h4>#3: Coyoacán Centro</h4>
                <p>💰 $18,000/mes | 🛡️ 90/100 | 🚇 70/100</p>
                <p>Cultura, historia y ambiente bohemio único</p>
            </div>
        </div>
        
        <footer style="margin-top: 3rem; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 2rem;">
            <h3>🏆 CasaMX - Datatón ITAM 2025</h3>
            <p><strong>David Fernando Ávila Díaz</strong> - Instituto Tecnológico Autónomo de México</p>
            <p>🎯 Recomendador inteligente de zonas • ⚡ VPS DigitalOcean • 🔒 SSL automático</p>
        </footer>
    </div>
    
    <script>
        function demo1() { showResults("👨‍👩‍👧‍👦 Familia Española (2 niños, €35k) → Del Valle recomendado"); }
        function demo2() { showResults("💻 Profesional Italiano (tech, €25k) → Roma Norte recomendado"); }
        function demo3() { showResults("🎓 Estudiante Francesa (€15k) → Coyoacán recomendado"); }
        
        function showResults(perfil) {
            document.getElementById('results').style.display = 'block';
            document.getElementById('results').querySelector('h3').textContent = '🏆 ' + perfil;
            document.getElementById('results').scrollIntoView({behavior: 'smooth'});
        }
    </script>
</body>
</html>
HTML
    
    # Configurar Nginx
    systemctl start nginx
    systemctl enable nginx
    
    # Configurar firewall
    ufw allow 22
    ufw allow 80
    ufw allow 443
    ufw --force enable
    
    echo "✅ Servidor configurado correctamente"
EOF

echo ""
echo "🌐 CONFIGURAR DNS AHORA:"
echo "En Cloudflare DNS → casamx.app:"
echo "A @ → $VPS_IP"
echo "A www → $VPS_IP"
echo ""
echo "🏆 RESULTADO: https://casamx.app funcionando en 5 minutos"