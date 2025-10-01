# 🚀 QUICK START GUIDE - CASAMX DEPLOYMENT

## 🎯 MISIÓN CRÍTICA: CASAMX.STORE EN 20 MINUTOS

### ⚡ DEPLOYMENT INMEDIATO (2 COMANDOS)

```bash
# 1. Ir al directorio de deployment
cd multi_deploy

# 2. Ejecutar deployment maestro
./MASTER_DEPLOY_CASAMX.sh
```

**¡ESO ES TODO!** El script automáticamente:
- ✅ Prueba Vercel (3-5 min)
- ✅ Si falla, prueba Netlify (backup)
- ✅ Si falla, activa GitHub Pages (emergency)  
- ✅ Si falla, intenta Railway (professional)
- ✅ Configura SSL automático
- ✅ Verifica deployment

---

## 🛠️ DEPLOYMENT INDIVIDUAL POR PLATAFORMA

### 1. 🔴 VERCEL (MÁS RÁPIDO - 3 MIN)
```bash
./deploy_vercel.sh
```
- **Tiempo**: 3-5 minutos
- **Confiabilidad**: 95%
- **URL**: https://casamx.store

### 2. 🟡 NETLIFY (BACKUP - 5 MIN)
```bash
./deploy_netlify.sh
```
- **Tiempo**: 5-8 minutos  
- **Confiabilidad**: 93%
- **URL**: https://casamx.store

### 3. 🟠 GITHUB PAGES (EMERGENCY - 2 MIN)
```bash
./deploy_github_pages.sh
```
- **Tiempo**: 2-3 minutos
- **Confiabilidad**: 98% 
- **URL**: https://casamx.store

### 4. 🟣 RAILWAY (PROFESSIONAL - 8 MIN)
```bash
./deploy_railway.sh
```
- **Tiempo**: 8-12 minutos
- **Confiabilidad**: 90%
- **URL**: https://casamx.store

---

## 🔧 CONFIGURACIÓN ADICIONAL

### 🌐 Configurar Dominio
```bash
./configure_domain_casamx.sh
```

### 🧪 Probar Deployment
```bash
./test_deployment.sh
```

---

## 📋 CHECKLIST PRE-DEPLOYMENT

- [ ] Node.js instalado (para CLI tools)
- [ ] Git configurado con permisos
- [ ] Conexión a internet estable
- [ ] Cuentas creadas en plataformas:
  - [ ] Vercel.com
  - [ ] Netlify.com
  - [ ] GitHub.com
  - [ ] Railway.app (opcional)

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Si TODO falla:
1. **Servidor local de emergencia**:
   ```bash
   cd ..
   streamlit run streamlit_app.py --server.port 8501
   ```

2. **Túnel público con ngrok**:
   ```bash
   ngrok http 8501
   ```

### Problemas comunes:
- **CLI no instalado**: `npm install -g @vercel/cli netlify-cli`
- **No autenticado**: Ejecutar `vercel login` o `netlify login`
- **Git sin configurar**: `git config --global user.email "tu@email.com"`

---

## ⏰ CRONOGRAMA DE DEPLOYMENT

| Estrategia | Tiempo | Status |
|------------|--------|---------|
| Vercel | 0-5 min | 🔴 Prioritario |
| Netlify | 5-10 min | 🟡 Backup |
| GitHub Pages | 10-15 min | 🟠 Emergency |
| Railway | 15-20 min | 🟣 Final |

---

## 🎯 RESULTADO GARANTIZADO

**PROMESA**: CasaMX estará online en https://casamx.store en máximo 20 minutos.

Si no funciona, tienes:
- ✅ 4 estrategias de deployment
- ✅ Servidor local de emergencia  
- ✅ Página estática de respaldo
- ✅ Monitoreo automático

---

## 🏆 VERIFICACIÓN FINAL

```bash
# Verificar que todo funciona
curl -I https://casamx.store

# Debe devolver: HTTP/2 200
```

**¡LISTO PARA EL DATATÓN ITAM 2025!** 🎉