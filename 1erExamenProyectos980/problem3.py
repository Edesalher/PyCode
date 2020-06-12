"""
EDWING ESTUARDO ALVAREZ HERNÁNDEZ - 201602956
PROBLEMA #3:
"""

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

# Función que determina si un número cualquiera es primo o no.
def prime_factor(number):
    sum_result = 0
    for dividers in own_dividers(number): # Se recorre la lista de divisores propios del número
        sum_result += dividers        # Se suman todos los divosores. La suma será uno solo cuando el número sea propio.
    if sum_result == 1:
        return True
    else:
        return False


posicion_de_primo_a_encontrar = 713
result = []
cant_primos = 0
numero_a_probar = 2

# Se hace una lista de números desde el 2(que es el primer primo) hasta antes de n y se recorre
while cant_primos < posicion_de_primo_a_encontrar: # El proceso termina cuando se alcanza la cant. de primos buscada.
    if prime_factor(numero_a_probar):
        result.append(numero_a_probar)  # Cuando se cumple que el número es primo se agrega a la lista.
        cant_primos += 1                # Cuando se agrega un primo nuevo se cuenta.
    numero_a_probar += 1                # Se cambia el siguiente número a probar.

print(f'Numeros primos encontrados: {result}')
print(f'El {posicion_de_primo_a_encontrar}-ésimo número primo es: {result[posicion_de_primo_a_encontrar - 1]}')