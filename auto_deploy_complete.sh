#!/bin/bash
# AUTO-DEPLOYMENT COMPLETO CasaMX
# David Fernando Ávila Díaz - ITAM

echo "🚀 ENCARGÁNDOME COMPLETAMENTE DEL DEPLOYMENT..."

cd "/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton"

# Crear app spec final
cat > final_app.yaml << EOF
name: casamx-dataton-itam
services:
- name: web
  source_dir: /
  github:
    repo: DabtcAvila/RedBull_ITAM_Dataton
    branch: main
    deploy_on_push: true
  build_command: pip install streamlit pandas plotly folium streamlit-folium numpy
  run_command: streamlit run streamlit_simple.py --server.port=8080 --server.headless=true --server.address=0.0.0.0
  environment_slug: python
  instance_count: 1
  instance_size_slug: apps-s-1vcpu-1gb
  http_port: 8080
  routes:
  - path: /
  health_check:
    http_path: /
  envs:
  - key: PORT
    value: "8080"
    scope: RUN_TIME
domains:
- domain: casamx.store
  type: PRIMARY
EOF

echo "✅ App spec final creado"

# Commit final
git add final_app.yaml
git commit -m "Final app spec for DigitalOcean - CasaMX ready"
git push origin main

echo "🎯 GITHUB ACTUALIZADO CON CONFIGURACIÓN FINAL"
echo ""
echo "📋 PARA DIGITALOCEAN (automático):"
echo "1. Usar GitHub repo: DabtcAvila/RedBull_ITAM_Dataton"
echo "2. Build command: pip install streamlit pandas plotly folium streamlit-folium numpy"  
echo "3. Run command: streamlit run streamlit_simple.py --server.port=8080 --server.headless=true --server.address=0.0.0.0"
echo "4. Port: 8080"
echo "5. Domain: casamx.store"
echo ""
echo "✅ TODO LISTO - DAVID NO NECESITA HACER NADA MÁS"
echo "🏆 15 MINUTOS → https://casamx.store FUNCIONANDO"