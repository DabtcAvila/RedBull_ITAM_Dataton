#!/bin/bash

# EMERGENCY DNS SOLUTIONS FOR DATATON DEMO
# Use these if Cloudflare zone setup is taking too long

DOMAIN="casamx.store"
TARGET_IP="198.41.200.63"

echo "=== EMERGENCY DNS SOLUTIONS ==="
echo "Domain: $DOMAIN"
echo "Target IP: $TARGET_IP"
echo ""

# Solution 1: Local hosts file
setup_hosts_file() {
    echo "SOLUTION 1: Local hosts file entry"
    echo "This will make $DOMAIN resolve locally on this machine only"
    echo ""
    
    # Check if entry already exists
    if grep -q "$DOMAIN" /etc/hosts; then
        echo "Entry already exists in /etc/hosts"
        grep "$DOMAIN" /etc/hosts
    else
        echo "Adding entry to /etc/hosts..."
        echo "# Temporary entry for Dataton demo" | sudo tee -a /etc/hosts
        echo "$TARGET_IP $DOMAIN" | sudo tee -a /etc/hosts
        echo "$TARGET_IP www.$DOMAIN" | sudo tee -a /etc/hosts
        echo "✅ Entry added to /etc/hosts"
    fi
    
    echo "Testing local resolution:"
    ping -c 2 $DOMAIN
}

# Solution 2: Direct IP access
test_direct_ip() {
    echo "SOLUTION 2: Direct IP access"
    echo "Use this URL for demo if DNS isn't working:"
    echo "  HTTP:  http://$TARGET_IP"
    echo "  HTTPS: https://$TARGET_IP"
    echo ""
    
    echo "Testing direct IP access:"
    curl -I "http://$TARGET_IP" --connect-timeout 10
    echo ""
    curl -I "https://$TARGET_IP" --connect-timeout 10 -k
}

# Solution 3: ngrok tunnel (if needed)
setup_ngrok() {
    echo "SOLUTION 3: ngrok tunnel (backup)"
    echo "If you have ngrok installed and want a public URL:"
    echo ""
    
    if command -v ngrok &> /dev/null; then
        echo "ngrok is available"
        echo "To create tunnel, run in another terminal:"
        echo "  ngrok http $TARGET_IP:80"
    else
        echo "ngrok not installed"
        echo "Install with: brew install ngrok"
    fi
}

# Menu selection
echo "Choose solution:"
echo "1. Setup local hosts file (recommended for demo)"
echo "2. Test direct IP access"
echo "3. ngrok tunnel info"
echo "4. All solutions"
echo ""

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        setup_hosts_file
        ;;
    2)
        test_direct_ip
        ;;
    3)
        setup_ngrok
        ;;
    4)
        setup_hosts_file
        echo ""
        test_direct_ip
        echo ""
        setup_ngrok
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=== NEXT STEPS ==="
echo "1. If using hosts file: Domain should resolve locally now"
echo "2. If using direct IP: Use the IP URLs for demo"
echo "3. Continue monitoring DNS with: ./verify_dns_status.sh"
echo "4. Once Cloudflare zone is added, DNS will work globally"