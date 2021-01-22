#!usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

HOST = ''
PORT = 8081
BUFFER_SIZE = 2048

def handle_request(connection, address):
    data = connection.recv(BUFFER_SIZE)
    
    print(data)

    time.sleep(0.5)
    connection.sendall(data)
    connection.shutdown(socket.SHUT_RDWR)
    connection.close()
    
    print("Sent Data Back to", address)

def main():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((HOST,PORT))
        print("Starting TCP localhost Server on Port 8081")

        server_socket.listen(2)

        while True:

            connection, address = server_socket.accept()
            print("Receiving Connection from:", address)
            
            # Start a process for each incoming request to send data back
            p = Process(target=handle_request, args=(connection, address))
            p.daemon = True
            p.start()
            print("Started new Process", p) 
                

if __name__ == '__main__':
    main()