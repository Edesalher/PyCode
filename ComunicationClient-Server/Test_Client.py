import socket

host = 'localhost'  #Dirección IP del host servidor
port = 9091  #Número de puerto de comunicación

My_PC = socket.socket()  #Creación de objeto socket (lado cliente).

My_PC.connect((host, port))  #Conexión con el servidor.
print('CONECTADO AL SERVIDOR!')
print()

while True:
    Envio_mensaje = input('Mensaje desde My_PC al servidor >> ')  #Entrada de datos para que cliente envíe mensajes.
    #Envio_mensaje = 'Hola desde el Cliente'  #Mensaje que envía el cliente.
    My_PC.send(Envio_mensaje.encode())  #Se envía el mensaje al servidor.

    Respuesta_servidor = My_PC.recv(1024)  #Se recibe la respuesta del servidor.
    print('Servidor responde >> ' + Respuesta_servidor.decode())

#My_PC.close()  #Se cierra la instancia de objeto servidor.
print('SE CERRÓ LA CONEXIÓN')  #Se cierra la conexión.
