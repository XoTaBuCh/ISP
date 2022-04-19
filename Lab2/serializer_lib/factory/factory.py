from serializer_lib.factory.parsers.json.ParserJson import ParserJson
from serializer_lib.factory.parsers.toml.ParserToml import ParserToml
from serializer_lib.factory.parsers.yaml.ParserYaml import ParserYaml


class Factory(object):

    @staticmethod
    def get_parser(pars_type: str):
        if pars_type.__eq__("json"):
            return ParserJson()
        elif pars_type.__eq__("toml"):
            return ParserToml()
        elif pars_type.__eq__("yaml"):
            return ParserYaml()
        else:
            pass
