from serializer_lib.factory.parsers.parser import Parser
from salt.serializers.toml import serialize, deserialize
from tomli_w import dumps

class ParserToml(Parser):

    def dump(self, obj, file):  # obj to file
        file.write(dumps(obj))

    def dumps(self, obj):  # obj to string
        return dumps(obj)

    def load(self, file):  # file to obj
        return deserialize(file.read())

    def loads(self, string):  # string to obj
        return deserialize(string)
