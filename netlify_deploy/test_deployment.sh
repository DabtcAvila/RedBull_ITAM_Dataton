#!/bin/bash

# CasaMX Netlify Deployment Test Script

echo "🧪 Testing CasaMX Netlify Deployment..."

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "${BLUE}[TEST]${NC} $test_name"
    
    if eval "$test_command"; then
        echo -e "${GREEN}[PASS]${NC} $test_name ✅"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}[FAIL]${NC} $test_name ❌"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# File existence tests
run_test "index.html exists" "[ -f index.html ]"
run_test "netlify.toml exists" "[ -f netlify.toml ]"
run_test "_redirects exists" "[ -f _redirects ]"
run_test "robots.txt exists" "[ -f robots.txt ]"
run_test "sitemap.xml exists" "[ -f sitemap.xml ]"
run_test "404.html exists" "[ -f 404.html ]"
run_test "deploy.sh is executable" "[ -x deploy.sh ]"
run_test "package.json exists" "[ -f package.json ]"

# Content validation tests
run_test "index.html contains CasaMX title" "grep -q 'CasaMX' index.html"
run_test "index.html contains CDMX_DATA" "grep -q 'CDMX_DATA' index.html"
run_test "index.html contains RecommendationEngine" "grep -q 'RecommendationEngine' index.html"
run_test "netlify.toml has redirects" "grep -q 'redirects' netlify.toml"
run_test "robots.txt allows root" "grep -q 'Allow: /' robots.txt"
run_test "sitemap.xml contains casamx.store" "grep -q 'casamx.store' sitemap.xml"

# JavaScript validation (basic)
run_test "JavaScript syntax check" "node -c <(grep -A 9999 '<script>' index.html | grep -B 9999 '</script>' | sed '1d;$d') 2>/dev/null"

# HTML validation (basic)
run_test "HTML has DOCTYPE" "grep -q '<!DOCTYPE html>' index.html"
run_test "HTML has lang attribute" "grep -q 'lang=\"es\"' index.html"
run_test "HTML has viewport meta" "grep -q 'viewport' index.html"

# Local server test
echo -e "${BLUE}[TEST]${NC} Starting local server for 5 seconds..."
python3 -m http.server 8001 > /dev/null 2>&1 &
SERVER_PID=$!
sleep 2

if curl -s http://localhost:8001 > /dev/null; then
    echo -e "${GREEN}[PASS]${NC} Local server works ✅"
    ((TESTS_PASSED++))
else
    echo -e "${RED}[FAIL]${NC} Local server failed ❌"
    ((TESTS_FAILED++))
fi

kill $SERVER_PID 2>/dev/null
echo ""

# Summary
TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
echo "======================================"
echo "🧪 TEST SUMMARY"
echo "======================================"
echo -e "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 ALL TESTS PASSED!${NC}"
    echo -e "${GREEN}✅ Deployment is ready for Netlify!${NC}"
    echo ""
    echo "Ready to deploy:"
    echo "  ./deploy.sh"
    echo ""
    echo "Or drag & drop to: https://netlify.com/drop"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed.${NC}"
    echo "Please fix the issues before deploying."
    exit 1
fi