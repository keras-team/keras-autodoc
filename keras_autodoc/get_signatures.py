import inspect
import warnings


def get_signature_start(function, clean_module_name):
    """For the Dense layer, it should return the string 'keras.layers.Dense'"""
    try:
        function_module = function.__module__
    except AttributeError:
        warnings.warn(f'function {function} has no module. '
                      f'It will not be included in the signature.')
        function_module = ''
    else:
        function_module = f'{clean_module_name(function_module)}.'
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


def get_function_signature(
    function, clean_module_name, post_process_signature, method=True
):
    original_function = getattr(function, "_original_function", function)
    signature = inspect.getfullargspec(original_function)
    args = list(signature.args)
    if method and args and args[0] == 'self':
        args.pop(0)
    defaults = signature.defaults
    if defaults:
        kwargs = zip(args[-len(defaults):], defaults)
        args = args[: -len(defaults)]
    else:
        kwargs = []

    signature_start = get_signature_start(function, clean_module_name)
    signature_end = get_signature_end(args, kwargs)
    return post_process_signature(signature_start + signature_end)


def get_class_signature(cls, clean_module_name, post_process_signature):
    try:
        init_method = cls.__init__
    except (TypeError, AttributeError):
        # in case the class inherits from object and does not
        # define __init__
        class_signature = f"{cls.__module__}.{cls.__name__}()"
    else:
        class_signature = get_function_signature(
            init_method, clean_module_name, post_process_signature
        )
        class_signature = class_signature.replace("__init__", cls.__name__)
    return post_process_signature(class_signature)
