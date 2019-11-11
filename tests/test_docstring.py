from keras_autodoc.docstring import process_docstring


docstring1 = """This is a docstring

Some text is here.

# Arguments
    arg1: some argument.
    arg2: Some other
        argument with a line break.

Some more text.
"""

expected1 = """This is a docstring

Some text is here.

__Arguments__

- __arg1__: some argument.
- __arg2__: Some other
    argument with a line break.

Some more text.
"""


def test_generate_docstring_basic():
    computed = process_docstring(docstring1)
    assert computed == expected1


docstring2 = """This is a docstring

Some text is here.

# Arguments
    arg1: some argument
        here written: with colon

Some more text.
"""

expected2 = """This is a docstring

Some text is here.

__Arguments__

- __arg1__: some argument
    here written: with colon

Some more text.
"""


def test_generate_docstring_with_colon():
    computed = process_docstring(docstring2)
    assert computed == expected2
