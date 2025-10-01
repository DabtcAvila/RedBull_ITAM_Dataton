from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''<h1>🏠 CasaMX</h1><p>Tu hogar ideal en México</p><p>Datatón ITAM 2025 - David Fernando Ávila Díaz</p>'''

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))