# caseSever.py
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
import socketserver
import os

url_views = {'/py': '/views/py.html',
             '/error': '/views/error.html',
             '/': '/views/index.html',
             '/index': '/views/index.html'}


class CaseExistingFile:
    @classmethod
    def test(cls, path):
        return path in url_views

    @classmethod
    def act(cls, handler):
        handler.handle_file()


class CaseNonExistingFile:
    @classmethod
    def test(cls, path):
        return path not in url_views

    @classmethod
    def act(cls, handler):
        handler.handle_error()


class RequestHandler(BaseHTTPRequestHandler):
    Cases = [CaseExistingFile(),
             CaseNonExistingFile()]
    Error_Page = """
        <html>
        <body>
        <h1>{msg}</h1>
        <p>Error accessing {path}</p>
        </body>
        </html>
        """

    def do_GET(self):
        for case in self.Cases:
            if case.test(self.path):
                case.act(self)
                break

    def handle_file(self):
        try:
            full_path = os.getcwd() + url_views.get(self.path)
            with open(full_path, 'rb') as f:
                content = f.read()
            self.send_content(content, 200)
        except Exception:
            self.handle_error()

    def handle_error(self):
        content = bytes(self.Error_Page.format(path=self.path, msg='404'), encoding='utf-8')
        self.send_content(content, 404)

    def send_content(self, content, status):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)


if __name__ == '__main__':
    with socketserver.TCPServer(('', 8881), RequestHandler) as httpd:
        httpd.serve_forever()
