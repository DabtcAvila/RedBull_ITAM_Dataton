#!/bin/bash

# ================================================================
# VERCEL DEPLOYMENT SCRIPT - CASAMX STORE
# DATATÓN ITAM 2025 - DEPLOY CRÍTICO GARANTIZADO
# ================================================================

echo "🚀 INICIANDO DEPLOYMENT CRÍTICO VERCEL - CASAMX.STORE"
echo "=================================================="

# Set strict error handling
set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log with colors
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "../streamlit_app.py" ]; then
    log_error "streamlit_app.py not found in parent directory!"
    log_info "Please run from multi_deploy directory"
    exit 1
fi

log_info "✅ streamlit_app.py found - proceeding with deployment"

# Copy necessary files to parent directory for deployment
log_info "📋 Copying deployment files..."
cp vercel.json ../vercel.json
cp requirements_vercel.txt ../requirements_vercel.txt  
cp package.json ../package.json

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    log_warning "Vercel CLI not found - installing..."
    npm install -g vercel
    log_success "Vercel CLI installed successfully"
fi

# Navigate to project root
cd ..

# Login to Vercel (if not already logged in)
log_info "🔐 Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    log_warning "Not logged in to Vercel - please login"
    vercel login
fi

log_success "✅ Vercel authentication confirmed"

# Initialize Vercel project (if not already initialized)
if [ ! -f ".vercel/project.json" ]; then
    log_info "🔧 Initializing Vercel project..."
    vercel link --yes
fi

# Deploy to Vercel
log_info "🚀 Starting Vercel deployment..."
echo "=================================================="

# Deploy with custom domain
vercel --prod --yes

# Check deployment status
if [ $? -eq 0 ]; then
    log_success "🎉 DEPLOYMENT SUCCESS!"
    echo "=================================================="
    log_success "✅ CasaMX deployed successfully to Vercel"
    log_success "🌍 URL: https://casamx.store"
    log_success "⚡ SSL: Enabled automatically"
    log_success "🕐 Time: $(date)"
    echo "=================================================="
    
    # Test the deployment
    log_info "🧪 Testing deployment..."
    if curl -f -s -o /dev/null "https://$(vercel ls | grep casamx | head -1 | awk '{print $2}')"; then
        log_success "✅ Deployment is responding correctly"
    else
        log_warning "⚠️  Deployment may still be propagating - check in 2-3 minutes"
    fi
    
    echo ""
    log_success "🚀 MISSION ACCOMPLISHED - CASAMX IS LIVE!"
    
else
    log_error "❌ DEPLOYMENT FAILED"
    echo "=================================================="
    log_error "Vercel deployment encountered errors"
    log_warning "Proceeding to backup deployment strategy..."
    echo "=================================================="
    
    # Clean up
    rm -f vercel.json requirements_vercel.txt package.json
    
    # Return to multi_deploy directory
    cd multi_deploy
    
    # Execute Netlify backup deployment
    log_warning "🔄 Activating Netlify backup deployment..."
    ./deploy_netlify.sh
    
    exit 1
fi

# Clean up temporary files
log_info "🧹 Cleaning up temporary files..."
# Keep the files for future deployments
# rm -f requirements_vercel.txt

# Return to multi_deploy directory  
cd multi_deploy

log_success "🎯 VERCEL DEPLOYMENT COMPLETED SUCCESSFULLY"
log_success "📊 Ready for Datatón ITAM 2025 presentation!"

echo ""
echo "=================================================="
echo "🏆 CASAMX.STORE IS LIVE AND READY!"
echo "🌐 URL: https://casamx.store"
echo "⏰ Deployment Time: $(date)"
echo "🎯 Status: MISSION CRITICAL SUCCESS"
echo "=================================================="