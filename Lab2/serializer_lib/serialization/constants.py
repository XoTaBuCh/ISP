
OBJECT_TYPE_REGEX = "\'([\w\W]+)\'"

TYPE_FIELD = "TYPE"
VALUE_FIELD = "VALUE"

CLASS_NAME = "class"
OBJECT_NAME = "object"
DICTIONARY_NAME = "dict"
FUNCTION_NAME = "function"
CODE_NAME = "code"
MODULE_NAME = "module"
BUILTIN_NAME = "builtin_function_or_method"

BASE_NAME = "base"
DATA_NAME = "data"

TYPES_NAMES = [
    "int",
    "float",
    "complex",
    "bool",
    "str",
    "NoneType"

]

ITERABLE_NAMES = [
    "list",
    "tuple",
    "bytes",
    "set"
]

CLASS_ATTRIBUTE_NAME = "__class__"

FUNCTION_ATTRIBUTES_NAMES = [
    "__code__",
    "__name__",
    "__defaults__",
    "__closure__",
]

FUNCTION_CREATE_ATTRIBUTES_NAMES = [
    "__code__",
    "__globals__",
    "__name__",
    "__defaults__",
    "__closure__",
]

OBJECT_ATTRIBUTES_NAMES = [
    "__object_type__",
    "__fields__"
]

CODE_FIELD = "__code__"
GLOBAL_FIELD = "__globals__"
NAME_FIELD = "__name__"

CO_NAMES_FIELD = "co_names"

CODE_ARGS = (
    'co_argcount',
    'co_posonlyargcount',
    'co_kwonlyargcount',
    'co_nlocals',
    'co_stacksize',
    'co_flags',
    'co_code',
    'co_consts',
    'co_names',
    'co_varnames',
    'co_filename',
    'co_name',
    'co_firstlineno',
    'co_lnotab',
    'co_freevars',
    'co_cellvars'
)