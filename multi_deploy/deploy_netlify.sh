#!/bin/bash

# ================================================================
# NETLIFY DEPLOYMENT SCRIPT - CASAMX STORE BACKUP
# DATATÓN ITAM 2025 - BACKUP DEPLOYMENT GARANTIZADO
# ================================================================

echo "🔄 INICIANDO BACKUP DEPLOYMENT NETLIFY - CASAMX.STORE"
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

log_info "✅ streamlit_app.py found - proceeding with Netlify deployment"

# Copy necessary files to parent directory for deployment
log_info "📋 Copying Netlify deployment files..."
cp netlify.toml ../netlify.toml
cp requirements_netlify.txt ../requirements_netlify.txt  
cp _redirects ../_redirects

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    log_warning "Netlify CLI not found - installing..."
    npm install -g netlify-cli
    log_success "Netlify CLI installed successfully"
fi

# Navigate to project root
cd ..

# Login to Netlify (if not already logged in)
log_info "🔐 Checking Netlify authentication..."
if ! netlify status &> /dev/null; then
    log_warning "Not logged in to Netlify - please login"
    netlify login
fi

log_success "✅ Netlify authentication confirmed"

# Initialize Netlify site (if not already initialized)
if [ ! -f ".netlify/state.json" ]; then
    log_info "🔧 Initializing Netlify site..."
    netlify init
fi

# Build the application
log_info "🏗️  Building application..."
echo "=================================================="

# Create a simple build process
mkdir -p dist
cp streamlit_app.py dist/
cp -r data/ dist/ 2>/dev/null || log_warning "No data directory found"

# Deploy to Netlify
log_info "🚀 Starting Netlify deployment..."
echo "=================================================="

# Deploy to production
netlify deploy --prod --dir=dist

# Check deployment status
if [ $? -eq 0 ]; then
    log_success "🎉 NETLIFY DEPLOYMENT SUCCESS!"
    echo "=================================================="
    log_success "✅ CasaMX deployed successfully to Netlify"
    
    # Get the deployment URL
    DEPLOY_URL=$(netlify status | grep "Website URL" | awk '{print $3}')
    
    log_success "🌍 URL: $DEPLOY_URL"
    log_success "⚡ SSL: Enabled automatically"
    log_success "🕐 Time: $(date)"
    echo "=================================================="
    
    # Test the deployment
    log_info "🧪 Testing deployment..."
    if curl -f -s -o /dev/null "$DEPLOY_URL"; then
        log_success "✅ Deployment is responding correctly"
    else
        log_warning "⚠️  Deployment may still be propagating - check in 2-3 minutes"
    fi
    
    echo ""
    log_success "🚀 NETLIFY BACKUP MISSION ACCOMPLISHED!"
    log_info "Next step: Configure custom domain casamx.store in Netlify dashboard"
    
else
    log_error "❌ NETLIFY DEPLOYMENT FAILED"
    echo "=================================================="
    log_error "Netlify deployment encountered errors"
    log_warning "Proceeding to GitHub Pages emergency deployment..."
    echo "=================================================="
    
    # Clean up
    rm -f netlify.toml requirements_netlify.txt _redirects
    rm -rf dist
    
    # Return to multi_deploy directory
    cd multi_deploy
    
    # Execute GitHub Pages emergency deployment
    log_warning "🆘 Activating GitHub Pages emergency deployment..."
    ./deploy_github_pages.sh
    
    exit 1
fi

# Clean up temporary files
log_info "🧹 Cleaning up..."
# Keep deployment files for future use
rm -rf dist

# Return to multi_deploy directory  
cd multi_deploy

log_success "🎯 NETLIFY BACKUP DEPLOYMENT COMPLETED"
log_success "📊 Ready as backup for Datatón ITAM 2025!"

echo ""
echo "=================================================="
echo "🔄 NETLIFY BACKUP DEPLOYMENT SUCCESSFUL!"
echo "🌐 URL: Available in Netlify dashboard"
echo "⏰ Deployment Time: $(date)"
echo "🎯 Status: BACKUP MISSION SUCCESS"
echo "=================================================="

# Instructions for domain setup
echo ""
log_info "📋 NEXT STEPS FOR DOMAIN SETUP:"
log_info "1. Open Netlify dashboard: https://app.netlify.com"
log_info "2. Go to Site settings → Domain management"
log_info "3. Add custom domain: casamx.store"
log_info "4. Update DNS records as instructed"
log_info "5. SSL will be automatically provisioned"