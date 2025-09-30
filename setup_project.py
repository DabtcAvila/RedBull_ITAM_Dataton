#!/usr/bin/env python3
"""
CasaMX - Setup Project Script
Datatón ITAM 2025

Este script automatiza la configuración del proyecto CasaMX incluyendo:
- Instalación de dependencias
- Creación de estructura de directorios
- Configuración del entorno virtual
- Preparación de datos mock
- Verificación de componentes
"""

import os
import sys
import subprocess
import json
import sqlite3
from pathlib import Path

class CasaMXSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.data_path = self.project_root / "data"
        self.src_path = self.project_root / "src"
        self.tests_path = self.project_root / "tests"
        
    def print_step(self, step, message):
        """Imprime un paso del proceso de setup"""
        print(f"\n{'='*60}")
        print(f"PASO {step}: {message}")
        print(f"{'='*60}")
    
    def run_command(self, command, check=True):
        """Ejecuta un comando y maneja errores"""
        try:
            result = subprocess.run(command, shell=True, check=check, 
                                  capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando comando: {command}")
            print(f"Error: {e.stderr}")
            if check:
                sys.exit(1)
            return e
    
    def create_virtual_environment(self):
        """Crea y configura el entorno virtual"""
        self.print_step(1, "Creando entorno virtual")
        
        if self.venv_path.exists():
            print(f"Entorno virtual ya existe en {self.venv_path}")
            return
        
        # Crear entorno virtual
        self.run_command(f"python3 -m venv {self.venv_path}")
        print(f"Entorno virtual creado en {self.venv_path}")
        
        # Actualizar pip
        pip_cmd = f"{self.venv_path}/bin/pip" if os.name != 'nt' else f"{self.venv_path}\\Scripts\\pip.exe"
        self.run_command(f"{pip_cmd} install --upgrade pip")
        
    def install_dependencies(self):
        """Instala las dependencias desde requirements.txt"""
        self.print_step(2, "Instalando dependencias")
        
        pip_cmd = f"{self.venv_path}/bin/pip" if os.name != 'nt' else f"{self.venv_path}\\Scripts\\pip.exe"
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("ERROR: No se encontró requirements.txt")
            sys.exit(1)
        
        # Instalar dependencias
        self.run_command(f"{pip_cmd} install -r {requirements_file}")
        print("Dependencias instaladas exitosamente")
        
    def create_directory_structure(self):
        """Crea la estructura de directorios del proyecto"""
        self.print_step(3, "Creando estructura de directorios")
        
        directories = [
            self.data_path,
            self.data_path / "raw",
            self.data_path / "processed", 
            self.data_path / "mock",
            self.data_path / "geographic",
            self.src_path,
            self.src_path / "api",
            self.src_path / "models",
            self.src_path / "utils",
            self.src_path / "visualization",
            self.tests_path,
            self.project_root / "notebooks",
            self.project_root / "config",
            self.project_root / "logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"Creado: {directory}")
            
        # Crear archivos __init__.py para hacer los directorios paquetes de Python
        init_files = [
            self.src_path / "__init__.py",
            self.src_path / "api" / "__init__.py",
            self.src_path / "models" / "__init__.py", 
            self.src_path / "utils" / "__init__.py",
            self.src_path / "visualization" / "__init__.py",
            self.tests_path / "__init__.py"
        ]
        
        for init_file in init_files:
            init_file.touch()
            
    def setup_database(self):
        """Crea la base de datos SQLite y carga datos mock"""
        self.print_step(4, "Configurando base de datos")
        
        db_path = self.data_path / "casamx.db"
        
        # Conectar a la base de datos (se crea si no existe)
        conn = sqlite3.connect(db_path)
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
        mock_file = self.project_root / "dataset_mock_cdmx.json"
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
        
        print(f"Base de datos configurada en: {db_path}")
        print("Datos mock cargados exitosamente")
        
    def copy_mock_data(self):
        """Copia archivos de datos mock a la carpeta data/mock"""
        self.print_step(5, "Copiando datos mock")
        
        mock_source = self.project_root / "dataset_mock_cdmx.json"
        mock_dest = self.data_path / "mock" / "dataset_mock_cdmx.json"
        
        if mock_source.exists():
            import shutil
            shutil.copy2(mock_source, mock_dest)
            print(f"Datos mock copiados a: {mock_dest}")
        
    def create_config_files(self):
        """Crea archivos de configuración básicos"""
        self.print_step(6, "Creando archivos de configuración")
        
        # Archivo de configuración principal
        config_content = {
            "project_name": "CasaMX",
            "version": "1.0.0",
            "database": {
                "type": "sqlite",
                "path": "data/casamx.db"
            },
            "api": {
                "host": "localhost",
                "port": 8000,
                "debug": True
            },
            "data_sources": {
                "inegi": {
                    "base_url": "https://www.inegi.org.mx/app/api/",
                    "timeout": 30
                }
            },
            "logging": {
                "level": "INFO",
                "file": "logs/casamx.log"
            }
        }
        
        config_file = self.project_root / "config" / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_content, f, indent=2, ensure_ascii=False)
        
        # Archivo .env de ejemplo
        env_content = """# CasaMX Environment Variables
DATABASE_URL=sqlite:///data/casamx.db
API_HOST=localhost
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO

# API Keys (agregar cuando sea necesario)
# GOOGLE_MAPS_API_KEY=your_key_here
# INEGI_API_KEY=your_key_here
"""
        
        env_file = self.project_root / ".env.example"
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("Archivos de configuración creados")
        
    def create_basic_api(self):
        """Crea una API básica de FastAPI"""
        self.print_step(7, "Creando API básica")
        
        api_content = '''"""
CasaMX API - Datatón ITAM 2025
FastAPI básica para el proyecto de análisis de vivienda
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any

app = FastAPI(
    title="CasaMX API",
    description="API para análisis de datos de vivienda en CDMX",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de la base de datos
DB_PATH = Path(__file__).parent.parent.parent / "data" / "casamx.db"

def get_db_connection():
    """Obtiene conexión a la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {"message": "CasaMX API - Datatón ITAM 2025", "status": "active"}

@app.get("/colonias")
async def get_colonias():
    """Obtiene todas las colonias"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM colonias")
        rows = cursor.fetchall()
        conn.close()
        
        colonias = []
        for row in rows:
            colonias.append(dict(row))
        
        return {"colonias": colonias}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/colonias/{colonia_id}")
async def get_colonia(colonia_id: str):
    """Obtiene una colonia específica"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM colonias WHERE id = ?", (colonia_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            raise HTTPException(status_code=404, detail="Colonia no encontrada")
        
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def search_colonias(
    alcaldia: str = None,
    min_seguridad: float = None,
    max_precio_renta: float = None
):
    """Busca colonias con filtros"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM colonias WHERE 1=1"
        params = []
        
        if alcaldia:
            query += " AND alcaldia = ?"
            params.append(alcaldia)
        
        if min_seguridad:
            query += " AND score_seguridad >= ?"
            params.append(min_seguridad)
        
        if max_precio_renta:
            query += " AND renta_m2 <= ?"
            params.append(max_precio_renta)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        colonias = []
        for row in rows:
            colonias.append(dict(row))
        
        return {"colonias": colonias}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        
        api_file = self.src_path / "api" / "main.py"
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(api_content)
        
        print("API básica creada en src/api/main.py")
        
    def verify_installation(self):
        """Verifica que todo esté instalado correctamente"""
        self.print_step(8, "Verificando instalación")
        
        # Verificar Python y entorno virtual
        python_cmd = f"{self.venv_path}/bin/python" if os.name != 'nt' else f"{self.venv_path}\\Scripts\\python.exe"
        result = self.run_command(f"{python_cmd} --version")
        
        # Verificar paquetes críticos
        pip_cmd = f"{self.venv_path}/bin/pip" if os.name != 'nt' else f"{self.venv_path}\\Scripts\\pip.exe"
        critical_packages = ["pandas", "fastapi", "sqlite3"]
        
        for package in critical_packages:
            result = self.run_command(f"{python_cmd} -c \"import {package}; print(f'{package} OK')\"", check=False)
            
        # Verificar base de datos
        db_path = self.data_path / "casamx.db"
        if db_path.exists():
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM colonias")
            count = cursor.fetchone()[0]
            conn.close()
            print(f"Base de datos: {count} colonias cargadas")
        
        print("\n✅ Verificación completada")
        
    def run_setup(self):
        """Ejecuta todo el proceso de setup"""
        print("🏠 CasaMX - Setup del Proyecto")
        print("Datatón ITAM 2025")
        print("="*60)
        
        try:
            self.create_virtual_environment()
            self.install_dependencies()
            self.create_directory_structure()
            self.setup_database()
            self.copy_mock_data()
            self.create_config_files()
            self.create_basic_api()
            self.verify_installation()
            
            print("\n🎉 SETUP COMPLETADO EXITOSAMENTE")
            print("="*60)
            print("Para usar el proyecto:")
            print(f"1. Activar entorno virtual: source {self.venv_path}/bin/activate")
            print("2. Ejecutar API: python src/api/main.py")
            print("3. Abrir navegador en: http://localhost:8000")
            print("4. Ver documentación API en: http://localhost:8000/docs")
            
        except Exception as e:
            print(f"\n❌ ERROR en el setup: {e}")
            sys.exit(1)

if __name__ == "__main__":
    setup = CasaMXSetup()
    setup.run_setup()