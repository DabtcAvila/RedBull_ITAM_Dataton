# 🚀 CLOUDFLARE WORKERS - DEPLOY CASAMX.APP

## DAVID: PASOS EXACTOS (5 MINUTOS)

### 1. Ve a Cloudflare Dashboard:
```
https://dash.cloudflare.com/
```

### 2. Workers & Pages → Create:
- **Create Worker**
- Name: `casamx-app`

### 3. Copy & Paste este código:
```javascript
// Contenido completo está en cloudflare-worker.js
// Copiar TODO el contenido del archivo
```

### 4. Deploy & Save:
- Clic **Save and Deploy**
- URL temporal: `casamx-app.YOURUSER.workers.dev`

### 5. Custom Domain Setup:
- Workers → casamx-app → **Triggers**
- **Add Custom Domain**: `casamx.app`
- SSL: Automatic (ya configurado)

## ✅ RESULTADO INMEDIATO:
- **https://casamx.app** funcionando en 2-3 minutos
- Sirve desde GitHub automáticamente
- SSL gratis de Cloudflare
- Cache optimizado (5 minutos)
- **CasaMX completa** con 8 colonias CDMX

## 🎯 VENTAJAS CLOUDFLARE:
- ⚡ **99.9% uptime** garantizado
- 🌍 **CDN global** ultra-rápido  
- 🔒 **SSL automático**
- 💰 **Plan gratuito** (100k requests/día)
- 🚀 **Deploy instantáneo**

### ¿CONFIGURAS EL WORKER AHORA?

**Archivo:** `cloudflare-worker.js` tiene TODO el código listo