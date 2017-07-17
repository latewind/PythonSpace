# Sever.py
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import socketserver
import os
url_views={'/py': '/views/py.html', '/error': '/views/error.html'}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()

    def handle_request(self):
        try:
            viewname = os.getcwd()+url_views.get(self.path)
            self.send_response(200)
        except TypeError:
            viewname = os.getcwd()+url_views.get('/error')
            self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(viewname, 'rb') as f:
            self.wfile.write(f.read())

if __name__ == '__main__':
    with socketserver.TCPServer(('', 8880), RequestHandler) as httpd:
        httpd.serve_forever()