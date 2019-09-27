FROM python:3.6

RUN pip install tensorflow
RUN pip install markdown mkdocs pytest

RUN git clone https://github.com/keras-team/keras.git
RUN pip install -e ./keras

COPY ./ ./keras-autodoc
RUN pip install -e ./keras-autodoc
RUN pytest ./keras-autodoc/tests/test_keras_integration.py
