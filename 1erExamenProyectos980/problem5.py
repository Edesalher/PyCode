'''
EDWING ESTUARDO ALVAREZ HERNÁNDEZ - 201602956
PROBLEMA #5:
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


numero_limite = 1904
numeros_perfectos = []
numero = 1
flag = True

while cant_abundantes :
    sumatoria = 0
    for divisor in own_dividers(numero): # Se recorre la lista de los divisores propios encontrado del numero.
        sumatoria += divisor
    if sumatoria != 1 and sumatoria == numero:    # "sumatoria != 1" es para evitar a los números primos.
        numeros_perfectos.append(numero)          # Si el número es perfecto se agrega a la lista.
        if numeros_perfectos[-1] > numero_limite:
            numeros_perfectos.pop()           # Si el último número agregado a la lista fué mayor a límite, se remueve.
            flag = False                      # Se baja la bandera para detener el ciclo del while
    numero += 1

print(f'Los números perfectos por debajo de {numero_limite} son: \n{str(numeros_perfectos)[1:-1]}')

suma = 0
for n in numeros_perfectos:  # Se recorre la lista de números perfectos y se suman.
    suma += n
print(f'La suma de todos los números perfectos por debajo de {numero_limite} es: \n{suma}')