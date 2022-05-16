from tests.objects import *
from serializer_lib.factory.factory import Factory

JSON_PATH = "files/JSONtest.json"
TOML_PATH = "files/TOMLtest.toml"
YAML_PATH = "files/YAMLtest.yaml"


def test_simples(parser="yaml"):
    parser = Factory.get_parser(parser)
    simples = [test_int, test_float, test_complex, test_bool, test_str, test_none]
    for simple in simples:
        parser.dump(simple, TOML_PATH)
        assert simple == parser.load(TOML_PATH)


def test_iterables(parser="json"):
    parser = Factory.get_parser(parser)
    iterables = [test_list, test_tuple, test_complex, test_set, test_dict]
    for iterable in iterables:
        assert iterable == parser.loads(parser.dumps(iterable))


def test_functions(parser="yaml"):
    parser = Factory.get_parser(parser)
    functions = [function_factorial_test, function_sum_test, function_abs_test, function_ref_test, function_sin_test]
    for function in functions:
        parser.dump(function, YAML_PATH)
        assert function(5) == parser.load(YAML_PATH)(5)


def test_lambdas(parser="json"):
    parser = Factory.get_parser(parser)
    assert lambda_test(4) == parser.loads(parser.dumps(lambda_test))(4)


def test_classes(parser="json"):
    parser = Factory.get_parser(parser)
    classes = [Car, OldCar]
    for cls in classes:
        parser.dump(cls, JSON_PATH)
        assert cls.model == parser.load(JSON_PATH).model
    car_orig = Car()
    car_ser = parser.loads(parser.dumps(Car))()
    assert car_orig.get_info() == car_ser.get_info()

a = A()

def test_objects(parser="yaml"):
    parser = Factory.get_parser(parser)
    car_orig = Car(5000, "White")
    car_ser = parser.loads(parser.dumps(car_orig))
    assert car_orig.meth() == car_ser.meth()
    assert car_orig.get_color() == car_ser.get_color()
    assert car_orig.get_info() == car_ser.get_info()

    fake_a = parser.loads(parser.dumps(a))
    assert a.meth() == fake_a.meth()

