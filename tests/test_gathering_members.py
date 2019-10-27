from keras_autodoc import get_functions
from keras_autodoc import get_classes
from keras_autodoc import get_methods
from .dummy_package import dummy_module


def test_get_module_functions():
    expected = {dummy_module.to_categorical}
    computed = set(get_functions(dummy_module, return_strings=False))
    assert expected == computed


def test_get_module_functions_to_str():
    expected = {'tests.dummy_package.dummy_module.to_categorical'}
    assert set(get_functions(dummy_module)) == expected


def test_get_module_functions_from_str_to_str():
    expected = {'tests.dummy_package.to_categorical'}
    computed = set(get_functions('tests.dummy_package'))
    assert computed == expected


def test_get_module_classes():
    expected = {dummy_module.ImageDataGenerator, dummy_module.Dense}
    assert set(get_classes(dummy_module, return_strings=False)) == expected


def test_get_module_classes_from_str_to_str():
    expected = {'tests.dummy_package.dummy_module.ImageDataGenerator',
                'tests.dummy_package.dummy_module.Dense'}
    assert set(get_classes(dummy_module)) == expected


def test_get_class_methods():
    expected = {
        dummy_module.ImageDataGenerator.flow,
        dummy_module.ImageDataGenerator.flow_from_directory
    }
    computed = get_methods(dummy_module.ImageDataGenerator, return_strings=False)
    computed = set(computed)
    assert computed == expected


def test_get_class_methods_aliases():
    expected = {
        'tests.dummy_package.DataGenerator.flow',
        'tests.dummy_package.DataGenerator.flow_from_directory'
    }
    computed = set(get_methods('tests.dummy_package.DataGenerator'))
    assert computed == expected
