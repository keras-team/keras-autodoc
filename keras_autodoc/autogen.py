import shutil
import pathlib
from inspect import isclass, isfunction, getdoc
from typing import Dict, Union

from .docstring import process_docstring
from .examples import copy_examples
from .get_signatures import get_function_signature, get_class_signature

from . import utils


class DocumentationGenerator:

    def __init__(self,
                 pages: Dict[str, list] = None,
                 project_url: Union[str, Dict[str, str]] = None,
                 template_dir: pathlib.Path = None,
                 examples_dir: pathlib.Path = None):
        self.template_dir = template_dir
        self.pages = pages
        self.project_url = project_url
        self.examples_dir = examples_dir

    def generate(self, dest_dir: pathlib.Path):
        print("Cleaning up existing sources directory.")
        if dest_dir.exists():
            shutil.rmtree(dest_dir)

        print("Populating sources directory with templates.")
        shutil.copytree(self.template_dir, dest_dir)

        for file_path, elements in self.pages.items():
            markdown_text = ''
            for element in elements:
                markdown_text += self._render(element)
            utils.insert_in_file(markdown_text, dest_dir / file_path)

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

    def _render(self, element):
        if isinstance(element, str):
            signature_override = element
            element = utils.import_object(element)
        else:
            signature_override = None
        if isclass(element):
            return self._render_class(element, signature_override)
        elif utils.ismethod(element):
            if signature_override is not None:
                signature_override = '.'.join(signature_override.split('.')[-2:])
            return self._render_method(element, signature_override)
        elif isfunction(element):
            return self._render_function(element, signature_override)
        else:
            raise TypeError(f'Object {element} with type {type(element)}'
                            f' is not a class nor a function.')

    def _render_class(self, cls, signature_override=None):
        subblocks = []
        if self.project_url is not None:
            subblocks.append(utils.make_source_link(cls, self.project_url))
        subblocks.append(f"### {cls.__name__} class:\n")

        signature = get_class_signature(cls, signature_override)
        signature = self.process_signature(signature)
        subblocks.append(utils.code_snippet(signature))
        docstring = getdoc(cls)
        if docstring:
            subblocks.append(self.process_class_docstring(docstring, cls))
        return '\n'.join(subblocks) + '\n\n----\n\n'

    def _render_method(self, method, signature_override=None):
        subblocks = []
        signature = get_function_signature(method, signature_override)
        signature = self.process_signature(signature)
        subblocks.append(f"### {method.__name__} method:\n")
        subblocks.append(utils.code_snippet(signature))

        docstring = getdoc(method)
        if docstring:
            docstring = self.process_method_docstring(docstring, method)
            subblocks.append(docstring)
        return "\n\n".join(subblocks) + '\n\n----\n\n'

    def _render_function(self, function, signature_override=None):
        subblocks = []
        signature = get_function_signature(function, signature_override)
        signature = self.process_signature(signature)
        subblocks.append(f"### {function.__name__} function:\n")
        subblocks.append(utils.code_snippet(signature))

        docstring = getdoc(function)
        if docstring:
            docstring = self.process_function_docstring(docstring, function)
            subblocks.append(docstring)
        return "\n\n".join(subblocks) + '\n\n----\n\n'
