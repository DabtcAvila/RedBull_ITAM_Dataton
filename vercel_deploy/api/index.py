#!/usr/bin/env python3
"""
CasaMX Vercel Serverless Entry Point
Optimized for Vercel deployment with proper HTTP handling
"""

import os
import sys
import subprocess
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import json

# Configure environment for Streamlit
os.environ.update({
    'STREAMLIT_SERVER_PORT': '8501',
    'STREAMLIT_SERVER_ADDRESS': '0.0.0.0',
    'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false',
    'STREAMLIT_SERVER_HEADLESS': 'true',
    'STREAMLIT_SERVER_ENABLE_CORS': 'false',
    'STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION': 'false',
    'STREAMLIT_SERVER_MAX_UPLOAD_SIZE': '50'
})

def start_streamlit():
    """Start Streamlit app in background"""
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 
        '../streamlit_simple.py',
        '--server.port', '8501',
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false'
    ]
    
    subprocess.Popen(cmd, cwd=os.path.dirname(__file__))

def handler(request):
    """Main Vercel handler function"""
    
    # Start Streamlit if not running
    try:
        urllib.request.urlopen('http://localhost:8501', timeout=1)
    except:
        start_streamlit()
        time.sleep(3)  # Wait for Streamlit to start
    
    # Proxy request to Streamlit
    try:
        path = request.get('path', '/')
        method = request.get('httpMethod', 'GET')
        
        if path.startswith('/_stcore'):
            # Handle Streamlit internal requests
            proxy_url = f"http://localhost:8501{path}"
        else:
            # Handle main app requests
            proxy_url = f"http://localhost:8501{path}"
        
        # Make request to Streamlit
        req = urllib.request.Request(proxy_url)
        
        if method == 'POST':
            body = request.get('body', '')
            if body:
                req.data = body.encode()
        
        # Forward headers
        headers = request.get('headers', {})
        for key, value in headers.items():
            if key.lower() not in ['host', 'content-length']:
                req.add_header(key, value)
        
        response = urllib.request.urlopen(req, timeout=10)
        
        return {
            'statusCode': response.getcode(),
            'headers': {
                'Content-Type': response.getheader('Content-Type', 'text/html'),
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': response.read().decode('utf-8', errors='ignore')
        }
        
    except Exception as e:
        # Fallback response
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>CasaMX - Cargando...</title>
                <meta http-equiv="refresh" content="3">
            </head>
            <body>
                <h1>🏠 CasaMX está iniciando...</h1>
                <p>Por favor espera unos segundos mientras la aplicación se carga.</p>
                <script>setTimeout(function(){{ location.reload(); }}, 3000);</script>
            </body>
            </html>
            """
        }

# For local testing
if __name__ == "__main__":
    start_streamlit()
    print("Streamlit started on http://localhost:8501")