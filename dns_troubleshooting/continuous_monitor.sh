#!/bin/bash

# CONTINUOUS DNS MONITORING FOR casamx.store
# Monitors DNS resolution every 30 seconds until working

DOMAIN="casamx.store"
TARGET_IP="198.41.200.63"
LOGFILE="/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton/dns_troubleshooting/monitoring.log"

echo "=== CONTINUOUS DNS MONITORING STARTED ===" | tee -a $LOGFILE
echo "Domain: $DOMAIN" | tee -a $LOGFILE
echo "Target IP: $TARGET_IP" | tee -a $LOGFILE  
echo "Started: $(date)" | tee -a $LOGFILE
echo "Press Ctrl+C to stop monitoring" | tee -a $LOGFILE
echo "" | tee -a $LOGFILE

# Counter for attempts
ATTEMPT=1

while true; do
    echo "=== ATTEMPT $ATTEMPT - $(date) ===" | tee -a $LOGFILE
    
    # Test DNS resolution
    if RESOLVED_IP=$(dig +short $DOMAIN 2>/dev/null) && [ -n "$RESOLVED_IP" ]; then
        echo "🟢 SUCCESS! $DOMAIN resolves to: $RESOLVED_IP" | tee -a $LOGFILE
        
        if [ "$RESOLVED_IP" == "$TARGET_IP" ]; then
            echo "✅ IP matches target perfectly!" | tee -a $LOGFILE
        else
            echo "⚠️ IP different from target ($TARGET_IP)" | tee -a $LOGFILE
        fi
        
        # Test HTTP connectivity
        if curl -s --connect-timeout 5 "http://$DOMAIN" > /dev/null 2>&1; then
            echo "✅ HTTP access working!" | tee -a $LOGFILE
        else
            echo "❌ HTTP access failed" | tee -a $LOGFILE
        fi
        
        if curl -s --connect-timeout 5 -k "https://$DOMAIN" > /dev/null 2>&1; then
            echo "✅ HTTPS access working!" | tee -a $LOGFILE
        else
            echo "❌ HTTPS access failed" | tee -a $LOGFILE
        fi
        
        echo "" | tee -a $LOGFILE
        echo "🎉 DNS IS NOW WORKING! casamx.store is accessible!" | tee -a $LOGFILE
        echo "Demo URLs:" | tee -a $LOGFILE
        echo "  - http://$DOMAIN" | tee -a $LOGFILE
        echo "  - https://$DOMAIN" | tee -a $LOGFILE
        echo "" | tee -a $LOGFILE
        break
        
    else
        echo "❌ Still not resolving (NXDOMAIN)" | tee -a $LOGFILE
        
        # Test Cloudflare nameservers
        CF_TEST=$(dig @liv.ns.cloudflare.com +short $DOMAIN 2>/dev/null)
        if [ -n "$CF_TEST" ]; then
            echo "   Cloudflare NS working: $CF_TEST" | tee -a $LOGFILE
        else
            echo "   Cloudflare NS still returns NXDOMAIN" | tee -a $LOGFILE
        fi
    fi
    
    echo "   Waiting 30 seconds for next check..." | tee -a $LOGFILE
    echo "" | tee -a $LOGFILE
    
    ATTEMPT=$((ATTEMPT + 1))
    sleep 30
done

echo "=== MONITORING COMPLETED ===" | tee -a $LOGFILE
echo "Final status: DNS working at $(date)" | tee -a $LOGFILE