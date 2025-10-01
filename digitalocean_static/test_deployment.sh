#!/bin/bash

# CasaMX - DigitalOcean Static Site Deployment Test Script
# Usage: ./test_deployment.sh [url]
# Example: ./test_deployment.sh https://casamx.store

URL=${1:-"http://localhost:8000"}
echo "🧪 Testing CasaMX deployment at: $URL"
echo "================================================"

# Check if URL is reachable
echo "📡 Checking connectivity..."
if curl -s --head "$URL" | head -n 1 | grep -q "200 OK"; then
    echo "✅ Site is reachable"
else
    echo "❌ Site is NOT reachable"
    exit 1
fi

# Check response time
echo ""
echo "⚡ Testing performance..."
RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' "$URL")
if (( $(echo "$RESPONSE_TIME < 3.0" | bc -l) )); then
    echo "✅ Fast response time: ${RESPONSE_TIME}s"
else
    echo "⚠️  Slow response time: ${RESPONSE_TIME}s"
fi

# Check if critical elements exist
echo ""
echo "🔍 Checking critical elements..."

# Check for main app structure
if curl -s "$URL" | grep -q "CasaMX"; then
    echo "✅ App title found"
else
    echo "❌ App title missing"
fi

if curl -s "$URL" | grep -q "tab-content"; then
    echo "✅ Tab navigation found"
else
    echo "❌ Tab navigation missing"
fi

if curl -s "$URL" | grep -q "searchForm"; then
    echo "✅ Search form found"
else
    echo "❌ Search form missing"
fi

if curl -s "$URL" | grep -q "leafletMap"; then
    echo "✅ Map container found"
else
    echo "❌ Map container missing"
fi

# Check for embedded data
if curl -s "$URL" | grep -q "CasaMXData"; then
    echo "✅ Embedded data found"
else
    echo "❌ Embedded data missing"
fi

# Check for PWA elements
echo ""
echo "📱 Checking PWA elements..."

if curl -s "$URL" | grep -q "manifest.json"; then
    echo "✅ PWA manifest linked"
else
    echo "❌ PWA manifest missing"
fi

# Check for SEO elements
echo ""
echo "🔍 Checking SEO elements..."

if curl -s "$URL" | grep -q "og:title"; then
    echo "✅ Open Graph tags found"
else
    echo "❌ Open Graph tags missing"
fi

if curl -s "$URL" | grep -q "description"; then
    echo "✅ Meta description found"
else
    echo "❌ Meta description missing"
fi

# Check supporting files
echo ""
echo "📄 Checking supporting files..."

# Check robots.txt
if curl -s "$URL/robots.txt" | grep -q "User-agent"; then
    echo "✅ robots.txt accessible"
else
    echo "⚠️  robots.txt not accessible"
fi

# Check sitemap.xml
if curl -s "$URL/sitemap.xml" | grep -q "sitemap"; then
    echo "✅ sitemap.xml accessible"
else
    echo "⚠️  sitemap.xml not accessible"
fi

# Check manifest.json
if curl -s "$URL/manifest.json" | grep -q "CasaMX"; then
    echo "✅ manifest.json accessible"
else
    echo "⚠️  manifest.json not accessible"
fi

# Final report
echo ""
echo "================================================"
echo "🎯 DEPLOYMENT TEST SUMMARY"
echo "================================================"
echo "URL: $URL"
echo "Response Time: ${RESPONSE_TIME}s"
echo ""

# Recommendations
if curl -s --head "$URL" | head -n 1 | grep -q "200 OK" && \
   curl -s "$URL" | grep -q "CasaMX" && \
   curl -s "$URL" | grep -q "searchForm" && \
   (( $(echo "$RESPONSE_TIME < 3.0" | bc -l) )); then
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo "✅ App is ready for production"
    echo "✅ All critical elements working"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Test search functionality manually"
    echo "   2. Try demo cases (Alex, María, Sophie)"
    echo "   3. Verify map loads with markers"
    echo "   4. Test PWA installation on mobile"
    echo "   5. Check responsive design on different devices"
else
    echo "❌ DEPLOYMENT HAS ISSUES"
    echo "❌ Please check the errors above"
    echo ""
    echo "🔧 Common fixes:"
    echo "   1. Verify index.html is in root directory"
    echo "   2. Check all files uploaded correctly"
    echo "   3. Ensure Static Site (not Web Service) selected"
    echo "   4. Wait a few minutes for DNS propagation"
fi

echo ""
echo "================================================"