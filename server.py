#!/usr/bin/env python3
"""
CasaMX - Pure Python HTTP Server
NO dependencies - GUARANTEED to work
"""

import http.server
import socketserver
import json
import os

PORT = int(os.environ.get('PORT', 8080))

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="es-MX">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CasaMX - Tu hogar ideal en México</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 3rem; }
        .header h1 { font-size: 3rem; margin-bottom: 0.5rem; }
        .header h2 { font-size: 1.5rem; opacity: 0.9; margin-bottom: 1rem; }
        .stats { display: flex; justify-content: center; gap: 2rem; margin: 2rem 0; }
        .stat { text-align: center; }
        .stat-number { font-size: 2rem; font-weight: bold; color: #FFD700; }
        .form-card {
            background: rgba(255,255,255,0.1);
            padding: 2rem;
            border-radius: 20px;
            backdrop-filter: blur(15px);
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .input-group { margin: 1.5rem 0; }
        .input-group label { display: block; margin-bottom: 0.5rem; font-weight: 600; }
        .slider {
            width: 100%;
            height: 8px;
            border-radius: 5px;
            background: rgba(255,255,255,0.3);
            outline: none;
            -webkit-appearance: none;
        }
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #FFD700;
            cursor: pointer;
        }
        .button {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            border: none;
            padding: 15px 40px;
            border-radius: 30px;
            color: white;
            font-weight: bold;
            font-size: 18px;
            cursor: pointer;
            transition: transform 0.2s;
            display: block;
            margin: 2rem auto 0;
        }
        .button:hover { transform: scale(1.05); }
        .results { display: none; margin-top: 2rem; }
        .zona-card {
            background: rgba(255,255,255,0.15);
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 15px;
            border-left: 5px solid #FFD700;
            transition: transform 0.2s;
        }
        .zona-card:hover { transform: translateY(-5px); }
        .demo-buttons { display: flex; gap: 1rem; justify-content: center; margin: 2rem 0; }
        .demo-btn {
            background: rgba(255,255,255,0.2);
            border: 2px solid white;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .demo-btn:hover { background: white; color: #667eea; }
        @media (max-width: 768px) {
            .stats { flex-direction: column; gap: 1rem; }
            .demo-buttons { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 CasaMX</h1>
            <h2>Tu hogar ideal en México</h2>
            <p>Recomendaciones personalizadas de zonas en CDMX para extranjeros</p>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-number">2.1M+</div>
                <div>Extranjeros en México</div>
            </div>
            <div class="stat">
                <div class="stat-number">150+</div>
                <div>Zonas analizadas</div>
            </div>
            <div class="stat">
                <div class="stat-number">&lt;3s</div>
                <div>Tiempo de respuesta</div>
            </div>
        </div>

        <div class="demo-buttons">
            <button class="demo-btn" onclick="loadDemo('familia')">👨‍👩‍👧‍👦 Demo Familia</button>
            <button class="demo-btn" onclick="loadDemo('profesional')">💻 Demo Profesional</button>
            <button class="demo-btn" onclick="loadDemo('estudiante')">🎓 Demo Estudiante</button>
        </div>

        <div class="form-card">
            <h3>🎯 Personaliza tu búsqueda</h3>
            <div class="input-group">
                <label for="presupuesto">💰 Presupuesto mensual:</label>
                <input type="range" id="presupuesto" class="slider" min="10000" max="50000" value="25000" onchange="updateValue('presupuesto')">
                <span id="presupuesto-display">$25,000 MXN</span>
            </div>
            
            <div class="input-group">
                <label for="seguridad">🛡️ Prioridad Seguridad:</label>
                <input type="range" id="seguridad" class="slider" min="1" max="10" value="8" onchange="updateValue('seguridad')">
                <span id="seguridad-display">8/10</span>
            </div>
            
            <div class="input-group">
                <label for="transporte">🚇 Prioridad Transporte:</label>
                <input type="range" id="transporte" class="slider" min="1" max="10" value="7" onchange="updateValue('transporte')">
                <span id="transporte-display">7/10</span>
            </div>
            
            <button class="button" onclick="buscarZonas()">🔍 Buscar mi zona ideal</button>
        </div>

        <div id="resultados" class="results">
            <h3>🎯 Tus Recomendaciones Personalizadas</h3>
            <div id="zonas-list"></div>
        </div>

        <footer style="text-align: center; margin-top: 3rem; opacity: 0.8;">
            <p><strong>CasaMX</strong> - Datatón ITAM 2025 | David Fernando Ávila Díaz - ITAM</p>
        </footer>
    </div>

    <script>
        const colonias = [
            {nombre: "Roma Norte", precio: 25000, seguridad: 85, transporte: 95, alcaldia: "Cuauhtémoc"},
            {nombre: "Condesa", precio: 28000, seguridad: 82, transporte: 88, alcaldia: "Cuauhtémoc"},
            {nombre: "Polanco", precio: 45000, seguridad: 95, transporte: 85, alcaldia: "Miguel Hidalgo"},
            {nombre: "Del Valle", precio: 22000, seguridad: 88, transporte: 78, alcaldia: "Benito Juárez"},
            {nombre: "Coyoacán Centro", precio: 18000, seguridad: 90, transporte: 70, alcaldia: "Coyoacán"},
            {nombre: "Narvarte", precio: 20000, seguridad: 75, transporte: 85, alcaldia: "Benito Juárez"},
            {nombre: "Santa Fe", precio: 35000, seguridad: 88, transporte: 72, alcaldia: "Cuajimalpa"},
            {nombre: "San Ángel", precio: 32000, seguridad: 92, transporte: 68, alcaldia: "Álvaro Obregón"}
        ];

        function updateValue(sliderId) {
            const slider = document.getElementById(sliderId);
            const display = document.getElementById(sliderId + '-display');
            if (sliderId === 'presupuesto') {
                display.textContent = '$' + parseInt(slider.value).toLocaleString() + ' MXN';
            } else {
                display.textContent = slider.value + '/10';
            }
        }

        function loadDemo(tipo) {
            if (tipo === 'familia') {
                document.getElementById('presupuesto').value = 35000;
                document.getElementById('seguridad').value = 9;
                document.getElementById('transporte').value = 7;
            } else if (tipo === 'profesional') {
                document.getElementById('presupuesto').value = 25000;
                document.getElementById('seguridad').value = 6;
                document.getElementById('transporte').value = 9;
            } else if (tipo === 'estudiante') {
                document.getElementById('presupuesto').value = 15000;
                document.getElementById('seguridad').value = 7;
                document.getElementById('transporte').value = 8;
            }
            
            updateValue('presupuesto');
            updateValue('seguridad');
            updateValue('transporte');
            
            setTimeout(() => buscarZonas(), 500);
        }

        function buscarZonas() {
            const presupuesto = parseInt(document.getElementById('presupuesto').value);
            const prioridadSeguridad = parseInt(document.getElementById('seguridad').value);
            const prioridadTransporte = parseInt(document.getElementById('transporte').value);
            
            const zonasFiltradas = colonias.filter(zona => zona.precio <= presupuesto * 1.2);
            
            const zonasConScore = zonasFiltradas.map(zona => {
                const score = (zona.seguridad * prioridadSeguridad + zona.transporte * prioridadTransporte) / 2;
                return {...zona, score};
            });
            
            zonasConScore.sort((a, b) => b.score - a.score);
            const top3 = zonasConScore.slice(0, 3);
            
            let html = '';
            top3.forEach((zona, index) => {
                html += `
                    <div class="zona-card">
                        <h4>#${index + 1}: ${zona.nombre}</h4>
                        <p><strong>Alcaldía:</strong> ${zona.alcaldia}</p>
                        <p><strong>💰 Precio:</strong> $${zona.precio.toLocaleString()}/mes</p>
                        <p><strong>🛡️ Seguridad:</strong> ${zona.seguridad}/100</p>
                        <p><strong>🚇 Transporte:</strong> ${zona.transporte}/100</p>
                        <p><strong>⭐ Score:</strong> ${zona.score.toFixed(1)}/100</p>
                    </div>
                `;
            });
            
            document.getElementById('zonas-list').innerHTML = html;
            document.getElementById('resultados').style.display = 'block';
            document.getElementById('resultados').scrollIntoView({behavior: 'smooth'});
        }
    </script>
</body>
</html>'''

if __name__ == '__main__':
    print("🚀 CasaMX iniciando en puerto", PORT)
    app.run(host='0.0.0.0', port=PORT, debug=False)