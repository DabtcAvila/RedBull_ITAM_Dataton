# CasaMX DigitalOcean Enterprise Deployment Guide

## OBJETIVO CRÍTICO
Deployment profesional de CasaMX en DigitalOcean para ganar el Datatón ITAM 2025.
**casamx.store funcionando en 30-45 minutos**.

## PASO 1: CREAR DROPLET EN DIGITALOCEAN

### 1.1 Configuración del Droplet ($12/mes - 4GB RAM, 2 vCPUs)
```bash
# Specs recomendadas:
- Ubuntu 22.04 LTS
- 4GB RAM / 2 vCPUs / 80GB SSD
- Región: NYC1 o SF03 (menor latencia)
- Enable: Backups, Monitoring, IPv6
```

### 1.2 Configuración Inicial del Servidor
```bash
# SSH al servidor
ssh root@YOUR_DROPLET_IP

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias base
apt install -y curl wget git vim htop nginx certbot python3-certbot-nginx
```

## PASO 2: CONFIGURAR DOMINIO

### 2.1 DNS Configuration
```bash
# En DigitalOcean DNS:
A Record: casamx.store → YOUR_DROPLET_IP
CNAME: www → casamx.store
```

## PASO 3: DEPLOYMENT AUTOMATIZADO

### 3.1 Ejecutar Script Principal
```bash
# En el servidor:
curl -fsSL https://raw.githubusercontent.com/tu-repo/deploy_to_digitalocean.sh | bash
```

### 3.2 Verificar Deployment
```bash
# Verificar servicios
docker ps
systemctl status nginx
curl -I https://casamx.store
```

## PASO 4: VERIFICACIÓN FINAL

### 4.1 Health Checks
- ✅ https://casamx.store (Frontend React)
- ✅ https://casamx.store/api (FastAPI Backend)
- ✅ https://casamx.store/api/docs (Swagger UI)
- ✅ SSL Certificate válido
- ✅ CDN y Gzip activo

### 4.2 Performance Tests
```bash
# Speed test
curl -w "@curl-format.txt" -s -o /dev/null https://casamx.store

# Load test básico
ab -n 100 -c 10 https://casamx.store/
```

## TROUBLESHOOTING

### Common Issues:
1. **SSL No Funciona**: `certbot --nginx -d casamx.store`
2. **Docker No Inicia**: `systemctl restart docker`
3. **Nginx Error**: `nginx -t && systemctl reload nginx`

## MONITORING

### Logs en Tiempo Real:
```bash
# Application logs
docker logs -f casamx-app

# Nginx logs
tail -f /var/log/nginx/access.log

# System resources
htop
```

## BACKUP & RECOVERY

### Automated Backups:
- DigitalOcean Snapshots: Diario
- Database Backup: 6 horas
- Código en GitHub: Automático

## ESCALABILIDAD

### Para más tráfico:
1. Upgrade Droplet: $24/mes (8GB RAM)
2. Load Balancer: $15/mes
3. Managed Database: $15/mes

---

**🚀 TIEMPO TOTAL ESTIMADO: 30-45 MINUTOS**
**🎯 OBJETIVO: casamx.store funcionando perfectamente para el Datatón**