import inspect
from inspect import isclass, isfunction, isroutine
from .utils import import_object


def get_classes(module, exclude=None, return_strings=True):
    return _get_all_module_element(module, exclude, return_strings, True)


def get_functions(module, exclude=None, return_strings=True):
    return _get_all_module_element(module, exclude, return_strings, False)


def get_methods(cls, exclude=None, return_strings=True):
    if isinstance(cls, str):
        cls_str = cls
        cls = import_object(cls)
    else:
        cls_str = f'{cls.__module__}.{cls.__name__}'
    exclude = exclude or []
    methods = []
    for _, method in inspect.getmembers(cls, predicate=isroutine):
        if method.__name__[0] == "_" or method.__name__ in exclude:
            continue
        if return_strings:
            methods.append(f'{cls_str}.{method.__name__}')
        else:
            methods.append(method)
    return methods


def _get_all_module_element(module, exclude, return_strings, class_):
    if isinstance(module, str):
        module = import_object(module)
    exclude = exclude or []
    module_data = []
    for name in dir(module):
        module_member = getattr(module, name)
        if not (isfunction(module_member) or isclass(module_member)):
            continue
        if name[0] == "_" or name in exclude:
            continue
        if module.__name__ not in module_member.__module__:
            continue
        if module_member in module_data:
            continue
        if class_ and not isclass(module_member):
            continue
        if not class_ and not isfunction(module_member):
            continue
        if return_strings:
            module_data.append(f'{module.__name__}.{name}')
        else:
            module_data.append(module_member)
    module_data.sort(key=id)
    return module_data
