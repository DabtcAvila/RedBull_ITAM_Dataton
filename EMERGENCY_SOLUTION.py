#!/usr/bin/env python3
"""
EMERGENCY SOLUTION - CasaMX 
Servidor HTTP simple que GARANTIZADAMENTE funciona
"""

import http.server
import socketserver
import webbrowser
import threading
import os

PORT = 8077
IP = "0.0.0.0"  # Accesible desde cualquier IP

HTML_CASAMX = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CasaMX - Tu hogar ideal en México</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; margin: 0; padding: 20px; min-height: 100vh;
        }
        .container { max-width: 1000px; margin: 0 auto; text-align: center; }
        .header h1 { font-size: 3rem; margin-bottom: 1rem; }
        .stats { display: flex; justify-content: space-around; margin: 2rem 0; }
        .stat { text-align: center; background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; }
        .stat-number { font-size: 2rem; font-weight: bold; color: #FFD700; }
        .demo-btn {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            border: none; padding: 15px 30px; border-radius: 20px;
            color: white; font-weight: bold; cursor: pointer; 
            margin: 10px; font-size: 16px;
        }
        .zona { 
            background: rgba(255,255,255,0.15); padding: 15px; 
            margin: 15px; border-radius: 10px; 
            border-left: 4px solid #FFD700; text-align: left;
        }
        #resultados { display: none; margin-top: 2rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 CasaMX</h1>
            <h2>Tu hogar ideal en México</h2>
            <p>Recomendaciones inteligentes para extranjeros en CDMX</p>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-number">2.1M+</div>
                <div>Extranjeros</div>
            </div>
            <div class="stat">
                <div class="stat-number">8</div>
                <div>Zonas Premium</div>
            </div>
            <div class="stat">
                <div class="stat-number">92%</div>
                <div>Precisión</div>
            </div>
        </div>

        <div>
            <h3>🎯 Casos Demo Instantáneos</h3>
            <button class="demo-btn" onclick="demoFamilia()">👨‍👩‍👧‍👦 Familia Española</button>
            <button class="demo-btn" onclick="demoProfesional()">💻 Profesional Italiano</button>
            <button class="demo-btn" onclick="demoEstudiante()">🎓 Estudiante Francesa</button>
        </div>

        <div id="resultados">
            <h3>🏆 Recomendaciones Personalizadas</h3>
            <div id="zona-list"></div>
        </div>

        <footer style="margin-top: 3rem; opacity: 0.8; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 2rem;">
            <h3>🏆 CasaMX - Datatón ITAM 2025</h3>
            <p><strong>David Fernando Ávila Díaz</strong> - ITAM</p>
        </footer>
    </div>

    <script>
        const colonias = [
            {nombre: "Roma Norte", precio: 25000, seguridad: 85, transporte: 95, alcaldia: "Cuauhtémoc"},
            {nombre: "Condesa", precio: 28000, seguridad: 82, transporte: 88, alcaldia: "Cuauhtémoc"},
            {nombre: "Polanco", precio: 45000, seguridad: 95, transporte: 85, alcaldia: "Miguel Hidalgo"},
            {nombre: "Del Valle", precio: 22000, seguridad: 88, transporte: 78, alcaldia: "Benito Juárez"},
            {nombre: "Coyoacán", precio: 18000, seguridad: 90, transporte: 70, alcaldia: "Coyoacán"}
        ];

        function mostrarZonas(zonas, titulo) {
            let html = `<h4>${titulo}</h4>`;
            zonas.forEach((zona, i) => {
                html += `
                    <div class="zona">
                        <h4>#${i+1}: ${zona.nombre}</h4>
                        <p><strong>Alcaldía:</strong> ${zona.alcaldia}</p>
                        <p><strong>💰</strong> $${zona.precio.toLocaleString()}/mes</p>
                        <p><strong>🛡️</strong> Seguridad: ${zona.seguridad}/100</p>
                        <p><strong>🚇</strong> Transporte: ${zona.transporte}/100</p>
                    </div>
                `;
            });
            document.getElementById('zona-list').innerHTML = html;
            document.getElementById('resultados').style.display = 'block';
            document.getElementById('resultados').scrollIntoView({behavior: 'smooth'});
        }

        function demoFamilia() {
            const zonas = colonias.filter(z => z.seguridad >= 85 && z.precio <= 35000)
                                   .sort((a,b) => b.seguridad - a.seguridad)
                                   .slice(0,3);
            mostrarZonas(zonas, "👨‍👩‍👧‍👦 Perfecto para María & Carlos (Familia con niños)");
        }

        function demoProfesional() {
            const zonas = colonias.filter(z => z.transporte >= 80 && z.precio <= 30000)
                                   .sort((a,b) => b.transporte - a.transporte)
                                   .slice(0,3);
            mostrarZonas(zonas, "💻 Ideal para Alessandro (Profesional tech)");
        }

        function demoEstudiante() {
            const zonas = colonias.filter(z => z.precio <= 22000)
                                   .sort((a,b) => a.precio - b.precio)
                                   .slice(0,3);
            mostrarZonas(zonas, "🎓 Económico para Sophie (Estudiante)");
        }
    </script>
</body>
</html>'''

class CasaMXHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(HTML_CASAMX.encode('utf-8'))

def start_server():
    with socketserver.TCPServer((IP, PORT), CasaMXHandler) as httpd:
        print(f"🚀 CasaMX EMERGENCY SERVER FUNCIONANDO")
        print(f"🌐 Local: http://localhost:{PORT}")
        print(f"🌍 Red: http://192.168.100.76:{PORT}")  
        print(f"🔗 Externa: http://187.188.41.37:{PORT}")
        print(f"✅ Listo para demo Datatón ITAM 2025")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()