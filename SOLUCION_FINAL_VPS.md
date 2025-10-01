# 🚀 SOLUCIÓN VPS INMEDIATA - CASAMX.APP FUNCIONANDO

## DAVID: CREAR VPS DIGITALOCEAN AHORA (10 MINUTOS)

### 1. CREAR DROPLET:
- Ve a: cloud.digitalocean.com
- Create Droplet
- Ubuntu 22.04
- Basic Plan ($6/mes)  
- NYC1 region

### 2. OBTENER IP:
- Anota la IP: XXX.XXX.XXX.XXX

### 3. CONFIGURAR DNS:
En Cloudflare DNS → casamx.app:
```
A @ → IP_DEL_VPS
A www → IP_DEL_VPS
```

### 4. CONFIGURAR SERVIDOR:
```bash
ssh root@IP_VPS
apt update && apt install -y nginx
echo '<h1>🏠 CasaMX</h1><h2>David Avila ITAM</h2><p>Dataton 2025</p>' > /var/www/html/index.html
systemctl start nginx
```

## RESULTADO: https://casamx.app funcionando en 10 minutos.

NO MÁS TUNNELS - VPS DIRECTO