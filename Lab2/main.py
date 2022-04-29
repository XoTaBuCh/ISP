from frozendict import frozendict

from serializer_lib.factory.parsers.json.ParserJson import ParserJson
from serializer_lib.factory.parsers.yaml.ParserYaml import ParserYaml
from serializer_lib.factory.parsers.toml.ParserToml import ParserToml

from serializer_lib.serialization.serializer import Serializer
import math
from math import sin


class Aboba:
    name = "zalupa"
    count = 34.5

    #def aboba_print(self):
    #    print(self.name)

class Aboba2(Aboba):
    pass


def f(x=5, y=6):
    return sin(x*y)


def gfg(raise_power_to):

    def power(number):
        return number ** raise_power_to
    return power


if __name__ == '__main__':


    s = Serializer()
    sri = s.serialize({(4, 7): 8})
    sri2 = s.serialize([4, 6])
    sri3 = s.serialize(5)

    pj = ParserJson()
    print(pj.dumps(sri))
    print(pj.dumps(sri2))

    #print(pj.dumps(sri2))
    print(pj.dumps(sri3))

    print(pj.loads(pj.dumps(sri)))
    print(sri)

    #print(sin.__module__)
    #k_k = s.deserialize(s.serialize(f))(5, 6)
    #print(k_k)

