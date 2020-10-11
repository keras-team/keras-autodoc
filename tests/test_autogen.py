from markdown import markdown
from keras_autodoc import autogen
from keras_autodoc import get_methods
import pytest
import sys
import pathlib
from typing import Union, Optional, Tuple
from .dummy_package import dummy_module
from . import dummy_package

test_doc1 = {
    "doc": """Base class for recurrent layers.

# Arguments
    cell: A RNN cell instance. A RNN cell is a class that has:
        - a `call(input_at_t, states_at_t)` method, returning
            `(output_at_t, states_at_t_plus_1)`. The call method of the
            cell can also take the optional argument `constants`, see
            section "Note on passing external constants" below.
        - a `state_size` attribute. This can be a single integer
            (single state) in which case it is
            the size of the recurrent state
            (which should be the same as the size of the cell output).
            This can also be a list/tuple of integers
            (one size per state). In this case, the first entry
            (`state_size[0]`) should be the same as
            the size of the cell output.
        It is also possible for `cell` to be a list of RNN cell instances,
        in which cases the cells get stacked on after the other in the RNN,
        implementing an efficient stacked RNN.
    return_sequences: Boolean. Whether to return the last output
        in the output sequence, or the full sequence.
    return_state: Boolean. Whether to return the last state
        in addition to the output.
    go_backwards: Boolean (default False).
        If True, process the input sequence backwards and return the
        reversed sequence.
    stateful: Boolean (default False). If True, the last state
        for each sample at index i in a batch will be used as initial
        state for the sample of index i in the following batch.
    unroll: Boolean (default False).
        If True, the network will be unrolled,
        else a symbolic loop will be used.
        Unrolling can speed-up a RNN,
        although it tends to be more memory-intensive.
        Unrolling is only suitable for short sequences.
    input_dim: dimensionality of the input (integer).
        This argument (or alternatively,
        the keyword argument `input_shape`)
        is required when using this layer as the first layer in a model.
    input_length: Length of input sequences, to be specified
        when it is constant.
        This argument is required if you are going to connect
        `Flatten` then `Dense` layers upstream
        (without it, the shape of the dense outputs cannot be computed).
        Note that if the recurrent layer is not the first layer
        in your model, you would need to specify the input length
        at the level of the first layer
        (e.g. via the `input_shape` argument)

# Input shape
    3D tensor with shape `(batch_size, timesteps, input_dim)`.

# Output shape
    - if `return_state`: a list of tensors. The first tensor is
        the output. The remaining tensors are the last states,
        each with shape `(batch_size, units)`.
    - if `return_sequences`: 3D tensor with shape
        `(batch_size, timesteps, units)`.
    - else, 2D tensor with shape `(batch_size, units)`.

# Masking
    This layer supports masking for input data with a variable number
    of timesteps. To introduce masks to your data,
    use an [Embedding](embeddings.md) layer with the `mask_zero` parameter
    set to `True`.

# Note on using statefulness in RNNs
    You can set RNN layers to be 'stateful', which means that the states
    computed for the samples in one batch will be reused as initial states
    for the samples in the next batch. This assumes a one-to-one mapping
    between samples in different successive batches.

    To enable statefulness:
    - specify `stateful=True` in the layer constructor.
    - specify a fixed batch size for your model, by passing
        if sequential model:
          `batch_input_shape=(...)` to the first layer in your model.
        else for functional model with 1 or more Input layers:
          `batch_shape=(...)` to all the first layers in your model.
        This is the expected shape of your inputs
        *including the batch size*.
        It should be a tuple of integers, e.g. `(32, 10, 100)`.
    - specify `shuffle=False` when calling fit().

    To reset the states of your model, call `.reset_states()` on either
    a specific layer, or on your entire model.

# Note on specifying the initial state of RNNs

Note that
One: You can specify the initial state of RNN layers symbolically by
    calling them with the keyword argument `initial_state`.
Two: The value of `initial_state` should be a tensor or list of
    tensors representing
    the initial state of the RNN layer.
You can specify the initial state of RNN layers numerically by:
One: calling `reset_states`
    - With the keyword argument `states`.
        - The value of
    `states` should be a numpy array or
    list of numpy arrays representing
the initial state of the RNN layer.

# Note on passing external constants to RNNs
    You can pass "external" constants to the cell using the `constants`
    keyword: argument of `RNN.__call__` (as well as `RNN.call`) method.
    This: requires that the `cell.call` method accepts the same keyword argument
    `constants`. Such constants can be used to condition the cell
    transformation on additional static inputs (not changing over time),
    a.k.a. an attention mechanism.

# Examples

```python
# First, let's define a RNN Cell, as a layer subclass.

class MinimalRNNCell(keras.layers.Layer):

    def __init__(self, units, **kwargs):
        self.units = units
        self.state_size = units
        super(MinimalRNNCell, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(shape=(input_shape[-1], self.units),
                                      initializer='uniform',
                                      name='kernel')
        self.recurrent_kernel = self.add_weight(
            shape=(self.units, self.units),
            initializer='uniform',
            name='recurrent_kernel')
        self.built = True

    def call(self, inputs, states):
        prev_output = states[0]
        h = K.dot(inputs, self.kernel)
        output = h + K.dot(prev_output, self.recurrent_kernel)
        return output, [output]

# Let's use this cell in a RNN layer:

cell = MinimalRNNCell(32)
x = keras.Input((None, 5))
layer = RNN(cell)
y = layer(x)

# Here's how to use the cell to build a stacked RNN:

cells = [MinimalRNNCell(32), MinimalRNNCell(64)]
x = keras.Input((None, 5))
layer = RNN(cells)
y = layer(x)
```
""",
    "result": """Base class for recurrent layers.

__Arguments__

- __cell__: A RNN cell instance. A RNN cell is a class that has:
    - a `call(input_at_t, states_at_t)` method, returning
        `(output_at_t, states_at_t_plus_1)`. The call method of the
        cell can also take the optional argument `constants`, see
        section "Note on passing external constants" below.
    - a `state_size` attribute. This can be a single integer
        (single state) in which case it is
        the size of the recurrent state
        (which should be the same as the size of the cell output).
        This can also be a list/tuple of integers
        (one size per state). In this case, the first entry
        (`state_size[0]`) should be the same as
        the size of the cell output.
    It is also possible for `cell` to be a list of RNN cell instances,
    in which cases the cells get stacked on after the other in the RNN,
    implementing an efficient stacked RNN.
- __return_sequences__: Boolean. Whether to return the last output
    in the output sequence, or the full sequence.
- __return_state__: Boolean. Whether to return the last state
    in addition to the output.
- __go_backwards__: Boolean (default False).
    If True, process the input sequence backwards and return the
    reversed sequence.
- __stateful__: Boolean (default False). If True, the last state
    for each sample at index i in a batch will be used as initial
    state for the sample of index i in the following batch.
- __unroll__: Boolean (default False).
    If True, the network will be unrolled,
    else a symbolic loop will be used.
    Unrolling can speed-up a RNN,
    although it tends to be more memory-intensive.
    Unrolling is only suitable for short sequences.
- __input_dim__: dimensionality of the input (integer).
    This argument (or alternatively,
    the keyword argument `input_shape`)
    is required when using this layer as the first layer in a model.
- __input_length__: Length of input sequences, to be specified
    when it is constant.
    This argument is required if you are going to connect
    `Flatten` then `Dense` layers upstream
    (without it, the shape of the dense outputs cannot be computed).
    Note that if the recurrent layer is not the first layer
    in your model, you would need to specify the input length
    at the level of the first layer
    (e.g. via the `input_shape` argument)

__Input shape__

3D tensor with shape `(batch_size, timesteps, input_dim)`.

__Output shape__

- if `return_state`: a list of tensors. The first tensor is
    the output. The remaining tensors are the last states,
    each with shape `(batch_size, units)`.
- if `return_sequences`: 3D tensor with shape
    `(batch_size, timesteps, units)`.
- else, 2D tensor with shape `(batch_size, units)`.

__Masking__

This layer supports masking for input data with a variable number
of timesteps. To introduce masks to your data,
use an [Embedding](embeddings.md) layer with the `mask_zero` parameter
set to `True`.

__Note on using statefulness in RNNs__

You can set RNN layers to be 'stateful', which means that the states
computed for the samples in one batch will be reused as initial states
for the samples in the next batch. This assumes a one-to-one mapping
between samples in different successive batches.

To enable statefulness:
- specify `stateful=True` in the layer constructor.
- specify a fixed batch size for your model, by passing
    if sequential model:
      `batch_input_shape=(...)` to the first layer in your model.
    else for functional model with 1 or more Input layers:
      `batch_shape=(...)` to all the first layers in your model.
    This is the expected shape of your inputs
    *including the batch size*.
    It should be a tuple of integers, e.g. `(32, 10, 100)`.
- specify `shuffle=False` when calling fit().

To reset the states of your model, call `.reset_states()` on either
a specific layer, or on your entire model.

__Note on specifying the initial state of RNNs__

Note that
One: You can specify the initial state of RNN layers symbolically by
    calling them with the keyword argument `initial_state`.
Two: The value of `initial_state` should be a tensor or list of
    tensors representing
    the initial state of the RNN layer.
You can specify the initial state of RNN layers numerically by:
One: calling `reset_states`
    - With the keyword argument `states`.
        - The value of
    `states` should be a numpy array or
    list of numpy arrays representing
the initial state of the RNN layer.

__Note on passing external constants to RNNs__

You can pass "external" constants to the cell using the `constants`
keyword: argument of `RNN.__call__` (as well as `RNN.call`) method.
This: requires that the `cell.call` method accepts the same keyword argument
`constants`. Such constants can be used to condition the cell
transformation on additional static inputs (not changing over time),
a.k.a. an attention mechanism.

__Examples__

```python
# First, let's define a RNN Cell, as a layer subclass.

class MinimalRNNCell(keras.layers.Layer):

    def __init__(self, units, **kwargs):
        self.units = units
        self.state_size = units
        super(MinimalRNNCell, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(shape=(input_shape[-1], self.units),
                                      initializer='uniform',
                                      name='kernel')
        self.recurrent_kernel = self.add_weight(
            shape=(self.units, self.units),
            initializer='uniform',
            name='recurrent_kernel')
        self.built = True

    def call(self, inputs, states):
        prev_output = states[0]
        h = K.dot(inputs, self.kernel)
        output = h + K.dot(prev_output, self.recurrent_kernel)
        return output, [output]

# Let's use this cell in a RNN layer:

cell = MinimalRNNCell(32)
x = keras.Input((None, 5))
layer = RNN(cell)
y = layer(x)

# Here's how to use the cell to build a stacked RNN:

cells = [MinimalRNNCell(32), MinimalRNNCell(64)]
x = keras.Input((None, 5))
layer = RNN(cells)
y = layer(x)
```
""",
}

test_doc_with_arguments_as_last_block = {
    "doc": """Base class for recurrent layers.

# Arguments
    return_sequences: Boolean. Whether to return the last output
        in the output sequence, or the full sequence.
    return_state: Boolean. Whether to return the last state
        in addition to the output.
""",
    "result": """Base class for recurrent layers.

__Arguments__

- __return_sequences__: Boolean. Whether to return the last output
    in the output sequence, or the full sequence.
- __return_state__: Boolean. Whether to return the last state
    in addition to the output.
""",
}


@pytest.mark.parametrize(
    "docs_descriptor", [test_doc_with_arguments_as_last_block, test_doc1]
)
def test_doc_lists(docs_descriptor):
    docstring = autogen.process_docstring(docs_descriptor["doc"])
    assert markdown(docstring) == markdown(docs_descriptor["result"])


dummy_docstring = """Multiplies 2 tensors (and/or variables) and returns a *tensor*.

When attempting to multiply a nD tensor
with a nD tensor, it reproduces the Theano behavior.
(e.g. `(2, 3) * (4, 3, 5) -> (2, 4, 5)`)

# Examples
```python
# Theano-like behavior example
>>> x = K.random_uniform_variable(shape=(2, 3), low=0, high=1)
>>> y = K.ones((4, 3, 5))
>>> xy = K.dot(x, y)
>>> K.int_shape(xy)
(2, 4, 5)
```

# Numpy implementation
```python
def dot(x, y):
    return dot(x, y)
```
    """


def test_doc_multiple_sections_code():
    """ Checks that we can have code blocks in multiple sections."""
    generated = autogen.process_docstring(dummy_docstring)
    assert "# Theano-like behavior example" in generated
    assert "def dot(x, y):" in generated


def check_against_expected(elements):
    doc_generator = autogen.DocumentationGenerator(
        project_url='www.dummy.com/my_project'
    )
    markdown_text = ''
    for element in elements:
        markdown_text += doc_generator._render(element)

    current_file_path = pathlib.Path(__file__).resolve()
    expected_file = current_file_path.parent / 'dummy_package' / 'expected.md'
    expected_text = expected_file.read_text()
    # we check that the generated html is the same
    # to ignore blank lines or other differences not relevant.
    assert markdown(markdown_text) == markdown(expected_text)


def test_generate_markdown():
    elements = [dummy_module.Dense, dummy_module.ImageDataGenerator]
    elements += get_methods(dummy_module.ImageDataGenerator)
    elements.append(dummy_module.to_categorical)
    check_against_expected(elements)


def test_generate_markdown_from_string():
    elements = [
        'tests.dummy_package.dummy_module.Dense',
        'tests.dummy_package.dummy_module.ImageDataGenerator',
        'tests.dummy_package.dummy_module.ImageDataGenerator.flow',
        'tests.dummy_package.dummy_module.ImageDataGenerator.flow_from_directory',
        'tests.dummy_package.dummy_module.to_categorical'
    ]
    check_against_expected(elements)


@pytest.mark.parametrize('element', [
    'tests.dummy_package.DataGenerator',
    'tests.dummy_package.to_categorical'
])
def test_aliases_class_function(element):
    doc_generator = autogen.DocumentationGenerator()
    computed = doc_generator._render(element)
    expected = element + '('
    assert expected in computed


@pytest.mark.parametrize(['element', 'expected'], [
    ('tests.dummy_package.DataGenerator.flow', '\nDataGenerator.flow('),
    ('tests.dummy_package.DataGenerator.flow_from_directory',
     '\nDataGenerator.flow_from_directory('),
])
def test_aliases_methods(element, expected):
    doc_generator = autogen.DocumentationGenerator()
    computed = doc_generator._render(element)
    assert expected in computed


expected_dodo = """ dodo


```python
tests.dummy_package.dummy_module2.dodo(x)
```


Some dodo


----

"""


@pytest.mark.parametrize("titles_size", ["###", "##"])
def test_aliases_in_hints(titles_size):
    pages = {'dod.md': ['tests.dummy_package.DataGenerator',
                        'tests.dummy_package.dummy_module2.dodo']}
    doc_generator = autogen.DocumentationGenerator(pages=pages, titles_size=titles_size)
    result = doc_generator._render('tests.dummy_package.dummy_module2.dodo')
    assert result == titles_size + expected_dodo


class A:
    def dodo(self):
        """Some docstring."""
        pass


class B(A):
    def dodo(self):
        pass


def test_get_docstring_of_super_class():
    computed = autogen.DocumentationGenerator()._render(B.dodo)
    assert 'Some docstring' in computed


def water_plant(
    self, amount: Union[int, float], fertilizer_type: Optional[str] = None
):
    """Give your plant some water.

    # Arguments
        amount: How much water to give.
        fertilizer_type: What kind of fertilizer to add.
    """

    pass


def test_types_in_docstring():
    result = autogen.DocumentationGenerator()._render(water_plant)

    assert "water_plant(self, amount, fertilizer_type=None)" in result
    assert "- __amount__ `Union[int, float]`: How much" in result
    assert "- __fertilizer_type__ `Optional[str]`: What" in result


def hard_method(self, arg: Union[int, Tuple[int, int]], arg2: int = 0) -> int:
    """Can we parse this?

    # Arguments
        arg: One or two integers.
        arg2: One integer.
    """
    pass


def test_hard_method():
    generated = autogen.DocumentationGenerator()._render(hard_method)

    assert "- __arg__ `Union[int, Tuple[int, int]]`: One or" in generated
    assert "- __arg2__ `int`: One integer." in generated


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


def test_rendinging_with_extra_alias_custom_alias():
    extra_aliases = {"tests.dummy_package.dummy_module.ImageDataGenerator":
                     "some.new.Thing"}
    generated = autogen.DocumentationGenerator(extra_aliases=extra_aliases)._render(
        doing_things)
    assert "- __an_argument__ `some.new.Thing`: Some" in generated


@pytest.mark.skipif(
    sys.version_info < (3, 7),
    reason="the __future__ annotations only works with py37+."
)
def test_future_annotations():
    from . import autogen_future
    autogen_future.test_rendinging_with_extra_alias()


if __name__ == "__main__":
    pytest.main([__file__])
