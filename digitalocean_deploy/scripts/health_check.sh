#!/bin/bash

# CasaMX Health Check Script
# Verifica el estado de todos los servicios

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
DOMAIN="casamx.store"
APP_DIR="/opt/casamx"

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

# Check Docker containers
check_containers() {
    log "Verificando contenedores Docker..."
    
    local containers=("casamx-app" "casamx-redis" "casamx-nginx")
    local failed=0
    
    for container in "${containers[@]}"; do
        if docker ps --filter "name=$container" --filter "status=running" | grep -q "$container"; then
            echo "✅ $container: Running"
        else
            echo "❌ $container: Not running"
            ((failed++))
        fi
    done
    
    if [[ $failed -eq 0 ]]; then
        log "Todos los contenedores están funcionando"
    else
        error "$failed contenedor(es) no están funcionando"
        return 1
    fi
}

# Check application health
check_app_health() {
    log "Verificando salud de la aplicación..."
    
    local endpoints=("http://localhost:8000/health" "http://localhost:8000/api/")
    local failed=0
    
    for endpoint in "${endpoints[@]}"; do
        if curl -f -s "$endpoint" > /dev/null; then
            echo "✅ $endpoint: OK"
        else
            echo "❌ $endpoint: Failed"
            ((failed++))
        fi
    done
    
    if [[ $failed -eq 0 ]]; then
        log "Todos los endpoints están funcionando"
    else
        error "$failed endpoint(s) no están funcionando"
        return 1
    fi
}

# Check external connectivity
check_external() {
    log "Verificando conectividad externa..."
    
    local urls=("https://$DOMAIN" "https://$DOMAIN/api/")
    local failed=0
    
    for url in "${urls[@]}"; do
        local status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        if [[ "$status_code" == "200" ]]; then
            echo "✅ $url: HTTP $status_code"
        else
            echo "❌ $url: HTTP $status_code"
            ((failed++))
        fi
    done
    
    if [[ $failed -eq 0 ]]; then
        log "Conectividad externa OK"
    else
        error "Problemas de conectividad externa"
        return 1
    fi
}

# Check SSL certificate
check_ssl() {
    log "Verificando certificado SSL..."
    
    local expiry_date=$(echo | openssl s_client -connect "$DOMAIN:443" 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
    local expiry_epoch=$(date -d "$expiry_date" +%s)
    local current_epoch=$(date +%s)
    local days_until_expiry=$(( (expiry_epoch - current_epoch) / 86400 ))
    
    if [[ $days_until_expiry -gt 30 ]]; then
        echo "✅ SSL Certificate: Valid for $days_until_expiry days"
    elif [[ $days_until_expiry -gt 7 ]]; then
        warning "SSL Certificate: Expires in $days_until_expiry days (renew soon)"
    else
        error "SSL Certificate: Expires in $days_until_expiry days (URGENT)"
        return 1
    fi
}

# Check system resources
check_resources() {
    log "Verificando recursos del sistema..."
    
    # Memory usage
    local mem_usage=$(free | awk '/Mem:/ {printf("%.1f", $3/$2 * 100)}')
    echo "💾 Memory usage: ${mem_usage}%"
    
    # Disk usage
    local disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    echo "💽 Disk usage: ${disk_usage}%"
    
    # CPU load
    local cpu_load=$(uptime | awk -F'load average:' '{print $2}' | cut -d, -f1 | xargs)
    echo "🖥️  CPU load (1min): $cpu_load"
    
    # Check thresholds
    local warnings=0
    if (( $(echo "$mem_usage > 85" | bc -l) )); then
        warning "High memory usage: ${mem_usage}%"
        ((warnings++))
    fi
    
    if [[ $disk_usage -gt 85 ]]; then
        warning "High disk usage: ${disk_usage}%"
        ((warnings++))
    fi
    
    if [[ $warnings -eq 0 ]]; then
        log "Recursos del sistema OK"
    else
        warning "$warnings advertencia(s) de recursos"
    fi
}

# Check logs for errors
check_logs() {
    log "Verificando logs recientes..."
    
    # Check application logs for errors in last 5 minutes
    local error_count=$(docker logs --since="5m" casamx-app 2>&1 | grep -i "error\|exception\|failed" | wc -l)
    
    if [[ $error_count -eq 0 ]]; then
        echo "✅ No errors in application logs (last 5 minutes)"
    else
        warning "$error_count error(s) found in application logs"
        info "Recent errors:"
        docker logs --since="5m" casamx-app 2>&1 | grep -i "error\|exception\|failed" | tail -3
    fi
    
    # Check nginx logs
    local nginx_errors=$(tail -n 100 /var/log/nginx/error.log | grep "$(date +'%Y/%m/%d %H:%M')" | wc -l)
    
    if [[ $nginx_errors -eq 0 ]]; then
        echo "✅ No errors in Nginx logs (last minute)"
    else
        warning "$nginx_errors error(s) in Nginx logs"
    fi
}

# Performance check
performance_check() {
    log "Verificando rendimiento..."
    
    # Response time check
    local response_time=$(curl -w "%{time_total}" -s -o /dev/null "https://$DOMAIN")
    
    if (( $(echo "$response_time < 2.0" | bc -l) )); then
        echo "✅ Response time: ${response_time}s"
    else
        warning "Slow response time: ${response_time}s"
    fi
    
    # Database connection check (if applicable)
    cd "$APP_DIR"
    if docker exec casamx-app python -c "
import sqlite3
try:
    conn = sqlite3.connect('data/casamx.db')
    conn.execute('SELECT 1')
    conn.close()
    print('✅ Database: OK')
except Exception as e:
    print(f'❌ Database: {e}')
    exit(1)
" 2>/dev/null; then
        echo "Database connection successful"
    else
        error "Database connection failed"
        return 1
    fi
}

# Generate health report
generate_report() {
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')
    local report_file="/var/log/casamx_health_$(date +'%Y%m%d').log"
    
    {
        echo "======================================"
        echo "CasaMX Health Check Report"
        echo "Timestamp: $timestamp"
        echo "======================================"
        echo
    } >> "$report_file"
    
    # Run all checks and capture results
    {
        check_containers
        check_app_health
        check_external
        check_ssl
        check_resources
        check_logs
        performance_check
    } 2>&1 | tee -a "$report_file"
    
    echo "Report saved to: $report_file"
}

# Auto-recovery function
auto_recovery() {
    log "Iniciando recuperación automática..."
    
    cd "$APP_DIR"
    
    # Restart failed containers
    if ! docker ps --filter "name=casamx-app" --filter "status=running" | grep -q "casamx-app"; then
        warning "Reiniciando casamx-app..."
        docker-compose restart casamx-app
        sleep 30
    fi
    
    if ! docker ps --filter "name=casamx-redis" --filter "status=running" | grep -q "casamx-redis"; then
        warning "Reiniciando casamx-redis..."
        docker-compose restart casamx-redis
        sleep 15
    fi
    
    # Reload nginx if needed
    if ! systemctl is-active --quiet nginx; then
        warning "Reiniciando nginx..."
        systemctl restart nginx
    fi
    
    log "Recuperación automática completada"
}

# Main function
main() {
    log "🔍 Iniciando health check de CasaMX..."
    
    local exit_code=0
    
    check_containers || exit_code=$?
    check_app_health || exit_code=$?
    check_external || exit_code=$?
    check_ssl || exit_code=$?
    check_resources
    check_logs
    performance_check || exit_code=$?
    
    if [[ $exit_code -ne 0 ]]; then
        error "Health check failed with exit code $exit_code"
        
        # Auto-recovery if enabled
        if [[ "${AUTO_RECOVERY:-false}" == "true" ]]; then
            auto_recovery
            
            # Re-run critical checks
            log "Re-verificando después de recuperación..."
            check_containers && check_app_health && check_external
            exit_code=$?
        fi
    else
        log "✅ All health checks passed!"
    fi
    
    # Generate report if requested
    if [[ "${GENERATE_REPORT:-false}" == "true" ]]; then
        generate_report
    fi
    
    exit $exit_code
}

# Handle command line arguments
case "${1:-check}" in
    "check")
        main
        ;;
    "report")
        GENERATE_REPORT=true main
        ;;
    "recovery")
        AUTO_RECOVERY=true main
        ;;
    "monitor")
        while true; do
            main
            sleep 60
        done
        ;;
    *)
        echo "Usage: $0 {check|report|recovery|monitor}"
        echo "  check    - Run health checks (default)"
        echo "  report   - Run checks and generate report"
        echo "  recovery - Run checks with auto-recovery"
        echo "  monitor  - Continuous monitoring (every 60s)"
        exit 1
        ;;
esac