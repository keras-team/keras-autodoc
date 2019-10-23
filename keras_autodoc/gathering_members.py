import inspect


def get_classes(module, exclude=None):
    exclude = exclude or []
    return _get_all_module_element(module, 'classes', exclude)


def get_functions(module, exclude=None):
    exclude = exclude or []
    return _get_all_module_element(module, 'functions', exclude)


def get_methods(cls, exclude=None):
    exclude = exclude or []
    methods = []
    for _, method in inspect.getmembers(cls, predicate=inspect.isroutine):
        if method.__name__[0] == "_" or method.__name__ in exclude:
            continue
        methods.append(method)
    return methods


def _get_all_module_element(module, element_type, exclude):
    module_data = []
    for name in dir(module):
        if name[0] == "_" or name in exclude:
            continue
        module_member = getattr(module, name)
        if (
                inspect.isclass(module_member)
                and element_type == "classes"
                or inspect.isfunction(module_member)
                and element_type == "functions"
        ):
            instance = module_member
            if module.__name__ in instance.__module__:
                if instance not in module_data:
                    module_data.append(instance)
    module_data.sort(key=id)
    return module_data
