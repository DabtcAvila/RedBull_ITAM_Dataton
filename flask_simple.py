from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>CasaMX</title>
<style>body{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;margin:0;padding:20px;text-align:center}.container{max-width:800px;margin:0 auto}h1{font-size:3rem}.card{background:rgba(255,255,255,0.1);padding:2rem;border-radius:15px;margin:2rem 0}.btn{background:#FF6B6B;color:white;border:none;padding:15px 30px;border-radius:20px;cursor:pointer;margin:10px}.zona{background:rgba(255,255,255,0.15);padding:15px;margin:15px;border-radius:10px}#results{display:none}</style>
</head><body><div class="container"><h1>🏠 CasaMX</h1><h2>Tu hogar ideal en México</h2>
<div class="card"><h3>🎯 Demo Datatón ITAM 2025</h3>
<button class="btn" onclick="demo1()">👨‍👩‍👧‍👦 Familia</button>
<button class="btn" onclick="demo2()">💻 Profesional</button>
<button class="btn" onclick="demo3()">🎓 Estudiante</button></div>
<div id="results"><h3>Top 3 Zonas:</h3>
<div class="zona"><h4>Roma Norte</h4><p>💰 $25,000/mes | 🛡️ 85/100 | 🚇 95/100</p></div>
<div class="zona"><h4>Del Valle</h4><p>💰 $22,000/mes | 🛡️ 88/100 | 🚇 78/100</p></div>
<div class="zona"><h4>Coyoacán</h4><p>💰 $18,000/mes | 🛡️ 90/100 | 🚇 70/100</p></div>
</div><footer style="margin-top:3rem"><p><strong>CasaMX</strong> - David Fernando Ávila Díaz - ITAM</p></footer></div>
<script>function demo1(){show("Familia Española")}function demo2(){show("Profesional Italiano")}function demo3(){show("Estudiante Francesa")}function show(p){document.getElementById("results").style.display="block"}</script>
</body></html>'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)