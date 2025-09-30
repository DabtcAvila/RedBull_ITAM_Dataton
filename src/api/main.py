#!/usr/bin/env python3
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
