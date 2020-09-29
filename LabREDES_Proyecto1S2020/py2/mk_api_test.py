# -*- coding: utf-8 -*-
#

#
# Univesidad de San Carlos de Guatemala
# Facultad de Ingenieria
# Telecomunicaciones y Redes Locales (969)
# Laboratorio de Electrónica
# Ing. Rodrigo de León
#

#
# Ejemplo de uso de Mk API
#



import socket
import MikrotikApi2

MK_API_PORT =   # Default Port
SOCKET_TIMEOUT = 2	# Second
host = ''
credentials = {
	'user': '',
	'pass': ''
}
debug = True	## Print in console strout from router


## Variables
HOST_IS_ALIVE = None
PORT_IS_OPEN = None
socket_test = None

try:
	sk_test_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sk_test_conn.settimeout(SOCKET_TIMEOUT)
	sk_test_conn.connect((host, MK_API_PORT))
	HOST_IS_ALIVE = True
	PORT_IS_OPEN = True
	socket_test = True
except socket.error as socket_error:
	socket_error = str(socket_error)
	if('timed out' in socket_error or 'Errno 113' in socket_error):
		HOST_IS_ALIVE = False
	elif('Errno 111' in socket_error):
		PORT_IS_OPEN = False
except TypeError:
	INVALID_HOST = True
finally:
	sk_test_conn.close()

print('HOST_IS_ALIVE: {}'.format(HOST_IS_ALIVE))
print('PORT_IS_OPEN: {}'.format(PORT_IS_OPEN))
print('socket_test: {}'.format(socket_test))

### Mikrotik Connection
if socket_test:
	socket_api = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_api.settimeout(SOCKET_TIMEOUT)
	socket_api.connect((host, MK_API_PORT))
	mk_api = MikrotikApi2.ApiRos(socket_api, debug=debug)					
	mk_conn = mk_api.login(credentials['user'], credentials['pass'])

	# mk_response = mk_api.talk(['/queue/simple/print'])

	mk_api.talk([
		# '/ip/address/print'
		# '/user/print'
		# '/snmp/print'
		'/ip/service/print'
	])
