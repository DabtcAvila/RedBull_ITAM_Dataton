#!/usr/bin/env python3
"""
CasaMX - Setup Rápido
Datatón ITAM 2025 - Setup simplificado sin entorno virtual
"""

import os
import sys
import subprocess
import json
import sqlite3
from pathlib import Path

def print_step(step, message):
    """Imprime un paso del proceso de setup"""
    print(f"\n{'='*50}")
    print(f"PASO {step}: {message}")
    print(f"{'='*50}")

def run_pip_install():
    """Instala las dependencias críticas"""
    print_step(1, "Instalando dependencias críticas")
    
    critical_packages = [
        "pandas",
        "numpy",
        "fastapi",
        "uvicorn",
        "sqlite3", 
        "requests",
        "plotly",
        "folium"
    ]
    
    for package in critical_packages:
        try:
            if package == "sqlite3":
                # sqlite3 viene incluido en Python
                continue
            print(f"Instalando {package}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {package} instalado")
            else:
                print(f"⚠️  Error instalando {package}: {result.stderr}")
        except Exception as e:
            print(f"❌ Error con {package}: {e}")

def create_directories():
    """Crea la estructura de directorios"""
    print_step(2, "Creando directorios")
    
    base_path = Path(__file__).parent
    directories = [
        "data",
        "data/mock", 
        "data/processed",
        "src",
        "src/api",
        "notebooks",
        "config"
    ]
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}")

def setup_database():
    """Configura la base de datos SQLite"""
    print_step(3, "Configurando base de datos")
    
    base_path = Path(__file__).parent
    db_path = base_path / "data" / "casamx.db"
    
    # Conectar a la base de datos
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Crear tabla de colonias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS colonias (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            alcaldia TEXT NOT NULL,
            codigo_postal TEXT,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            score_seguridad REAL,
            score_transporte REAL,
            score_amenidades REAL,
            score_precio REAL,
            renta_m2 REAL,
            venta_m2 REAL,
            renta_1br REAL,
            renta_2br REAL,
            renta_3br REAL,
            nivel_socioeconomico TEXT,
            poblacion INTEGER,
            densidad_poblacional REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Cargar datos mock
    mock_file = base_path / "dataset_mock_cdmx.json"
    if mock_file.exists():
        with open(mock_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for colonia in data['colonias']:
            cursor.execute("""
                INSERT OR REPLACE INTO colonias (
                    id, nombre, alcaldia, codigo_postal, lat, lon,
                    score_seguridad, score_transporte, score_amenidades, score_precio,
                    renta_m2, venta_m2, renta_1br, renta_2br, renta_3br,
                    nivel_socioeconomico, poblacion, densidad_poblacional
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                colonia['id'],
                colonia['nombre'],
                colonia['alcaldia'],
                colonia['codigo_postal'],
                colonia['coordenadas']['lat'],
                colonia['coordenadas']['lon'],
                colonia['scores']['seguridad'],
                colonia['scores']['transporte'],
                colonia['scores']['amenidades'],
                colonia['scores']['precio'],
                colonia['precios']['renta_m2'],
                colonia['precios']['venta_m2'],
                colonia['precios']['renta_1br'],
                colonia['precios']['renta_2br'],
                colonia['precios']['renta_3br'],
                colonia['caracteristicas']['nivel_socioeconomico'],
                colonia['caracteristicas']['poblacion'],
                colonia['caracteristicas']['densidad_poblacional']
            ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Base de datos creada en: {db_path}")

def create_simple_api():
    """Crea una API simple de prueba"""
    print_step(4, "Creando API de prueba")
    
    base_path = Path(__file__).parent
    api_content = '''#!/usr/bin/env python3
"""CasaMX API Simple"""
from fastapi import FastAPI
import sqlite3
from pathlib import Path

app = FastAPI(title="CasaMX API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "CasaMX API funcionando", "status": "OK"}

@app.get("/colonias")
def get_colonias():
    db_path = Path(__file__).parent.parent / "data" / "casamx.db"
    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM colonias LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return {"colonias": [dict(row) for row in rows]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando API en http://localhost:8000")
    print("📖 Documentación en http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    api_file = base_path / "src" / "api" / "main.py"
    with open(api_file, 'w', encoding='utf-8') as f:
        f.write(api_content)
    
    # Hacer ejecutable
    os.chmod(str(api_file), 0o755)
    print(f"✅ API creada en: {api_file}")

def verify_setup():
    """Verifica que todo esté funcionando"""
    print_step(5, "Verificando setup")
    
    base_path = Path(__file__).parent
    
    # Verificar archivos críticos
    critical_files = [
        "requirements.txt",
        "dataset_mock_cdmx.json", 
        "datos_geograficos_cdmx.json",
        "data/casamx.db",
        "src/api/main.py"
    ]
    
    all_good = True
    for file_path in critical_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ FALTA: {file_path}")
            all_good = False
    
    # Verificar base de datos
    db_path = base_path / "data" / "casamx.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM colonias")
            count = cursor.fetchone()[0]
            conn.close()
            print(f"✅ Base de datos: {count} colonias cargadas")
        except Exception as e:
            print(f"❌ Error en base de datos: {e}")
            all_good = False
    
    return all_good

def main():
    print("🏠 CasaMX - Setup Rápido")
    print("Datatón ITAM 2025")
    print("="*50)
    
    try:
        run_pip_install()
        create_directories() 
        setup_database()
        create_simple_api()
        
        if verify_setup():
            print("\n🎉 SETUP COMPLETADO!")
            print("="*50)
            print("Para probar:")
            print("1. python src/api/main.py")
            print("2. Abrir: http://localhost:8000")
        else:
            print("\n⚠️  Setup completado con errores")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()