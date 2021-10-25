# Installation instructions

**WARNING**: `pyguitemp` is in an early stage of development and the API might change
without notice. Use it in production with caution. And please, contribute to it to
help improving its maturity as fast as posisble!

`pyguitemp` and its dependencies can be installed with `pip` in Widnows,
[Linux](#what-about-linux) and [MacOS](#what-about-macos) (see notes below):

```bash
pip install pyguitemp
```

## What about linux

`pyguitemp` can be installed in Linux with `pip`, but `wxPython` will likely need to be
built from source as there are not *manylinux* wheels for it, yet.

The best option is for you to check if there is a wheel available for your specific
linux distirbution and python version in the [wxPython downloads
webpage](https://wxpython.org/pages/downloads/index.html) and install that one before
installing `pyguitemp`. Otherwise, in the same webpage you have instructions on how to
install `wxPython` from source.

Alternatively, if you use `conda`, you can install `wxPython` from `conda-forge` and
then install `pyguitemp` as above.

## What about MacOS

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
1. Install `pyguitemp` inside virtual environment, and all should work!

Alternatively, if you use `conda` to install `wxPython`, you will need to use `pythonw`
to execute your applications. See [wxPython downloads
webpage](https://wxpython.org/pages/downloads/index.html) for more information on this.