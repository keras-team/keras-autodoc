# keras-autodoc

![](https://https://github.com/keras-team/keras-autodoc/workflows/.github/workflows/dockerimage.yml/badge.svg?branch=master)


[Autodoc](http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) for [mkdocs](https://www.mkdocs.org/).

keras-autodoc will fetch the docstrings from the functions you wish to document and will insert them in the markdown files.

Take a look at the [documentation](https://gabrieldemarmiesse.github.io/keras-autodoc/)!

### Install

```bash
pip install keras-autodoc
```

We recommend pinning the version (eg: `pip install keras-autodoc==0.3.2`). We may break compatibility without any warning.

### Example

Let's suppose that you have a `docs` directory:

```
./docs
|-- autogen.py
|-- mkdocs.yml
```

The API is quite simple:

```python
# content of docs/autogen.py

from keras_autodoc import DocumentationGenerator


pages = {'layers/core.md': ['keras.layers.Dense', 'keras.layers.Flatten'],
         'callbacks.md': ['keras.callbacks.TensorBoard']}

doc_generator = DocumentationGenerator(pages)
doc_generator.generate('./sources')
```

```yaml
# content of docs/mkdocs.yml

site_name: My_site
docs_dir: sources
site_description: 'My pretty site.'

nav:
    - Core: layers/core.md
    - Callbacks:
      - Some callbacks: callbacks.md
```

Then you just have to run:

```bash
python autogen.py
mkdocs serve
```

and you'll be able to see your website at [localhost:8000/callbacks](http://localhost:8000/callbacks/).

### Docstring format:

The docstrings used should use the The docstrings follow the [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#381-docstrings) with markdown, or just plain markdown.

For example, let's take this class:

```python
class ImageDataGenerator:
    """Generate batches of tensor image data with real-time data augmentation.

    The data will be looped over (in batches).

    # Arguments
        featurewise_center: Boolean.
            Set input mean to 0 over the dataset, feature-wise.
        zca_whitening: Boolean. Apply ZCA whitening.
        width_shift_range: Float, 1-D array-like or int
            - float: fraction of total width, if < 1, or pixels if >= 1.
            - 1-D array-like: random elements from the array.
            - int: integer number of pixels from interval
                `(-width_shift_range, +width_shift_range)`
            - With `width_shift_range=2` possible values
                are integers `[-1, 0, +1]`,
                same as with `width_shift_range=[-1, 0, +1]`,
                while with `width_shift_range=1.0` possible values are floats
                in the interval `[-1.0, +1.0)`.

    # Examples

    Example of using `.flow(x, y)`:
    ```python
    datagen = ImageDataGenerator(
        featurewise_center=True,
        zca_whitening=True,
        width_shift_range=0.2)
    # compute quantities required for featurewise normalization
    # (std, mean, and principal components if ZCA whitening is applied)
    datagen.fit(x_train)
    # fits the model on batches with real-time data augmentation:
    model.fit_generator(datagen.flow(x_train, y_train, batch_size=32),
                        steps_per_epoch=len(x_train) / 32, epochs=epochs)
    ```
    """

    def __init__(self,featurewise_center, zca_whitening, width_shift_range):
        pass
```

will be rendered as:

### ImageDataGenerator class:

```python
dummy_module.ImageDataGenerator(featurewise_center, zca_whitening, width_shift_range=0.0)
```

Generate batches of tensor image data with real-time data augmentation.

The data will be looped over (in batches).

__Arguments__

- __featurewise_center__: Boolean.
    Set input mean to 0 over the dataset, feature-wise.
- __zca_whitening__: Boolean. Apply ZCA whitening.
- __width_shift_range__: Float, 1-D array-like or int
    - float: fraction of total width, if < 1, or pixels if >= 1.
    - 1-D array-like: random elements from the array.
    - int: integer number of pixels from interval
        `(-width_shift_range, +width_shift_range)`
    - With `width_shift_range=2` possible values
        are integers `[-1, 0, +1]`,
        same as with `width_shift_range=[-1, 0, +1]`,
        while with `width_shift_range=1.0` possible values are floats
        in the interval `[-1.0, +1.0)`.

__Examples__


Example of using `.flow(x, y)`:
```python
datagen = ImageDataGenerator(
    featurewise_center=True,
    zca_whitening=True,
    width_shift_range=0.2)
# compute quantities required for featurewise normalization
# (std, mean, and principal components if ZCA whitening is applied)
datagen.fit(x_train)
# fits the model on batches with real-time data augmentation:
model.fit_generator(datagen.flow(x_train, y_train, batch_size=32),
                    steps_per_epoch=len(x_train) / 32, epochs=epochs)
```

### Take a look at our docs

If you want examples, you can take a look at [the docs directory of autokeras](https://github.com/keras-team/autokeras/tree/master/docs) as well as [the generated docs](https://autokeras.com/).

You can also look at [the docs directory of keras-tuner](https://github.com/keras-team/keras-tuner/tree/master/docs).
