# keras-autodoc

[Autodoc](http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) for [mkdocs](https://www.mkdocs.org/).

keras-autodoc will fetch the docstrings from the functions you wish to document and will insert them in the markdown files.


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

Call this Python code, then you just have to run:

```bash
mkdocs serve
```

and you'll be able to see your website at [localhost:8000/callbacks](http://localhost:8000/callbacks/).

### Take a look at our docs

If you want examples, you can take a look at [the docs directory of autokeras](https://github.com/keras-team/autokeras/tree/master/docs) as well as [the generated docs](https://autokeras.com/).

You can also look at [the docs directory of keras-tuner](https://github.com/keras-team/keras-tuner/tree/master/docs).
