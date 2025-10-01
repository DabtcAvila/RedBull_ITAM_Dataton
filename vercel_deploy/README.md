# CasaMX - Vercel Deployment

## 🚀 Deploy Inmediato - 5 Minutos

### Opción 1: Deploy Automático (Recomendado)

```bash
cd vercel_deploy
chmod +x deploy_casamx.sh
./deploy_casamx.sh
```

### Opción 2: Deploy Manual

1. **Instalar Vercel CLI**
```bash
npm install -g vercel
```

2. **Autenticar**
```bash
vercel login
```

3. **Deploy**
```bash
vercel --prod
```

### Opción 3: GitHub Integration

1. Fork el repo: `DabtcAvila/RedBull_ITAM_Dataton`
2. Ve a [vercel.com](https://vercel.com)
3. Conecta tu GitHub y selecciona el repo
4. Deploy automático

## 📁 Archivos de Deployment

```
vercel_deploy/
├── vercel.json          # Configuración Vercel optimizada
├── vercel_simple.json   # Configuración alternativa
├── main.py             # App principal (HTML puro)
├── streamlit_simple.py  # App Streamlit original
├── requirements.txt     # Dependencias mínimas
├── api/index.py        # Handler serverless
├── deploy_casamx.sh    # Script de deployment
└── package.json        # Metadatos del proyecto
```

## 🌐 Configuración de Dominio

### Automático (via script)
El script configura automáticamente `casamx.store`

### Manual
```bash
vercel domains add casamx.store
vercel alias https://tu-deployment.vercel.app casamx.store
```

## ⚡ Características

- **Runtime**: Python 3.9
- **Framework**: HTML/JavaScript puro + Pandas
- **Deploy Time**: ~2 minutos
- **Cold Start**: <3 segundos
- **SSL**: Automático
- **CDN**: Global

## 🔧 Configuración

### Variables de Entorno
```json
{
  "PYTHONPATH": ".",
  "NODE_ENV": "production"
}
```

### Dominios Soportados
- `*.vercel.app` (automático)
- `casamx.store` (personalizado)
- Cualquier dominio custom

## 📊 Performance

- **Tiempo de carga**: <2s
- **Tamaño bundle**: ~15MB
- **Memoria**: 128MB
- **Timeout**: 30s

## 🏠 URL Final

Después del deployment:
- **Vercel**: https://casamx.vercel.app
- **Custom**: https://casamx.store

## 📝 Notas

- El archivo `main.py` sirve HTML puro para mejor performance
- `streamlit_simple.py` está incluido para deployment Streamlit alternativo
- SSL se configura automáticamente
- CDN global incluido

---
**CasaMX** - Datatón ITAM 2025 | David Fernando Ávila Díaz