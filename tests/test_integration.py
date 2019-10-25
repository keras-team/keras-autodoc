from keras import Model
from keras_autodoc.get_signatures import get_function_signature


def test_signature():
    excpected = ('Model.compile(optimizer, loss=None, metrics=None, '
                 'loss_weights=None, sample_weight_mode=None, '
                 'weighted_metrics=None, target_tensors=None, '
                 '**kwargs)')
    computed = get_function_signature(Model.compile)
    assert computed == excpected
