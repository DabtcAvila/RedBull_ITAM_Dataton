#!/bin/bash
# Test deployment continuo hasta SUCCESS
# David Fernando Ávila Díaz - ITAM

echo "🎯 TESTING CASAMX DEPLOYMENT..."

# Test múltiples aspectos
test_dns() {
    echo "🔍 Testing DNS..."
    if nslookup casamx.store | grep -q "Address:"; then
        echo "✅ DNS resolving"
        return 0
    else
        echo "❌ DNS not resolving"
        return 1
    fi
}

test_http() {
    echo "🌐 Testing HTTP..."
    if curl -s -I http://casamx.store | grep -q "200\|301\|302"; then
        echo "✅ HTTP working"
        return 0
    else
        echo "❌ HTTP not working"
        return 1
    fi
}

test_https() {
    echo "🔒 Testing HTTPS..."
    if curl -s -I https://casamx.store | grep -q "200\|301\|302"; then
        echo "✅ HTTPS working"
        return 0
    else
        echo "❌ HTTPS not working"
        return 1
    fi
}

# Loop hasta que funcione
for i in {1..20}; do
    echo ""
    echo "🔄 Test Round $i - $(date)"
    echo "================================"
    
    if test_dns && test_https; then
        echo ""
        echo "🎉🎉🎉 ¡¡¡CASAMX.STORE FUNCIONANDO!!! 🎉🎉🎉"
        echo "✅ DNS: OK"
        echo "✅ HTTPS: OK" 
        echo "🌐 URL: https://casamx.store"
        echo "🏆 LISTO PARA DATATÓN ITAM 2025!"
        break
    else
        echo "⏳ Build aún en progreso... esperando 2 minutos"
        sleep 120
    fi
done