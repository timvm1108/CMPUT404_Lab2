import socket, time, sys
from multiprocessing import Process

HOST = ''
END_HOST = 'www.google.com'
PORT = 8081
END_PORT = 80
BUFFER_SIZE = 2048

def handle_request(connection, address, proxy_end):
    data = connection.recv(BUFFER_SIZE)

    proxy_end.sendall(data)

    proxy_end.shutdown(socket.SHUT_WR)
    
    end_data = b""

    while True:
        data = proxy_end.recv(BUFFER_SIZE)
        if not data:
            break
        end_data += data
    
    print(f"Received Data from {END_HOST}")

    time.sleep(0.5)
    connection.sendall(end_data)
    
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
            

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print(f"Connecting to {END_HOST}")

                proxy_end.connect((END_HOST, END_PORT))
                print(f"Connected to {END_HOST} and Sending Data")

                # Start a process for each incoming connection with the correct arguments
                p = Process(target=handle_request, args=(connection, address, proxy_end))
                p.daemon = True
                p.start()
                print("Started new Process", p) 
                

            connection.close()

if __name__ == '__main__':
    main()