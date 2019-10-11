import inspect


def get_function_signature(
    function, clean_module_name, post_process_signature, method=True
):
    wrapped = getattr(function, "_original_function", None)
    if wrapped is None:
        signature = inspect.getfullargspec(function)
    else:
        signature = inspect.getfullargspec(wrapped)
    defaults = signature.defaults
    if method:
        args = signature.args[1:]
    else:
        args = signature.args
    if defaults:
        kwargs = zip(args[-len(defaults):], defaults)
        args = args[: -len(defaults)]
    else:
        kwargs = []
    st = f"{clean_module_name(function.__module__)}.{function.__name__}("

    for a in args:
        st += str(a) + ", "
    for a, v in kwargs:
        if isinstance(v, str):
            v = f"'{v}'"
        st += f'{a}={v}, '
    if kwargs or args:
        signature = st[:-2] + ")"
    else:
        signature = st + ")"
    return post_process_signature(signature)


def get_class_signature(cls, clean_module_name, post_process_signature):
    try:
        class_signature = get_function_signature(
            cls.__init__, clean_module_name, post_process_signature
        )
        class_signature = class_signature.replace("__init__", cls.__name__)
    except (TypeError, AttributeError):
        # in case the class inherits from object and does not
        # define __init__
        class_signature = f"{cls.__module__}.{cls.__name__}()"
    return post_process_signature(class_signature)
