from keras_autodoc import get_functions
from keras_autodoc import get_classes
from keras_autodoc import get_methods
from .dummy_package import dummy_module


def test_get_module_functions():
    assert set(get_functions(dummy_module)) == {dummy_module.to_categorical}


def test_get_module_classes():
    expected = {dummy_module.ImageDataGenerator, dummy_module.Dense}
    assert set(get_classes(dummy_module)) == expected


def test_get_class_methods():
    expected = {
        dummy_module.ImageDataGenerator.flow,
        dummy_module.ImageDataGenerator.flow_from_directory
    }
    assert set(get_methods(dummy_module.ImageDataGenerator)) == expected
