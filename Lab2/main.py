
from serializer_lib.serialization.serializer import Serializer
from math import sin

class Aboba:
    name = "zalupa"
    count = 34.5

    #def aboba_print(self):
    #    print(self.name)

class Aboba2(Aboba):
    pass

c =42

def f(x, y):
    return sin(x*y*c)


def gfg(raise_power_to):

    def power(number):
        return number ** raise_power_to
    return power

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    s = Serializer()
    k_k = s.deserialize(s.serialize(f(5, 6)))
    print(k_k)

