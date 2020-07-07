from ecommerce.shipping import calc_shipping

calc_shipping()


class Mammal:
    def walk(self):
        print('walk')


class Dog(Mammal):
    pass


class Cat(Mammal):
    pass


dog1 = Dog()
dog1.walk()
