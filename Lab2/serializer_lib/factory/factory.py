from serializer_lib.factory.parsers.constans import *
from serializer_lib.factory.parsers.json.ParserJson import ParserJson
from serializer_lib.factory.parsers.toml.ParserToml import ParserToml
from serializer_lib.factory.parsers.yaml.ParserYaml import ParserYaml


class Factory(object):

    @staticmethod
    def get_parser(pars_type: str):
        if pars_type.__eq__(JSON_NAME):
            return ParserJson()
        elif pars_type.__eq__(TOML_NAME):
            return ParserToml()
        elif pars_type.__eq__(YAML_NAME):
            return ParserYaml()
        else:
            return ParserYaml()
