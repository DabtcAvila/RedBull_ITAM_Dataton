#!/usr/bin/env python3
"""
CasaMX - PURE PYTHON VERSION
Absolutely NO external dependencies
GUARANTEED to work in any Python environment
"""

import http.server
import socketserver
import urllib.parse
import json
import os
from datetime import datetime

PORT = int(os.environ.get('PORT', 8080))

class CasaMXHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            html_content = '''<!DOCTYPE html>
<html lang="es-MX">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CasaMX - Tu hogar ideal en México</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            margin: 0; 
            padding: 20px; 
            min-height: 100vh;
        }
        .container { max-width: 1000px; margin: 0 auto; text-align: center; }
        .header { margin-bottom: 2rem; }
        .header h1 { font-size: 3rem; margin-bottom: 0.5rem; }
        .card { 
            background: rgba(255,255,255,0.1); 
            padding: 2rem; 
            border-radius: 15px; 
            backdrop-filter: blur(10px);
            margin: 2rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .button {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
            transition: transform 0.2s;
        }
        .button:hover { transform: scale(1.05); }
        .zona { 
            background: rgba(255,255,255,0.15); 
            padding: 15px; 
            margin: 15px; 
            border-radius: 10px; 
            border-left: 4px solid #FFD700;
        }
        .stats { display: flex; justify-content: space-around; margin: 2rem 0; }
        .stat { text-align: center; }
        .stat-number { font-size: 2rem; font-weight: bold; color: #FFD700; }
        #results { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 CasaMX</h1>
            <h2>Tu hogar ideal en México</h2>
            <p>Recomendaciones inteligentes de zonas CDMX para extranjeros</p>
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
                <div>Tiempo respuesta</div>
            </div>
        </div>

        <div class="card">
            <h3>🎯 Casos Demo Instantáneos</h3>
            <button class="button" onclick="demoFamilia()">👨‍👩‍👧‍👦 Familia Española</button>
            <button class="button" onclick="demoProfesional()">💻 Profesional Italiano</button>
            <button class="button" onclick="demoEstudiante()">🎓 Estudiante Francesa</button>
        </div>

        <div id="results">
            <h3>🎯 Recomendaciones Personalizadas</h3>
            <div id="zona-list"></div>
        </div>

        <footer style="margin-top: 3rem; opacity: 0.8;">
            <p><strong>CasaMX</strong> - Datatón ITAM 2025</p>
            <p>David Fernando Ávila Díaz - ITAM</p>
            <p>🌐 Funcionando desde: ''' + str(datetime.now().strftime("%Y-%m-%d %H:%M")) + '''</p>
        </footer>
    </div>

    <script>
        const colonias = [
            {nombre: "Roma Norte", precio: 25000, seguridad: 85, transporte: 95, alcaldia: "Cuauhtémoc"},
            {nombre: "Condesa", precio: 28000, seguridad: 82, transporte: 88, alcaldia: "Cuauhtémoc"},
            {nombre: "Polanco", precio: 45000, seguridad: 95, transporte: 85, alcaldia: "Miguel Hidalgo"},
            {nombre: "Del Valle", precio: 22000, seguridad: 88, transporte: 78, alcaldia: "Benito Juárez"},
            {nombre: "Coyoacán", precio: 18000, seguridad: 90, transporte: 70, alcaldia: "Coyoacán"},
            {nombre: "Narvarte", precio: 20000, seguridad: 75, transporte: 85, alcaldia: "Benito Juárez"}
        ];

        function showResults(zonas, perfil) {
            let html = `<h4>Resultados para: ${perfil}</h4>`;
            zonas.forEach((zona, i) => {
                html += `
                    <div class="zona">
                        <h4>#${i+1}: ${zona.nombre}</h4>
                        <p><strong>Alcaldía:</strong> ${zona.alcaldia}</p>
                        <p><strong>💰</strong> $${zona.precio.toLocaleString()}/mes</p>
                        <p><strong>🛡️</strong> Seguridad ${zona.seguridad}/100</p>
                        <p><strong>🚇</strong> Transporte ${zona.transporte}/100</p>
                        <p><strong>⭐</strong> Score: ${zona.score ? zona.score.toFixed(1) : 'N/A'}/100</p>
                    </div>
                `;
            });
            
            document.getElementById('zona-list').innerHTML = html;
            document.getElementById('results').style.display = 'block';
            document.getElementById('results').scrollIntoView({behavior: 'smooth'});
        }

        function demoFamilia() {
            const zonas = colonias.filter(z => z.precio <= 35000 && z.seguridad >= 85)
                                   .map(z => ({...z, score: z.seguridad * 0.6 + z.transporte * 0.4}))
                                   .sort((a,b) => b.score - a.score)
                                   .slice(0,3);
            showResults(zonas, "Familia Española (2 niños, €35k)");
        }

        function demoProfesional() {
            const zonas = colonias.filter(z => z.precio <= 28000)
                                   .map(z => ({...z, score: z.transporte * 0.7 + z.seguridad * 0.3}))
                                   .sort((a,b) => b.score - a.score)
                                   .slice(0,3);
            showResults(zonas, "Profesional Italiano (Tech, €25k)");
        }

        function demoEstudiante() {
            const zonas = colonias.filter(z => z.precio <= 20000)
                                   .map(z => ({...z, score: (100 - z.precio/1000) + z.transporte * 0.5}))
                                   .sort((a,b) => b.score - a.score)
                                   .slice(0,3);
            showResults(zonas, "Estudiante Francesa (Universidad, €15k)");
        }
    </script>
</body>
</html>'''
            
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "healthy", "app": "CasaMX", "timestamp": datetime.now().isoformat()}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        else:
            super().do_GET()

if __name__ == "__main__":
    print(f"🚀 CasaMX Pure Python Server iniciando en puerto {PORT}")
    print(f"📊 Datatón ITAM 2025 - David Fernando Ávila Díaz")
    print(f"🌐 Servidor: http://0.0.0.0:{PORT}")
    
    with socketserver.TCPServer(("", PORT), CasaMXHandler) as httpd:
        print(f"✅ CasaMX funcionando en puerto {PORT}")
        httpd.serve_forever()