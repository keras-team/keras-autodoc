import os
import io
from keras_autodoc import utils
from . import dummy_package


def test_import_object():
    assert os.path.join == utils.import_object('os.path.join')
    assert io.BytesIO.flush == utils.import_object('io.BytesIO.flush')
    assert dummy_package == utils.import_object('tests.dummy_package')
