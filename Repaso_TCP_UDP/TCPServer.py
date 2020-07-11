# Implementation of a basic server with TCP.

import socket

IP_ADDRESS = 'localhost'  # The IP where the server wants to get up.
IP_PORT = 8080            # The port to which clients should connect.
BUFFER_SIZE = 16 * 1024   # 16KB blocks.

# Creating a socket using IPv4 for TCP.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP and port.
server_address = (IP_ADDRESS, IP_PORT)
print(f'Starting up server {IP_ADDRESS} on port {IP_PORT}')
server_socket.bind(server_address)

# Enables server listening on the indicated interfaces.
# It will accept only one queued client.
server_socket.listen(1)

while True:
    print('Waiting for a connection...')
    connection, client_address = server_socket.accept()
    try:
        print(f'Connection established from {client_address}\n')

        # The data is received in small pieces and then it is retransmitted to the client.
        while True:
            data = connection.recv(BUFFER_SIZE)
            # The data is decoded to string.
            data = data.decode()
            print(f'Received: {data}')
            # if data is received, which means the client is still send the message.
            if data:
                print('Sending data back to the client')
                # The data is encoded.
                data = data.encode()
                connection.sendall(data)
            else:
                print(f'\nTransmission completed from the client {client_address}\n\n')
                break
    except KeyboardInterrupt:
        server_socket.close()  # The server is shut down.
    finally:
        print('Connecton close')
        connection.close()     # The connection with the client is ended.
