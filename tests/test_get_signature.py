from keras_autodoc.get_signatures import get_signature_end
from keras_autodoc.get_signatures import get_signature_start
from keras_autodoc.get_signatures import get_class_signature
from keras_autodoc.get_signatures import format_signature


def test_get_signature_end():
    def some_function(*args, **kwargs):
        pass

    expected = '(*args, **kwargs)'
    computed = get_signature_end(some_function)
    assert expected == computed


class Dog:
    def woof(self, volume, good_boy=True, name='doggy'):
        pass


def test_get_signature_end_method():

    expected = "(volume, good_boy=True, name='doggy')"
    computed = get_signature_end(Dog.woof)
    assert expected == computed


def test_get_signature_start_method():

    expected = "Dog.woof"
    computed = get_signature_start(Dog.woof)
    assert expected == computed


class HelloWorld:
    def __init__(self):
        pass


def test_get_class_signature():
    expected = 'tests.test_get_signature.HelloWorld()'
    computed = get_class_signature(HelloWorld)
    assert expected == computed


class HelloWorld2:
    def __init__(self, one, two, three=3):
        pass


def test_get_class_signature_with_args():
    expected = 'tests.test_get_signature.HelloWorld2(one, two, three=3)'
    computed = get_class_signature(HelloWorld2)
    assert expected == computed


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
