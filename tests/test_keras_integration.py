from keras_autodoc.autogen import generate
import os


def test_docs_in_custom_destination_dir(tmpdir):
    generate(str(tmpdir))
    assert os.path.isdir(os.path.join(tmpdir, 'layers'))
    assert os.path.isdir(os.path.join(tmpdir, 'models'))
    assert os.path.isdir(os.path.join(tmpdir, 'examples'))
    assert os.listdir(os.path.join(tmpdir, 'examples'))

