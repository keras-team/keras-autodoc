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


docstring3 = """This is a docstring

Some text is here.

# A section
    Some stuff written

    Some line jump

Some more text.
"""

expected3 = """This is a docstring

Some text is here.

__A section__

Some stuff written

Some line jump

Some more text.
"""


def test_generate_docstring_line_jump():
    computed = process_docstring(docstring3)
    assert computed == expected3


docstring4 = """This is a docstring

Some text is here.

# A section
    Some stuff written
    Some line jump
Some more text.
"""

expected4 = """This is a docstring

Some text is here.

__A section__

Some stuff written
Some line jump

Some more text.
"""


def test_generate_docstring_lines_stuck():
    computed = process_docstring(docstring4)
    assert computed == expected4


docstring5 = """This is a docstring

Some text is here.

# A section

Some stuff written
Some line jump

Some more text.
"""

expected5 = """This is a docstring

Some text is here.

__A section__

Some stuff written
Some line jump

Some more text.
"""


def test_generate_docstring_no_indent():
    computed = process_docstring(docstring5)
    assert computed == expected5


docstring6 = """This is a docstring

Some text is here.

# Output shape
    nD tensor with shape: `(batch_size, ..., units)`.
    For instance, for a 2D input with shape `(batch_size, input_dim)`,
    the output would have shape `(batch_size, units)`.
"""

expected6 = """This is a docstring

Some text is here.

__Output shape__

nD tensor with shape: `(batch_size, ..., units)`.
For instance, for a 2D input with shape `(batch_size, input_dim)`,
the output would have shape `(batch_size, units)`.
"""


def test_generate_docstring_weird_poing_bug():
    computed = process_docstring(docstring6)
    assert computed == expected6
