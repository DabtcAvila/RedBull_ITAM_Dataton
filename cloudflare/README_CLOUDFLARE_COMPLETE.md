# Configuración Completa de Cloudflare para casamx.store

## DATATÓN ITAM 2025 - CONFIGURACIÓN CRÍTICA

**Dominio**: casamx.store  
**Tunnel ID**: d198c64a-c169-42ce-9279-e0abdd0b71df  
**Estado**: Configuración lista para producción  

---

## 🚀 INICIO RÁPIDO (5 MINUTOS)

### Prerequisitos Verificados ✅
- Dominio casamx.store comprado en Squarespace
- Tunnel Cloudflare creado: d198c64a-c169-42ce-9279-e0abdd0b71df
- App CasaMX funcionando en localhost:8503

### Secuencia de Configuración

```bash
# 1. Setup inicial (solo una vez)
cd "/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton"
chmod +x cloudflare/*.sh
./cloudflare/setup_casamx_cloudflare.sh

# 2. Configurar DNS en Cloudflare Dashboard (manual)
# Ver: cloudflare/01_GUIA_CLOUDFLARE_DASHBOARD.md

# 3. Cambiar nameservers en Squarespace (manual)
# Ver: cloudflare/02_CAMBIAR_NAMESERVERS_SQUARESPACE.md

# 4. Ejecutar aplicación con tunnel
source casamx_env/bin/activate
./cloudflare/run_casamx_tunnel.sh

# 5. Verificar funcionamiento
./cloudflare/verify_casamx_deployment.sh
```

---

## 📁 ARCHIVOS DE CONFIGURACIÓN

### Scripts Principales
- **`setup_casamx_cloudflare.sh`** - Configuración inicial completa
- **`run_casamx_tunnel.sh`** - Ejecutar aplicación con tunnel
- **`verify_casamx_deployment.sh`** - Verificar que todo funcione

### Guías Paso a Paso
- **`01_GUIA_CLOUDFLARE_DASHBOARD.md`** - Configurar dominio en Cloudflare
- **`02_CAMBIAR_NAMESERVERS_SQUARESPACE.md`** - Cambiar DNS en Squarespace
- **`03_CONFIGURACION_TUNNEL.md`** - Configuración avanzada del tunnel

---

## ⚙️ CONFIGURACIÓN TÉCNICA

### DNS Records Requeridos
```
Type: A     | Name: @   | Content: 198.41.200.63                           | Proxy: ON
Type: CNAME | Name: www | Content: d198c64a-c169-42ce-9279-e0abdd0b71df.cfargotunnel.com | Proxy: ON
```

### Nameservers de Cloudflare
**⚠️ OBTENER DEL DASHBOARD** (únicos por cuenta):
```
ejemplo.ns.cloudflare.com
ejemplo.ns.cloudflare.com
```

### Configuración del Tunnel
```yaml
tunnel: d198c64a-c169-42ce-9279-e0abdd0b71df
credentials-file: ~/.cloudflared/d198c64a-c169-42ce-9279-e0abdd0b71df.json

ingress:
  - hostname: casamx.store
    service: http://localhost:8503
  - hostname: www.casamx.store
    service: http://localhost:8503
  - service: http_status:404
```

---

## 🌐 URLs FINALES

Una vez configurado completamente:
- **Principal**: https://casamx.store
- **WWW**: https://www.casamx.store  
- **Local**: http://localhost:8503

### Características Automáticas
- ✅ HTTPS automático
- ✅ Certificado SSL válido
- ✅ CDN global de Cloudflare
- ✅ Protección DDoS
- ✅ Compresión y optimización
- ✅ Analytics básicos

---

## 🔧 COMANDOS ÚTILES

### Verificar Estado del Tunnel
```bash
cloudflared tunnel list
cloudflared tunnel info d198c64a-c169-42ce-9279-e0abdd0b71df
```

### Logs y Monitoring
```bash
# Logs de Streamlit
tail -f logs/streamlit_tunnel.log

# Logs del tunnel
tail -f ~/.cloudflared/tunnel.log

# Verificar proceso de Streamlit
ps aux | grep streamlit

# Verificar puerto ocupado
lsof -i :8503
```

### Verificación DNS
```bash
# Verificar nameservers
dig NS casamx.store

# Verificar records A
dig A casamx.store

# Verificar records CNAME
dig CNAME www.casamx.store
```

### Test de Conectividad
```bash
# Test básico
curl -I https://casamx.store

# Test con timing
curl -w "@-" -o /dev/null -s https://casamx.store <<'EOF'
     namelookup:  %{time_namelookup}s
        connect:  %{time_connect}s
     appconnect:  %{time_appconnect}s
    pretransfer:  %{time_pretransfer}s
  starttransfer:  %{time_starttransfer}s
          total:  %{time_total}s
EOF
```

---

## 🚨 TROUBLESHOOTING

### Problema: Dominio no resuelve
**Causa**: DNS no propagado o nameservers incorrectos
**Solución**: 
1. Verificar nameservers en Squarespace
2. Esperar propagación (2-48 horas)
3. Usar `dig NS casamx.store` para verificar

### Problema: SSL/HTTPS no funciona  
**Causa**: Certificado no emitido o configuración SSL
**Solución**:
1. Ir a Cloudflare Dashboard → SSL/TLS
2. Configurar modo "Flexible" o "Full"
3. Activar "Always Use HTTPS"

### Problema: App no carga (502/504 errors)
**Causa**: Streamlit no corriendo o puerto incorrecto
**Solución**:
1. Verificar que Streamlit esté en puerto 8503
2. Revisar logs: `tail -f logs/streamlit_tunnel.log`
3. Reiniciar tunnel: `./cloudflare/run_casamx_tunnel.sh`

### Problema: Tunnel no inicia
**Causa**: Credenciales o configuración incorrecta
**Solución**:
1. Re-autenticar: `cloudflared tunnel login`
2. Validar config: `cloudflared tunnel validate ~/.cloudflared/config.yml`
3. Recrear configuración: `./cloudflare/setup_casamx_cloudflare.sh`

---

## 📊 CHECKLIST DE DEPLOYMENT

### Pre-deployment ✅
- [ ] Dominio casamx.store comprado
- [ ] Cuenta Cloudflare creada
- [ ] Tunnel creado con ID: d198c64a-c169-42ce-9279-e0abdd0b71df
- [ ] App CasaMX funcionando localmente

### Configuración Cloudflare ✅
- [ ] Dominio añadido en Cloudflare Dashboard
- [ ] Nameservers obtenidos de Cloudflare
- [ ] DNS Records configurados (A @ y CNAME www)
- [ ] SSL/TLS configurado (Flexible/Full)
- [ ] Optimizaciones activadas

### Configuración Squarespace ✅
- [ ] Nameservers cambiados a Cloudflare
- [ ] Cambios guardados y confirmados
- [ ] Propagación DNS iniciada

### Aplicación ✅
- [ ] Entorno virtual activado
- [ ] Streamlit corriendo en puerto 8503
- [ ] Tunnel configurado y ejecutándose
- [ ] URLs accesibles desde internet

### Verificación Final ✅
- [ ] https://casamx.store carga correctamente
- [ ] https://www.casamx.store carga correctamente
- [ ] HTTPS automático funciona
- [ ] Redirección HTTP → HTTPS activa
- [ ] Certificado SSL válido
- [ ] Performance optimizada

---

## 🎯 PARA EL DATATÓN

### URLs para Demo
```
Principal: https://casamx.store
Backup:    https://www.casamx.store
```

### Comandos de Emergencia
```bash
# Inicio rápido total
source casamx_env/bin/activate && ./cloudflare/run_casamx_tunnel.sh

# Verificación rápida
curl -I https://casamx.store

# Restart completo si algo falla
pkill -f streamlit && pkill -f cloudflared && sleep 2 && ./cloudflare/run_casamx_tunnel.sh
```

### Contactos de Soporte
- **Cloudflare Support**: https://support.cloudflare.com/
- **Squarespace Support**: https://support.squarespace.com/

---

## 🏆 RESULTADO ESPERADO

**Estado Final**: Sistema profesional listo para demo
- ✅ Dominio propio casamx.store
- ✅ HTTPS automático y válido  
- ✅ Performance optimizada con CDN
- ✅ Protección DDoS incluida
- ✅ Analytics básicos disponibles
- ✅ Uptime confiable para demo

**Tiempo total de configuración**: 30-60 minutos  
**Tiempo de propagación DNS**: 2-48 horas  
**Listo para**: Datatón ITAM 2025 🚀

---

**Creado para**: Datatón ITAM 2025  
**Proyecto**: CasaMX - Sistema de Recomendación Inmobiliaria  
**Autor**: David Fernando Ávila Díaz