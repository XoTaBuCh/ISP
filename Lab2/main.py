from serializer_lib.factory.parsers.json.ParserJson import ParserJson
from serializer_lib.serialization.serializer import Serializer
import math

class Aboba:
    name = "zalupa"
    count = 34.5

    #def aboba_print(self):
    #    print(self.name)

class Aboba2(Aboba):
    pass


def f(x=5, y=6):
    return math.sin(0)


def gfg(raise_power_to):

    def power(number):
        return number ** raise_power_to
    return power


if __name__ == '__main__':

    s = Serializer()
    sri = s.serialize({5:6, "dg":5})

    pj = ParserJson()
    print(pj.dumps(sri))

    #k_k = s.deserialize(s.serialize(f))(5, 6)
    #print(k_k)

