#!/usr/bin/env python3
"""
Servidor simple para CasaMX - Puerto 8080
David Fernando Ávila Díaz - ITAM Datatón 2025
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

class CasaMXHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
            return
        
        return super().do_GET()

def main():
    PORT = int(os.environ.get('PORT', 8080))
    
    # Cambiar al directorio donde está index.html
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print(f"🚀 Starting CasaMX server on port {PORT}")
    print(f"📁 Serving from: {os.getcwd()}")
    print(f"📄 Index file: {'✅' if os.path.exists('index.html') else '❌'}")
    
    with socketserver.TCPServer(("", PORT), CasaMXHandler) as httpd:
        print(f"🌐 Server running at http://localhost:{PORT}")
        print("🏠 CasaMX - Datatón ITAM 2025 - David Fernando Ávila Díaz")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Shutting down CasaMX server...")
            httpd.shutdown()

if __name__ == "__main__":
    main()