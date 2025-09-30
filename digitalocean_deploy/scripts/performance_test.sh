#!/bin/bash

# CasaMX Performance Testing Script
# Tests load, response times, and overall performance

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
DOMAIN="${DOMAIN:-casamx.store}"
CONCURRENT_USERS="${CONCURRENT_USERS:-10}"
TOTAL_REQUESTS="${TOTAL_REQUESTS:-100}"
TEST_DURATION="${TEST_DURATION:-60}"

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Install dependencies if needed
install_dependencies() {
    log "Verificando herramientas de testing..."
    
    # Check for Apache Bench
    if ! command -v ab &> /dev/null; then
        info "Instalando Apache Bench..."
        apt-get update && apt-get install -y apache2-utils
    fi
    
    # Check for curl
    if ! command -v curl &> /dev/null; then
        info "Instalando curl..."
        apt-get update && apt-get install -y curl
    fi
    
    # Check for wrk (advanced load testing)
    if ! command -v wrk &> /dev/null; then
        info "Instalando wrk..."
        git clone https://github.com/wg/wrk.git /tmp/wrk
        cd /tmp/wrk && make && cp wrk /usr/local/bin/
        cd - && rm -rf /tmp/wrk
    fi
}

# Basic response time test
response_time_test() {
    log "🚀 Probando tiempos de respuesta..."
    
    local urls=(
        "https://$DOMAIN"
        "https://$DOMAIN/api/"
        "https://$DOMAIN/api/colonias"
    )
    
    echo "URL,Response Time (s),Status Code,Size (bytes)"
    
    for url in "${urls[@]}"; do
        local output=$(curl -w "%{time_total},%{http_code},%{size_download}" -s -o /dev/null "$url")
        echo "$url,$output"
    done
    
    log "Tiempos de respuesta completados"
}

# Load test with Apache Bench
load_test_ab() {
    log "📊 Ejecutando load test con Apache Bench..."
    
    local test_url="https://$DOMAIN/"
    
    info "Testing: $test_url"
    info "Concurrent users: $CONCURRENT_USERS"
    info "Total requests: $TOTAL_REQUESTS"
    
    # Run Apache Bench test
    ab -n "$TOTAL_REQUESTS" -c "$CONCURRENT_USERS" -g ab_results.tsv "$test_url" | tee ab_results.txt
    
    # Extract key metrics
    local requests_per_sec=$(grep "Requests per second" ab_results.txt | awk '{print $4}')
    local time_per_request=$(grep "Time per request.*mean" ab_results.txt | head -n1 | awk '{print $4}')
    local failed_requests=$(grep "Failed requests" ab_results.txt | awk '{print $3}')
    
    echo
    log "📈 Resultados del Load Test:"
    echo "   - Requests per second: $requests_per_sec"
    echo "   - Time per request: ${time_per_request}ms"
    echo "   - Failed requests: $failed_requests"
    
    # Performance thresholds
    if (( $(echo "$requests_per_sec > 100" | bc -l) )); then
        log "✅ Excellent performance (>100 req/s)"
    elif (( $(echo "$requests_per_sec > 50" | bc -l) )); then
        log "✅ Good performance (>50 req/s)"
    else
        warning "⚠️  Performance could be improved (<50 req/s)"
    fi
}

# Advanced load test with wrk
load_test_wrk() {
    log "🔥 Ejecutando load test avanzado con wrk..."
    
    local test_url="https://$DOMAIN/"
    
    info "Testing: $test_url"
    info "Concurrent connections: $CONCURRENT_USERS"
    info "Duration: ${TEST_DURATION}s"
    
    # Run wrk test
    wrk -t4 -c"$CONCURRENT_USERS" -d"${TEST_DURATION}s" --timeout=30s "$test_url" | tee wrk_results.txt
    
    log "Load test avanzado completado"
}

# SSL/TLS performance test
ssl_test() {
    log "🔒 Probando rendimiento SSL/TLS..."
    
    local ssl_metrics=$(curl -w "DNS Lookup: %{time_namelookup}s\nTCP Connect: %{time_connect}s\nTLS Handshake: %{time_appconnect}s\nServer Response: %{time_starttransfer}s\nTotal Time: %{time_total}s\n" -s -o /dev/null "https://$DOMAIN")
    
    echo "$ssl_metrics"
    
    # Extract TLS handshake time
    local tls_time=$(echo "$ssl_metrics" | grep "TLS Handshake" | awk '{print $3}' | sed 's/s//')
    
    if (( $(echo "$tls_time < 0.5" | bc -l) )); then
        log "✅ TLS handshake excellent (<0.5s)"
    elif (( $(echo "$tls_time < 1.0" | bc -l) )); then
        log "✅ TLS handshake good (<1.0s)"
    else
        warning "⚠️  TLS handshake slow (>1.0s)"
    fi
}

# API endpoint performance test
api_performance_test() {
    log "🔌 Probando rendimiento de endpoints API..."
    
    local api_endpoints=(
        "/api/"
        "/api/colonias"
        "/health"
    )
    
    echo "Endpoint,Avg Response Time (ms),Min (ms),Max (ms),Success Rate"
    
    for endpoint in "${api_endpoints[@]}"; do
        local url="https://$DOMAIN$endpoint"
        local times=()
        local success=0
        local total=10
        
        # Run 10 requests per endpoint
        for i in $(seq 1 $total); do
            local time_ms=$(curl -w "%{time_total}" -s -o /dev/null "$url" | awk '{print $1 * 1000}')
            local status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
            
            times+=("$time_ms")
            [[ "$status" == "200" ]] && ((success++))
        done
        
        # Calculate statistics
        local sum=0
        local min=999999
        local max=0
        
        for time in "${times[@]}"; do
            sum=$(echo "$sum + $time" | bc -l)
            min=$(echo "if ($time < $min) $time else $min" | bc -l)
            max=$(echo "if ($time > $max) $time else $max" | bc -l)
        done
        
        local avg=$(echo "scale=2; $sum / $total" | bc -l)
        local success_rate=$(echo "scale=1; $success * 100 / $total" | bc -l)
        
        echo "$endpoint,$avg,$min,$max,$success_rate%"
    done
}

# Database performance test
db_performance_test() {
    log "🗄️  Probando rendimiento de base de datos..."
    
    # Test database query performance
    local db_test_result=$(docker exec casamx-app python -c "
import time
import sqlite3
from pathlib import Path

db_path = Path('data/casamx.db')
if not db_path.exists():
    print('Database not found')
    exit(1)

# Test connection time
start_time = time.time()
conn = sqlite3.connect(str(db_path))
connect_time = (time.time() - start_time) * 1000

# Test simple query
start_time = time.time()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM colonias')
result = cursor.fetchone()
query_time = (time.time() - start_time) * 1000

# Test complex query (if data exists)
start_time = time.time()
cursor.execute('SELECT * FROM colonias LIMIT 100')
results = cursor.fetchall()
complex_query_time = (time.time() - start_time) * 1000

conn.close()

print(f'Connect Time: {connect_time:.2f}ms')
print(f'Simple Query: {query_time:.2f}ms')
print(f'Complex Query: {complex_query_time:.2f}ms')
print(f'Rows: {len(results)}')
" 2>/dev/null)
    
    echo "$db_test_result"
    
    local connect_time=$(echo "$db_test_result" | grep "Connect Time" | awk '{print $3}' | sed 's/ms//')
    
    if (( $(echo "$connect_time < 10" | bc -l) )); then
        log "✅ Database connection excellent (<10ms)"
    elif (( $(echo "$connect_time < 50" | bc -l) )); then
        log "✅ Database connection good (<50ms)"
    else
        warning "⚠️  Database connection slow (>50ms)"
    fi
}

# Memory and CPU usage during load
resource_usage_test() {
    log "📊 Monitoreando uso de recursos durante carga..."
    
    # Start background monitoring
    {
        for i in $(seq 1 30); do
            echo "$(date),$(docker stats --no-stream --format 'table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}' | grep casamx)"
            sleep 2
        done
    } > resource_usage.log &
    
    local monitor_pid=$!
    
    # Run load test during monitoring
    ab -n 200 -c 20 "https://$DOMAIN/" > /dev/null 2>&1
    
    # Stop monitoring
    sleep 5
    kill $monitor_pid 2>/dev/null || true
    
    log "Monitoreo de recursos completado (ver resource_usage.log)"
}

# Generate performance report
generate_performance_report() {
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')
    local report_file="casamx_performance_report_$(date +'%Y%m%d_%H%M%S').html"
    
    log "📊 Generando reporte de rendimiento..."
    
    cat > "$report_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>CasaMX Performance Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f4f4f4; padding: 20px; border-radius: 5px; }
        .metric { margin: 10px 0; }
        .good { color: green; }
        .warning { color: orange; }
        .error { color: red; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 CasaMX Performance Report</h1>
        <p>Generated: $timestamp</p>
        <p>Domain: $DOMAIN</p>
    </div>
    
    <h2>📈 Test Results Summary</h2>
    <div class="metric">
        <strong>Load Test:</strong> $(grep "Requests per second" ab_results.txt 2>/dev/null | awk '{print $4}' || echo "N/A") req/s
    </div>
    <div class="metric">
        <strong>Failed Requests:</strong> $(grep "Failed requests" ab_results.txt 2>/dev/null | awk '{print $3}' || echo "N/A")
    </div>
    <div class="metric">
        <strong>Mean Response Time:</strong> $(grep "Time per request.*mean" ab_results.txt 2>/dev/null | head -n1 | awk '{print $4}' || echo "N/A")ms
    </div>
    
    <h2>📊 Detailed Results</h2>
    <h3>Apache Bench Results:</h3>
    <pre>$(cat ab_results.txt 2>/dev/null || echo "No Apache Bench results found")</pre>
    
    <h3>WRK Results:</h3>
    <pre>$(cat wrk_results.txt 2>/dev/null || echo "No WRK results found")</pre>
    
    <h2>🔍 Recommendations</h2>
    <ul>
        <li>Monitor response times regularly</li>
        <li>Consider CDN for static assets</li>
        <li>Implement database connection pooling</li>
        <li>Enable HTTP/2 and compression</li>
        <li>Set up proper caching strategies</li>
    </ul>
    
    <footer>
        <p><small>Report generated by CasaMX Performance Testing Suite</small></p>
    </footer>
</body>
</html>
EOF
    
    log "📊 Reporte generado: $report_file"
}

# Main function
main() {
    log "🚀 Iniciando suite de pruebas de rendimiento CasaMX..."
    
    install_dependencies
    
    echo
    info "🎯 Configuración de pruebas:"
    echo "   Domain: $DOMAIN"
    echo "   Concurrent users: $CONCURRENT_USERS"
    echo "   Total requests: $TOTAL_REQUESTS"
    echo "   Test duration: ${TEST_DURATION}s"
    echo
    
    response_time_test
    echo
    
    ssl_test
    echo
    
    api_performance_test
    echo
    
    db_performance_test
    echo
    
    load_test_ab
    echo
    
    if command -v wrk &> /dev/null; then
        load_test_wrk
        echo
    fi
    
    resource_usage_test
    echo
    
    generate_performance_report
    
    log "✅ Suite de pruebas de rendimiento completada!"
    
    # Cleanup
    rm -f ab_results.tsv 2>/dev/null || true
    
    echo
    log "📊 Archivos generados:"
    ls -la *.txt *.html *.log 2>/dev/null | grep -E "(ab_results|wrk_results|performance_report|resource_usage)" || echo "No files generated"
}

# Handle command line arguments
case "${1:-full}" in
    "full")
        main
        ;;
    "quick")
        TOTAL_REQUESTS=50
        CONCURRENT_USERS=5
        TEST_DURATION=30
        main
        ;;
    "load")
        load_test_ab
        ;;
    "api")
        api_performance_test
        ;;
    "ssl")
        ssl_test
        ;;
    *)
        echo "Usage: $0 {full|quick|load|api|ssl}"
        echo "  full  - Run complete performance test suite (default)"
        echo "  quick - Run quick performance tests"
        echo "  load  - Run only load tests"
        echo "  api   - Test API endpoints only"
        echo "  ssl   - Test SSL/TLS performance only"
        exit 1
        ;;
esac