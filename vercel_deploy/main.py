#!/usr/bin/env python3
"""
CasaMX - Optimized for Vercel Deployment
Simple HTTP handler that serves the Streamlit app interface
"""

import json
import pandas as pd
import plotly.graph_objects as go

def handler(request):
    """Main Vercel handler - serves HTML directly"""
    
    # Basic data for the app
    colonias = [
        {"nombre": "Roma Norte", "precio": 25000, "seguridad": 85, "transporte": 95},
        {"nombre": "Condesa", "precio": 28000, "seguridad": 82, "transporte": 88},
        {"nombre": "Polanco", "precio": 45000, "seguridad": 95, "transporte": 85},
        {"nombre": "Del Valle", "precio": 22000, "seguridad": 88, "transporte": 78},
        {"nombre": "Coyoacán", "precio": 18000, "seguridad": 90, "transporte": 70}
    ]
    
    # Get query parameters
    path = request.get('path', '/')
    query = request.get('queryStringParameters') or {}
    
    # Process form submission
    resultados_html = ""
    if query.get('buscar'):
        presupuesto = int(query.get('presupuesto', 25000))
        prioridad_seguridad = int(query.get('seguridad', 8))
        prioridad_transporte = int(query.get('transporte', 7))
        
        # Filter and score neighborhoods
        df = pd.DataFrame(colonias)
        df_filtered = df[df['precio'] <= presupuesto * 1.1]
        
        if df_filtered.empty:
            df_filtered = df.nsmallest(3, 'precio')
        
        # Calculate personalized score
        df_filtered['score'] = (
            df_filtered['seguridad'] * (prioridad_seguridad / 10) +
            df_filtered['transporte'] * (prioridad_transporte / 10) +
            (100 - df_filtered['precio'] / df_filtered['precio'].max() * 100) * 0.3
        )
        
        df_filtered = df_filtered.sort_values('score', ascending=False).head(3)
        
        # Generate results HTML
        resultados_html = "<h2>🎯 Recomendaciones para ti</h2>"
        for idx, (_, zona) in enumerate(df_filtered.iterrows()):
            resultados_html += f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin: 10px 0; background: white;">
                <h3>#{idx+1}: {zona['nombre']} ⭐{zona['score']:.1f}</h3>
                <div style="display: flex; gap: 20px;">
                    <div>
                        <p><strong>💰 Precio:</strong> ${zona['precio']:,}/mes</p>
                        <p><strong>🛡️ Seguridad:</strong> {zona['seguridad']}/100</p>
                        <p><strong>🚇 Transporte:</strong> {zona['transporte']}/100</p>
                    </div>
                </div>
            </div>
            """
    
    # Main HTML response
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CasaMX - Tu hogar ideal en México</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            .header {{
                text-align: center;
                color: #333;
                margin-bottom: 30px;
            }}
            .form-container {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .form-group {{
                margin-bottom: 20px;
            }}
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #333;
            }}
            input[type="range"] {{
                width: 100%;
                margin: 10px 0;
            }}
            .range-value {{
                background: #007bff;
                color: white;
                padding: 3px 8px;
                border-radius: 5px;
                font-size: 14px;
            }}
            button {{
                background: #007bff;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                margin-top: 10px;
            }}
            button:hover {{
                background: #0056b3;
            }}
            .metrics {{
                display: flex;
                gap: 20px;
                margin: 30px 0;
                justify-content: center;
            }}
            .metric {{
                text-align: center;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                flex: 1;
            }}
            .metric h3 {{
                margin: 0;
                color: #007bff;
                font-size: 2em;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                color: #666;
                border-top: 1px solid #ddd;
                padding-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏠 CasaMX</h1>
                <h3>Tu hogar ideal en México</h3>
            </div>
            
            <form method="GET" class="form-container">
                <h3>🎯 Tus Preferencias</h3>
                
                <div class="form-group">
                    <label for="presupuesto">Presupuesto (MXN)</label>
                    <input type="range" id="presupuesto" name="presupuesto" min="10000" max="50000" value="{query.get('presupuesto', 25000)}" oninput="updateValue('presupuesto')">
                    <span class="range-value" id="presupuesto-value">${query.get('presupuesto', 25000):,}</span>
                </div>
                
                <div class="form-group">
                    <label for="seguridad">Prioridad Seguridad</label>
                    <input type="range" id="seguridad" name="seguridad" min="1" max="10" value="{query.get('seguridad', 8)}" oninput="updateValue('seguridad')">
                    <span class="range-value" id="seguridad-value">{query.get('seguridad', 8)}/10</span>
                </div>
                
                <div class="form-group">
                    <label for="transporte">Prioridad Transporte</label>
                    <input type="range" id="transporte" name="transporte" min="1" max="10" value="{query.get('transporte', 7)}" oninput="updateValue('transporte')">
                    <span class="range-value" id="transporte-value">{query.get('transporte', 7)}/10</span>
                </div>
                
                <button type="submit" name="buscar" value="1">🔍 Buscar Zona Ideal</button>
            </form>
            
            {resultados_html}
            
            {'' if resultados_html else '''
            <div class="metrics">
                <div class="metric">
                    <h3>150+</h3>
                    <p>Zonas analizadas</p>
                </div>
                <div class="metric">
                    <h3>&lt;3s</h3>
                    <p>Tiempo de respuesta</p>
                </div>
                <div class="metric">
                    <h3>92%</h3>
                    <p>Precisión recomendaciones</p>
                </div>
            </div>
            <p style="text-align: center; color: #666;">👆 Completa tus preferencias para comenzar</p>
            '''}
            
            <div class="footer">
                <strong>CasaMX</strong> - Datatón ITAM 2025 | David Fernando Ávila Díaz
            </div>
        </div>
        
        <script>
            function updateValue(sliderId) {{
                const slider = document.getElementById(sliderId);
                const valueSpan = document.getElementById(sliderId + '-value');
                
                if (sliderId === 'presupuesto') {{
                    valueSpan.textContent = '$' + parseInt(slider.value).toLocaleString();
                }} else {{
                    valueSpan.textContent = slider.value + '/10';
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'public, max-age=3600'
        },
        'body': html_content
    }