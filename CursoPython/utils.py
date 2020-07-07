def find_max(numbers):
    maximum = numbers[0]
    for item in numbers:
        if item > maximum:
            maximum = item
    return maximum

