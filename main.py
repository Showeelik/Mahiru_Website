from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
from urllib.parse import parse_qs

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='static', **kwargs)

    def do_GET(self):
        if self.path.endswith('.css'):
            # Если запрашивается CSS файл, отдаем его
            css_path = os.path.join(self.directory, self.path.lstrip('/'))
            if os.path.exists(css_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()

                with open(css_path, 'r', encoding='utf-8') as file:
                    css_content = file.read()
                    self.wfile.write(css_content.encode('utf-8'))
            else:
                self.send_error(404, "CSS file not found")
        else:
            # Возвращаем страницу контактов для любого другого GET запроса
            contacts_path = os.path.join(self.directory, 'contacts.html')

            if os.path.exists(contacts_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                with open(contacts_path, 'r', encoding='utf-8') as file:
                    contacts_content = file.read()
                    self.wfile.write(contacts_content.encode('utf-8'))
            else:
                self.send_error(404, "Contacts page not found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        # Читаем данные POST-запроса
        post_data = self.rfile.read(content_length)
        
        # Парсим данные из POST-запроса
        parsed_data = parse_qs(post_data.decode('utf-8'))

        # Печатаем данные в консоль
        print("Received POST data:")
        for key, value in parsed_data.items():
            print(f"{key}: {value}")

        # После обработки POST-запроса можно вернуть страницу
        self.path = '/contacts.html'
        self.do_GET()

def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on http://localhost:{port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
