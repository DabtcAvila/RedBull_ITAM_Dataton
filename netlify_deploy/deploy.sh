#!/bin/bash

# CasaMX Netlify Deployment Script
# Usage: ./deploy.sh

set -e  # Exit on any error

echo "🚀 Starting CasaMX Netlify Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SITE_NAME="casamx-store"
DOMAIN="casamx.store"
BUILD_DIR="."

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    print_error "Netlify CLI not found. Installing..."
    npm install -g netlify-cli
    print_success "Netlify CLI installed successfully"
fi

# Login to Netlify (if not already logged in)
print_status "Checking Netlify authentication..."
if ! netlify status &> /dev/null; then
    print_warning "Not logged into Netlify. Please log in:"
    netlify login
fi

print_success "Netlify authentication verified"

# Initialize site if not exists
print_status "Initializing Netlify site..."
if [ ! -f ".netlify/state.json" ]; then
    print_status "Creating new Netlify site: $SITE_NAME"
    netlify init --manual
else
    print_success "Netlify site already initialized"
fi

# Validate files before deployment
print_status "Validating deployment files..."
required_files=("index.html" "netlify.toml" "_redirects" "robots.txt" "sitemap.xml")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "✓ $file found"
    else
        print_error "✗ $file missing"
        exit 1
    fi
done

# Test HTML validation (basic)
if command -v htmlhint &> /dev/null; then
    print_status "Running HTML validation..."
    htmlhint index.html || print_warning "HTML validation warnings detected"
fi

# Deploy to Netlify
print_status "Deploying to Netlify..."
netlify deploy --prod --dir="$BUILD_DIR"

if [ $? -eq 0 ]; then
    print_success "🎉 Deployment successful!"
    print_status "Site URL: https://$DOMAIN"
    print_status "Admin URL: https://app.netlify.com/sites/$SITE_NAME"
    
    # Open site in browser (optional)
    if command -v open &> /dev/null; then
        print_status "Opening site in browser..."
        open "https://$DOMAIN"
    elif command -v xdg-open &> /dev/null; then
        print_status "Opening site in browser..."
        xdg-open "https://$DOMAIN"
    fi
    
    print_success "🏠 CasaMX is now live at https://$DOMAIN"
else
    print_error "❌ Deployment failed"
    exit 1
fi

# Display deployment summary
echo ""
echo "==================================="
echo "📊 DEPLOYMENT SUMMARY"
echo "==================================="
echo "Site Name: $SITE_NAME"
echo "Domain: $DOMAIN"
echo "Status: Live ✅"
echo "Deploy Time: $(date)"
echo "==================================="

print_success "CasaMX deployment completed successfully! 🎉"
print_status "Your site is ready at: https://$DOMAIN"