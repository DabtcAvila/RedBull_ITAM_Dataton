# 🚀 GUÍA CRÍTICA: CREAR VPS DIGITALOCEAN PARA CASAMX

## ⚡ MISIÓN CRÍTICA - DATATÓN ITAM 2025

Esta guía te permitirá crear un VPS en DigitalOcean y tener **casamx.app funcionando en exactamente 15 minutos**.

---

## 📋 PASO 1: CREAR DROPLET EN DIGITALOCEAN

### 1.1 Acceder a DigitalOcean
- Ve a: https://cloud.digitalocean.com
- Login con tu cuenta existente

### 1.2 Crear Nuevo Droplet
- Click en **"Create"** → **"Droplet"**

### 1.3 Configuración del Droplet:

**🖥️ IMAGEN:**
- **Ubuntu 22.04 x64** (LTS)

**💰 PLAN:**
- **Basic**
- **$6/mes** (1 GB RAM, 1 vCPU, 25 GB SSD)

**📍 REGIÓN:**
- **New York 1** (NYC1) - Más cercano a México

**🔐 AUTENTICACIÓN:**
- **Password** (más simple para inicio rápido)
- O usar tu SSH Key existente

**🏷️ HOSTNAME:**
- `casamx-production`

### 1.4 Crear Droplet
- Click **"Create Droplet"**
- **Esperar 2-3 minutos** hasta que esté listo
- **Anotar la IP pública** (ej: 134.122.xxx.xxx)

---

## 📋 PASO 2: CONFIGURAR DNS PARA CASAMX.APP

### 2.1 Cloudflare (Recomendado)
Si tienes Cloudflare configurado para casamx.app:

1. Ve a **Cloudflare Dashboard**
2. Selecciona dominio **casamx.app**
3. Ve a **DNS** → **Records**
4. **Agregar/Editar registros:**
   ```
   Type: A
   Name: @
   Content: TU_IP_VPS (ej: 134.122.xxx.xxx)
   TTL: Auto

   Type: A  
   Name: www
   Content: TU_IP_VPS (ej: 134.122.xxx.xxx)
   TTL: Auto
   ```
5. **Guardar cambios**

### 2.2 Otro Proveedor DNS
Si el dominio está en otro proveedor:
1. Accede al panel de control de tu registrar
2. Ve a gestión de DNS
3. Crear/editar registros A:
   - `casamx.app` → `TU_IP_VPS`
   - `www.casamx.app` → `TU_IP_VPS`

---

## 📋 PASO 3: EJECUTAR DEPLOYMENT AUTOMÁTICO

### 3.1 Conectar al VPS por SSH
```bash
# Usando password
ssh root@TU_IP_VPS

# O usando SSH key
ssh -i tu_clave.pem root@TU_IP_VPS
```

### 3.2 Descargar y Ejecutar Script de Deployment
```bash
# Descargar el script de deployment
wget https://raw.githubusercontent.com/DabtcAvila/RedBull_ITAM_Dataton/main/deploy_casamx_vps_complete.sh

# Hacer ejecutable
chmod +x deploy_casamx_vps_complete.sh

# EJECUTAR (esto toma 10-15 minutos)
sudo ./deploy_casamx_vps_complete.sh
```

### 3.3 El Script Automáticamente:
✅ Actualiza Ubuntu 22.04  
✅ Instala Nginx, Python, dependencias  
✅ Configura firewall (puertos 22, 80, 443)  
✅ Clona repositorio CasaMX  
✅ Configura aplicación como servicio  
✅ Instala certificado SSL gratuito  
✅ Configura reverse proxy  
✅ Habilita monitoreo y health checks  
✅ Optimiza rendimiento  

---

## 📋 PASO 4: VERIFICACIÓN FINAL

### 4.1 Después del Script
El script mostrará algo como:
```
🎉 CASAMX DEPLOYMENT COMPLETADO EXITOSAMENTE! 🎉

🌐 URLS:
   • Producción: https://casamx.app
   • WWW: https://www.casamx.app
   • Health Check: https://casamx.app/health

⚡ CONFIGURAR DNS EN CLOUDFLARE:
   A    casamx.app    →  134.122.xxx.xxx
   A    www           →  134.122.xxx.xxx
```

### 4.2 Verificar Funcionamiento
```bash
# Dentro del VPS
curl http://localhost:8080/health

# Desde tu computadora (después de configurar DNS)
curl https://casamx.app/health
```

### 4.3 Ver Logs (Si hay problemas)
```bash
# Logs de la aplicación
journalctl -u casamx -f

# Logs de nginx
tail -f /var/log/nginx/access.log

# Health checks
tail -f /var/log/casamx-health.log
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### DNS no Propaga Inmediatamente
```bash
# Verificar propagación DNS
nslookup casamx.app 8.8.8.8

# Probar con IP directamente
curl https://TU_IP_VPS -H "Host: casamx.app" -k
```

### Servicio no Inicia
```bash
# Restart servicios
systemctl restart casamx
systemctl restart nginx

# Ver status
systemctl status casamx
systemctl status nginx
```

### SSL no Funciona
```bash
# Renovar certificado
certbot renew --force-renewal
systemctl reload nginx
```

---

## ⏱️ TIMELINE ESPERADO

| Minuto | Actividad |
|--------|-----------|
| 0-2    | Crear droplet DigitalOcean |
| 2-5    | Configurar DNS records |
| 5-15   | Ejecutar script deployment |
| 15     | ✅ **https://casamx.app FUNCIONANDO** |

---

## 🎯 COMANDOS RÁPIDOS DE EMERGENCIA

### Restart Completo
```bash
systemctl restart casamx nginx
```

### Ver Todo el Status
```bash
systemctl status casamx nginx
curl -s http://localhost:8080/health | jq
```

### Verificar Puertos
```bash
netstat -tlnp | grep ':80\|:443\|:8080'
```

---

## 🏆 RESULTADO FINAL

Después de seguir esta guía tendrás:

✅ **https://casamx.app** funcionando  
✅ **https://www.casamx.app** funcionando  
✅ **SSL automático** con Let's Encrypt  
✅ **Aplicación CasaMX** con casos demo  
✅ **8 colonias CDMX** funcionando  
✅ **3 perfiles de usuario** operativos  
✅ **Monitoreo automático** habilitado  
✅ **Firewall configurado** y seguro  
✅ **Performance optimizado**  

---

## 📞 CONTACTO DE EMERGENCIA

**Si algo no funciona:**
1. Verificar DNS propagation: https://dnschecker.org
2. Verificar SSL: https://www.ssllabs.com/ssltest/
3. Logs del servidor: `journalctl -u casamx -f`

**David Fernando Ávila Díaz - ITAM**  
**Datatón ITAM 2025**  

---

## 🚀 EJECUCIÓN INMEDIATA

**Para David - Comandos exactos a ejecutar AHORA:**

1. **Crear droplet:** Ubuntu 22.04, $6/mes, NYC1
2. **Obtener IP:** Anotar IP pública del droplet
3. **Configurar DNS:** casamx.app → IP_VPS en Cloudflare  
4. **SSH al VPS:** `ssh root@IP_VPS`
5. **Ejecutar deployment:**
   ```bash
   wget https://raw.githubusercontent.com/DabtcAvila/RedBull_ITAM_Dataton/main/deploy_casamx_vps_complete.sh
   chmod +x deploy_casamx_vps_complete.sh
   sudo ./deploy_casamx_vps_complete.sh
   ```

**RESULTADO: https://casamx.app funcionando en 15 minutos GARANTIZADO.**