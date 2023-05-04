import mimetypes

from flask import Flask, render_template, request
import socket
import pickle

app = Flask(__name__, static_url_path='', static_folder='web/static', template_folder='web/templates')
UDP_IP = 'localhost'
UDP_PORT = 5000

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        user_name = request.form.get('username')
        message = request.form.get('message')
        get_data_start_socket(user_name, message)
        return  render_template('thanks.html')
    return render_template('message.html')

def get_data_start_socket(user_name,message):
    print(f'DATA FROM FORM IS: {user_name}, {message}')
    data = (user_name, message)
    run_client(UDP_IP, UDP_PORT, data)



def run_client(ip, port, data):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.connect(server)
    username, message = data
    # sock.sendall(username.encode())
    # sock.sendall(message.encode())
    d_file = pickle.dumps((username, message))
    sock.sendall(d_file)



    while True:
        data =  sock.recv(1024)
        print(f'Received data from server {data.decode().lower()}')
        if not data:
            break
    sock.close()

# def send_static(self):
#     self.send_response(200)
#     mt = mimetypes.guess_type(self.path)
#     if mt:
#         self.send_header("Content-type", mt[0])
#     else:
#         self.send_header("Content-type", 'text/plain')
#     self.end_headers()
#     with open(f'.{self.path}', 'rb') as file:
#         self.wfile.write(file.read())

@app.route('/error')
def error():
    return render_template('error.html')


if __name__ =='__main__':
    app.run(debug=False)