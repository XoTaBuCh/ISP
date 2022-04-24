from serializer_lib.factory.parsers.parser import Parser


class ParserJson(Parser):

    def dump(self, obj, file):  # obj to file
        result = self.dumps(obj)
        file.write(result)

    def dumps(self, obj):  # obj to string

        result = obj

    def load(self, file):  # file to obj

        pass

    def loads(self, string):  # string to obj

        pass
