from setuptools import setup
from setuptools import find_packages


setup(
    name="keras-autodoc",
    version="0.1.3",
    description="Building the Keras projects docs.",
    author="The Keras team",
    license="MIT",
    install_requires=["markdown", 'sphinx'],
    extras_require={"tests": ["pytest", "pytest-pep8"]},
    packages=find_packages(),
)
