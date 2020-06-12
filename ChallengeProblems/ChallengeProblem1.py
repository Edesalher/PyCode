"""
PROBLEM #1:
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these
multiples is 23.
Find the sum of all the multiples of 3 or 5 below 1000.
"""


# This function checks if a number is a multiple of the indicated number(base).
def verify_multiple(number, base):
    if number % base == 0:
        return True
    else:
        return False


n = 1000
multiples = []
sumResult = 0
for num in range(1, n):
    if verify_multiple(num, 3):
        multiples.append(num)
        sumResult += num
    elif verify_multiple(num, 5):
        multiples.append(num)
        sumResult += num
print(f'The multiples of 3 and 5 below {n} are: \n {multiples}')
print(f'The sum of all the multiples is: \n {sumResult}')
