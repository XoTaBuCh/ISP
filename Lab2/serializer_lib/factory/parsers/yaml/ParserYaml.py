from yaml import UnsafeLoader

from serializer_lib.factory.parsers.parser import Parser
import yaml


class ParserYaml(Parser):

    def dump(self, obj, file):  # obj to file
        with open(file, "w") as f:
            f.write(self.dumps(obj))

    def dumps(self, obj):  # obj to string
        return yaml.dump(self.serializer.serialize(obj))

    def load(self, file):  # file to obj
        with open(file, "r") as f:
            return self.loads(f.read())

    def loads(self, string):  # string to obj
        return self.serializer.deserialize(yaml.load(string, Loader=UnsafeLoader))
