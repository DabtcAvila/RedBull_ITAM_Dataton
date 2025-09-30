#!/bin/bash

echo "🚀 Iniciando CasaMX con Sistema de Casos Demo..."
echo "📊 Para presentación fluida de 10 minutos"
echo ""
echo "Casos disponibles:"
echo "1. 👩‍👧‍👦 MARÍA - Familia española (4 personas, $35,000 MXN)"
echo "2. 👨‍💻 ALEX - Profesional tech italiano (soltero, $25,000 MXN)"
echo "3. 👩‍🎓 SOPHIE - Estudiante francesa (soltera, $15,000 MXN)"
echo ""
echo "🌐 Abriendo aplicación en: http://localhost:8501"
echo "👆 Haz clic en los botones de casos demo para presentación instantánea"
echo ""

cd "/Users/davicho/MASTER proyectos/RedBull_ITAM_Dataton"

# Activar entorno virtual
source casamx_env/bin/activate

# Ejecutar Streamlit
streamlit run streamlit_app_fixed.py --server.port=8501 --server.address=0.0.0.0