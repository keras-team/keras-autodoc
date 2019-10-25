import warnings
from sphinx.util.inspect import Signature
from . import utils


def get_signature_start(function):
    """For the Dense layer, it should return the string 'keras.layers.Dense'"""
    if utils.ismethod(function):
        prefix = f'{utils.get_class_from_method(function).__name__}.'
    else:
        try:
            prefix = f'{function.__module__}.'
        except AttributeError:
            warnings.warn(f'function {function} has no module. '
                          f'It will not be included in the signature.')
            prefix = ''

    return f'{prefix}{function.__name__}'


def get_signature_end(function):
    signature_end = Signature(function).format_args()
    if utils.ismethod(function):
        signature_end = signature_end.replace('(self, ', '(')
        signature_end = signature_end.replace('(self)', '()')
    return signature_end


def get_function_signature(function):
    signature_start = get_signature_start(function)
    signature_end = get_signature_end(function)
    return signature_start + signature_end


def get_class_signature(cls):
    signature_end = get_signature_end(cls.__init__)
    class_signature = f"{cls.__module__}.{cls.__name__}{signature_end}"
    return class_signature
