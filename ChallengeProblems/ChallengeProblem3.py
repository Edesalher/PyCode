"""
PROBLEMA #3:
The prime factors of 13195 are 5, 7, 13 and 29.
What is the largest prime factor of the number 600851475143 ?
"""


def own_dividers(number):
    dividers = []
    divider = 1
    while divider < number:
        if (number % divider) == 0:
            dividers.append(divider)
        divider += 1
    return dividers


def prime_factor(number):
    sum_result = 0
    for dividers in own_dividers(number):
        sum_result += dividers
    if sum_result == 1:
        return True
    else:
        return False


n = 600851475143
list_of_prime_factors = []
for num in own_dividers(n):
    if prime_factor(num):
        list_of_prime_factors.append(num)

print(f'The prime factors of {n} are: \n {list_of_prime_factors}')
