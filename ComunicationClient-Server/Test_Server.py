import socket

host = 'localhost'  #Dirección IP del host servidor
port = 9091  #Número de puerto de comunicación

My_Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Creación de objeto socket (lado servidor).

My_Server.bind((host, port))  #Vinculación de socket con dirección a conectarse.
My_Server.listen(1)  #Se inicia el servidor como oyente.

cliente, address = My_Server.accept() #Instanciamos un objeto cliente para recibir datos (socket cliente).
                                      #Acepta pasivamente conexión del cliente, esperando hasta que la conexión llegue.
print('NUEVA CONEXIÓN ESTABLECIDA!')
print('Recibo conexión de la IP: ' + str(address[0]) + ', Puerto ' + str(address[1]))
print()

while True:
    Recibo_mensaje = cliente.recv(1024)  #Se recibe el mensaje del cliente.
    #print('Recibo conexión de la IP: ' + str(address[0]) + ', Puerto ' + str(address[1]))
    print('Cliente envía >> ' + Recibo_mensaje.decode())

    Respondo_cliente = input('Respuesta desde servidor al cliente >> ')
    cliente.send(Respondo_cliente.encode())  #Se envía la respuesta al cliente.

    #cliente.close()
    #print('CONEXIÓN CERRADA')
