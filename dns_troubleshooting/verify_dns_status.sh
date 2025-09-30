#!/bin/bash

# DNS VERIFICATION SCRIPT FOR casamx.store
# Run this continuously to monitor DNS resolution status

DOMAIN="casamx.store"
TARGET_IP="198.41.200.63"

echo "=== DNS VERIFICATION FOR $DOMAIN ==="
echo "Timestamp: $(date)"
echo "Target IP: $TARGET_IP"
echo ""

# Quick resolution test
echo "1. QUICK RESOLUTION TEST:"
if nslookup $DOMAIN > /dev/null 2>&1; then
    echo "   ✅ $DOMAIN is resolving!"
    RESOLVED_IP=$(dig +short $DOMAIN | head -1)
    echo "   Resolved to: $RESOLVED_IP"
    
    if [ "$RESOLVED_IP" == "$TARGET_IP" ]; then
        echo "   ✅ IP matches target!"
    else
        echo "   ⚠️  IP doesn't match target ($TARGET_IP)"
    fi
else
    echo "   ❌ $DOMAIN is NOT resolving (NXDOMAIN)"
fi

echo ""

# Test nameservers
echo "2. NAMESERVER TEST:"
NAMESERVERS=$(dig +short NS $DOMAIN)
if [ -n "$NAMESERVERS" ]; then
    echo "   ✅ Nameservers found:"
    echo "$NAMESERVERS" | sed 's/^/   - /'
else
    echo "   ❌ No nameservers found"
fi

echo ""

# Test Cloudflare nameservers directly
echo "3. CLOUDFLARE NAMESERVER TEST:"
CF_RESULT_LIV=$(dig @liv.ns.cloudflare.com +short $DOMAIN 2>/dev/null)
CF_RESULT_SID=$(dig @sid.ns.cloudflare.com +short $DOMAIN 2>/dev/null)

if [ -n "$CF_RESULT_LIV" ]; then
    echo "   ✅ liv.ns.cloudflare.com returns: $CF_RESULT_LIV"
else
    echo "   ❌ liv.ns.cloudflare.com returns NXDOMAIN"
fi

if [ -n "$CF_RESULT_SID" ]; then  
    echo "   ✅ sid.ns.cloudflare.com returns: $CF_RESULT_SID"
else
    echo "   ❌ sid.ns.cloudflare.com returns NXDOMAIN"
fi

echo ""

# Test HTTP connectivity  
echo "4. HTTP CONNECTIVITY TEST:"
if curl -s --connect-timeout 5 http://$TARGET_IP > /dev/null; then
    echo "   ✅ HTTP connection to $TARGET_IP successful"
else
    echo "   ❌ HTTP connection to $TARGET_IP failed"
fi

if curl -s --connect-timeout 5 -k https://$TARGET_IP > /dev/null; then
    echo "   ✅ HTTPS connection to $TARGET_IP successful"  
else
    echo "   ❌ HTTPS connection to $TARGET_IP failed"
fi

echo ""

# Overall status
echo "5. OVERALL STATUS:"
if nslookup $DOMAIN > /dev/null 2>&1; then
    echo "   🟢 DNS is WORKING - casamx.store is accessible!"
    echo "   Test URL: http://$DOMAIN"
    echo "   Test URL: https://$DOMAIN"
else
    echo "   🔴 DNS is NOT WORKING - casamx.store is NOT accessible"
    echo "   Action required: Add domain zone to Cloudflare Dashboard"
fi

echo ""
echo "=== END VERIFICATION ==="