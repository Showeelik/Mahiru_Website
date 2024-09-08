import http.server
import socketserver
import os
import webbrowser

PORT = 5500
DIRECTORY = ""

class SPARequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Если путь равен '/' или '/index.html' перенаправляем на '/home'
        if self.path == '/' or self.path == '/index.html':
            self.send_response(302)  # 302 Redirect
            self.send_header('Location', '/home')
            self.end_headers()
        elif self.path != '/' and not os.path.exists(os.path.join(self.directory, self.path.lstrip('/'))):
            self.path = '/index.html'
        return super().do_GET()

with socketserver.TCPServer(("", PORT), SPARequestHandler) as httpd:
    print(f"Serving on url http://localhost:{PORT}")
    webbrowser.open(f"http://localhost:{PORT}")
    httpd.serve_forever()
