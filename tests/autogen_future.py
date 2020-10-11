from __future__ import annotations

from keras_autodoc import autogen

from . import dummy_package


def doing_things(an_argument: dummy_package.DataGenerator):
    """A function

    # Arguments
        an_argument: Some generator

    """


def test_rendinging_with_extra_alias():
    extra_aliases = ["tests.dummy_package.DataGenerator"]
    generated = autogen.DocumentationGenerator(extra_aliases=extra_aliases)._render(
        doing_things)
    assert "- __an_argument__ `tests.dummy_package.DataGenerator`: Some" in generated
