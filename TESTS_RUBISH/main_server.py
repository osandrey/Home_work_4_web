from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote_plus


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/':
            self.send_html_file('../web/templates/index.html')
        elif url.path == '/message':
            self.send_html_file('../web/templates/message.html')
        elif url.path == '/thanks':
            self.send_html_file('../web/templates/thanks.html', 302)
        else:
            self.send_html_file('../web/templates/error.html', 404)


    def send_html_file(self, filename, status=200):

        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def do_POST(self):

        raw_data = self.rfile.read()
        data_parse = unquote_plus(raw_data.decode())
        data_parse = self.parse_from_data(data_parse)
        print(data_parse)

        self.send_response(302)
        self.send_header('Location', '/thanks')
        self.end_headers()


    def parse_from_data(self, data):
        data_dict = {key: value for key, value in [el.split('=') for el in data.split('&')]}
        return data_dict

if __name__ == '__main__':
    server = HTTPServer(('localhost', 5353), MyHandler)
    server.serve_forever()