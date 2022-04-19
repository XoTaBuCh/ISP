import inspect
import re

from frozendict import frozendict

from serializer_lib.serialization.constants import *


class Serializer:

    def serialize(self, obj):
        obj_type = type(obj)
        obj_type_string = re.search(OBJECT_TYPE, str(obj_type)).group(1)
        result = {}

        if obj_type == dict:
            result = self.serialize_dict(obj)
        elif isinstance(obj, (int, float, complex, bool, str)) or obj is None:
            result = self.serialize_types(obj)
        elif obj_type == list or obj_type == tuple or obj_type == bytes:
            result = self.serialize_it(obj)
        elif inspect.isfunction(obj):
            result = self.serialize_function(obj)

        result[TYPE_FIELD] = obj_type_string
        fd = frozendict(result)

        return fd

    def deserialize(self, obj):

        pass

    def serialize_dict(self, obj: dict):
        result = {VALUE_FIELD: {}}

        for key, value in obj.items():
            result_key = self.serialize(key)
            result_value = self.serialize(value)
            result[VALUE_FIELD][result_key] = result_value

        return result

    def serialize_types(self, obj):
        result = {VALUE_FIELD: obj}

        return result

    def serialize_it(self, obj):
        result = {VALUE_FIELD: []}

        for value in obj:
            result[VALUE_FIELD].append(self.serialize(value))

        return result

    def serialize_function(self, obj):
        result = {VALUE_FIELD: {}}
        members = inspect.getmembers(obj)
        print(members)
        for member in members:
            if inspect.isbuiltin(members[1]):
                continue

        return result

    def serialize_class(self, obj):
        result = {VALUE_FIELD: {}}
