from setuptools import setup
from setuptools import find_packages
from pathlib import Path

this_file = Path(__file__).resolve()
readme = this_file.parent / 'README.md'


setup(
    name='keras-autodoc',
    version='0.7.0',
    packages=find_packages(),
    install_requires=['markdown', 'sphinx', 'black==20.8b1'],
    package_data={'': ['README.md']},
    author='The Keras team',
    author_email='gabrieldemarmiesse@gmail.com',
    description='Building the Keras projects docs.',
    long_description=readme.read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/keras-team/keras-autodoc',
    license='Apache License 2.0',
    extras_require={'tests': ['pytest', 'pytest-pep8']},
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'Topic :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License'
    ]
)
