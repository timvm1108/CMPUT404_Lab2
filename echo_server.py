import socket, time

HOST = ''
PORT = 8081
BUFFER_SIZE = 2048

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((HOST,PORT))
        print("Starting TCP localhost Server on Port 8081")

        server_socket.listen(2)

        while True:

            # Accept incoming connection and send data back to client
            connection, address = server_socket.accept()
            print("Receiving Connection from:", address)
            data = connection.recv(BUFFER_SIZE)
            time.sleep(0.5)
            print("Sending Data:", data, "to", address)
            connection.sendall(data)

            connection.close()


if __name__ == '__main__':
    main()