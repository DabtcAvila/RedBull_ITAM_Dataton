# 🚀 GUÍA INMEDIATA: Crear CasaMX en DigitalOcean App Platform

## SITUACIÓN CRÍTICA - DATATÓN ITAM 2025
**TIEMPO ESTIMADO: 10-15 minutos**  
**OBJETIVO: https://casamx.store funcionando AHORA**

---

## ✅ PRE-REQUISITOS VERIFICADOS

- ✅ **Repositorio GitHub**: `https://github.com/DabtcAvila/RedBull_ITAM_Dataton`
- ✅ **Configuración app.yaml**: Lista y optimizada
- ✅ **Código pusheado**: Branch main actualizada
- ✅ **Requirements.txt**: Dependencies de producción configuradas
- ✅ **Cuenta DigitalOcean**: Conectada a GitHub

---

## 🎯 PASOS INMEDIATOS (CRONOMETRADOS)

### PASO 1: Acceso a DigitalOcean (30 segundos)
```
1. Abrir: https://cloud.digitalocean.com
2. Login con tu cuenta de David
3. Dashboard principal debe aparecer
```

### PASO 2: Crear Nueva App (1 minuto)
```
1. Click en "Apps" en el menú lateral izquierdo
2. Click en "Create App" (botón azul prominente)
3. Seleccionar "GitHub" como fuente
4. Autorizar conexión si es primera vez
```

### PASO 3: Configurar Repositorio (1 minuto)
```
CONFIGURACIÓN EXACTA:
├─ Repository: DabtcAvila/RedBull_ITAM_Dataton
├─ Branch: main
├─ Source Directory: / (raíz)
└─ Autodeploy: ✅ ENABLED
```

### PASO 4: Usar App Spec YAML (2 minutos)
```
🔥 CRÍTICO: NO usar el wizard, usar YAML directamente

1. Click en "Edit App Spec" o "Advanced"
2. Borrar TODO el contenido del editor
3. Copiar EXACTAMENTE este contenido:
```

```yaml
name: casamx-app
region: nyc

domains:
- domain: casamx.store
  type: PRIMARY

services:
- name: web
  source_dir: /
  github:
    repo: DabtcAvila/RedBull_ITAM_Dataton
    branch: main
    deploy_on_push: true
  
  run_command: python -m streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
  
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  
  envs:
  - key: PORT
    scope: RUN_TIME
    value: "8080"
  - key: ENVIRONMENT
    scope: RUN_TIME
    value: "production"
  - key: STREAMLIT_SERVER_PORT
    scope: RUN_TIME
    value: "8080"
  - key: STREAMLIT_SERVER_ADDRESS
    scope: RUN_TIME
    value: "0.0.0.0"
  - key: STREAMLIT_SERVER_HEADLESS
    scope: RUN_TIME
    value: "true"
  - key: STREAMLIT_BROWSER_GATHER_USAGE_STATS
    scope: RUN_TIME
    value: "false"
  
  health_check:
    http_path: /
    initial_delay_seconds: 30
    period_seconds: 10
    timeout_seconds: 5
    success_threshold: 1
    failure_threshold: 3
  
  http_port: 8080

- name: api
  source_dir: /
  github:
    repo: DabtcAvila/RedBull_ITAM_Dataton
    branch: main
    deploy_on_push: true
  
  run_command: cd src/api && python -m uvicorn main:app --host=0.0.0.0 --port=$PORT
  
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  
  envs:
  - key: PORT
    scope: RUN_TIME
    value: "8000"
  - key: ENVIRONMENT
    scope: RUN_TIME
    value: "production"
  
  health_check:
    http_path: /
    initial_delay_seconds: 20
    period_seconds: 10
    timeout_seconds: 5
    success_threshold: 1
    failure_threshold: 3
  
  http_port: 8000
  
  routes:
  - path: /api

jobs: []
databases: []

ingress:
  rules:
  - match:
      path:
        prefix: /api
    component:
      name: api
  - match:
      path:
        prefix: /
    component:
      name: web
```

### PASO 5: Configuración de Plan y Dominio (2 minutos)
```
PLAN RECOMENDADO:
├─ Tier: Basic ($5/mes)
├─ Compute: basic-xxs (suficiente para demo)
├─ Dominio: casamx.store
└─ SSL: Automático (Let's Encrypt)

DOMINIO CUSTOM:
1. Verificar que "casamx.store" esté en la sección domains
2. SSL será automático
3. Type: PRIMARY
```

### PASO 6: Deploy Inmediato (1 minuto)
```
1. Click "Create Resources" (botón azul)
2. DigitalOcean comenzará el build automáticamente
3. Monitorear en tiempo real en "Activity" tab
```

---

## 📊 MONITOREO DE DEPLOYMENT (5-10 minutos)

### Lo que verás en tiempo real:
```
🔄 Building... (2-3 minutos)
├─ Cloning repository
├─ Installing Python dependencies 
├─ Building application

🚀 Deploying... (2-3 minutos)
├─ Creating containers
├─ Starting services
├─ Health checks

✅ Live! (1-2 minutos)
├─ DNS propagation
├─ SSL certificate
└─ https://casamx.store ONLINE
```

### Logs importantes a verificar:
```
✅ "Build completed successfully"
✅ "Deployment completed" 
✅ "Health check passed"
✅ "SSL certificate issued"
✅ "Domain configured"
```

---

## 🎯 VERIFICACIÓN INMEDIATA

### URLs a probar:
```
🌐 Frontend: https://casamx.store
🔧 API: https://casamx.store/api
📊 Health: https://casamx.store/_health (si disponible)
```

### Tests críticos:
```
1. ¿Carga la página principal?
2. ¿Funciona el mapa interactivo?
3. ¿Responde la búsqueda de propiedades?
4. ¿SSL certificate válido?
```

---

## 🔧 RESOLUCIÓN RÁPIDA DE PROBLEMAS

### Si Build Falla:
```
📝 Revisar logs en "Runtime Logs"
🔍 Buscar error en requirements.txt
🔄 Trigger re-deploy manual si necesario
```

### Si Health Check Falla:
```
⏰ Aumentar initial_delay_seconds a 60
🔧 Verificar puerto 8080 en logs
🔄 Re-deploy después de ajustar
```

### Si Dominio No Resuelve:
```
⏳ Esperar 5-10 min para DNS propagation
🌐 Probar con IP temporal de DO mientras tanto
🔍 Verificar DNS con: dig casamx.store
```

---

## 📱 CONFIGURACIÓN POST-DEPLOYMENT (Opcional)

### Monitoring básico:
```
1. Alerts → Create Alert
2. Metric: "HTTP 5XX errors"
3. Threshold: > 5 in 5 minutes
4. Notification: Email/Slack
```

### Backup automático:
```
- Auto-deploy from GitHub: ✅ Ya configurado
- Database backup: SQLite se respalda con código
- Logs: Automático por 7 días
```

---

## 🎉 RESULTADO ESPERADO

### ✅ SUCCESS CRITERIA:
- **URL**: https://casamx.store responde en <3 segundos
- **SSL**: Certificado válido y automático  
- **Funcionalidad**: Búsqueda de propiedades operativa
- **API**: Endpoints /api/* funcionando
- **Logs**: Sin errores críticos
- **Costo**: $5/mes (básico, escalable)

### 📊 Performance esperado:
- **Load time**: <3 segundos iniciales
- **Availability**: >99.9% 
- **Concurrent users**: 50+ simultáneos
- **Auto-scaling**: Si se necesita más tráfico

---

## 🚨 CONTINGENCIAS (Solo si algo falla)

### Plan B - Si DigitalOcean falla:
```
1. Heroku: git push heroku main (Procfile ya existe)
2. Vercel: npm run build && vercel --prod
3. Railway: railway up
```

### Plan C - Local con tunnel:
```
1. streamlit run streamlit_app.py
2. cloudflared tunnel --url localhost:8501
3. Share tunnel URL temporalmente
```

---

## ⚡ CHECKLIST FINAL ANTES DE PRESENTAR

```
□ https://casamx.store carga correctamente
□ Mapa de CDMX se visualiza
□ Búsqueda de propiedades funciona
□ Filtros por colonia operativos
□ Recomendaciones se generan
□ API endpoints responden
□ SSL certificate válido
□ Performance <3 segundos
□ Sin errores en logs
□ Dominio custom funcionando
```

---

## 📞 CONTACTO DE EMERGENCIA

**Si algo falla durante el Datatón:**
- GitHub Issues: Crear issue inmediato
- Logs DigitalOcean: Runtime logs en tiempo real
- Rollback: Git revert + nuevo deploy automático

**TIEMPO TOTAL ESTIMADO: 10-15 MINUTOS**
**RESULTADO: https://casamx.store ONLINE Y FUNCIONANDO**

---
*Creado para Datatón ITAM 2025 - CasaMX Deploy Guide*
*Última actualización: 2025-09-30*