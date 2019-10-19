import shutil
import pathlib
import inspect

from .docstring import process_docstring
from .examples import copy_examples
from .get_signatures import get_class_signature, get_function_signature

from . import utils


def to_path(path):
    if path is None:
        return None
    else:
        return pathlib.Path(path)


class DocumentationGenerator:

    def __init__(self,
                 pages=None,
                 project_url=None,
                 template_dir=None,
                 examples_dir=None,
                 exclude=None):
        self.template_dir = to_path(template_dir)
        self.pages = pages
        self.project_url = project_url
        self.examples_dir = to_path(examples_dir)
        self.exclude = exclude or []

    def generate(self, dest_dir):
        dest_dir = pathlib.Path(dest_dir)
        print("Cleaning up existing sources directory.")
        if dest_dir.exists():
            shutil.rmtree(dest_dir)

        print("Populating sources directory with templates.")
        shutil.copytree(self.template_dir, dest_dir)

        for page in self.pages:
            mkdown = self._generate_markdown(page)
            utils.insert_in_file(mkdown, dest_dir / page["page"])

        if self.examples_dir is not None:
            copy_examples(self.examples_dir, dest_dir / "examples")

    def process_function_docstring(self, docstring, function):
        return process_docstring(docstring)

    def process_class_docstring(self, docstring, class_):
        return process_docstring(docstring)

    def process_method_docstring(self, docstring, method):
        return process_docstring(docstring)

    def process_signature(self, signature):
        return signature

    def _generate_markdown(self, page):
        classes, methods, functions = read_page_data(page, self.exclude)
        utils.format_page_values(classes, methods, functions, name=page['page'])

        blocks = []
        for element in classes:
            subblocks = self._get_class_and_methods(element)
            block = "\n".join(subblocks)
            blocks.append(block)

        for method in methods:
            block = self._render_function(method, method=True)
            blocks.append(block)

        for function in functions:
            block = self._render_function(function)
            blocks.append(block)

        if not blocks:
            raise RuntimeError("Found no content for page " + page["page"])

        mkdown = "\n----\n\n".join(blocks)
        return mkdown

    def _render_function(self, function, method=False):
        subblocks = []
        signature = self.process_signature(get_function_signature(
            function, method=method
        ))
        if method:
            signature = signature.replace(function.__module__ + ".", "")
        subblocks.append(f"### {function.__name__}\n")
        subblocks.append(utils.code_snippet(signature))

        docstring = function.__doc__
        if docstring:
            if method:
                docstring = self.process_method_docstring(docstring, function)
            else:
                docstring = self.process_function_docstring(docstring, function)
            subblocks.append(docstring)
        return "\n\n".join(subblocks)

    def _get_class_and_methods(self, element):
        cls = element[0]
        subblocks = []
        if self.project_url is not None:
            subblocks.append(utils.make_source_link(cls, self.project_url))
        if element[1]:
            subblocks.append(f"## {cls.__name__} class\n")
        else:
            subblocks.append(f"### {cls.__name__}\n")
        signature = self.process_signature(get_class_signature(cls))
        subblocks.append(utils.code_snippet(signature))
        docstring = cls.__doc__
        if docstring:
            subblocks.append(self.process_class_docstring(docstring, cls))
        methods = collect_class_methods(cls, element[1], self.exclude)
        if methods:
            subblocks.append("\n---")
            subblocks.append(f"## {cls.__name__} methods\n")
            subblocks.append(
                "\n---\n".join(
                    [
                        self._render_function(method, method=True)
                        for method in methods
                    ]
                )
            )
        return subblocks


def read_page_data(page_data, exclude):
    data_types = []
    for type_ in ["classes", "methods", "functions"]:
        data = page_data.get(type_, [])
        for module in page_data.get(f"all_module_{type_}", []):
            module_data = []
            for name in dir(module):
                if name[0] == "_" or name in exclude:
                    continue
                module_member = getattr(module, name)
                if (
                    inspect.isclass(module_member)
                    and type_ == "classes"
                    or inspect.isfunction(module_member)
                    and type_ == "functions"
                ):
                    instance = module_member
                    if module.__name__ in instance.__module__:
                        if instance not in module_data:
                            module_data.append(instance)
            module_data.sort(key=id)
            data += module_data
        data_types.append(data)
    return data_types


def collect_class_methods(cls, methods, exclude):
    if isinstance(methods, (list, tuple)):
        return [getattr(cls, m) if isinstance(m, str) else m for m in methods]
    methods = []
    for _, method in inspect.getmembers(cls, predicate=inspect.isroutine):
        if method.__name__[0] == "_" or method.__name__ in exclude:
            continue
        methods.append(method)
    return methods


# TODO: remove that
def generate(
    dest_dir,
    template_dir,
    pages,
    project_url,
    examples_dir=None,
    exclude=None,
    post_process_signature=lambda x: x,
    preprocess_docstring=None,
):
    """Generates the markdown files for the documentation.

    # Arguments
        sources_dir: Where to put the markdown files.
    """
    doc_generator = DocumentationGenerator(pages,
                                           project_url,
                                           template_dir,
                                           examples_dir,
                                           exclude)
    doc_generator.process_signature = post_process_signature
    doc_generator.process_function_docstring = preprocess_docstring
    doc_generator.generate(dest_dir)
