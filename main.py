"""
CasaMX - Flask version for DigitalOcean
GUARANTEED to work
"""

from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CasaMX - Tu hogar ideal en México</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            margin: 0; 
            padding: 20px; 
        }
        .container { max-width: 800px; margin: 0 auto; text-align: center; }
        .card { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 15px; 
            margin: 20px 0; 
        }
        .button {
            background: #FF6B6B;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
        }
        .zona { 
            background: rgba(255,255,255,0.15); 
            padding: 15px; 
            margin: 10px; 
            border-radius: 10px; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 CasaMX</h1>
        <h2>Tu hogar ideal en México</h2>
        
        <div class="card">
            <h3>🎯 Recomendaciones Instantáneas</h3>
            <button class="button" onclick="showDemo()">Ver Demo</button>
        </div>
        
        <div id="results" style="display:none;">
            <h3>Top 3 Zonas para Ti:</h3>
            <div class="zona">
                <h4>#1: Roma Norte</h4>
                <p>💰 $25,000/mes | 🛡️ 85/100 | 🚇 95/100</p>
                <p>Excelente vida nocturna y transporte</p>
            </div>
            <div class="zona">
                <h4>#2: Del Valle</h4>
                <p>💰 $22,000/mes | 🛡️ 88/100 | 🚇 78/100</p>
                <p>Ideal para familias, zona tranquila</p>
            </div>
            <div class="zona">
                <h4>#3: Coyoacán Centro</h4>
                <p>💰 $18,000/mes | 🛡️ 90/100 | 🚇 70/100</p>
                <p>Cultura, historia y ambiente bohemio</p>
            </div>
        </div>
        
        <div style="margin-top: 40px;">
            <p><strong>CasaMX</strong> - Datatón ITAM 2025</p>
            <p>David Fernando Ávila Díaz</p>
        </div>
    </div>
    
    <script>
        function showDemo() {
            document.getElementById('results').style.display = 'block';
            document.getElementById('results').scrollIntoView({behavior: 'smooth'});
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return {"status": "healthy", "app": "CasaMX"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)