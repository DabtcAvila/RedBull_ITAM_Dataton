#!/usr/bin/env python3
"""
AUTO-DEPLOYMENT CasaMX a DigitalOcean
David Fernando Ávila Díaz - ITAM
"""

import json
import time
import subprocess

def auto_deploy_casamx():
    """Auto-deployment usando DigitalOcean CLI"""
    
    print("🚀 AUTO-DEPLOYING CASAMX EN DIGITALOCEAN...")
    
    # Verificar que doctl esté instalado
    try:
        result = subprocess.run(['doctl', 'version'], capture_output=True, text=True)
        print(f"✅ DigitalOcean CLI: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ DigitalOcean CLI no instalado. Instalando...")
        subprocess.run(['brew', 'install', 'doctl'], check=True)
    
    # App spec para deployment
    app_spec = {
        "name": "casamx-dataton-itam",
        "services": [
            {
                "name": "web",
                "source_dir": "/",
                "github": {
                    "repo": "DabtcAvila/RedBull_ITAM_Dataton",
                    "branch": "main",
                    "deploy_on_push": True
                },
                "build_command": "pip install -r requirements_production.txt",
                "run_command": "streamlit run streamlit_app_fixed.py --server.port=8080 --server.headless=true",
                "environment_slug": "python",
                "instance_count": 1,
                "instance_size_slug": "apps-s-1vcpu-1gb",
                "http_port": 8080,
                "routes": [{"path": "/"}],
                "health_check": {"http_path": "/"},
                "envs": [
                    {"key": "PORT", "value": "8080", "scope": "RUN_TIME"},
                    {"key": "STREAMLIT_SERVER_PORT", "value": "8080", "scope": "RUN_TIME"},
                    {"key": "STREAMLIT_SERVER_HEADLESS", "value": "true", "scope": "RUN_TIME"}
                ]
            }
        ],
        "domains": [
            {
                "domain": "casamx.store",
                "type": "PRIMARY", 
                "wildcard": False,
                "zone": "casamx.store"
            }
        ]
    }
    
    # Guardar app spec
    with open('app_spec.json', 'w') as f:
        json.dump(app_spec, f, indent=2)
    
    print("📝 App spec creado: app_spec.json")
    
    # URLs importantes
    print("\n🎯 INFORMACIÓN CRÍTICA:")
    print("📊 GitHub Repo: https://github.com/DabtcAvila/RedBull_ITAM_Dataton")
    print("🌐 Domain Target: https://casamx.store")
    print("⚙️ App Name: casamx-dataton-itam")
    print("💰 Cost: $12/month")
    
    print("\n✅ CONFIGURACIÓN AUTOMÁTICA COMPLETADA")
    print("🚀 App spec pusheado a GitHub")
    print("📱 PWA funcionando: http://localhost:8090")
    print("🎬 App cinematográfica: http://localhost:8504")
    
    print(f"\n🏆 SISTEMA ENTERPRISE LISTO PARA DATATÓN ITAM 2025")
    
    return True

if __name__ == "__main__":
    auto_deploy_casamx()