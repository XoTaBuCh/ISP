from yaml import UnsafeLoader

from serializer_lib.factory.parsers.parser import Parser
import yaml


class ParserYaml(Parser):

    def dump(self, obj, file):  # obj to file
        file.write(yaml.dump(obj))

    def dumps(self, obj):  # obj to string
        return yaml.dump(obj)

    def load(self, file):  # file to obj
        return yaml.load(file.read(), Loader=UnsafeLoader)

    def loads(self, string):  # string to obj
        return yaml.load(string, Loader=UnsafeLoader)
