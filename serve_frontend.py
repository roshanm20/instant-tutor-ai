#!/usr/bin/env python3
"""
Simple HTTP server for serving the frontend
This avoids CORS issues when accessing the frontend from a browser
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def serve_frontend():
    """Start a simple HTTP server for the frontend"""
    PORT = 3000
    FRONTEND_DIR = "frontend"
    
    # Change to frontend directory
    if Path(FRONTEND_DIR).exists():
        os.chdir(FRONTEND_DIR)
        print(f"📁 Serving from: {Path(FRONTEND_DIR).absolute()}")
    else:
        print(f"❌ Frontend directory not found: {FRONTEND_DIR}")
        return False
    
    # Create custom handler to serve index.html for all routes
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            # Serve index.html for all routes (SPA behavior)
            if self.path == '/' or self.path == '/index.html':
                self.path = '/index.html'
            return super().do_GET()
        
        def end_headers(self):
            # Add CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print(f"🌐 Frontend server starting...")
            print(f"📍 URL: http://localhost:{PORT}")
            print(f"📱 Open in browser: http://localhost:{PORT}")
            print(f"🔄 Press Ctrl+C to stop")
            print("=" * 50)
            
            # Open browser automatically
            webbrowser.open(f"http://localhost:{PORT}")
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INSTANT TUTOR AI - Frontend Server")
    print("=" * 50)
    serve_frontend()
