#!usr/bin/env python3
import socket, sys

def create_socket():
    try:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print(f'Failed to create socket')
        sys.exit()
    print('Created Socket')
    return new_socket

        
def send_data(ssocket, data):
    try:
        ssocket.sendall(data.encode())
    except socket.error:
        print('Failed to send data')
        sys.exit()
    print("Sent Data")

def main():
    try:
        host = 'www.google.com'
        port = 80
        data = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
        buffer = 4096

        google_socket = create_socket()
        google_socket.connect((host, port))
        print (f'Socket Connected to {host} on {port}')

        send_data(google_socket, data)
        google_socket.shutdown(socket.SHUT_WR)

        final_data = b""

        while True:
            data = google_socket.recv(buffer)
            if not data:
                break
            final_data += data
        print(final_data)

    except Exception as e:
        print(e)
    finally:
        google_socket.close

if __name__ == '__main__':
    main()