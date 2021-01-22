#!usr/bin/env python3
import socket, time

HOST = ''
END_HOST = 'www.google.com'
PORT = 8081
END_PORT = 80
BUFFER_SIZE = 2048

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((HOST,PORT))
        print("Starting TCP localhost Server on Port 8081")

        server_socket.listen(2)

        while True:
            
            # Receive connection from client
            connection, address = server_socket.accept()
            print("Receiving Connection from:", address)
            data = connection.recv(BUFFER_SIZE)

            # Set up TCP socket for sending request to Google, and sends the request
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print(f"Connecting to {END_HOST}")

                proxy_end.connect((END_HOST, END_PORT))
                print(f"Connected to {END_HOST} and Sending Data")

                proxy_end.sendall(data)

                proxy_end.shutdown(socket.SHUT_WR)
                
                end_data = b""

                while True:
                    data = proxy_end.recv(BUFFER_SIZE)
                    if not data:
                        break
                    end_data += data
                
                print(f"Received Data from {END_HOST}")
                print(end_data)

            # Send what is received from Google back to client.
            time.sleep(0.5)
            connection.sendall(end_data)
            
            print("Sent Data Back to", address)

            connection.close()


if __name__ == '__main__':
    main()