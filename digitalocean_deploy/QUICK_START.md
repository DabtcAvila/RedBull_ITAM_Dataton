# 🚀 CasaMX DigitalOcean Quick Start

## DEPLOYMENT EN 30 MINUTOS

### PASO 1: Crear Droplet (5 min)

1. **Login a DigitalOcean**: https://cloud.digitalocean.com
2. **Create Droplet**:
   - **OS**: Ubuntu 22.04 LTS
   - **Plan**: Regular Intel - $12/mo (4GB RAM, 2 vCPUs)
   - **Region**: New York 1 (NYC1)
   - **Authentication**: SSH Key (recomendado) o Password
   - **Options**: ✅ Enable backups, ✅ Monitoring

3. **Anotar IP**: `___.___.___.___`

### PASO 2: Configurar DNS (5 min)

En tu proveedor DNS (Squarespace, Cloudflare, etc.):
```
A Record:     casamx.store     →  DROPLET_IP
CNAME:        www              →  casamx.store
```

**Verificar**: `nslookup casamx.store`

### PASO 3: Deployment Automático (20 min)

```bash
# 1. SSH al servidor
ssh root@DROPLET_IP

# 2. Ejecutar script automático
curl -fsSL https://raw.githubusercontent.com/tu-usuario/RedBull_ITAM_Dataton/main/digitalocean_deploy/deploy_to_digitalocean.sh | bash
```

**O manual**:
```bash
# Descargar y ejecutar
wget https://raw.githubusercontent.com/tu-usuario/RedBull_ITAM_Dataton/main/digitalocean_deploy/deploy_to_digitalocean.sh
chmod +x deploy_to_digitalocean.sh
./deploy_to_digitalocean.sh
```

### PASO 4: Verificación (5 min)

```bash
# Verificar servicios
docker ps
curl -I https://casamx.store
curl -I https://casamx.store/api/

# Health check
./scripts/health_check.sh
```

## RESULTADO ESPERADO

✅ **URLs Funcionando**:
- https://casamx.store - Frontend
- https://casamx.store/api/ - API
- https://casamx.store/api/docs - Swagger
- https://casamx.store/health - Health Check

✅ **SSL**: Certificado válido automático
✅ **Performance**: < 2s response time  
✅ **Security**: Firewall configurado
✅ **Monitoring**: Health checks activos

---

## TROUBLESHOOTING EXPRESS

### ❌ SSL No Funciona
```bash
certbot --nginx -d casamx.store -d www.casamx.store
systemctl reload nginx
```

### ❌ API No Responde  
```bash
cd /opt/casamx
docker-compose restart casamx-app
docker logs casamx-app
```

### ❌ Droplet No Responde
```bash
# En DigitalOcean Console:
# 1. Access → Console
# 2. Login y verificar servicios
systemctl status nginx docker
```

---

## CUSTOMIZACIÓN RÁPIDA

### Cambiar Dominio
```bash
# Editar variables en el servidor
nano /opt/casamx/.env
# Cambiar DOMAIN=tu-dominio.com
docker-compose restart
```

### Actualizar App  
```bash
cd /opt/casamx
git pull origin main
docker-compose build --no-cache
docker-compose up -d
```

### Ver Logs
```bash
# App logs
docker logs -f casamx-app

# Nginx logs  
tail -f /var/log/nginx/access.log

# System logs
journalctl -f -u docker
```

---

## NEXT STEPS

1. **CI/CD**: Configurar GitHub Actions
2. **Monitoring**: Configurar alertas
3. **Backup**: Validar backups automáticos
4. **Scale**: Preparar para más tráfico

**🎯 LISTO PARA EL DATATÓN ITAM 2025!**