"""
Hash files
encode() 		: convertir string a bytes.
hexdigest() 	: retorna la inforamción en formato hexadecimal.
"""

import hashlib


text = 'Texto de prueba'
result = hashlib.sha1(text.encode())
print('{} HASH={}'.format(text, result.hexdigest()))


# Hash file
content = None
with open('hash_this_file.txt', 'rb') as file:
    content = file.read()


# Equivalente: sha1sum <filename>
result = hashlib.sha1(content)
print('HASH del archivo: {}'.format(result.hexdigest()))
