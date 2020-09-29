"""
Ejemplo conceptual
FTP Client
"""

import sys
import socket
from ftplib import FTP, error_perm


# Autenticación
username = ''
password = ''
HOST = ''
PORT_FTP = 21

# FTP
# NLST:	Returns a list of f names in a specified directory.
# https://en.wikipedia.org/wiki/List_of_FTP_commands


try:
    ftp = FTP(timeout=6)
    ftp.connect(HOST, PORT_FTP)
    ftp.login(username, password)
    files = ftp.nlst('backups')  # Files inside backups folder
    ftp.quit()
except error_perm as e:
    e = str(e)
    if '530' in e:
        sys.exit('¡Las credenciales son incorrectas!')
    elif '550' in e:
        sys.exit('No existe el directorio en el servidor')
    else:
        raise
except socket.timeout:
    sys.exit('Timeout!')

for f in files:
    print('- ' + f)
