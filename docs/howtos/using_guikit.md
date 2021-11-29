# Using guikit

The purpose of `guikit` is to save you time to start creating your GUI. Therefore, no
matter how you use it: if it saves you time, it is well used. There are, however, some
general approaches that you could follow:

## The indended way

The intention when creating `guikit` is to remove from sight everything that is not
the code you need to implement the business logic and the views specific for your
application. For that reason, the simplest way of using `guikit` is as a dependency
for your project from where you import all the relevant components that you need.

To get you started, just create a virtual environment to host your project, install
`guikit` in there with `pip install guikit` (see the [installation
instructions](installation.md) for extra information on this) and then run:

```bash
python -m guikit init my_app -t .
```

This command will create in the target directory a package called `my_app` with several
modules inside and a subpackage called `extensions` in where to put your plugins (see
the secction about [creating plugins](add_plugin.md)).

```bash
- my_app
 |- __init__.py
 |- __main__.py
 |- config.py
 |- extensions
    |- __init__.py
```

These files in reality contain very little code: they just import `guikit` to create
the main window, the logger and give some default values to the few configuration
options. All you need to do now is to populate the extensions subpackage with the
plugins you need.

If you add the following `setup.cfg`, `setup.py` and `pyproject.toml` files at the same level that
`my_app` (you can read more about these two files in the [`setuptools`
documentation](https://setuptools.pypa.io/en/latest/index.html)):

```toml
# pyproject.toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

```ini
# setup.cfg
[metadata]
name = my_app
version = attr: my_app.VERSION

[options]
packages = find:
include_package_data = True
install_requires =
    guikit
    wxPython
```

```python
# setup.py
# Only needed to install the tool in 'edit' mode
from setuptools import setup

setup()
```

Then you can install your new package in edit mode and see the magic happens:

```bash
pip install -e .
python -m my_app
```

The last line will launch your new application, opening its main window - altough with
nothing inside. If you are using `conda` on MacOS, the last command should be:

```bash
pythonw -m my_app
```

## The advanced way

The above option is the simplest and fastest one, but you will need to acept the design
choices we have made in terms of layout of components and how to structure the code and
extensions.

If you want to have the freedom of changing any of this and adapt it to your needs, just
download the [lastest version of the code from
GitHub](https://github.com/ImperialCollegeLondon/python-gui-template) and use
`guikit` source code itself as a template to create your own application. You
will  want to remove some information from there, like the documentation, the `skeleton`
or some of the script options for initialising a repo, as above. And you
will need to adapt the metadata from `setup.cfg`, and the secrets used in GitHub
Actions. But otherwise it should be a fully functional tool that, again, will save you
time.
