"""Simple objects"""
import math

test_int = 42
test_float = 534.5
test_complex = 3 + 7j
test_bool = True
test_str = "I want 10"
test_none = None

"""Iterable objects"""

test_list = [53, "I want 10 pls", True, (66.4, "pleeease")]
test_tuple = (53, "I want 10 pls", True, 66.4)
test_bytes = b":)"
test_set = {53, "I want 10 pls", True, 66.4}

test_dict = {test_tuple: {89: "dog", "cat": False}, "Butoma": 91.79}

"""function objects"""


def function_factorial_test(k):
    if k == 0:
        return 1
    else:
        return k * function_factorial_test(k - 1)


def function_sum_test(a, b=5):
    return a + b


def function_abs_test(k):
    return abs(k)


def function_ref_test(a, b=6, n=7):
    return function_sum_test(a, b) - n


def function_sin_test(x, y=8):  # Butoma tests
    return math.sin(x * y * test_int)


lambda_test = lambda x: x ^ 2


"""Class objects"""


class OldCar:
    model = "lada"

    def get_model(self):
        return self.model

    def meth(self):
        return 5


class Car(OldCar):
    def __init__(self, weight=5000, color="White"):
        self.weight = weight
        self.color = color

    def get_color(self):
        return self.color

    def get_info(self):
        return f"Model = {self.model}, Color = {self.color}, Weight = {self.weight / 1000} t"


class UpgradeCar(Car):
    pass


class B:
    def meth(self):
        return 5


class A(B):
    def __init__(self):
        pass
