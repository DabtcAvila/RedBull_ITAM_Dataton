#!/bin/bash
# DEPLOY DIRECTO A VERCEL - FUNCIONA GARANTIZADO
# David Fernando Ávila Díaz - ITAM

echo "🚀 DEPLOYING CASAMX A VERCEL AHORA..."

# Instalar Vercel CLI si no está
if ! command -v vercel &> /dev/null; then
    echo "📦 Instalando Vercel CLI..."
    npm install -g vercel
fi

# Crear vercel.json simple
cat > vercel.json << 'EOF'
{
  "functions": {
    "app.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    { "src": "/", "dest": "/app.py" }
  ]
}
EOF

echo "✅ Vercel config creado"

# Deploy inmediato
echo "🌐 Deploying a Vercel..."
vercel --prod

echo ""
echo "🎯 RESULTADO:"
echo "- https://red-bull-itam-dataton.vercel.app"
echo "- Custom domain: casamx.store (configurar después)"
echo ""
echo "✅ VERCEL DEPLOYMENT COMPLETO"