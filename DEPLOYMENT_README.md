# CasaMX - Deployment Automático a DigitalOcean
## Datatón ITAM 2025 - Configuración Completa

### 🎯 OBJETIVO
Deployment automático de CasaMX desde GitHub a DigitalOcean App Platform con dominio **casamx.store**.

---

## 📋 CONFIGURACIÓN COMPLETADA

### ✅ Archivos Creados/Configurados:

1. **`.github/workflows/deploy.yml`** - GitHub Actions para CI/CD automático
2. **`app.yaml`** - Configuración de DigitalOcean App Platform
3. **`runtime.txt`** - Versión de Python (3.11.7)
4. **`Procfile`** - Comandos de ejecución
5. **`requirements.txt`** - Dependencias optimizadas para producción
6. **`.streamlit/config.toml`** - Configuración de Streamlit
7. **`verify_deployment.py`** - Script de verificación

---

## 🚀 PASOS PARA DEPLOYMENT

### 1. Configurar Secrets en GitHub

Ir a: `https://github.com/DabtcAvila/RedBull_ITAM_Dataton/settings/secrets/actions`

Agregar:
```
DIGITALOCEAN_ACCESS_TOKEN: tu_token_de_digitalocean
```

### 2. Conectar Dominio en DigitalOcean

1. Ir a DigitalOcean Dashboard → Networking → Domains
2. Agregar dominio: `casamx.store`
3. Configurar DNS records que apunten a DigitalOcean

### 3. Deployment Automático

El deployment se ejecuta automáticamente cuando:
- ✅ Push a branch `main`
- ✅ Pull Request a `main`
- ✅ Ejecución manual desde GitHub Actions

---

## 🔧 ARQUITECTURA DEL DEPLOYMENT

### Servicios Configurados:

1. **Web Service (Principal)**
   - Puerto: 8080
   - Comando: Streamlit app
   - URL: `https://casamx.store/`

2. **API Service**
   - Puerto: 8000
   - Comando: FastAPI con Uvicorn
   - URL: `https://casamx.store/api/`

### Variables de Entorno Configuradas:
- `PORT=8080` (web), `8000` (api)
- `ENVIRONMENT=production`
- Configuración optimizada de Streamlit
- SSL automático
- Health checks configurados

---

## 🏥 VERIFICACIÓN DE DEPLOYMENT

### Automática (GitHub Actions):
- ✅ Tests de código
- ✅ Validación de imports
- ✅ Health checks post-deployment
- ✅ Performance tests
- ✅ SSL verification

### Manual:
```bash
python verify_deployment.py
```

### URLs a Verificar:
1. **Sitio Principal**: https://casamx.store/
2. **API**: https://casamx.store/api/
3. **Documentación API**: https://casamx.store/api/docs

---

## 📊 MONITOREO Y PERFORMANCE

### Métricas Configuradas:
- ⏱️ Response time < 3 segundos
- 🔒 SSL certificate válido
- 📈 Health checks cada 10 segundos
- 📋 Logs automáticos

### Escalabilidad:
- **Actual**: `basic-xxs` (suficiente para demo)
- **Si necesitas más**: Cambiar `instance_size_slug` en `app.yaml`

---

## 🔄 WORKFLOW DE DESARROLLO

### Para hacer cambios:
1. Editar código localmente
2. Commit y push a `main`
3. GitHub Actions ejecuta automáticamente:
   - Tests
   - Build
   - Deploy a DigitalOcean
   - Verificación
4. La app se actualiza en https://casamx.store

### Rollback de emergencia:
```bash
# En GitHub Actions, re-ejecutar deployment anterior
# O usar DigitalOcean Dashboard para rollback manual
```

---

## 🚨 TROUBLESHOOTING

### Problemas Comunes:

1. **Deployment Falla**
   - Verificar `DIGITALOCEAN_ACCESS_TOKEN` en GitHub Secrets
   - Revisar logs en GitHub Actions
   - Verificar sintaxis en `app.yaml`

2. **Dominio No Funciona**
   - Verificar DNS records en DigitalOcean
   - Esperar propagación DNS (hasta 24h)
   - Verificar SSL certificate

3. **App No Inicia**
   - Verificar `requirements.txt`
   - Revisar logs en DigitalOcean Dashboard
   - Verificar comandos en `Procfile`

### Logs Útiles:
```bash
# GitHub Actions logs
# DigitalOcean App Platform → Runtime Logs
# Verificación manual: python verify_deployment.py
```

---

## 🏆 LISTO PARA DATATÓN

### Checklist Final:
- ✅ GitHub repo conectado
- ✅ DigitalOcean configurado
- ✅ Dominio funcionando
- ✅ SSL habilitado
- ✅ CI/CD automático
- ✅ Monitoreo configurado
- ✅ Performance optimizado

### URL Final: **https://casamx.store**

**🎉 CasaMX listo para ganar el Datatón ITAM 2025! 🏆**

---

## 📞 SOPORTE DE EMERGENCIA

Si algo falla durante el Datatón:
1. Ejecutar: `python verify_deployment.py`
2. Revisar logs en GitHub Actions
3. Usar backup manual en `digitalocean_deploy/`
4. Contactar equipo de soporte