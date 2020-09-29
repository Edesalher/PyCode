# -*- coding: utf-8 -*-
import sys
import socket
from ftplib import FTP, error_perm
import MikrotikApi2

def test_socket(host, port, socket_timeout):
	host_is_online = False
	try:
		socket_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_test.settimeout(socket_timeout)
		socket_test.connect((host, port))
		host_is_online = True
	except socket.error as e:
		e = str(e)
		if 'Errno 113' in e or 'timed out' in e:
			msg = 'HOST {} no responde'.format(host)
		elif'Errno 111' in e:
			msg = 'Puerto cerrado: {}'.format(port)
		else:
			msg = 'Ha ocurrido un error en la conexión'
		print('{}. (Error = "{}")'.format(msg, e))
	finally:
		socket_test.close()
	return host_is_online

# Autenticación
ROUTER_username = ''
ROUTER_password = ''

## Acceso
host = ''	# IP addr.
SOCKET_TIMEOUT = 3		# Segundos
PORT_API = 
PORT_FTP = 

## Nombre de backups
MIKROTIK_BACKUP_FILENAME = 'Redes_grupo_no.backup' 	# Dentro del Router
downloaded_file = 'Router.backup' 					# En nuentra computadora

# Comprobar que se puede realizar la conexión al Host y Port específicos
online_api = test_socket(host, PORT_API, SOCKET_TIMEOUT)
online_ftp = test_socket(host, PORT_FTP, SOCKET_TIMEOUT)


if online_api:
	#    
	# Conexion API MIKTROTIK
	# 
	socket_mikrotik = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_mikrotik.connect((host, PORT_API))
	mikrotik = MikrotikApi2.ApiRos(socket_mikrotik, debug=True)
	mikrotik.login(ROUTER_username, ROUTER_password)
	print('Login Router correcto.')
	mikrotik_response = mikrotik.talk(
		['/system/backup/save',
		 '=name={}'.format(MIKROTIK_BACKUP_FILENAME)]
	)
	try:
		# Cerrando conexion con el API. 
		# Este comando siempre genera una excepcion
		mikrotik.talk(['/quit'])
	except RuntimeError:
		pass
	print('Backup generado dentro del Router.')
else:
	sys.exit('No fue posible generar un backup dentro del Router.')

if online_ftp:
	#
	# Conexión FTP: generando cliente FTP
	# 
	try:
		ftp = FTP(host, timeout=6)
	except socket.error as e:
		print(e)

	try:                
		ftp.login(ROUTER_username, ROUTER_password)
	except error_perm, resp:
		resp = str(resp)
		if '530' in resp: # FTP Login Incorrecto
			print('¡Las credenciales son incorrectas!')
		else:
			print(resp)
			# raise
	except AttributeError as e:
		print(e, host)
	except socket.timeout as e:
		print('{} ftp.login timeout'.format(e), host)

	## Descargando el archivo de backup del Router a la computadora
	with open(downloaded_file, 'wb') as file:
		cmd = 'RETR {}'.format(MIKROTIK_BACKUP_FILENAME) # comando FTP
		print('ftp.retrbinary cmd={}'.format(cmd))
		try:
		# Se puede quedar colgado infitamente si no hay timeout en la conexion ftp
		# https://stackoverflow.com/a/19693709/4112006
			ftp.retrbinary(cmd=cmd, callback=file.write)
		except socket.timeout as e:
			e = str(e)
			msg = e + ' ftp.retrbinary no respondió'
			print(msg)

	# Cerrando conexión FTP
	try:
		ftp.quit()
	except Exception as e:
		pass
	print('Conexion FTP cerrada')

