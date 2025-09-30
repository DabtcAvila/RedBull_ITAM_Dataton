#!/bin/bash

# DNS FIX SCRIPT FOR casamx.store
# CRITICAL: Domain zone must be added to Cloudflare first

DOMAIN="casamx.store"
TARGET_IP="198.41.200.63"
LOGFILE="/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton/dns_troubleshooting/dns_fix.log"

echo "=== DNS FIX SCRIPT FOR $DOMAIN ===" | tee -a $LOGFILE
echo "Timestamp: $(date)" | tee -a $LOGFILE

# Function to test DNS resolution
test_dns() {
    echo "Testing DNS resolution..." | tee -a $LOGFILE
    
    echo "1. Testing with nslookup:" | tee -a $LOGFILE
    nslookup $DOMAIN | tee -a $LOGFILE
    
    echo "2. Testing with dig:" | tee -a $LOGFILE  
    dig $DOMAIN | tee -a $LOGFILE
    
    echo "3. Testing Cloudflare nameservers directly:" | tee -a $LOGFILE
    dig @liv.ns.cloudflare.com $DOMAIN | tee -a $LOGFILE
    dig @sid.ns.cloudflare.com $DOMAIN | tee -a $LOGFILE
}

# Function to flush DNS cache
flush_dns() {
    echo "Flushing DNS cache..." | tee -a $LOGFILE
    sudo dscacheutil -flushcache
    sudo killall -HUP mDNSResponder
    echo "DNS cache flushed" | tee -a $LOGFILE
}

# Function to test HTTP connectivity
test_http() {
    echo "Testing HTTP connectivity to target IP..." | tee -a $LOGFILE
    curl -I http://$TARGET_IP --connect-timeout 10 | tee -a $LOGFILE
    echo "Testing HTTPS connectivity..." | tee -a $LOGFILE
    curl -I https://$TARGET_IP --connect-timeout 10 -k | tee -a $LOGFILE
}

# Function to check multiple DNS servers
check_multiple_dns() {
    echo "Checking multiple DNS servers..." | tee -a $LOGFILE
    
    DNS_SERVERS=("8.8.8.8" "1.1.1.1" "208.67.222.222" "liv.ns.cloudflare.com" "sid.ns.cloudflare.com")
    
    for server in "${DNS_SERVERS[@]}"; do
        echo "Testing with DNS server $server:" | tee -a $LOGFILE
        dig @$server $DOMAIN | tee -a $LOGFILE
        echo "---" | tee -a $LOGFILE
    done
}

# Main execution
echo "STEP 1: Initial DNS test" | tee -a $LOGFILE
test_dns

echo -e "\nSTEP 2: Flushing local DNS cache" | tee -a $LOGFILE  
flush_dns

echo -e "\nSTEP 3: Testing connectivity to target IP" | tee -a $LOGFILE
test_http

echo -e "\nSTEP 4: Checking multiple DNS servers" | tee -a $LOGFILE
check_multiple_dns

echo -e "\nSTEP 5: Waiting 60 seconds for propagation..." | tee -a $LOGFILE
sleep 60

echo -e "\nSTEP 6: Final DNS test after waiting" | tee -a $LOGFILE
test_dns

echo -e "\n=== MANUAL STEPS REQUIRED ===" | tee -a $LOGFILE
echo "1. Login to Cloudflare Dashboard" | tee -a $LOGFILE
echo "2. Add domain: $DOMAIN" | tee -a $LOGFILE
echo "3. Configure DNS records:" | tee -a $LOGFILE
echo "   A @ -> $TARGET_IP (Proxied)" | tee -a $LOGFILE
echo "   CNAME www -> tunnel (Proxied)" | tee -a $LOGFILE
echo "4. Run this script again after zone is added" | tee -a $LOGFILE

echo -e "\nScript completed. Check $LOGFILE for details." | tee -a $LOGFILE