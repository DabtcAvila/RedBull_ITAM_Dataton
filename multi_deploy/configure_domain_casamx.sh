#!/bin/bash

# ================================================================
# DOMAIN CONFIGURATION SCRIPT - CASAMX.STORE
# DATATÓN ITAM 2025 - AUTOMATED DNS SETUP
# ================================================================

echo "🌐 CONFIGURANDO DOMINIO CASAMX.STORE"
echo "=================================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Domain information
DOMAIN="casamx.store"
SUBDOMAIN="www.casamx.store"

echo "🎯 Target Domain: $DOMAIN"
echo "🔗 Subdomain: $SUBDOMAIN"
echo ""

# Function to check domain status
check_domain_status() {
    local domain=$1
    log_info "🔍 Checking DNS status for $domain..."
    
    # Check if domain resolves
    if nslookup "$domain" &> /dev/null; then
        local ip=$(nslookup "$domain" | grep "Address:" | tail -1 | awk '{print $2}')
        log_success "✅ $domain resolves to: $ip"
        return 0
    else
        log_warning "⚠️ $domain does not resolve yet"
        return 1
    fi
}

# Function to test HTTPS
test_https() {
    local url=$1
    log_info "🔒 Testing HTTPS for $url..."
    
    if curl -f -s -I "$url" | grep "HTTP/.*200" &> /dev/null; then
        log_success "✅ HTTPS working for $url"
        return 0
    else
        log_warning "⚠️ HTTPS not ready for $url"
        return 1
    fi
}

# PLATFORM-SPECIFIC DNS CONFIGURATIONS
echo "🏗️ PLATFORM-SPECIFIC DNS CONFIGURATIONS"
echo "=================================================="

log_info "📋 DNS RECORDS NEEDED FOR EACH PLATFORM:"
echo ""

echo -e "${BLUE}1. VERCEL CONFIGURATION:${NC}"
echo "   A Record:     $DOMAIN     →  76.76.19.61"
echo "   CNAME Record: $SUBDOMAIN  →  cname.vercel-dns.com"
echo ""

echo -e "${BLUE}2. NETLIFY CONFIGURATION:${NC}" 
echo "   A Record:     $DOMAIN     →  75.2.60.5"
echo "   CNAME Record: $SUBDOMAIN  →  casamx-store.netlify.app"
echo ""

echo -e "${BLUE}3. GITHUB PAGES CONFIGURATION:${NC}"
echo "   A Record:     $DOMAIN     →  185.199.108.153"
echo "   A Record:     $DOMAIN     →  185.199.109.153"  
echo "   A Record:     $DOMAIN     →  185.199.110.153"
echo "   A Record:     $DOMAIN     →  185.199.111.153"
echo "   CNAME Record: $SUBDOMAIN  →  davidaviladiaz.github.io"
echo ""

echo -e "${BLUE}4. RAILWAY CONFIGURATION:${NC}"
echo "   CNAME Record: $DOMAIN     →  [railway-provided-domain]"
echo "   CNAME Record: $SUBDOMAIN  →  [railway-provided-domain]"
echo ""

# DNS CHECK AND MONITORING
echo "🔍 DNS STATUS CHECK"
echo "=================================================="

check_domain_status "$DOMAIN"
MAIN_STATUS=$?

check_domain_status "$SUBDOMAIN" 
SUB_STATUS=$?

# HTTPS CHECK
echo ""
echo "🔒 HTTPS VERIFICATION"
echo "=================================================="

test_https "https://$DOMAIN"
HTTPS_MAIN_STATUS=$?

test_https "https://$SUBDOMAIN"
HTTPS_SUB_STATUS=$?

# AUTOMATED DNS SETUP (if dig is available)
if command -v dig &> /dev/null; then
    echo ""
    echo "🔧 AUTOMATED DNS ANALYSIS"
    echo "=================================================="
    
    log_info "🔍 Performing detailed DNS lookup..."
    
    # Check current DNS records
    A_RECORDS=$(dig +short A "$DOMAIN" 2>/dev/null || echo "No A records")
    CNAME_RECORDS=$(dig +short CNAME "$DOMAIN" 2>/dev/null || echo "No CNAME records") 
    
    echo "Current A records for $DOMAIN: $A_RECORDS"
    echo "Current CNAME records for $DOMAIN: $CNAME_RECORDS"
    
    # Detect which platform is configured
    if echo "$A_RECORDS" | grep -q "76.76.19.61"; then
        log_success "🎯 Vercel DNS detected"
        DETECTED_PLATFORM="Vercel"
    elif echo "$A_RECORDS" | grep -q "75.2.60.5"; then
        log_success "🎯 Netlify DNS detected" 
        DETECTED_PLATFORM="Netlify"
    elif echo "$A_RECORDS" | grep -q "185.199.10"; then
        log_success "🎯 GitHub Pages DNS detected"
        DETECTED_PLATFORM="GitHub Pages"
    elif echo "$CNAME_RECORDS" | grep -q "railway"; then
        log_success "🎯 Railway DNS detected"
        DETECTED_PLATFORM="Railway" 
    else
        log_warning "⚠️ Platform not detected or DNS not configured"
        DETECTED_PLATFORM="Unknown"
    fi
else
    log_warning "⚠️ dig command not available - install dnsutils for detailed analysis"
    DETECTED_PLATFORM="Unknown"
fi

# CLOUDFLARE DETECTION
echo ""
echo "☁️ CLOUDFLARE ANALYSIS"  
echo "=================================================="

if command -v dig &> /dev/null; then
    NS_SERVERS=$(dig +short NS "$DOMAIN" 2>/dev/null)
    
    if echo "$NS_SERVERS" | grep -q "cloudflare"; then
        log_success "✅ Cloudflare DNS detected"
        log_info "🔧 Cloudflare provides additional performance and security"
        USES_CLOUDFLARE=true
    else
        log_info "ℹ️ Not using Cloudflare DNS (optional)"
        USES_CLOUDFLARE=false
    fi
    
    echo "Name servers: $NS_SERVERS"
else
    USES_CLOUDFLARE=false
fi

# PROPAGATION CHECK
echo ""
echo "🌍 DNS PROPAGATION CHECK"
echo "=================================================="

log_info "🔄 Checking DNS propagation globally..."

# Check multiple DNS servers
DNS_SERVERS=("8.8.8.8" "1.1.1.1" "208.67.222.222")

for dns in "${DNS_SERVERS[@]}"; do
    log_info "Checking via $dns..."
    if dig +short "@$dns" "$DOMAIN" &> /dev/null; then
        result=$(dig +short "@$dns" "$DOMAIN" 2>/dev/null)
        if [ -n "$result" ]; then
            log_success "✅ $dns: $result"
        else
            log_warning "⚠️ $dns: No response"
        fi
    else
        log_warning "⚠️ $dns: Query failed"
    fi
done

# FINAL STATUS REPORT
echo ""
echo "📊 DOMAIN CONFIGURATION REPORT"  
echo "=================================================="

echo "Domain: $DOMAIN"
echo "Subdomain: $SUBDOMAIN" 
echo "Detected Platform: $DETECTED_PLATFORM"
echo "Uses Cloudflare: $([ "$USES_CLOUDFLARE" = true ] && echo "Yes" || echo "No")"
echo "DNS Resolution: $([ $MAIN_STATUS -eq 0 ] && echo "✅ Working" || echo "❌ Failed")"
echo "HTTPS Status: $([ $HTTPS_MAIN_STATUS -eq 0 ] && echo "✅ Working" || echo "❌ Not Ready")"

# RECOMMENDATIONS
echo ""
echo "💡 RECOMMENDATIONS"
echo "=================================================="

if [ $MAIN_STATUS -ne 0 ]; then
    log_warning "🔧 DNS not configured - please set up DNS records"
    echo "   1. Access your domain registrar's DNS settings"
    echo "   2. Add the A/CNAME records shown above"
    echo "   3. Wait 5-60 minutes for propagation"
fi

if [ $HTTPS_MAIN_STATUS -ne 0 ]; then
    log_warning "🔒 HTTPS not ready - this is normal for new deployments"
    echo "   1. HTTPS certificates are auto-generated"
    echo "   2. Wait 10-30 minutes after DNS propagation"
    echo "   3. Certificates auto-renew"
fi

# MONITORING SCRIPT
echo ""
log_info "📊 Creating continuous monitoring script..."

cat > monitor_casamx_domain.sh << 'EOF'
#!/bin/bash
# Continuous monitoring for casamx.store

echo "🔄 Monitoring casamx.store status..."
while true; do
    if curl -f -s -o /dev/null "https://casamx.store"; then
        echo "$(date): ✅ casamx.store is online"
        break
    else  
        echo "$(date): ⚠️  casamx.store not responding, checking again..."
    fi
    sleep 30
done
echo "$(date): 🎉 casamx.store is fully operational!"
EOF

chmod +x monitor_casamx_domain.sh

log_success "✅ Monitoring script created: ./monitor_casamx_domain.sh"

echo ""
echo "🏆 DOMAIN CONFIGURATION ANALYSIS COMPLETE"
echo "=================================================="

exit 0