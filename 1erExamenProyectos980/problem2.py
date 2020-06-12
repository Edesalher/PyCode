"""
EDWING ESTUARDO ALVAREZ HERNÁNDEZ - 201602956
PROBLEMA #2:
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


n = 9183
result = []
result2 = 0
for num in range(2, n): # Se hace una lista de números desde el 2(que es el primer primo) hasta antes de n y se recorre
    if prime_factor(num):
        result.append(num)  # Cuando se cumple que el número es primo se agrega a la lista.
        result2 += num

print(f'Numeros primos inferiores a {n}: {result}') # Se muestra la lista de los números primos por debajo de n
print(f'Suma: {result2}') #Se imprime el resultado de la suma de todos los primos encontrados