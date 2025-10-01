#!/bin/bash
# 🚀 Deploy CasaMX to Cloudflare Workers
# David Fernando Ávila Díaz - ITAM

echo "🏠 DEPLOYING CASAMX TO CLOUDFLARE WORKERS..."

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "📦 Installing Wrangler CLI..."
    npm install -g wrangler
fi

# Login to Cloudflare (if not already)
echo "🔐 Checking Cloudflare authentication..."
wrangler auth list || wrangler login

# Deploy to production
echo "🚀 Deploying CasaMX Worker..."
wrangler publish --env production

# Add custom domain
echo "🌐 Configuring custom domain casamx.app..."
echo "⚠️  Manual step needed:"
echo "   1. Go to: https://dash.cloudflare.com/"
echo "   2. Workers → casamx-app → Triggers"
echo "   3. Add Custom Domain: casamx.app"

echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo "🌐 Worker URL: https://casamx-app.YOUR_USER.workers.dev"
echo "🎯 Custom domain: https://casamx.app (after DNS setup)"
echo ""
echo "🏠 CasaMX - Datatón ITAM 2025"
echo "👨‍💻 David Fernando Ávila Díaz"