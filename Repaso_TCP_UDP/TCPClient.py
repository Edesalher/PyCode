# Implementation of a basic client with TCP.

import socket

SERVER_IP = 'localhost'       # The IP to which the client will connect.
SERVER_PORT = 8080            # The port to which the client will connect.
BUFFER_SIZE = 16 * 1024      # 16KB blocks.

# Creating a socket using IPv4 for TCP.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting the socket to the port where the server is listening.
server_address = (SERVER_IP, SERVER_PORT)
print(f'Connecting to {SERVER_IP} on port {SERVER_PORT}\n\n')
client_socket.connect(server_address)

try:
    message = input('>')
    # message = 'My name is Edwing Alvarez.'
    print(f'Sending the following data: {message}\n')
    # A binary encoded text is sent.
    message = message.encode()
    client_socket.sendall(message)

    # A response is expected from the server, therefore the data is received.
    bytes_received = 0
    bytes_expected = len(message)
    message_received = ''
    while bytes_received < bytes_expected:
        data = client_socket.recv(BUFFER_SIZE)
        bytes_received += len(data)
        # The data is decoded to string.
        data = data.decode()
        print(f'Receiving: {data}')
        message_received += data

    print(f'\nMessage received: {message_received}\n\n')  # The full message is displayed.
finally:
    print('Connection ended with the server.')
    client_socket.close()

