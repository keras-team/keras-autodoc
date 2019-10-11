import inspect
import os
import shutil
import pathlib

from .docstring import process_docstring
from .examples import copy_examples
from .get_signatures import get_class_signature, get_function_signature


def render_function(function, clean_module_name, post_process_signature,
                    preprocess_docstring=None,
                    method=True):
    subblocks = []
    signature = get_function_signature(
        function, clean_module_name, post_process_signature, method=method
    )
    if method:
        signature = signature.replace(clean_module_name(function.__module__) + ".",
                                      "")
    subblocks.append(f"### {function.__name__}\n")
    subblocks.append(code_snippet(signature))
    docstring = function.__doc__
    if docstring:
        if preprocess_docstring is not None:
            docstring = preprocess_docstring(docstring, function, signature)
        subblocks.append(process_docstring(docstring))
    return "\n\n".join(subblocks)


def read_page_data(page_data, type, exclude):
    assert type in ["classes", "functions", "methods"]
    data = page_data.get(type, [])
    for module in page_data.get(f"all_module_{type}", []):
        module_data = []
        for name in dir(module):
            if name[0] == "_" or name in exclude:
                continue
            module_member = getattr(module, name)
            if (
                inspect.isclass(module_member)
                and type == "classes"
                or inspect.isfunction(module_member)
                and type == "functions"
            ):
                instance = module_member
                if module.__name__ in instance.__module__:
                    if instance not in module_data:
                        module_data.append(instance)
        module_data.sort(key=lambda x: id(x))
        data += module_data
    return data


def class_to_source_link(cls, clean_module_name, project_url):
    module_name = clean_module_name(cls.__module__)
    path = module_name.replace(".", "/")
    path += ".py"
    line = inspect.getsourcelines(cls)[-1]
    return f"[[source]]({project_url}/{path}#L{line})"


def collect_class_methods(cls, methods, exclude):
    if isinstance(methods, (list, tuple)):
        return [getattr(cls, m) if isinstance(m, str) else m for m in methods]
    methods = []
    for _, method in inspect.getmembers(cls, predicate=inspect.isroutine):
        if method.__name__[0] == "_" or method.__name__ in exclude:
            continue
        methods.append(method)
    return methods


def code_snippet(snippet):
    return (
        f'```python\n'
        f'{snippet.encode("unicode_escape").decode("utf8")}\n'
        f'```\n')


def generate(
    dest_dir,
    template_dir,
    pages,
    project_url,
    examples_dir=None,
    exclude=None,
    clean_module_name=lambda x: x,
    post_process_signature=lambda x: x,
    preprocess_docstring=None,
):
    """Generates the markdown files for the documentation.

    # Arguments
        sources_dir: Where to put the markdown files.
    """
    dest_dir = pathlib.Path(dest_dir)
    template_dir = pathlib.Path(template_dir)
    if examples_dir is not None:
        examples_dir = pathlib.Path(examples_dir)
    exclude = exclude or []

    print("Cleaning up existing sources directory.")
    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    print("Populating sources directory with templates.")
    shutil.copytree(template_dir, dest_dir)

    for page_data in pages:
        classes = read_page_data(page_data, "classes", exclude)

        blocks = []
        for element in classes:
            if not isinstance(element, (list, tuple)):
                element = (element, [])
            cls = element[0]
            subblocks = []
            signature = get_class_signature(
                cls, clean_module_name, post_process_signature
            )
            subblocks.append(
                '<span style="float:right;">'
                + class_to_source_link(cls, clean_module_name, project_url)
                + "</span>"
            )
            if element[1]:
                subblocks.append("## " + cls.__name__ + " class\n")
            else:
                subblocks.append("### " + cls.__name__ + "\n")
            subblocks.append(code_snippet(signature))
            docstring = cls.__doc__
            if docstring:
                subblocks.append(process_docstring(docstring))
            methods = collect_class_methods(cls, element[1], exclude)
            if methods:
                subblocks.append("\n---")
                subblocks.append("## " + cls.__name__ + " methods\n")
                subblocks.append(
                    "\n---\n".join(
                        [
                            render_function(
                                method,
                                clean_module_name,
                                post_process_signature,
                                method=True,
                            )
                            for method in methods
                        ]
                    )
                )
            blocks.append("\n".join(subblocks))

        methods = read_page_data(page_data, "methods", exclude)

        for method in methods:
            blocks.append(
                render_function(
                    method, clean_module_name, post_process_signature, method=True
                )
            )

        functions = read_page_data(page_data, "functions", exclude)

        for function in functions:
            blocks.append(
                render_function(
                    function, clean_module_name,
                    post_process_signature, preprocess_docstring,
                    method=False,
                )
            )

        if not blocks:
            raise RuntimeError("Found no content for page " + page_data["page"])

        mkdown = "\n----\n\n".join(blocks)
        # Save module page.
        # Either insert content into existing page,
        # or create page otherwise.
        page_name = page_data["page"]
        path = dest_dir / page_name
        if path.exists():
            template = path.read_text(encoding="utf-8")
            if "{{autogenerated}}" not in template:
                raise RuntimeError(
                    "Template found for " + path + " but missing {{autogenerated}}"
                    " tag."
                )
            mkdown = template.replace("{{autogenerated}}", mkdown)
            print("...inserting autogenerated content into template:", path)
        else:
            print("...creating new page with autogenerated content:", path)
        subdir = path.parent
        os.makedirs(subdir, exist_ok=True)
        path.write_text(mkdown, encoding="utf-8")

    if examples_dir is not None:
        copy_examples(examples_dir, dest_dir / "examples")
