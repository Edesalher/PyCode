# import converters
from converters import kg_to_lbs
from utils import find_max


class Person:
    def __init__(self, name):
        self.name = name

    def talk(self):
        print(f'Hello! I am {self.name}')


girl = Person('Emma')
boy = Person('John')
girl.talk()
boy.talk()

print(kg_to_lbs(70))

numbers = [10, 3, 23, 2]
print(find_max(numbers))
