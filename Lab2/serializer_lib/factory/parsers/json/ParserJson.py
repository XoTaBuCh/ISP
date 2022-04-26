from frozendict import frozendict

from serializer_lib.factory.parsers.parser import Parser


class ParserJson(Parser):

    def dump(self, obj, file):  # obj to file
        result = self.dumps(obj)
        file.write(result)

    def dumps(self, obj):  # obj to string
        ans = ""
        serialized = []
        if type(obj) == frozendict or type(obj) == dict:
            ans = "{"
            for key, value in obj.items():
                serialized.append("(" + self.dumps(key) + "): " + self.dumps(value))
            ans += ", ".join(serialized)
            ans += "}"
            return f"{ans}"
        elif type(obj) == list:
            serialized = []
            for i in obj:
                serialized.append(f"{self.dumps(i)}")
            ans = ", ".join(serialized)
            return f"[{ans}]"
        else:
            return f"\"{str(obj)}\""


    def load(self, file):  # file to obj

        pass

    def loads(self, string):  # string to obj

        pass
