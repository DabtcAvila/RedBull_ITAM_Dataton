FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements_production.txt .
RUN pip install --no-cache-dir -r requirements_production.txt

# Copiar aplicación
COPY streamlit_simple.py .
COPY .streamlit/ .streamlit/

EXPOSE 8080

# Comando optimizado para producción
CMD ["streamlit", "run", "streamlit_simple.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]
