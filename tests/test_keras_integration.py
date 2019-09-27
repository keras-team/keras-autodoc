from keras_autodoc.autogen import generate
from docs.structure import PAGES
import os


def make_keras_docs(dest_dir):
    generate(str(dest_dir), PAGES)


def test_docs_in_custom_destination_dir(tmpdir):
    make_keras_docs(tmpdir)
    assert os.path.isdir(os.path.join(tmpdir, 'layers'))
    assert os.path.isdir(os.path.join(tmpdir, 'models'))
    assert os.path.isdir(os.path.join(tmpdir, 'examples'))
    assert os.listdir(os.path.join(tmpdir, 'examples'))
