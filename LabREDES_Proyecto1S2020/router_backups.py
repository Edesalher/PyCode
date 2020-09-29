"""
Script for connection to MK Router.
Default ports
winbox  8291
api     8728
www     80
ftp     21
Práctica de Laboratorio de ejemplo.
"""

import os
import sys
import socket
from ftplib import FTP, error_perm
from MikrotikApi3 import ApiRos


username = ''
password = ''
HOST = ''
MK_API_PORT = 8728
PORT_FTP = 21
SOCKET_TIMEOUT = 6
MIKROTIK_BACKUP_FOLDER = 'backups'
BACKUP_NAME = '<carnet>'
filename = os.path.join(MIKROTIK_BACKUP_FOLDER, BACKUP_NAME)

# Open FTP connection
try:
    ftp = FTP(timeout=SOCKET_TIMEOUT)
    ftp.connect(HOST, PORT_FTP)
    ftp.login(username, password)
except error_perm as e:
    if '530' in str(e):
        sys.exit('FTP username or password failed! closing.')
    else:
        raise
except socket.timeout:
    sys.exit('Timeout. No FTP responses!')
else:
    if MIKROTIK_BACKUP_FOLDER not in ftp.nlst():
        ftp.mkd(MIKROTIK_BACKUP_FOLDER)
        print('Creating folder in Mikrotik FTP Server')
    else:
        print('Folder exists. Skipping.')

# Api connection
try:
    socket_api = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_api.settimeout(SOCKET_TIMEOUT)
    socket_api.connect((HOST, MK_API_PORT))
    mk_api = ApiRos(socket_api)
    mk_api.login(username, password)
    # mk_api.talk(['/queue/simple/print'])
    mk_api.talk(['/system/backup/save', f'=name={filename}'])
except socket.error:
    raise
finally:
    socket_api.close()

# Download and save Backup
with open(f'{BACKUP_NAME}.backup', 'wb') as f:
    cmd = f'RETR {filename}.backup'
    try:
        ftp.retrbinary(cmd=cmd, callback=f.write)
    except socket.timeout:
        print('Error. Get and donwload backup has failed.')
    finally:
        ftp.quit()
