import socket

SERVER_IP   = '157.245.82.242'
SERVER_PORT = 9800
BUFFER_SIZE = 16 * 1024

# Se crea socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se conecta al puerto donde el servidor se encuentra a la escucha
server_address = (SERVER_IP, SERVER_PORT)
print('Conectando a {} en el puerto {}'.format(*server_address))
sock.connect(server_address)

try:

    # Se envia un texto codificado EN BINARIO
    # message = b'Este es un mensaje.  El texto se divide en bloques de BUFFER_SIZE bytes.'
    message = b'Estoy haciendo una prueba de conexion por TCP xD'
    print('\n\nEnviando el siguiente texto:  {!s}'.format(message))
    sock.sendall(message) #Se envia utilizando "socket.sendall"

    print("\n\n")

    # Esperamos la respuesta del ping servidor
    bytesRecibidos = 0
    bytesEsperados = len(message)

    #TCP envia por bloques de BUFFER_SIZE bytes
    while bytesRecibidos < bytesEsperados:
        data = sock.recv(BUFFER_SIZE)
        bytesRecibidos += len(data)
        print('Recibido: {!s}'.format(data))

finally:
    print('\n\nConexion finalizada con el servidor')
    sock.close()