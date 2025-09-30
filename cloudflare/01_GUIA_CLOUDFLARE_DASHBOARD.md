# Guía Paso a Paso: Configurar casamx.store en Cloudflare Dashboard

## DATOS DEL PROYECTO
- **Dominio**: casamx.store
- **Evento**: Datatón ITAM 2025
- **Tunnel ID**: d198c64a-c169-42ce-9279-e0abdd0b71df
- **App Local**: localhost:8503

---

## PASO 1: AÑADIR DOMINIO EN CLOUDFLARE

### 1.1 Acceder a Cloudflare Dashboard
1. Ir a: https://dash.cloudflare.com/
2. Iniciar sesión con tu cuenta Cloudflare
3. En el panel principal, buscar el botón **"Add a Site"** o **"Añadir un sitio"**

### 1.2 Agregar el Dominio
1. **Escribir el dominio**: `casamx.store` (sin www)
2. **Seleccionar plan**: Free Plan (suficiente para el datatón)
3. **Continuar** hasta que aparezcan los nameservers

### 1.3 Obtener Nameservers
Cloudflare asignará nameservers únicos que lucirán así:
```
clara.ns.cloudflare.com
ken.ns.cloudflare.com
```

**IMPORTANTE**: Anota EXACTAMENTE los nameservers que te asignen, son únicos para tu cuenta.

---

## PASO 2: CONFIGURAR DNS RECORDS

### 2.1 Ir a la sección DNS
1. En el dashboard de tu dominio casamx.store
2. Click en **"DNS"** en el menú lateral
3. Ir a **"Records"**

### 2.2 Añadir Record A (Root Domain)
```
Type: A
Name: @ 
Content: 198.41.200.63
Proxy status: Proxied (nube naranja activada)
TTL: Auto
```

### 2.3 Añadir Record CNAME (WWW)
```
Type: CNAME
Name: www
Content: d198c64a-c169-42ce-9279-e0abdd0b71df.cfargotunnel.com
Proxy status: Proxied (nube naranja activada)
TTL: Auto
```

### 2.4 Verificar Configuración
Deberías ver dos records:
- `casamx.store` → A record → 198.41.200.63 (Proxied)
- `www.casamx.store` → CNAME → [tunnel-id].cfargotunnel.com (Proxied)

---

## PASO 3: CONFIGURACIONES ADICIONALES

### 3.1 SSL/TLS Settings
1. Ir a **SSL/TLS** → **Overview**
2. Configurar: **"Flexible"** o **"Full"**
3. Activar **"Always Use HTTPS"**

### 3.2 Speed Optimizations
1. Ir a **Speed** → **Optimization**
2. Activar:
   - Auto Minify (HTML, CSS, JS)
   - Rocket Loader
   - Mirage

### 3.3 Security Settings
1. Ir a **Security** → **Settings**
2. Configurar Security Level: **Medium**
3. Activar Bot Fight Mode

---

## VERIFICACIÓN

Una vez configurado, verifica:
- [ ] Dominio añadido en Cloudflare
- [ ] Nameservers obtenidos
- [ ] A record configurado (@ → 198.41.200.63)
- [ ] CNAME record configurado (www → tunnel)
- [ ] SSL configurado
- [ ] Optimizaciones activadas

**SIGUIENTE PASO**: Cambiar nameservers en Squarespace (ver guía 02)

---

## NOTAS IMPORTANTES

- Los cambios DNS pueden tardar hasta 48 horas en propagarse
- Guarda los nameservers exactos que Cloudflare te asigne
- NO cambies los nameservers en Squarespace hasta completar toda la configuración
- El tunnel debe estar corriendo para que funcione el sitio

## SOPORTE

Si algo no funciona:
1. Verificar que el tunnel esté corriendo
2. Revisar los DNS records
3. Esperar propagación DNS (usar: https://dnschecker.org/)

**Tiempo estimado**: 15-20 minutos
**Dificultad**: Intermedio