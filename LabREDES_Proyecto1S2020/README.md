# Telecomunicaciones y Redes Locales

* Conceptos
	* Sockets
	* SSH
		* Tuneles SSH
		* Criptogafia
	* FTP
* Mikrotik
	* Comandos básicos de Mikrotik
	* Generar backup
	* Utilizar el API de Mikrotik
* Python
	* Cliente FTP
	* Hash
	* Sockets TCP
	* Manejo de archivos

## Práctica de Laboratorio

Se les solita una pequeña aplicación que hecha en Python 2 o 3 en la cuál deben enviar comandos a un Router Mikrotik a través del API de Mikrotk, que esta conectado en un segmento de red. Deben solicitar al Router que realice un backup de la configuración que tenga en ese momento, se debe generar un archivo: **Redes_grupo_\#.backup** en la raiz del directorio del Servidor FTP.

Seguido deben utilizar un cliente FTP en Python que se conecte con dicho protocolo y descargue el archivo de \*.backup generado previamente. 

Por último deben obtener el HASH del archivo y reportarlo como se les indique.

*Buena suerte*