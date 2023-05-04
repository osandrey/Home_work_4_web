import mimetypes
import pickle

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from pathlib import Path
import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 5000



class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        print(self.path)
        if pr_url.path == '/':
            self.send_html_file('../web/templates/index.html')
        elif pr_url.path == '/message':
            self.send_html_file('../web/templates/message.html')
        else:
            if Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('../web/templates/error.html', 404)



    def do_POST(self):
        data = self.rfile.read()

        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        run_client(UDP_IP, UDP_PORT, data_dict)
        print(f'DATA PARSED: {data_parse}')
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())


def run_client(ip, port, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.connect(server)
    username = data['username']
    message = data['message']
    d_file = pickle.dumps((username, message))
    sock.sendall(d_file)

    while True:
        data = sock.recv(1024)
        print(f'Received data from server {data.decode().lower()}')
        if not data:
            break
    sock.close()


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('127.0.0.1', 5000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
