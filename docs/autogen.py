import pathlib
import shutil

import keras_autodoc


PAGES = {
    'documentation_generator.md': [
        'keras_autodoc.DocumentationGenerator',
        'keras_autodoc.DocumentationGenerator.generate',
    ],
    'automatic_gathering.md': [
        'keras_autodoc.get_functions',
        'keras_autodoc.get_classes',
        'keras_autodoc.get_methods',
    ]
}


keras_autodoc_dir = pathlib.Path(__file__).resolve().parents[1]


def generate(dest_dir):
    doc_generator = keras_autodoc.DocumentationGenerator(
        PAGES,
        'https://github.com/keras-team/keras-autodoc/blob/master',
    )
    doc_generator.generate(dest_dir)
    shutil.copyfile(keras_autodoc_dir / 'README.md', dest_dir / 'index.md')


if __name__ == '__main__':
    generate(keras_autodoc_dir / 'docs' / 'sources')
