'''
EDWING ESTUARDO ALVAREZ HERNÁNDEZ - 201602956
PROBLEMA #4:
'''


# Función que encuentra todos los divisores propios de un cualquier número.
# Si el número es primo entonces la función va retornar una lista que tiene solo al número 1.
def own_dividers(number):
    dividers = []
    divider = 1
    while divider < number:          # El proceso termina cuando divider se igual al número en análisis
        if (number % divider) == 0:  # Se verifica si divider es divisor de el número
            dividers.append(divider) # Si es divisor lo agrega a la lista de sus divisores propios.
        divider += 1                 # Se aumenta el valor de divider a probar.
    return dividers


pos_abundante_a_encontrar = 713
numeros_abundantes = []
n = 1
cant_abundantes = 0

# El proceso termina cuando se alcanza la posición n-ésima de interés.
while cant_abundantes < pos_abundante_a_encontrar:
    suma = 0
    for num in own_dividers(n): # Se ecuentran los divisores propios de n y se suman.
        suma += num
    if suma > n:
        numeros_abundantes.append(n) # Si se cumple que el número es abundante se agrega a la lista.
        cant_abundantes += 1         # Se aumenta la cantidad de abundantes encontrados.
    n += 1                           # Se establece el sig. número a trabajar.

print(f'Los números abundantes encontrados son: \n{str(numeros_abundantes)[1:-1]}')
print(f'El {pos_abundante_a_encontrar}-ésimo número abundante es: {numeros_abundantes[pos_abundante_a_encontrar - 1]}')