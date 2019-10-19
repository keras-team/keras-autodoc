import inspect
import warnings


def get_signature_start(function):
    """For the Dense layer, it should return the string 'keras.layers.Dense'"""
    try:
        function_module = function.__module__
    except AttributeError:
        warnings.warn(f'function {function} has no module. '
                      f'It will not be included in the signature.')
        function_module = ''
    else:
        function_module = f'{function_module}.'
    return f'{function_module}{function.__name__}'


def get_signature_end(args, kwargs):
    kwargs_formatted = []
    for a, v in kwargs:
        if isinstance(v, str):
            v = f"'{v}'"
        kwargs_formatted.append(f'{a}={v}')

    all_args_str = map(str, args + kwargs_formatted)
    all_args_str = ', '.join(all_args_str)
    return f'({all_args_str})'


def get_function_signature(function, method=False):
    original_function = getattr(function, "_original_function", function)
    signature = inspect.getfullargspec(original_function)
    args = list(signature.args)
    if method and args and args[0] == 'self':
        args.pop(0)
    defaults = signature.defaults or []
    kwargs = zip(args[-len(defaults):], defaults)
    args = args[: len(args)-len(defaults)]

    signature_start = get_signature_start(function)
    signature_end = get_signature_end(args, kwargs)
    return signature_start + signature_end


def get_class_signature(cls):
    try:
        init_method = cls.__init__
    except (TypeError, AttributeError):
        # in case the class inherits from object and does not
        # define __init__
        class_signature = f"{cls.__module__}.{cls.__name__}()"
    else:
        class_signature = get_function_signature(init_method, method=True)
        class_signature = class_signature.replace("__init__", cls.__name__)
    return class_signature
