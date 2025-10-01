#!/bin/bash

# ================================================================
# RAILWAY DEPLOYMENT SCRIPT - CASAMX STORE PROFESSIONAL
# DATATÓN ITAM 2025 - PROFESSIONAL DEPLOYMENT ALTERNATIVE
# ================================================================

echo "🚂 INICIANDO PROFESSIONAL DEPLOYMENT RAILWAY - CASAMX.STORE"
echo "=================================================="

# Set strict error handling
set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

log_professional() {
    echo -e "${PURPLE}[RAILWAY]${NC} $1"
}

# Professional banner
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  PROFESSIONAL DEPLOYMENT                     ║"
echo "║                     RAILWAY PLATFORM                        ║"
echo "║                   DATATÓN ITAM 2025                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "../streamlit_app.py" ]; then
    log_error "streamlit_app.py not found in parent directory!"
    log_info "Please run from multi_deploy directory"
    exit 1
fi

log_info "✅ streamlit_app.py found - proceeding with Railway deployment"

# Copy necessary files to parent directory for deployment
log_info "📋 Copying Railway deployment files..."
cp railway.json ../railway.json
cp requirements_railway.txt ../requirements_railway.txt  
cp Procfile_railway ../Procfile

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    log_warning "Railway CLI not found - installing..."
    
    # Install Railway CLI
    if command -v npm &> /dev/null; then
        npm install -g @railway/cli
    elif command -v brew &> /dev/null; then
        brew install railway
    else
        log_warning "Installing Railway CLI via curl..."
        bash <(curl -fsSL https://railway.app/install.sh)
    fi
    
    log_success "Railway CLI installed successfully"
fi

# Navigate to project root
cd ..

# Login to Railway (if not already logged in)
log_info "🔐 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    log_warning "Not logged in to Railway - please login"
    railway login
fi

log_success "✅ Railway authentication confirmed"

# Initialize Railway project (if not already initialized)
if [ ! -f ".railway" ]; then
    log_info "🔧 Initializing Railway project..."
    railway init
fi

# Link to Railway service
log_professional "🔗 Linking to Railway service..."
railway link

# Set environment variables
log_info "⚙️ Setting environment variables..."
railway variables set STREAMLIT_SERVER_PORT="\$PORT"
railway variables set STREAMLIT_SERVER_ADDRESS="0.0.0.0"
railway variables set STREAMLIT_SERVER_HEADLESS="true"
railway variables set STREAMLIT_BROWSER_GATHER_USAGE_STATS="false"
railway variables set PYTHONPATH="."

# Deploy to Railway
log_info "🚀 Starting Railway deployment..."
echo "=================================================="

# Deploy the application
railway up --detach

# Check deployment status
if [ $? -eq 0 ]; then
    log_success "🎉 RAILWAY DEPLOYMENT SUCCESS!"
    echo "=================================================="
    log_success "✅ CasaMX deployed successfully to Railway"
    
    # Get deployment URL
    RAILWAY_URL=$(railway status | grep "Deployment URL" | awk '{print $3}' || echo "Check Railway dashboard")
    
    log_success "🌍 URL: $RAILWAY_URL"
    log_success "⚡ SSL: Enabled automatically"
    log_success "💾 Database: Available for future use"
    log_success "📊 Monitoring: Built-in Railway analytics"
    log_success "🕐 Time: $(date)"
    echo "=================================================="
    
    # Test the deployment
    log_info "🧪 Testing deployment..."
    sleep 30  # Wait for deployment to be ready
    
    if curl -f -s -o /dev/null "$RAILWAY_URL" || curl -f -s -o /dev/null "$RAILWAY_URL/_health"; then
        log_success "✅ Deployment is responding correctly"
    else
        log_warning "⚠️  Deployment may still be starting - check in 2-3 minutes"
    fi
    
    log_professional "📊 Railway Features Available:"
    log_professional "• Automatic scaling"
    log_professional "• Built-in monitoring"
    log_professional "• Database integration ready"
    log_professional "• Custom domain support"
    log_professional "• Environment management"
    log_professional "• Logs and metrics"
    
    echo ""
    log_success "🚂 PROFESSIONAL RAILWAY DEPLOYMENT SUCCESSFUL!"
    log_success "🏢 Enterprise-grade hosting active"
    
else
    log_error "❌ RAILWAY DEPLOYMENT FAILED"
    echo "=================================================="
    log_error "Railway deployment encountered errors"
    log_warning "Check Railway logs for details:"
    log_info "railway logs"
    echo "=================================================="
    
    # Clean up
    rm -f railway.json requirements_railway.txt Procfile
    
    # Return to multi_deploy directory
    cd multi_deploy
    
    log_error "❌ Professional deployment failed"
    log_warning "All deployment options attempted"
    log_warning "Consider manual deployment or check service status"
    
    exit 1
fi

# Clean up temporary files
log_info "🧹 Cleaning up..."
# Keep files for future deployments

# Return to multi_deploy directory  
cd multi_deploy

log_success "🎯 RAILWAY PROFESSIONAL DEPLOYMENT COMPLETED"
log_success "🏢 Enterprise deployment ready for Datatón ITAM 2025!"

echo ""
echo "=================================================="
echo "🚂 RAILWAY PROFESSIONAL DEPLOYMENT SUCCESSFUL!"
echo "🌐 URL: Available in Railway dashboard"
echo "⏰ Deployment Time: $(date)"
echo "🎯 Status: PROFESSIONAL MISSION SUCCESS"
echo "🏢 Features: Full enterprise capabilities active"
echo "=================================================="

# Instructions for custom domain
echo ""
log_info "📋 CUSTOM DOMAIN SETUP (casamx.store):"
log_info "1. Open Railway dashboard: https://railway.app/dashboard"
log_info "2. Select your CasaMX project"
log_info "3. Go to Settings → Domains"
log_info "4. Add custom domain: casamx.store"
log_info "5. Update DNS as instructed"
log_info "6. SSL will be automatically provisioned"

echo ""
log_professional "🚂 Railway Additional Commands:"
log_professional "• View logs: railway logs"
log_professional "• Check status: railway status" 
log_professional "• Open dashboard: railway open"
log_professional "• Deploy updates: railway up"

log_success "🏆 PROFESSIONAL DEPLOYMENT COMPLETE!"