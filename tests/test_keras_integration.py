from keras_autodoc.autogen import generate, keras_dir
from docs.structure import PAGES
import shutil
import os

from pathlib import Path

def make_keras_docs(dest_dir):
    dest_dir = str(dest_dir)
    generate(dest_dir, PAGES)
    shutil.copyfile(os.path.join(keras_dir, 'CONTRIBUTING.md'),
                    os.path.join(dest_dir, 'contributing.md'))


def test_docs_in_custom_destination_dir(tmpdir):
    make_keras_docs(tmpdir)
    tmpdir = Path(tmpdir)
    assert (tmpdir / 'layers').is_dir()
    assert (tmpdir / 'models').is_dir()
    assert (tmpdir / 'examples').is_dir()
    assert os.listdir(tmpdir / 'examples')
