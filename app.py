from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''<h1>🏠 CasaMX</h1><p>Tu hogar ideal en México</p><p>Datatón ITAM 2025 - David Fernando Ávila Díaz</p><p>Status: App funcionando correctamente</p>'''

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting CasaMX on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)