import inspect
import re

from frozendict import frozendict

from serializer_lib.serialization.constants import *


class Serializer:

    def serialize(self, obj):
        obj_type = type(obj)
        result = {}

        if inspect.isclass(obj):
            result = self.serialize_class(obj)
            obj_type_string = CLASS_NAME
        else:
            obj_type_string = re.search(OBJECT_TYPE, str(obj_type)).group(1)

            if obj_type == dict:
                result = self.serialize_dict(obj)
            elif isinstance(obj, (int, float, complex, bool, str)) or obj is None:
                result = self.serialize_types(obj)
            elif obj_type == list or obj_type == tuple or obj_type == bytes:
                result = self.serialize_it(obj)
            elif inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, staticmethod):
                result = self.serialize_function(obj)
            elif inspect.ismodule(obj) or inspect.isbuiltin(obj) or inspect.iscode(obj):
                result = self.serialize_instance(obj)
            elif hasattr(obj, "__dict__"):
                result = self.serialize_object(obj)

        result[TYPE_FIELD] = obj_type_string
        fd = frozendict(result)

        return fd

    def deserialize(self, obj: dict):
        obj_type_string = obj[TYPE_FIELD]

        result = object

        if obj_type_string == DICTIONARY_NAME:
            result = self.deserialize_dict(obj)
        elif obj_type_string in TYPES_NAMES:
            result = self.deserialize_types(obj)
        elif obj_type_string == FUNCTION_NAME:
            result = self.deserialize_function(obj)

        return result

    def serialize_dict(self, obj: dict):
        result = {VALUE_FIELD: {}}

        for key, value in obj.items():
            result_key = self.serialize(key)
            result_value = self.serialize(value)
            result[VALUE_FIELD][result_key] = result_value

        return result

    def deserialize_dict(self, obj: dict):
        result = {}

        for key, value in obj[VALUE_FIELD].items():
            result_key = self.deserialize(key)
            result_value = self.deserialize(value)
            result[result_key] = result_value

        return result

    def serialize_types(self, obj):
        result = {VALUE_FIELD: obj}

        return result

    def deserialize_types(self, obj):
        result = object

        if obj[TYPE_FIELD] == TYPES_NAMES[3]:
            result = (obj[VALUE_FIELD] == "True")
        else:
            result = obj[VALUE_FIELD]

        return result

    def serialize_it(self, obj):
        result = {VALUE_FIELD: []}

        for value in obj:
            result[VALUE_FIELD].append(self.serialize(value))

        return result

    def deserialize_it(self, obj):
        result = []

        for value in obj[VALUE_FIELD]:
            result_value = self.deserialize(value)
            result.append(result_value)

        if obj[TYPE_FIELD] == ITERABLE_NAMES[0]:
            result = result
        elif obj[TYPE_FIELD] == ITERABLE_NAMES[1]:
            result = tuple(result)
        elif obj[TYPE_FIELD] == ITERABLE_NAMES[2]:
            result = bytes(result)

        return result

    def serialize_function(self, obj):
        result = {VALUE_FIELD: {}}
        members = []

        for member in inspect.getmembers(obj):
            if member[0] in FUNCTION_ATTRIBUTES_NAMES:
                members.append(member)

        for key, value in members:
            result_key = self.serialize(key)
            result_value = self.serialize(value)
            result[VALUE_FIELD][result_key] = result_value

            if key == CODE_FIELD:
                global_key = self.serialize(GLOBAL_FIELD)
                result[VALUE_FIELD][global_key] = {}

                global_attributes = obj.__getattribute__(GLOBAL_FIELD)

                for attribute in value.__getattribute__(GLOBALS_FIELD):
                    result_attribute = self.serialize(attribute)

                    if attribute == obj.__name__:
                        result[VALUE_FIELD][global_key][result_attribute] = self.serialize(obj.__name__)
                    elif attribute in global_attributes:
                        if inspect.ismodule(global_attributes[attribute]) and attribute in __builtins__:
                            continue
                        result[VALUE_FIELD][global_key][result_attribute] = self.serialize(global_attributes[attribute])

        return result

    def deserialize_function(self, obj):
        result = object

        for key, value in obj.items():
            result_key = self.deserialize(key)
            result_value = self.deserialize(value)

        return result

    def serialize_class(self, obj):
        result = {VALUE_FIELD: {}}
        result[VALUE_FIELD][self.serialize(NAME_FIELD)] = self.serialize(obj.__name__)
        members = []

        for member in inspect.getmembers(obj):
            if not (member[0] in CLASS_ATTRIBUTES_NAMES):
                members.append(member)

        for key, value in members:
            result_key = self.serialize(key)
            result_value = self.serialize(value)
            result[VALUE_FIELD][result_key] = result_value

        return result

    def deserialize_class(self, obj):
        pass

    def serialize_instance(self, obj):
        result = {VALUE_FIELD: {}}
        members = []

        for member in inspect.getmembers(obj):
            if not callable(member[1]):
                members.append(member)

        for key, value in members:
            result_key = self.serialize(key)
            result_value = self.serialize(value)
            result[VALUE_FIELD][result_key] = result_value

        return result

    def deserialize_instance(self, obj):
        pass

    def serialize_object(self, obj):
        result = {VALUE_FIELD: {}}
        for attribute in dir(obj):
            if not attribute.startswith("__"):
                result_attribute = self.serialize(attribute)
                result_value = self.serialize(getattr(obj, attribute))
                result[VALUE_FIELD][result_attribute] = result_value

        return result

    def deserialize_object(self, obj):
        pass
