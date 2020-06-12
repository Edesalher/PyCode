"""
EDWING ESTUARDO ALVAREZ HERNÁNDEZ - 201602956
PROBLEMA #1
"""

n = 90
result1 = 0
result2 = 0
subtraction = 0

for number1 in range(1, n + 1): # Se genera una lista de números del 1 hasta n y se recorre.
    result1 += number1**2       # Cada número se eleva al cuadrado y la suma se va acumulando.

for number2 in range(1, n + 1): # Se genera una lista de número del 1 hasta n y se recorre.
    result2 += number2          # Se va acumulando la suma de todos los numeros.
result2 = result2**2            # Se eleva al cuadrado la suma acumulada.

subtraction = result2 - result1
print(result1)
print(result2)
print(f'Resultado de la resta: {subtraction}') # Se muestra la resta de los 2 resultados
