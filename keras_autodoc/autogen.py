import shutil
import pathlib
from typing import Dict, Union

from .docstring import process_docstring
from .examples import copy_examples
from .get_signatures import get_class_signature, get_function_signature

from . import utils


class DocumentationGenerator:

    def __init__(self,
                 pages=None,
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
        blocks = []
        classes = page.get('classes', [])
        page_name = page['page']
        for cls, methods in utils.format_classes_list(classes, page_name):
            subblocks = self._format_class_and_methods(cls, methods)
            block = "\n".join(subblocks)
            blocks.append(block)

        for method in page.get('methods', []):
            block = self._render_function(method, method=True)
            blocks.append(block)

        for function in page.get('functions', []):
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

    def _format_class_and_methods(self, cls, methods):
        subblocks = []
        if self.project_url is not None:
            subblocks.append(utils.make_source_link(cls, self.project_url))
        if methods:
            subblocks.append(f"## {cls.__name__} class\n")
        else:
            subblocks.append(f"### {cls.__name__}\n")
        signature = self.process_signature(get_class_signature(cls))
        subblocks.append(utils.code_snippet(signature))
        docstring = cls.__doc__
        if docstring:
            subblocks.append(self.process_class_docstring(docstring, cls))
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
