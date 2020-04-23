from typing import Tuple, Union

import pytest

from keras_autodoc.get_signatures import get_signature_end
from keras_autodoc.get_signatures import get_signature_start
from keras_autodoc.get_signatures import get_class_signature
from keras_autodoc.get_signatures import get_function_signature
from keras_autodoc.get_signatures import get_signature
from keras_autodoc.get_signatures import format_signature


def test_get_signature_end():
    def some_function(*args, **kwargs):
        pass

    expected = '(*args, **kwargs)'
    computed = get_signature_end(some_function)
    assert expected == computed


class Dog:
    def woof(self, volume, good_boy: bool = True, name: str = 'doggy') -> int:
        pass

    def hard_method(self, arg: Union[int, Tuple[int, int]], arg2: int = 0) -> int:
        pass


def test_get_signature_end_method():

    expected = "(volume, good_boy=True, name='doggy')"
    computed = get_signature_end(Dog.woof)
    assert expected == computed


def test_get_signature_end_method_hard():

    expected = "(arg, arg2=0)"
    result = get_signature_end(Dog.hard_method)
    assert expected == result


def test_get_signature_start_method():

    expected = "Dog.woof"
    computed = get_signature_start(Dog.woof)
    assert expected == computed


@pytest.mark.parametrize('fn', [get_function_signature, get_signature])
def test_get_function_signature_black(fn):
    expected_110 = 'Dog.woof(volume, good_boy=True, name="doggy")'
    assert expected_110 == fn(Dog.woof, max_line_length=110)

    expected_40 = ('Dog.woof(\n'
                   '    volume, good_boy=True, name="doggy"\n'
                   ')')
    assert expected_40 == fn(Dog.woof, max_line_length=40)

    expected_30 = ('Dog.woof(\n'
                   '    volume,\n'
                   '    good_boy=True,\n'
                   '    name="doggy",\n'
                   ')')
    assert expected_30 == fn(Dog.woof, max_line_length=30)


class HelloWorld:
    def __init__(self):
        pass


def test_get_class_signature():
    expected = 'tests.test_get_signature.HelloWorld()'
    computed = get_class_signature(HelloWorld)
    assert expected == computed


class HelloWorld2:
    def __init__(self, one, two, three: int = 3):
        pass


def test_get_class_signature_with_args():
    expected = 'tests.test_get_signature.HelloWorld2(one, two, three=3)'
    computed = get_class_signature(HelloWorld2)
    assert expected == computed


@pytest.mark.parametrize('fn', [get_class_signature, get_signature])
def test_get_class_signature_with_args_black(fn):
    expected_110 = 'tests.test_get_signature.HelloWorld2(one, two, three=3)'
    assert expected_110 == fn(HelloWorld2, max_line_length=110)

    expected_50 = ('tests.test_get_signature.HelloWorld2(\n'
                   '    one, two, three=3\n'
                   ')')
    assert expected_50 == fn(HelloWorld2, max_line_length=50)


def test_format_signature1():
    signature_start = 'hello.world'
    signature_end = '(dodo: str = "stuff", dada=(7, 9))'

    expected = signature_start + signature_end
    computed = format_signature(signature_start, signature_end)
    assert computed == expected


def test_format_signature2():
    signature_start = 'hello.very.incredibly.large.world'
    signature_end = ('(doddodododododo: str = "stuff", '
                     'dadadadadadadada: tuple = (7, 9), '
                     'dudududududududu=37, '
                     'stufffffffffffffff=48)')

    expected = ('hello.very.incredibly.large.world(\n'
                '    doddodododododo: str = "stuff",\n'
                '    dadadadadadadada: tuple = (7, 9),\n'
                '    dudududududududu=37,\n'
                '    stufffffffffffffff=48,\n'
                ')')

    computed = format_signature(signature_start, signature_end)
    assert computed == expected
