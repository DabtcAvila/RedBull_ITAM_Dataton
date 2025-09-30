# Configuración del Tunnel Cloudflare para casamx.store

## DATOS DEL TUNNEL
- **Tunnel ID**: d198c64a-c169-42ce-9279-e0abdd0b71df
- **Nombre**: casamx-dataton
- **Puerto local**: 8503 (Streamlit)
- **Dominio**: casamx.store

---

## PASO 1: VERIFICAR TUNNEL EXISTENTE

### 1.1 Comprobar si el tunnel existe
```bash
cloudflared tunnel list
```

Deberías ver algo como:
```
ID                                   NAME           CREATED
d198c64a-c169-42ce-9279-e0abdd0b71df casamx-dataton 2025-XX-XX
```

### 1.2 Si no aparece el tunnel
Si el tunnel no existe, créalo:
```bash
cloudflared tunnel create casamx-dataton
```

---

## PASO 2: CONFIGURAR ARCHIVO DE TUNNEL

### 2.1 Crear directorio de configuración
```bash
mkdir -p ~/.cloudflared
```

### 2.2 Crear archivo config.yml
```bash
cat > ~/.cloudflared/config.yml << 'EOF'
tunnel: d198c64a-c169-42ce-9279-e0abdd0b71df
credentials-file: ~/.cloudflared/d198c64a-c169-42ce-9279-e0abdd0b71df.json

ingress:
  - hostname: casamx.store
    service: http://localhost:8503
  - hostname: www.casamx.store
    service: http://localhost:8503
  - service: http_status:404
EOF
```

### 2.3 Verificar archivo de credenciales
El archivo de credenciales debe existir:
```bash
ls -la ~/.cloudflared/d198c64a-c169-42ce-9279-e0abdd0b71df.json
```

Si no existe, reautentícate:
```bash
cloudflared tunnel login
```

---

## PASO 3: CONFIGURAR DNS EN CLOUDFLARE

### 3.1 Añadir CNAME para el tunnel
```bash
cloudflared tunnel route dns d198c64a-c169-42ce-9279-e0abdd0b71df casamx.store
cloudflared tunnel route dns d198c64a-c169-42ce-9279-e0abdd0b71df www.casamx.store
```

O manualmente en el Dashboard:
- **Type**: CNAME
- **Name**: @ (para casamx.store)
- **Content**: d198c64a-c169-42ce-9279-e0abdd0b71df.cfargotunnel.com
- **Proxy**: ON (nube naranja)

---

## PASO 4: EJECUTAR EL TUNNEL

### 4.1 Iniciar Streamlit (puerto 8503)
```bash
cd "/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton"
source casamx_env/bin/activate
streamlit run streamlit_app.py --server.port=8503 --server.headless=true &
```

### 4.2 Iniciar el tunnel
```bash
cloudflared tunnel run d198c64a-c169-42ce-9279-e0abdd0b71df
```

O usando el nombre:
```bash
cloudflared tunnel run casamx-dataton
```

---

## PASO 5: VERIFICAR FUNCIONAMIENTO

### 5.1 Verificar que Streamlit está corriendo
```bash
curl http://localhost:8503
```

### 5.2 Verificar el tunnel
En otra terminal:
```bash
cloudflared tunnel info d198c64a-c169-42ce-9279-e0abdd0b71df
```

### 5.3 Probar URLs externas
- https://casamx.store
- https://www.casamx.store

---

## CONFIGURACIÓN AVANZADA

### Archivo config.yml completo con opciones adicionales:
```yaml
tunnel: d198c64a-c169-42ce-9279-e0abdd0b71df
credentials-file: ~/.cloudflared/d198c64a-c169-42ce-9279-e0abdd0b71df.json

# Configuraciones del tunnel
no-autoupdate: true
retries: 5
grace-period: 30s

# Rutas de tráfico
ingress:
  # Dominio principal
  - hostname: casamx.store
    service: http://localhost:8503
    originRequest:
      httpHostHeader: localhost:8503
      
  # Subdominio www
  - hostname: www.casamx.store
    service: http://localhost:8503
    originRequest:
      httpHostHeader: localhost:8503
      
  # Catch-all (obligatorio)
  - service: http_status:404

# Logging
loglevel: info
logfile: ~/.cloudflared/tunnel.log
```

---

## SCRIPTS DE AUTOMATIZACIÓN

### Script de inicio automático:
```bash
#!/bin/bash
# Archivo: start_casamx_tunnel.sh

echo "🚀 Iniciando CasaMX con Cloudflare Tunnel"

# Directorio del proyecto
PROJECT_DIR="/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton"
cd "$PROJECT_DIR"

# Activar entorno virtual
source casamx_env/bin/activate

# Verificar que el puerto esté libre
if lsof -Pi :8503 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Puerto 8503 ocupado, matando proceso..."
    kill $(lsof -Pi :8503 -sTCP:LISTEN -t)
    sleep 2
fi

echo "📡 Iniciando Streamlit en puerto 8503..."
# Ejecutar Streamlit en background
nohup streamlit run streamlit_app.py --server.port=8503 --server.headless=true > logs/streamlit_tunnel.log 2>&1 &
STREAMLIT_PID=$!

# Esperar que Streamlit inicie
sleep 5

echo "🌐 Iniciando Cloudflare Tunnel..."
# Ejecutar tunnel
cloudflared tunnel run d198c64a-c169-42ce-9279-e0abdd0b71df &
TUNNEL_PID=$!

echo ""
echo "✅ CasaMX FUNCIONANDO!"
echo "🌐 URLs disponibles:"
echo "   - https://casamx.store"
echo "   - https://www.casamx.store"
echo "   - Local: http://localhost:8503"
echo ""
echo "📊 Logs:"
echo "   - Streamlit: tail -f logs/streamlit_tunnel.log"
echo "   - Tunnel: logs en terminal"
echo ""
echo "🛑 Para detener:"
echo "   kill $STREAMLIT_PID $TUNNEL_PID"
echo "   o usar Ctrl+C"

# Guardar PIDs para fácil limpieza
echo $STREAMLIT_PID > /tmp/casamx_streamlit.pid
echo $TUNNEL_PID > /tmp/casamx_tunnel.pid

# Mantener script corriendo
wait
```

---

## TROUBLESHOOTING

### Tunnel no inicia
```bash
# Verificar configuración
cloudflared tunnel validate ~/.cloudflared/config.yml

# Verificar credenciales
cloudflared tunnel list
```

### Error de conexión
```bash
# Verificar Streamlit
ps aux | grep streamlit

# Verificar puerto
lsof -i :8503
```

### DNS no resuelve
```bash
# Verificar DNS
dig casamx.store
nslookup casamx.store

# Limpiar cache DNS local
sudo dscacheutil -flushcache
```

---

## MONITOREO

### Verificar status del tunnel:
```bash
cloudflared tunnel info d198c64a-c169-42ce-9279-e0abdd0b71df
```

### Ver logs del tunnel:
```bash
tail -f ~/.cloudflared/tunnel.log
```

### Verificar conectividad:
```bash
curl -I https://casamx.store
```

---

## CHECKLIST FINAL

- [ ] Tunnel creado y configurado
- [ ] Archivo config.yml correcto
- [ ] DNS records configurados en Cloudflare
- [ ] Streamlit corriendo en puerto 8503
- [ ] Tunnel ejecutándose
- [ ] URLs accesibles desde internet
- [ ] HTTPS funcionando automáticamente

**Tiempo estimado**: 10-15 minutos
**Dificultad**: Intermedio