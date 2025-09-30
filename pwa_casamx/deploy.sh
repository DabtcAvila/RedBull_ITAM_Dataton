#!/bin/bash

# CasaMX PWA - Quick Deployment Script
# Datatón ITAM 2025 - David Fernando Ávila Díaz

echo "🏠 CasaMX PWA - Enterprise Deployment Script"
echo "============================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the correct directory
if [ ! -f "index.html" ] || [ ! -f "manifest.json" ]; then
    echo -e "${RED}❌ Error: Must be run from pwa_casamx directory${NC}"
    echo -e "Current directory: $(pwd)"
    echo -e "Please cd to pwa_casamx folder first"
    exit 1
fi

echo -e "${BLUE}📂 Current directory: $(pwd)${NC}"
echo -e "${GREEN}✅ PWA files detected${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to find available port
find_available_port() {
    local port=8000
    while lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; do
        port=$((port + 1))
    done
    echo $port
}

# Validate PWA structure
echo -e "${YELLOW}🔍 Validating PWA structure...${NC}"

required_files=(
    "index.html"
    "manifest.json" 
    "sw.js"
    "assets/css/styles.css"
    "assets/js/app.js"
    "assets/js/recommendation-engine.js"
    "assets/js/map-handler.js"
    "assets/data/cdmx-neighborhoods.json"
    "assets/data/demo-cases.json"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo -e "${GREEN}✅ All required files present${NC}"
else
    echo -e "${RED}❌ Missing files:${NC}"
    printf '%s\n' "${missing_files[@]}"
    echo -e "${YELLOW}⚠️  PWA may not work correctly${NC}"
fi

# Count icons
icon_count=$(ls icons/*.svg 2>/dev/null | wc -l)
echo -e "${GREEN}📱 Icons available: $icon_count${NC}"

echo ""

# Deployment options
echo -e "${BLUE}🚀 Choose deployment method:${NC}"
echo "1. Python HTTP Server (recommended)"
echo "2. Node.js serve"
echo "3. PHP built-in server" 
echo "4. Open files directly (limited functionality)"
echo "5. Show deployment URLs for cloud platforms"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        if command_exists python3; then
            PORT=$(find_available_port)
            echo -e "${GREEN}🐍 Starting Python HTTP Server on port $PORT...${NC}"
            echo -e "${YELLOW}📱 PWA URL: http://localhost:$PORT${NC}"
            echo -e "${YELLOW}🧪 Test Suite: http://localhost:$PORT/test-pwa.html${NC}"
            echo -e "${YELLOW}🎨 Icon Generator: http://localhost:$PORT/generate-icons.html${NC}"
            echo ""
            echo -e "${BLUE}💡 Tips for demo:${NC}"
            echo "• Open on mobile for best install experience"
            echo "• Share URL with judges for instant installation"
            echo "• Works offline after first load"
            echo ""
            echo -e "${GREEN}Press Ctrl+C to stop server${NC}"
            echo ""
            python3 -m http.server $PORT
        elif command_exists python; then
            PORT=$(find_available_port)
            echo -e "${GREEN}🐍 Starting Python 2 HTTP Server on port $PORT...${NC}"
            echo -e "${YELLOW}📱 PWA URL: http://localhost:$PORT${NC}"
            python -m SimpleHTTPServer $PORT
        else
            echo -e "${RED}❌ Python not found. Please install Python or choose another option.${NC}"
        fi
        ;;
    2)
        if command_exists npx; then
            echo -e "${GREEN}📦 Starting Node.js serve...${NC}"
            npx serve . -s
        elif command_exists node && command_exists npm; then
            echo -e "${YELLOW}Installing serve globally...${NC}"
            npm install -g serve
            serve . -s
        else
            echo -e "${RED}❌ Node.js/npm not found. Please install Node.js or choose another option.${NC}"
        fi
        ;;
    3)
        if command_exists php; then
            PORT=$(find_available_port)
            echo -e "${GREEN}🐘 Starting PHP built-in server on port $PORT...${NC}"
            echo -e "${YELLOW}📱 PWA URL: http://localhost:$PORT${NC}"
            php -S localhost:$PORT
        else
            echo -e "${RED}❌ PHP not found. Please install PHP or choose another option.${NC}"
        fi
        ;;
    4)
        echo -e "${YELLOW}⚠️  Opening files directly (limited PWA functionality)...${NC}"
        if command_exists open; then
            open index.html
        elif command_exists xdg-open; then
            xdg-open index.html
        else
            echo -e "${BLUE}Please open index.html in your browser${NC}"
        fi
        ;;
    5)
        echo -e "${BLUE}☁️ Cloud Deployment Options:${NC}"
        echo ""
        echo -e "${GREEN}GitHub Pages (Free):${NC}"
        echo "1. Push pwa_casamx/ to GitHub repo"
        echo "2. Settings > Pages > Source: Deploy from branch"
        echo "3. URL: https://username.github.io/repo-name/"
        echo ""
        echo -e "${GREEN}Netlify (Free):${NC}"
        echo "1. Visit: https://netlify.com/drop"
        echo "2. Drag pwa_casamx/ folder to page"
        echo "3. Get instant HTTPS URL"
        echo ""
        echo -e "${GREEN}Vercel (Free):${NC}"
        echo "1. Run: npx vercel --cwd $(pwd)"
        echo "2. Follow prompts"
        echo "3. Get instant HTTPS URL"
        echo ""
        echo -e "${GREEN}Firebase Hosting (Free):${NC}"
        echo "1. Run: npm install -g firebase-tools"
        echo "2. Run: firebase login"
        echo "3. Run: firebase init hosting"
        echo "4. Run: firebase deploy"
        echo ""
        ;;
    *)
        echo -e "${RED}❌ Invalid choice. Please run again.${NC}"
        exit 1
        ;;
esac