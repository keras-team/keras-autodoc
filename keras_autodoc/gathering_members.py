import inspect


def get_classes(module, exclude=None):
    exclude = exclude or []
    all_elements = _get_all_module_element(module, exclude)
    return list(filter(inspect.isclass, all_elements))


def get_functions(module, exclude=None):
    exclude = exclude or []
    all_elements = _get_all_module_element(module, exclude)
    return list(filter(inspect.isfunction, all_elements))


def get_methods(cls, exclude=None):
    exclude = exclude or []
    methods = []
    for _, method in inspect.getmembers(cls, predicate=inspect.isroutine):
        if method.__name__[0] == "_" or method.__name__ in exclude:
            continue
        methods.append(method)
    return methods


def _get_all_module_element(module, exclude):
    module_data = []
    for name in dir(module):
        module_member = getattr(module, name)
        if name[0] == "_" or name in exclude:
            continue
        if module.__name__ not in module_member.__module__:
            continue
        if module_member in module_data:
            continue
        module_data.append(module_member)
    module_data.sort(key=id)
    return module_data
