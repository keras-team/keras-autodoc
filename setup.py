from setuptools import setup
from setuptools import find_packages


setup(
    name="keras-autodoc",
    version="0.1.0",
    description="Building the Keras projects docs.",
    author="Francois Chollet",
    author_email="francois.chollet@gmail.com",
    license="MIT",
    install_requires=["markdown"],
    extras_require={"tests": ["pytest", "pytest-pep8"]},
    packages=find_packages(),
)
