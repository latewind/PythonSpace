#windServer.py
#-*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import socketserver

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers()
        page = self.create_page()
        self.wfile.write(bytes(page,encoding='utf-8'))
    def create_page(self):
        values = {
        'date_time'         :self.date_time_string(),
        'client_address'    :self.client_address[0],
        'path'              :self.path
        }
        return self.Page.format(**values)

    Page = '''
<html>
<body>
<p>Hello, web!</p>
{date_time}
{client_address}
{path}
</body>
</html>
'''

if __name__ == '__main__':
    address=('',18887)
    with socketserver.TCPServer(address,RequestHandler)  as httpd:
        httpd.serve_forever()
