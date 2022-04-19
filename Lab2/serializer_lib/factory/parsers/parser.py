from abc import ABC, abstractmethod
from serializer_lib.serialization.serializer import Serializer


class Parser(ABC):

    def __init__(self):
        self.serializer = Serializer()

    @abstractmethod
    def dump(self, obj, file):  # obj to file

        pass

    @abstractmethod
    def dumps(self, obj):  # obj to string

        pass

    @abstractmethod
    def load(self, file):  # file to obj

        pass

    @abstractmethod
    def loads(self, string):  # string to obj

        pass
