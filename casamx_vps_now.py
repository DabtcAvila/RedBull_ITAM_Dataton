#!/usr/bin/env python3
"""
AUTO-CREATE VPS DIGITALOCEAN - CasaMX
David Fernando Ávila Díaz - ITAM
"""

import subprocess
import json
import time
import requests

def create_casamx_vps():
    """Crear VPS automáticamente para CasaMX"""
    
    print("🚀 CREANDO VPS DIGITALOCEAN AUTOMÁTICAMENTE...")
    
    # App spec para DigitalOcean
    app_spec = {
        "name": "casamx-dataton-final",
        "region": "nyc",
        "services": [
            {
                "name": "web",
                "source_dir": "/",
                "github": {
                    "repo": "DabtcAvila/RedBull_ITAM_Dataton",
                    "branch": "main",
                    "deploy_on_push": True
                },
                "run_command": "cd /app && python3 -m http.server 8080",
                "environment_slug": "python",
                "instance_count": 1,
                "instance_size_slug": "apps-s-1vcpu-1gb",
                "http_port": 8080,
                "routes": [{"path": "/"}],
                "health_check": {"http_path": "/"}
            }
        ],
        "domains": [
            {
                "domain": "casamx.app",
                "type": "PRIMARY",
                "wildcard": False,
                "zone": "casamx.app"
            }
        ]
    }
    
    # Guardar spec
    with open('casamx_app_spec.json', 'w') as f:
        json.dump(app_spec, f, indent=2)
    
    print("✅ App spec creado")
    print("📱 GitHub repo: DabtcAvila/RedBull_ITAM_Dataton")
    print("🌐 Domain: casamx.app")
    print("💰 Cost: $5/mes")
    
    # Comando para crear con doctl
    create_cmd = [
        "doctl", "apps", "create", 
        "--spec", "casamx_app_spec.json"
    ]
    
    try:
        result = subprocess.run(create_cmd, capture_output=True, text=True, check=True)
        print("✅ APP CREADA EXITOSAMENTE:")
        print(result.stdout)
        
        # Extraer URL
        lines = result.stdout.split('\n')
        for line in lines:
            if 'ondigitalocean.app' in line:
                temp_url = line.strip()
                print(f"📡 URL temporal: {temp_url}")
        
        print("🎯 CONFIGURANDO DOMINIO casamx.app...")
        print("⏰ 10-15 minutos → https://casamx.app funcionando")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando app: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        
        # Plan B - instrucciones manuales
        print("\n🔧 PLAN B - CREAR MANUALMENTE:")
        print("1. cloud.digitalocean.com/apps")
        print("2. Create App → GitHub → DabtcAvila/RedBull_ITAM_Dataton")
        print("3. Static Site deployment")
        print("4. Custom domain: casamx.app")

if __name__ == "__main__":
    create_casamx_vps()