import mimetypes
import pickle
import socket
import json
import datetime

UDP_IP = '127.0.0.1'
UDP_PORT = 5000

def run_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            d_data = pickle.loads(data)
            print(f'Received data: {d_data} from {address} ')
            user_name = d_data[0]
            message = d_data[1]
            time_now = str(datetime.datetime.now())
            print(time_now)
            user_dict = {}
            user_dict[time_now] = {}
            user_dict[time_now]['username'] = user_name
            user_dict[time_now]['message'] = message



            with open('./storage/data.json', 'a') as file:
                # json_obj = json.loads(f'{user_dict}')
                json.dump(user_dict, file)
            # sock.sendto(data, address)
            # print(f'Send data: {data.decode()}, to address: {address}')
    except KeyboardInterrupt:
        print('SERVER DESTROYED')
    finally:
        sock.close()
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


if __name__ == '__main__':
    run_server(UDP_IP, UDP_PORT)


