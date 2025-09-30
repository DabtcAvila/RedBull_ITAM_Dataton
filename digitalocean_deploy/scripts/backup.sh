#!/bin/bash

# CasaMX Backup Script
# Complete backup solution for production deployment

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/opt/backups}"
APP_DIR="${APP_DIR:-/opt/casamx}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
S3_BUCKET="${S3_BUCKET:-}"
DO_SPACES_BUCKET="${DO_SPACES_BUCKET:-}"

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Create backup directories
setup_backup_dirs() {
    log "Configurando directorios de backup..."
    
    mkdir -p "$BACKUP_DIR"/{daily,weekly,monthly,database,config,logs}
    
    # Set permissions
    chmod 700 "$BACKUP_DIR"
    chown root:root "$BACKUP_DIR"
}

# Database backup
backup_database() {
    local backup_type="$1"
    local timestamp=$(date +'%Y%m%d_%H%M%S')
    local db_backup_dir="$BACKUP_DIR/database/$backup_type"
    
    mkdir -p "$db_backup_dir"
    
    log "Realizando backup de base de datos ($backup_type)..."
    
    # SQLite backup
    if [[ -f "$APP_DIR/data/casamx.db" ]]; then
        cp "$APP_DIR/data/casamx.db" "$db_backup_dir/casamx_${timestamp}.db"
        
        # Compress database backup
        gzip "$db_backup_dir/casamx_${timestamp}.db"
        
        # Verify backup integrity
        if zcat "$db_backup_dir/casamx_${timestamp}.db.gz" | sqlite3 ":memory:" ".schema" > /dev/null 2>&1; then
            log "✅ Database backup verified: casamx_${timestamp}.db.gz"
        else
            error "❌ Database backup verification failed"
        fi
        
        # Create readable backup info
        cat > "$db_backup_dir/casamx_${timestamp}_info.txt" << EOF
Database Backup Information
==========================
Backup Date: $(date)
Backup Type: $backup_type
Original Size: $(du -h "$APP_DIR/data/casamx.db" | cut -f1)
Compressed Size: $(du -h "$db_backup_dir/casamx_${timestamp}.db.gz" | cut -f1)
Tables: $(sqlite3 "$APP_DIR/data/casamx.db" ".tables" 2>/dev/null || echo "Unable to read tables")
Record Count: $(sqlite3 "$APP_DIR/data/casamx.db" "SELECT COUNT(*) FROM colonias;" 2>/dev/null || echo "N/A")
EOF
    else
        warning "Database file not found: $APP_DIR/data/casamx.db"
    fi
}

# Configuration backup
backup_config() {
    local backup_type="$1"
    local timestamp=$(date +'%Y%m%d_%H%M%S')
    local config_backup_dir="$BACKUP_DIR/config/$backup_type"
    
    mkdir -p "$config_backup_dir"
    
    log "Realizando backup de configuración ($backup_type)..."
    
    # Backup application configuration
    cd "$APP_DIR"
    
    # Files to backup
    local config_files=(
        ".env"
        "docker-compose.yml"
        "nginx.conf"
        "Dockerfile"
    )
    
    # Create config backup archive
    tar -czf "$config_backup_dir/config_${timestamp}.tar.gz" \
        "${config_files[@]}" \
        scripts/ \
        2>/dev/null || warning "Some config files may be missing"
    
    # Backup system configuration
    tar -czf "$config_backup_dir/system_${timestamp}.tar.gz" \
        /etc/nginx/nginx.conf \
        /etc/systemd/system/casamx*.service \
        /etc/cron.d/casamx* \
        2>/dev/null || warning "Some system config files may be missing"
    
    # Create backup manifest
    cat > "$config_backup_dir/manifest_${timestamp}.txt" << EOF
Configuration Backup Manifest
============================
Backup Date: $(date)
Backup Type: $backup_type
Application Config: config_${timestamp}.tar.gz
System Config: system_${timestamp}.tar.gz

Files included:
$(tar -tzf "$config_backup_dir/config_${timestamp}.tar.gz" 2>/dev/null | sed 's/^/  - /')

System files:
$(tar -tzf "$config_backup_dir/system_${timestamp}.tar.gz" 2>/dev/null | sed 's/^/  - /' || echo "  - None found")
EOF
    
    log "✅ Configuration backup completed"
}

# Logs backup
backup_logs() {
    local backup_type="$1"
    local timestamp=$(date +'%Y%m%d_%H%M%S')
    local logs_backup_dir="$BACKUP_DIR/logs/$backup_type"
    
    mkdir -p "$logs_backup_dir"
    
    log "Realizando backup de logs ($backup_type)..."
    
    # Application logs
    if [[ -d "$APP_DIR/logs" ]]; then
        tar -czf "$logs_backup_dir/app_logs_${timestamp}.tar.gz" -C "$APP_DIR" logs/
    fi
    
    # System logs
    tar -czf "$logs_backup_dir/system_logs_${timestamp}.tar.gz" \
        /var/log/nginx/ \
        /var/log/syslog \
        /var/log/auth.log \
        /var/log/fail2ban.log \
        2>/dev/null || warning "Some system logs may not be accessible"
    
    # Docker logs
    docker logs casamx-app > "$logs_backup_dir/docker_casamx_app_${timestamp}.log" 2>&1 || warning "Could not get casamx-app logs"
    docker logs casamx-redis > "$logs_backup_dir/docker_casamx_redis_${timestamp}.log" 2>&1 || warning "Could not get casamx-redis logs"
    docker logs casamx-nginx > "$logs_backup_dir/docker_casamx_nginx_${timestamp}.log" 2>&1 || warning "Could not get casamx-nginx logs"
    
    log "✅ Logs backup completed"
}

# Full application backup
backup_full() {
    local backup_type="$1"
    local timestamp=$(date +'%Y%m%d_%H%M%S')
    local full_backup_dir="$BACKUP_DIR/$backup_type"
    
    mkdir -p "$full_backup_dir"
    
    log "Realizando backup completo ($backup_type)..."
    
    # Stop application for consistent backup
    info "Pausando aplicación para backup consistente..."
    cd "$APP_DIR"
    docker-compose pause casamx-app
    
    # Create full backup
    tar -czf "$full_backup_dir/casamx_full_${timestamp}.tar.gz" \
        --exclude="*.log" \
        --exclude="*.tmp" \
        --exclude=".git" \
        -C "$(dirname "$APP_DIR")" \
        "$(basename "$APP_DIR")"
    
    # Resume application
    docker-compose unpause casamx-app
    info "Aplicación reanudada"
    
    # Create backup info
    cat > "$full_backup_dir/backup_info_${timestamp}.txt" << EOF
Full Backup Information
======================
Backup Date: $(date)
Backup Type: $backup_type
Backup Size: $(du -h "$full_backup_dir/casamx_full_${timestamp}.tar.gz" | cut -f1)
Application Directory: $APP_DIR
Docker Containers: $(docker ps --format "table {{.Names}}\t{{.Status}}" | grep casamx)

Backup Contents:
$(tar -tzf "$full_backup_dir/casamx_full_${timestamp}.tar.gz" | head -20)
$([ $(tar -tzf "$full_backup_dir/casamx_full_${timestamp}.tar.gz" | wc -l) -gt 20 ] && echo "... and $(( $(tar -tzf "$full_backup_dir/casamx_full_${timestamp}.tar.gz" | wc -l) - 20 )) more files")
EOF
    
    log "✅ Full backup completed: $(du -h "$full_backup_dir/casamx_full_${timestamp}.tar.gz" | cut -f1)"
}

# Upload to cloud storage
upload_to_cloud() {
    local backup_file="$1"
    local backup_name=$(basename "$backup_file")
    
    # AWS S3 Upload
    if [[ -n "$S3_BUCKET" ]] && command -v aws &> /dev/null; then
        log "Subiendo a AWS S3: $S3_BUCKET..."
        aws s3 cp "$backup_file" "s3://$S3_BUCKET/casamx-backups/$backup_name" && \
        log "✅ Uploaded to S3: $backup_name" || \
        warning "Failed to upload to S3"
    fi
    
    # DigitalOcean Spaces Upload
    if [[ -n "$DO_SPACES_BUCKET" ]] && command -v s3cmd &> /dev/null; then
        log "Subiendo a DigitalOcean Spaces: $DO_SPACES_BUCKET..."
        s3cmd put "$backup_file" "s3://$DO_SPACES_BUCKET/casamx-backups/$backup_name" && \
        log "✅ Uploaded to DO Spaces: $backup_name" || \
        warning "Failed to upload to DO Spaces"
    fi
}

# Cleanup old backups
cleanup_old_backups() {
    log "Limpiando backups antiguos (>${RETENTION_DAYS} días)..."
    
    # Find and delete old backups
    find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_DIR" -type f -name "*.db.gz" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_DIR" -type f -name "*.log" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_DIR" -type f -name "*.txt" -mtime +$RETENTION_DAYS -delete
    
    # Remove empty directories
    find "$BACKUP_DIR" -type d -empty -delete 2>/dev/null || true
    
    log "✅ Cleanup completed"
}

# Verify backup integrity
verify_backup() {
    local backup_file="$1"
    
    log "Verificando integridad del backup: $backup_file..."
    
    if [[ "$backup_file" == *.tar.gz ]]; then
        if tar -tzf "$backup_file" > /dev/null 2>&1; then
            log "✅ Backup integrity verified"
            return 0
        else
            error "❌ Backup integrity check failed"
            return 1
        fi
    elif [[ "$backup_file" == *.db.gz ]]; then
        if zcat "$backup_file" | sqlite3 ":memory:" ".schema" > /dev/null 2>&1; then
            log "✅ Database backup integrity verified"
            return 0
        else
            error "❌ Database backup integrity check failed"
            return 1
        fi
    fi
}

# Restore from backup
restore_backup() {
    local backup_file="$1"
    local restore_type="${2:-full}"
    
    log "🔄 Iniciando restauración desde: $backup_file"
    
    # Verify backup before restore
    verify_backup "$backup_file" || error "Cannot restore from corrupted backup"
    
    # Create restore point
    local restore_timestamp=$(date +'%Y%m%d_%H%M%S')
    mkdir -p "$BACKUP_DIR/restore_points"
    
    case "$restore_type" in
        "full")
            log "Realizando restauración completa..."
            
            # Backup current state
            tar -czf "$BACKUP_DIR/restore_points/pre_restore_${restore_timestamp}.tar.gz" -C "$(dirname "$APP_DIR")" "$(basename "$APP_DIR")"
            
            # Stop application
            cd "$APP_DIR"
            docker-compose down
            
            # Extract backup
            cd "$(dirname "$APP_DIR")"
            tar -xzf "$backup_file"
            
            # Start application
            cd "$APP_DIR"
            docker-compose up -d
            ;;
            
        "database")
            log "Realizando restauración de base de datos..."
            
            # Backup current database
            cp "$APP_DIR/data/casamx.db" "$BACKUP_DIR/restore_points/casamx_pre_restore_${restore_timestamp}.db"
            
            # Restore database
            zcat "$backup_file" > "$APP_DIR/data/casamx.db"
            
            # Restart application
            cd "$APP_DIR"
            docker-compose restart casamx-app
            ;;
            
        "config")
            log "Realizando restauración de configuración..."
            
            # Backup current config
            cd "$APP_DIR"
            tar -czf "$BACKUP_DIR/restore_points/config_pre_restore_${restore_timestamp}.tar.gz" .env docker-compose.yml nginx.conf
            
            # Extract config
            tar -xzf "$backup_file"
            
            # Restart services
            docker-compose down && docker-compose up -d
            systemctl reload nginx
            ;;
    esac
    
    log "✅ Restauración completada"
}

# Generate backup report
generate_backup_report() {
    local report_file="$BACKUP_DIR/backup_report_$(date +'%Y%m%d').txt"
    
    log "📊 Generando reporte de backups..."
    
    cat > "$report_file" << EOF
CasaMX Backup Report
==================
Generated: $(date)
Backup Directory: $BACKUP_DIR
Retention Policy: $RETENTION_DAYS days

Backup Summary:
--------------
$(find "$BACKUP_DIR" -name "*.tar.gz" -o -name "*.db.gz" | wc -l) total backup files
$(du -sh "$BACKUP_DIR" | cut -f1) total backup size

Recent Backups:
--------------
$(find "$BACKUP_DIR" -type f \( -name "*.tar.gz" -o -name "*.db.gz" \) -mtime -7 -exec ls -lh {} \; | awk '{print $9 " - " $5 " - " $6 " " $7 " " $8}' | sort)

Backup Types:
------------
Daily Backups: $(find "$BACKUP_DIR/daily" -name "*.tar.gz" 2>/dev/null | wc -l)
Weekly Backups: $(find "$BACKUP_DIR/weekly" -name "*.tar.gz" 2>/dev/null | wc -l)
Monthly Backups: $(find "$BACKUP_DIR/monthly" -name "*.tar.gz" 2>/dev/null | wc -l)
Database Backups: $(find "$BACKUP_DIR/database" -name "*.db.gz" 2>/dev/null | wc -l)
Config Backups: $(find "$BACKUP_DIR/config" -name "*.tar.gz" 2>/dev/null | wc -l)

Disk Usage:
-----------
$(df -h "$BACKUP_DIR" | tail -1)

Next Actions:
------------
- Monitor backup sizes for growth trends
- Test restore procedures regularly
- Consider cloud storage for offsite backups
- Review retention policies based on compliance requirements
EOF

    log "📊 Reporte generado: $report_file"
}

# Main function
main() {
    local backup_type="${1:-daily}"
    local timestamp=$(date +'%Y%m%d_%H%M%S')
    
    log "🚀 Iniciando backup CasaMX ($backup_type)..."
    
    setup_backup_dirs
    
    case "$backup_type" in
        "daily")
            backup_database "daily"
            backup_config "daily"
            backup_logs "daily"
            ;;
        "weekly")
            backup_database "weekly"
            backup_config "weekly"
            backup_logs "weekly"
            backup_full "weekly"
            ;;
        "monthly")
            backup_full "monthly"
            generate_backup_report
            ;;
        "database")
            backup_database "manual"
            ;;
        "config")
            backup_config "manual"
            ;;
        "full")
            backup_full "manual"
            ;;
        *)
            error "Unknown backup type: $backup_type"
            ;;
    esac
    
    cleanup_old_backups
    
    log "✅ Backup completado exitosamente!"
    
    # Show backup summary
    echo
    info "📊 Backup Summary:"
    echo "   Type: $backup_type"
    echo "   Date: $(date)"
    echo "   Location: $BACKUP_DIR"
    echo "   Total Size: $(du -sh "$BACKUP_DIR" | cut -f1)"
    echo "   Files: $(find "$BACKUP_DIR" -type f | wc -l)"
}

# Handle command line arguments
case "${1:-daily}" in
    "daily"|"weekly"|"monthly"|"database"|"config"|"full")
        main "$1"
        ;;
    "restore")
        if [[ $# -lt 2 ]]; then
            error "Usage: $0 restore <backup_file> [restore_type]"
        fi
        restore_backup "$2" "${3:-full}"
        ;;
    "report")
        generate_backup_report
        ;;
    "verify")
        if [[ $# -lt 2 ]]; then
            error "Usage: $0 verify <backup_file>"
        fi
        verify_backup "$2"
        ;;
    "cleanup")
        cleanup_old_backups
        ;;
    *)
        echo "Usage: $0 {daily|weekly|monthly|database|config|full|restore|report|verify|cleanup}"
        echo ""
        echo "Backup types:"
        echo "  daily    - Database, config, and logs"
        echo "  weekly   - All of the above plus full application backup"
        echo "  monthly  - Full backup with extended retention"
        echo "  database - Database only"
        echo "  config   - Configuration files only"
        echo "  full     - Complete application backup"
        echo ""
        echo "Other commands:"
        echo "  restore  - Restore from backup file"
        echo "  report   - Generate backup report"
        echo "  verify   - Verify backup integrity"
        echo "  cleanup  - Remove old backups"
        exit 1
        ;;
esac