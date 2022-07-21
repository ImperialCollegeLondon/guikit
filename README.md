[![Test and build](https://github.com/ImperialCollegeLondon/guikit/actions/workflows/ci.yml/badge.svg)](https://github.com/ImperialCollegeLondon/guikit/actions/workflows/ci.yml)
[![PyPI version
shields.io](https://img.shields.io/pypi/v/guikit.svg)](https://pypi.python.org/pypi/guikit/)
[![PyPI
status](https://img.shields.io/pypi/status/guikit.svg)](https://pypi.python.org/pypi/guikit/)
[![PyPI
pyversions](https://img.shields.io/pypi/pyversions/guikit.svg)](https://pypi.python.org/pypi/guikit/)
[![PyPI
license](https://img.shields.io/pypi/l/guikit.svg)](https://pypi.python.org/pypi/guikit/)
[![Website guikit](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://imperialcollegelondon.github.io/guikit/)

# GUIKIT <!-- omit in toc -->

This little tool's purpose is to facilitate getting started building a GUI for your
software. It takes care of most of the boilerplate code that you need to build a GUI -
making some opinionated decisions about the general layout of the application - so you
can focus on adding the business logic and views specific to your problem.

`guikit` uses `wXPython` as the GUI framework, meaning that the resulting application
will have a native look and feel regadless of running it on Windows, Linux or MacOS.

## What `guikit` is and what is not

`guikit` takes care of the boilerplate code and enables you to have a minimal
application running in no time, but you still need to code the rest of your GUI
mannually yourself. That means you will need to learn how to use `wxPython`, the widgets
it offers and their options.

This is not a graphical designer for GUIs, as it could be [QT
Designer](https://realpython.com/qt-designer-python/), [Glade](https://glade.gnome.org)
or [Matlab's App Designer](https://www.mathworks.com/products/matlab/app-designer.html).
All of those are excellent tools... just a different kind of tools. `guikit` will
save you some valuable time when creating a GUI, but it is still a low level library.

## Why `wxPython` as GUI framework

While there are several excellent frameworks available, mature, well supported and with
many options for customization - in particular
[PySide2](https://wiki.qt.io/Qt_for_Python) and
[PyQt](https://riverbankcomputing.com/software/pyqt/intro), both based in QT -
`wxPython` offers a licensing scheme a little bit more flexible that makes it suitable
for both open and close source projects.

We strongly support open source software and open research, but we understand that it is
not always possible or advisable, at least at beginning, and we want to offer a tool
that could suit most users most of the time.

## Installation instructions

**WARNING**: `guikit` is in an early stage of development and the API might change
without notice. Use it in production with caution. And please, contribute to it to
help improving its maturity as fast as posisble!

`guikit` and its dependencies can be installed with `pip` in Windows,
[Linux](#what-about-linux) and [MacOS](#what-about-macos) (see notes below):

```bash
pip install guikit
```

### What about linux <!-- omit in toc -->

`guikit` can be installed in Linux with `pip`, but `wxPython` will likely need to be
built from source as there are not *manylinux* wheels for it, yet.

The best option is for you to check if there is a wheel available for your specific
linux distirbution and python version in the [wxPython downloads
webpage](https://wxpython.org/pages/downloads/index.html) and install that one before
installing `guikit`. Otherwise, in the same webpage you have instructions on how to
install `wxPython` from source.

Alternatively, if you use `conda`, you can install `wxPython` from `conda-forge` and
then install `guikit` as above.

### What about MacOS <!-- omit in toc -->

`wxPython` causes some issue on MacOS when installed with a "Non Framework" version of
python. It typically complains with this error message:

```
This program needs access to the screen. Please run with a
Framework build of python, and only when you are logged in
on the main display of your Mac.
```

To work around this:

1. Install a python.org version of python.
1. Find executable under `/Library/Frameworks/Python.framework/...`.
1. Use that executable to create a virtual environment: `/Library/Frameworks/Python.framework/Versions/<version>/bin/python3 -m venv .venv`.
1. Install `guikit` inside virtual environment, and all should work!

Alternatively, if you use `conda` to install `wxPython`, you will need to use `pythonw`
to execute your applications. See [wxPython downloads
webpage](https://wxpython.org/pages/downloads/index.html) for more information on this.

## Using `guikit`

There are several ways you can benefit from `guikit`, depending on what you want to
achieve. Check the
[documentation](https://imperialcollegelondon.github.io/guikit/) for full
details.

- Initialise your current directory with a skeleton for your GUI application using
  `guikit` with `python -m guikit init my_app`.
- Run `guikit` with all its available expensions for your to have a look and explore
  the things you can do with it, uwing `python -m guikit run`.
- Explore `guikit`'s repo, flick trhough the code, learn how to do things, brings
  those which are useful to your own application, or clone the whole repo and customize
  the core classes and functions to fully suit your needs.
