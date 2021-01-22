#!usr/bin/env python3
from multiprocessing import Pool
import socket

def connect(address):
    try:
        host = address[0]
        end_host = 'www.google.com'
        port = address[1]
        data = f'GET / HTTP/1.0\r\nHost: {end_host}\r\n\r\n'
        buffer = 4096

        google_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        google_socket.connect((host, port))
        print (f'Socket Connected to {host} on {port}')

        google_socket.sendall(data.encode())

        print("Sent Request to Server")
        google_socket.shutdown(socket.SHUT_WR)

        final_data = b""

        while True:
            data = google_socket.recv(buffer)
            if not data:
                break
            final_data += data
        print("Received Return Message")

    except Exception as e:
        print(e)
    finally:
        google_socket.close

def main():

    address = [('localhost', 8081)]

    # Set up 10 instances of the connect method to send requests to server
    with Pool() as p:
        p.map(connect, address * 10)

if __name__ == '__main__':
    main()