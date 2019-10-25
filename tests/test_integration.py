from keras import Model
from kerastuner import HyperParameters
from keras_autodoc.get_signatures import get_function_signature, get_signature_end


def test_signature():
    excpected = ('Model.compile(optimizer, loss=None, metrics=None, '
                 'loss_weights=None, sample_weight_mode=None, '
                 'weighted_metrics=None, target_tensors=None, '
                 '**kwargs)')
    computed = get_function_signature(Model.compile)
    assert computed == excpected


def test_wrapping_signature():
    expected = '(parent_name, parent_values)'
    computed = get_signature_end(HyperParameters.conditional_scope)
    assert computed == expected
