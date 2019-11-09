from keras import Model
from kerastuner import HyperParameters
from keras_autodoc.get_signatures import get_function_signature, get_signature_end


def test_signature():
    excpected = ('Model.compile(\n'
                 '    optimizer,\n'
                 '    loss=None,\n'
                 '    metrics=None,\n'
                 '    loss_weights=None,\n'
                 '    sample_weight_mode=None,\n'
                 '    weighted_metrics=None,\n'
                 '    target_tensors=None,\n'
                 '    **kwargs\n'
                 ')')
    computed = get_function_signature(Model.compile)
    assert computed == excpected


def test_wrapping_signature():
    expected = '(parent_name, parent_values)'
    computed = get_signature_end(HyperParameters.conditional_scope)
    assert computed == expected
