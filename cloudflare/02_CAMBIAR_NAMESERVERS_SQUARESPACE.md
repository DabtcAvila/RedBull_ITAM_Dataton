# Guía: Cambiar Nameservers en Squarespace

## INFORMACIÓN ACTUAL
- **Dominio**: casamx.store
- **Registrador**: Squarespace
- **Nameservers actuales**: ns-cloud-e1/e2/e3/e4.googledomains.com (no funcionales)

---

## PASO 1: ACCEDER A SQUARESPACE DOMAINS

### 1.1 Login en Squarespace
1. Ir a: https://account.squarespace.com/
2. Iniciar sesión con tu cuenta
3. Buscar la sección **"Domains"** o **"Dominios"**

### 1.2 Localizar casamx.store
1. En la lista de dominios, encontrar **casamx.store**
2. Click en el dominio para acceder a la configuración
3. Buscar **"DNS Settings"** o **"Advanced Settings"**

---

## PASO 2: CAMBIAR NAMESERVERS

### 2.1 Ir a Nameserver Settings
1. En la configuración del dominio, buscar:
   - **"Nameservers"**
   - **"DNS Settings"**
   - **"Custom Nameservers"**

### 2.2 Cambiar a Custom Nameservers
1. Seleccionar **"Use Custom Nameservers"**
2. **ELIMINAR** los nameservers actuales de Google:
   ```
   ns-cloud-e1.googledomains.com
   ns-cloud-e2.googledomains.com
   ns-cloud-e3.googledomains.com
   ns-cloud-e4.googledomains.com
   ```

### 2.3 Añadir Nameservers de Cloudflare
**IMPORTANTE**: Usa los nameservers EXACTOS que Cloudflare te asignó en el Paso 1.

Ejemplo (reemplazar con tus nameservers reales):
```
clara.ns.cloudflare.com
ken.ns.cloudflare.com
```

### 2.4 Guardar Cambios
1. Click **"Save"** o **"Guardar"**
2. Confirmar los cambios si aparece una ventana de confirmación

---

## PASO 3: VERIFICACIÓN EN SQUARESPACE

### 3.1 Confirmar Cambios
Después de guardar, deberías ver:
- Nameservers cambiados a Cloudflare
- Posible advertencia sobre pérdida de configuración DNS anterior
- Status: "Pending" o "Procesando"

### 3.2 Tiempo de Propagación
- **Inmediato**: Cambio guardado en Squarespace
- **2-4 horas**: Propagación inicial
- **24-48 horas**: Propagación completa mundial

---

## VERIFICAR CAMBIOS DE NAMESERVERS

### Usar herramientas online:
1. **WhatsMyDNS**: https://www.whatsmydns.net/
   - Buscar: `casamx.store`
   - Type: `NS`
   - Verificar que aparezcan los nameservers de Cloudflare

2. **DNS Checker**: https://dnschecker.org/
   - Mismo proceso de verificación

### Usar Terminal (Mac/Linux):
```bash
dig NS casamx.store
```

### Usar Command Prompt (Windows):
```cmd
nslookup -type=NS casamx.store
```

---

## PROBLEMAS COMUNES

### Nameservers no cambian
- **Causa**: Cache DNS local
- **Solución**: Esperar 2-4 horas, limpiar cache DNS

### Error al guardar en Squarespace
- **Causa**: Formato incorrecto de nameservers
- **Solución**: Verificar que solo incluyas el nombre del nameserver, sin http:// ni espacios extra

### Pérdida de email
- **Causa**: Cambio de nameservers elimina configuración anterior
- **Solución**: Configurar registros MX en Cloudflare si usas email del dominio

---

## CONFIGURACIONES ADICIONALES EN SQUARESPACE

### Si usas email del dominio:
1. **Antes** de cambiar nameservers, anotar configuración MX actual
2. **Después** del cambio, añadir registros MX en Cloudflare DNS

### Registros MX comunes de Squarespace:
```
Type: MX
Name: @
Content: aspmx.l.google.com
Priority: 1
```

---

## ROLLBACK (Si algo sale mal)

Si necesitas volver a los nameservers anteriores:
```
ns-cloud-e1.googledomains.com
ns-cloud-e2.googledomains.com
ns-cloud-e3.googledomains.com
ns-cloud-e4.googledomains.com
```

**IMPORTANTE**: Solo hacer rollback si el sitio no funciona después de 48 horas.

---

## CHECKLIST FINAL

- [ ] Nameservers cambiados en Squarespace
- [ ] Confirmación guardada
- [ ] Verificación con herramientas DNS
- [ ] Esperar propagación (2-4 horas mínimo)
- [ ] Probar acceso a casamx.store

**SIGUIENTE PASO**: Ejecutar tunnel y verificar funcionamiento (ver guía 03)

---

## CONTACTO SOPORTE SQUARESPACE

Si tienes problemas:
- **Help Center**: https://support.squarespace.com/
- **Chat Support**: Disponible en el dashboard
- **Email**: A través del sistema de tickets

**Tiempo estimado**: 10-15 minutos + tiempo de propagación
**Dificultad**: Fácil