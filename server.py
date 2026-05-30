#!/usr/bin/env python3
import http.server
import socketserver
import os

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Send custom error headers
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def do_GET(self):
        # Check if the requested file exists
        path = self.translate_path(self.path)
        if os.path.exists(path) and os.path.isfile(path):
            return super().do_GET()
        else:
            # File doesn't exist, serve 404 page
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Read and serve the 404.html file
            try:
                with open('404.html', 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                # Fallback if 404.html doesn't exist
                self.wfile.write(b'<h1>404 - Page Not Found</h1>')

PORT = 8001

with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()
