"""
Ejemplo socket
"""

import socket


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


if __name__ == '__main__':
    HOST = 'google.com'
    PORT = 443

    online = test_socket(host=HOST, port=PORT, socket_timeout=3)
    if online:
        print('Host {} con puerto {} esta activo'.format(HOST, PORT))
    else:
        print('Host {} con puerto {} esta inactivo'.format(HOST, PORT))
    # print(socket.gethostbyname(HOST))
    # # reverse lookup for a domain’s name
    # print(socket.gethostbyaddr(HOST))
