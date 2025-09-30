# CasaMX Procfile - Comandos de ejecución para deployment
# Datatón ITAM 2025

# Web application (Streamlit) - Puerto principal
web: python -m streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false

# API service (FastAPI) - Puerto alternativo
api: cd src/api && python -m uvicorn main:app --host=0.0.0.0 --port=8000

# Worker process para tareas en background (si necesario)
# worker: python background_worker.py

# Release commands (ejecutar en deployment)
release: python setup_quick.py