from serializer_lib.factory.parsers.parser import Parser
from toml import dumps, loads


class ParserToml(Parser):

    def dump(self, obj, file):  # obj to file
        with open(file, "w") as f:
            f.write(self.dumps(obj))

    def dumps(self, obj):  # obj to string
        result = dumps(self.serializer.serialize(obj))
        return result

    def load(self, file):  # file to obj
        with open(file, "r") as f:
            return self.loads(f.read())

    def loads(self, string):  # string to obj
        return self.serializer.deserialize(loads(string))
