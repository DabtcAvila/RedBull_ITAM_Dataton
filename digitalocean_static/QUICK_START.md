# ⚡ QUICK START - CasaMX Deployment

## 🚀 5 MINUTOS A PRODUCCIÓN

### 1️⃣ DigitalOcean Setup (2 minutos)
```bash
1. Go to: https://cloud.digitalocean.com/apps
2. "Create App" > "Upload files" > "Static Site"
3. Upload digitalocean_static.zip
4. Name: casamx-store
5. Deploy → ✅ DONE
```

### 2️⃣ Domain Setup (3 minutos)
```bash
1. App Settings > Domains > Add "casamx.store"
2. DNS: CNAME @ → [digitalocean-url]
3. Wait 5 minutes → ✅ https://casamx.store LIVE
```

---

## 🧪 Local Test (30 seconds)
```bash
cd digitalocean_static/
python3 -m http.server 8000
# Open: http://localhost:8000
```

---

## ✅ Verification Checklist
- [ ] Form works (try search)
- [ ] Demo cases work (click Alex/María/Sophie)  
- [ ] Map loads with markers
- [ ] Mobile responsive
- [ ] PWA installable

---

## 🚨 If Something Fails
1. **Build Error:** Check you selected "Static Site" (NOT Web Service)
2. **Domain Error:** Verify CNAME points to DigitalOcean URL
3. **App Error:** Refresh page, check browser console

---

## 📞 Emergency Backup (1 minute)
```bash
# Netlify instant backup
https://app.netlify.com/drop
# Drag digitalocean_static/ folder → INSTANT LIVE
```

---

**🎯 Result: Professional housing recommendation app live at https://casamx.store**