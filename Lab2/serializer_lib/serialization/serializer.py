import inspect
import re
from types import CodeType, FunctionType

from frozendict import frozendict

from serializer_lib.serialization.constants import *


class Serializer:

    def serialize(self, obj):
        result = {}

        if inspect.isclass(obj):
            result = self.serialize_class(obj)
            obj_type_string = CLASS_NAME
        else:
            obj_type = type(obj)
            obj_type_string = re.search(OBJECT_TYPE, str(obj_type)).group(1)
            print(str(obj_type))

            if obj_type == dict:
                result = self.serialize_dict(obj)
            elif isinstance(obj, (int, float, complex, bool, str, type(None))) or obj is None:
                result = self.serialize_types(obj)
            elif obj_type == list or obj_type == tuple or obj_type == bytes:
                result = self.serialize_it(obj)
            elif inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, staticmethod):
                result = self.serialize_function(obj)
            elif inspect.ismodule(obj) or inspect.isbuiltin(obj) or inspect.iscode(obj) or inspect.ismethoddescriptor(obj):
                result = self.serialize_instance(obj)
            elif hasattr(obj, "__dict__"):
                result = self.serialize_object(obj)
            else:
                result = self.serialize_instance(obj)

        result[TYPE_FIELD] = obj_type_string
        fd = frozendict(result)

        return fd

    def deserialize(self, obj: dict):
        try:
            obj_type_string = obj[TYPE_FIELD]
        except:
            print("Type cannot be found!")

        result = object

        if obj_type_string == DICTIONARY_NAME:
            result = self.deserialize_dict(obj)
        elif obj_type_string in TYPES_NAMES:
            result = self.deserialize_types(obj)
        elif obj_type_string in ITERABLE_NAMES:
            result = self.deserialize_it(obj)
        elif obj_type_string == FUNCTION_NAME:
            result = self.deserialize_function(obj)
        elif obj_type_string == CLASS_NAME:
            result = self.deserialize_class(obj)
        elif obj_type_string == OBJECT_NAME:
            result = self.deserialize_object(obj)

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
        elif obj[TYPE_FIELD] == TYPES_NAMES[5]:
            result = None
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
        if inspect.ismethod(obj):
            obj = obj.__func__

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

                for attribute in value.__getattribute__(CO_NAMES_FIELD):
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
        function_arguments = []
        code_arguments = []
        global_arguments = {"__builtins__": __builtins__}

        for key in FUNCTION_CREATE_ATTRIBUTES_NAMES:
            value = obj[VALUE_FIELD][self.serialize(key)]

            if key == CODE_FIELD:
                for argument_key in CODE_ARGS:
                    result_argument_value = self.deserialize(obj[VALUE_FIELD][self.serialize(CODE_FIELD)]
                                                             [VALUE_FIELD][self.serialize(argument_key)])
                    code_arguments.append(result_argument_value)

                function_arguments = [CodeType(*code_arguments)]

            elif key == GLOBAL_FIELD:
                for argument_key, argument_value in obj[VALUE_FIELD][self.serialize(GLOBAL_FIELD)].items():
                    global_arguments[self.deserialize(argument_key)] = self.deserialize(argument_value)
                function_arguments.append(global_arguments)

            else:
                function_arguments.append(self.deserialize(value))

        result = FunctionType(*function_arguments)

        if result.__name__ in result.__getattribute__(GLOBAL_FIELD):
            result.__getattribute__(GLOBAL_FIELD)[result.__name__] = result

        return result

    def serialize_class(self, obj):
        result = {VALUE_FIELD: {}}
        members = []
        bases = []

        for base in obj.__bases__:
            if obj.__name__ != OBJECT_NAME:
                bases.append(self.serialize(base))
        result[VALUE_FIELD][self.serialize(BASE_NAME)] = self.serialize(bases)

        for member in inspect.getmembers(obj):
            if member[0] != CLASS_ATTRIBUTE_NAME:
                members.append(member)

        result_data = self.serialize(DATA_NAME)
        result[VALUE_FIELD][result_data] = {}

        result[VALUE_FIELD][result_data][self.serialize(NAME_FIELD)] = self.serialize(obj.__name__)

        for key, value in members:
            result_key = self.serialize(key)
            result_value = self.serialize(value)
            result[VALUE_FIELD][result_data][result_key] = result_value

        return result

    def deserialize_class(self, obj):
        result = {}
        result_data = self.serialize(DATA_NAME)

        result_bases = tuple(self.deserialize(obj[VALUE_FIELD][self.serialize(BASE_NAME)]))

        for key, value in obj[VALUE_FIELD][result_data].items():
            result_key = self.deserialize(key)
            result_value = self.deserialize(value)
            result[result_key] = result_value
        print(result_bases)
        return type(result[NAME_FIELD], result_bases, result)

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
        obj_type = type(obj)

        for attribute, value in obj.__dict__.items():
            result_attribute = self.serialize(attribute)
            result_value = self.serialize(value)
            result[VALUE_FIELD][result_attribute] = result_value

        result[VALUE_FIELD][self.serialize(TYPE_FIELD)] = self.serialize(obj_type)
        return result

    def deserialize_object(self, obj):
        result = object

        result = self.deserialize(obj[VALUE_FIELD][self.serialize(TYPE_FIELD)])()
        for attribute, value in obj[VALUE_FIELD].items():
            result_attribute = self.deserialize(attribute)
            result_value = self.deserialize(value)
            result.result_attribute = result_value

        return result
