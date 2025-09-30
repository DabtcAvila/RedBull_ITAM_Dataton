# CasaMX DigitalOcean Deployment Checklist

## PRE-DEPLOYMENT (5-10 minutos)

### ✅ Requisitos Previos
- [ ] Cuenta DigitalOcean con billing configurado
- [ ] Dominio casamx.store configurado
- [ ] Acceso SSH configurado
- [ ] GitHub repo actualizado con código

### ✅ Preparación Local
- [ ] Validar que todos los scripts tienen permisos de ejecución
- [ ] Verificar .env.example está actualizado
- [ ] Confirmar requirements.txt incluye dependencias production

## DEPLOYMENT FASE 1: SERVIDOR (15 minutos)

### ✅ Crear Droplet
- [ ] Ubuntu 22.04 LTS
- [ ] 4GB RAM / 2 vCPUs / 80GB SSD
- [ ] Región: NYC1 o SF03
- [ ] Enable: Backups, Monitoring, IPv6
- [ ] SSH Key añadida
- [ ] **ANOTAR IP DEL DROPLET: `___________________`**

### ✅ Configuración DNS
- [ ] A Record: `casamx.store` → Droplet IP
- [ ] CNAME: `www` → casamx.store
- [ ] Verificar propagación DNS: `nslookup casamx.store`

### ✅ Acceso SSH
- [ ] `ssh root@DROPLET_IP` funciona
- [ ] Actualizar sistema: `apt update && apt upgrade -y`

## DEPLOYMENT FASE 2: AUTOMATIZACIÓN (20-25 minutos)

### ✅ Ejecutar Script Principal
```bash
# En el servidor:
curl -fsSL https://raw.githubusercontent.com/tu-repo/deploy_to_digitalocean.sh | bash

# O si prefieres paso a paso:
wget https://raw.githubusercontent.com/tu-repo/deploy_to_digitalocean.sh
chmod +x deploy_to_digitalocean.sh
./deploy_to_digitalocean.sh
```

### ✅ Monitorear Deployment
- [ ] Script se ejecuta sin errores
- [ ] Docker containers se inician correctamente
- [ ] Nginx se configura y reinicia
- [ ] SSL certificates se obtienen automáticamente

### ✅ Verificación Automática
El script debe reportar:
- [ ] ✅ HTTP redirect funcionando
- [ ] ✅ HTTPS funcionando  
- [ ] ✅ API funcionando
- [ ] ✅ Certificado SSL válido
- [ ] ✅ Contenedores Docker funcionando

## DEPLOYMENT FASE 3: VERIFICACIÓN MANUAL (5-10 minutos)

### ✅ Tests de Conectividad
```bash
# Tests externos
curl -I https://casamx.store
curl -I https://casamx.store/api/
curl -I https://casamx.store/api/docs

# Tests internos (en el servidor)
docker ps
docker logs -f casamx-app
systemctl status nginx
```

### ✅ Performance Test
```bash
# En el servidor:
cd /opt/casamx
./scripts/performance_test.sh quick
```

### ✅ Health Check
```bash
# En el servidor:
./scripts/health_check.sh
```

## CHECKLIST FINAL

### ✅ URLs Funcionando
- [ ] https://casamx.store (Frontend/Landing)
- [ ] https://casamx.store/api/ (API Status)
- [ ] https://casamx.store/api/colonias (Data Endpoint)
- [ ] https://casamx.store/api/docs (Swagger UI)
- [ ] https://casamx.store/health (Health Check)

### ✅ SSL y Seguridad
- [ ] Certificado SSL válido (sin warnings)
- [ ] HTTP redirige a HTTPS automáticamente
- [ ] Headers de seguridad presentes
- [ ] Firewall configurado (solo 22, 80, 443)

### ✅ Performance
- [ ] Response time < 2 segundos
- [ ] Gzip compression activo
- [ ] CDN headers configurados
- [ ] Caching funcionando

### ✅ Monitoring
- [ ] Health checks automáticos activos
- [ ] Logs rotando correctamente
- [ ] Backups programados
- [ ] Prometheus metrics disponibles

## TROUBLESHOOTING RÁPIDO

### 🔧 Si SSL No Funciona:
```bash
certbot --nginx -d casamx.store -d www.casamx.store
systemctl reload nginx
```

### 🔧 Si Docker No Inicia:
```bash
cd /opt/casamx
docker-compose down
docker-compose up -d --build
```

### 🔧 Si API No Responde:
```bash
docker logs casamx-app
docker exec -it casamx-app python -c "import sqlite3; print('DB OK')"
```

### 🔧 Si Nginx Error:
```bash
nginx -t
systemctl status nginx
tail -f /var/log/nginx/error.log
```

## POST-DEPLOYMENT

### ✅ Configuración Adicional
- [ ] Configurar CI/CD con GitHub Actions
- [ ] Setupear alertas de monitoring
- [ ] Documentar credenciales y accesos
- [ ] Realizar backup inicial manual

### ✅ Testing Final
- [ ] Load test con tráfico real
- [ ] Verificar logs por 24 horas
- [ ] Confirmar backups automáticos
- [ ] Validar restore procedures

---

## TIEMPOS ESTIMADOS

| Fase | Tiempo | Actividad |
|------|--------|-----------|
| Pre-deployment | 5-10 min | Setup local y DNS |
| Servidor Setup | 15 min | Droplet y configuración |
| Auto Deployment | 20-25 min | Scripts automatizados |
| Verificación | 5-10 min | Tests y validación |
| **TOTAL** | **45-60 min** | **Deployment completo** |

## CONTACTOS DE EMERGENCIA

- **DevOps Lead**: [Tu contacto]
- **DigitalOcean Support**: Panel de control
- **DNS Provider**: [Proveedor DNS]
- **Monitoring**: Alerts configuradas

---

**🎯 OBJETIVO: casamx.store funcionando perfectamente para el Datatón ITAM 2025**

**⚡ CRÍTICO: Deployment debe completarse 24-48 horas antes del evento**