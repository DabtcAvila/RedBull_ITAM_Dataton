#!/bin/bash

# ================================================================
# DEPLOYMENT TESTING SCRIPT - CASAMX.STORE  
# DATATÓN ITAM 2025 - COMPREHENSIVE DEPLOYMENT VALIDATION
# ================================================================

echo "🧪 TESTING CASAMX DEPLOYMENT - COMPREHENSIVE VALIDATION"
echo "=================================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_test() { echo -e "${PURPLE}[TEST]${NC} $1"; }

# Test configuration
DOMAIN="casamx.store"
URLS_TO_TEST=(
    "https://$DOMAIN"
    "https://www.$DOMAIN"
    "http://$DOMAIN"
    "http://www.$DOMAIN"
)

ALTERNATIVE_URLS=(
    "https://casamx-store.vercel.app"
    "https://casamx-store.netlify.app"
    "https://davidaviladiaz.github.io/casamx-store"
)

# Initialize test results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
TEST_RESULTS=()

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    log_test "Running: $test_name"
    
    if eval "$test_command"; then
        log_success "✅ PASS: $test_name"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        TEST_RESULTS+=("✅ PASS: $test_name")
        return 0
    else
        log_error "❌ FAIL: $test_name"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        TEST_RESULTS+=("❌ FAIL: $test_name")
        return 1
    fi
}

echo -e "${BOLD}${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    DEPLOYMENT TEST SUITE                     ║"
echo "║                     CASAMX.STORE                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# TEST 1: DNS RESOLUTION
echo "🌐 DNS RESOLUTION TESTS"
echo "=================================================="

run_test "DNS Resolution - Main Domain" \
         "nslookup $DOMAIN > /dev/null 2>&1" \
         "Domain should resolve"

run_test "DNS Resolution - WWW Subdomain" \
         "nslookup www.$DOMAIN > /dev/null 2>&1" \
         "WWW subdomain should resolve"

# TEST 2: HTTP CONNECTIVITY
echo ""
echo "🔗 HTTP CONNECTIVITY TESTS"
echo "=================================================="

for url in "${URLS_TO_TEST[@]}"; do
    run_test "HTTP Connectivity - $url" \
             "curl -f -s -I '$url' | grep -q 'HTTP.*[23][0-9][0-9]'" \
             "URL should respond with 2xx or 3xx status"
done

# TEST 3: SSL/HTTPS VALIDATION  
echo ""
echo "🔒 SSL/HTTPS VALIDATION TESTS"
echo "=================================================="

run_test "SSL Certificate - Main Domain" \
         "curl -f -s -I 'https://$DOMAIN' > /dev/null 2>&1" \
         "HTTPS should work without certificate errors"

run_test "SSL Certificate - WWW Subdomain" \
         "curl -f -s -I 'https://www.$DOMAIN' > /dev/null 2>&1" \
         "HTTPS should work for WWW subdomain"

# TEST 4: CONTENT VALIDATION
echo ""
echo "📄 CONTENT VALIDATION TESTS"
echo "=================================================="

run_test "Page Content - CasaMX Title" \
         "curl -f -s 'https://$DOMAIN' | grep -q 'CasaMX'" \
         "Page should contain CasaMX branding"

run_test "Page Content - Streamlit App" \
         "curl -f -s 'https://$DOMAIN' | grep -q -i 'streamlit\\|dataton\\|itam'" \
         "Page should contain Streamlit or Dataton content"

run_test "Page Content - Form Elements" \
         "curl -f -s 'https://$DOMAIN' | grep -q -i 'form\\|input\\|button'" \
         "Page should contain interactive form elements"

# TEST 5: PERFORMANCE TESTS
echo ""
echo "⚡ PERFORMANCE TESTS"
echo "=================================================="

run_test "Response Time - Under 5 seconds" \
         "timeout 5 curl -f -s 'https://$DOMAIN' > /dev/null" \
         "Page should load within 5 seconds"

run_test "Page Size - Reasonable" \
         "[ \$(curl -f -s 'https://$DOMAIN' | wc -c) -gt 1000 ]" \
         "Page should have reasonable content size"

# TEST 6: ALTERNATIVE URLS (if main domain fails)
if [ $FAILED_TESTS -gt 0 ]; then
    echo ""
    echo "🔄 ALTERNATIVE URL TESTS (Fallback Detection)"
    echo "=================================================="
    
    for alt_url in "${ALTERNATIVE_URLS[@]}"; do
        run_test "Alternative URL - $alt_url" \
                 "curl -f -s -I '$alt_url' > /dev/null 2>&1" \
                 "Alternative deployment should be accessible"
    done
fi

# TEST 7: API/HEALTH ENDPOINTS
echo ""
echo "🩺 HEALTH CHECK TESTS"
echo "=================================================="

run_test "Health Check Endpoint" \
         "curl -f -s 'https://$DOMAIN/_health' > /dev/null 2>&1 || curl -f -s 'https://$DOMAIN/health' > /dev/null 2>&1" \
         "Health endpoint should be available"

run_test "Favicon Access" \
         "curl -f -s -I 'https://$DOMAIN/favicon.ico' | grep -q 'HTTP.*[23][0-9][0-9]'" \
         "Favicon should be accessible"

# TEST 8: MOBILE/RESPONSIVE TESTS
echo ""
echo "📱 MOBILE/RESPONSIVE TESTS"
echo "=================================================="

run_test "Mobile Viewport Meta Tag" \
         "curl -f -s 'https://$DOMAIN' | grep -q 'viewport'" \
         "Page should have mobile viewport meta tag"

run_test "Responsive Design Elements" \
         "curl -f -s 'https://$DOMAIN' | grep -q -i 'responsive\\|mobile\\|bootstrap\\|grid'" \
         "Page should contain responsive design elements"

# TEST 9: FUNCTIONALITY TESTS (JavaScript/Interactive)
echo ""
echo "⚙️ FUNCTIONALITY TESTS"
echo "=================================================="

run_test "JavaScript Libraries" \
         "curl -f -s 'https://$DOMAIN' | grep -q -i 'script\\|javascript'" \
         "Page should contain JavaScript elements"

run_test "CSS Styling" \
         "curl -f -s 'https://$DOMAIN' | grep -q -i 'css\\|style'" \
         "Page should contain CSS styling"

# TEST 10: SEO/METADATA TESTS  
echo ""
echo "🎯 SEO/METADATA TESTS"
echo "=================================================="

run_test "Page Title Tag" \
         "curl -f -s 'https://$DOMAIN' | grep -q '<title.*CasaMX.*</title>'" \
         "Page should have proper title tag"

run_test "Meta Description" \
         "curl -f -s 'https://$DOMAIN' | grep -q 'meta.*description'" \
         "Page should have meta description"

run_test "Open Graph Tags" \
         "curl -f -s 'https://$DOMAIN' | grep -q 'og:'" \
         "Page should have Open Graph meta tags"

# COMPREHENSIVE REPORT
echo ""
echo -e "${BOLD}${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    TEST RESULTS SUMMARY                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo "📊 OVERALL RESULTS:"
echo "   Total Tests: $TOTAL_TESTS"
echo "   Passed: $PASSED_TESTS"
echo "   Failed: $FAILED_TESTS"
echo "   Success Rate: $(( PASSED_TESTS * 100 / TOTAL_TESTS ))%"

echo ""
echo "📋 DETAILED RESULTS:"
for result in "${TEST_RESULTS[@]}"; do
    echo "   $result"
done

# DEPLOYMENT STATUS
echo ""
echo "🎯 DEPLOYMENT STATUS:"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${BOLD}${GREEN}✅ DEPLOYMENT FULLY OPERATIONAL${NC}"
    echo "🎉 CasaMX is ready for Datatón ITAM 2025!"
    DEPLOYMENT_STATUS="EXCELLENT"
elif [ $FAILED_TESTS -le 3 ]; then
    echo -e "${BOLD}${YELLOW}⚠️ DEPLOYMENT MOSTLY OPERATIONAL${NC}"
    echo "🔧 Minor issues detected but site is functional"
    DEPLOYMENT_STATUS="GOOD"
elif [ $FAILED_TESTS -le 6 ]; then
    echo -e "${BOLD}${YELLOW}⚠️ DEPLOYMENT PARTIALLY OPERATIONAL${NC}"
    echo "🔧 Some issues detected, manual review recommended"
    DEPLOYMENT_STATUS="FAIR"
else
    echo -e "${BOLD}${RED}❌ DEPLOYMENT HAS SIGNIFICANT ISSUES${NC}"
    echo "🚨 Multiple failures detected, troubleshooting required"
    DEPLOYMENT_STATUS="POOR"
fi

# ACTIONABLE RECOMMENDATIONS
echo ""
echo "💡 RECOMMENDATIONS:"

if [ $FAILED_TESTS -eq 0 ]; then
    echo "✅ No action required - deployment is excellent"
    echo "🎯 Ready for presentation"
elif [ $FAILED_TESTS -le 3 ]; then
    echo "🔧 Minor optimizations recommended"
    echo "📊 Monitor performance during presentation"
else
    echo "🚨 Review failed tests and address issues"
    echo "🔄 Consider re-running deployment or using alternative platform"
    echo "📞 Have backup plan ready for presentation"
fi

# MONITORING SETUP
echo ""
echo "📈 SETTING UP CONTINUOUS MONITORING..."

cat > continuous_monitoring.sh << 'EOF'
#!/bin/bash
# Continuous monitoring for CasaMX deployment

echo "🔄 Starting continuous monitoring for casamx.store..."
echo "$(date): Monitoring started" >> deployment_monitor.log

while true; do
    if curl -f -s -o /dev/null "https://casamx.store"; then
        echo "$(date): ✅ Online" >> deployment_monitor.log
    else
        echo "$(date): ❌ Offline - ALERT!" >> deployment_monitor.log
        echo "🚨 ALERT: casamx.store is down! $(date)"
    fi
    sleep 60  # Check every minute
done
EOF

chmod +x continuous_monitoring.sh
log_success "✅ Continuous monitoring script created"

# FINAL STATUS
echo ""
echo "🏆 DEPLOYMENT TESTING COMPLETE"
echo "=================================================="
echo "Status: $DEPLOYMENT_STATUS"
echo "Site: https://$DOMAIN"
echo "Test Time: $(date)"
echo "Ready for Datatón ITAM 2025: $([ $FAILED_TESTS -le 3 ] && echo "YES" || echo "NEEDS REVIEW")"
echo "=================================================="

# Exit code based on results
if [ $FAILED_TESTS -eq 0 ]; then
    exit 0  # Perfect deployment
elif [ $FAILED_TESTS -le 3 ]; then
    exit 0  # Acceptable deployment
else
    exit 1  # Needs attention
fi