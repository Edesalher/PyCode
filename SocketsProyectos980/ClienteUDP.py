import socket

SERVER_ADDRESS = '157.245.82.242'
SERVER_PORT = 9800

#BUFFER_SIZE = 16 #Si BUFFER_SIZE es menor al mensaje, este se corta
BUFFER_SIZE = 4096 #Usamos buffer de 4KB



# Se crea el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Tupla de config. del servidor a quien se envia (y recibe de) la info
serverAddress = (SERVER_ADDRESS, SERVER_PORT)
message = 'Este mensaje se transmite del cliente al servidor. \
 Se espera sea devuelto de regreso: UDP no es un protocolo confiable, \
 pero para aplicaciones que toleran paquetes perdidos, funciona bien.'

message = message.encode() #Se convierte de str a bytes


try:

    # Se manda la data directamente (sin realizar una conexión directa al server)
    print('\nEnviando:  {!r}'.format(message))
    sent = sock.sendto(message, serverAddress)

    # Se espera respuesta de vuelta
    print('\nEsperando recepcion de vuelta...\n')
    data, server = sock.recvfrom(BUFFER_SIZE)
    print('\nRecibido: {!r}\n\n'.format(data))

finally:
    print('Cerrando socket')
    sock.close()