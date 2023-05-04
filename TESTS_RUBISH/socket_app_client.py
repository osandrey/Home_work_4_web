import socket


UDP_IP = 'localhost'
UDP_PORT = 5000

def run_client(ip, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.connect(server)
    sock.sendall(b'TEST')
    sock.sendall(b'ANDRII')

    while True:
        data =  sock.recv(1024)
        print(f'Received data from server {data.decode().lower()}')
        if not data:
            break



    sock.close()

if __name__ == '__main__':
    run_client(UDP_IP, UDP_PORT)


