|GitHub| |Test and build| |PyPI version shields.io| |PyPI status| |PyPI
pyversions| |PyPI license| |Website pyguitemp| |Windows| |macOS| |Linux|

Python GUI Template 
====================

This little tool’s purpose is to facilitate getting started building a
GUI for your software. It takes care of most of the boilerplate code
that you need to build a GUI - making some opinionated decisions about
the general layout of the application - so you can focus on adding the
business logic and views specific to your problem.

``pyguitemp`` uses ``wXPython`` as the GUI framework, meaning that the
resulting application will have a native look and feel regadless of
running it on Windows, Linux or MacOS.

What ``pyguitemp`` is and what is not
-------------------------------------

``pyguitemp`` takes care of the boilerplate code and enables you to have
a minimal application running in no time, but you still need to code the
rest of your GUI mannually yourself. That means you will need to learn
how to use ``wxPython``, the widgets it offers and their options.

This is not a graphical designer for GUIs, as it could be `QT
Designer <https://realpython.com/qt-designer-python/>`__,
`Glade <https://glade.gnome.org>`__ or `Matlab’s App
Designer <https://www.mathworks.com/products/matlab/app-designer.html>`__.
All of those are excellent tools… just a different kind of tools.
``pyguitemp`` will save you some valuable time when creating a GUI, but
it is still a low level library.

Why ``wxPython`` as GUI framework
---------------------------------

While there are several excellent frameworks available, mature, well
supported and with many options for customization - in particular
`PySide2 <https://wiki.qt.io/Qt_for_Python>`__ and
`PyQt <https://riverbankcomputing.com/software/pyqt/intro>`__, both
based in QT - ``wxPython`` offers a licensing scheme a little bit more
flexible that makes it suitable for both open and close source projects.

We strongly support open source software and open research, but we
understand that it is not always possible or advisable, at least at
beginning, and we want to offer a tool that could suit most users most
of the time.

Installation instructions
-------------------------

**WARNING**: ``pyguitemp`` is in an early stage of development and the
API might change without notice. Use it in production with caution. And
please, contribute to it to help improving its maturity as fast as
posisble!

``pyguitemp`` and its dependencies can be installed with ``pip`` in
Widnows, `Linux <#what-about-linux>`__ and `MacOS <#what-about-macos>`__
(see notes below):

.. code:: bash

   pip install pyguitemp

What about linux 
~~~~~~~~~~~~~~~~~

``pyguitemp`` can be installed in Linux with ``pip``, but ``wxPython``
will likely need to be built from source as there are not *manylinux*
wheels for it, yet.

The best option is for you to check if there is a wheel available for
your specific linux distirbution and python version in the `wxPython
downloads webpage <https://wxpython.org/pages/downloads/index.html>`__
and install that one before installing ``pyguitemp``. Otherwise, in the
same webpage you have instructions on how to install ``wxPython`` from
source.

Alternatively, if you use ``conda``, you can install ``wxPython`` from
``conda-forge`` and then install ``pyguitemp`` as above.

What about MacOS 
~~~~~~~~~~~~~~~~~

``wxPython`` causes some issue on MacOS when installed with a “Non
Framework” version of python. It typically complains with this error
message:

::

   This program needs access to the screen. Please run with a
   Framework build of python, and only when you are logged in
   on the main display of your Mac.

To work around this:

1. Install a python.org version of python.
2. Find executable under ``/Library/Frameworks/Python.framework/...``.
3. Use that executable to create a virtual environment:
   ``/Library/Frameworks/Python.framework/Versions/<version>/bin/python3 -m venv .venv``.
4. Install ``pyguitemp`` inside virtual environment, and all should
   work!

Alternatively, if you use ``conda`` to install ``wxPython``, you will
need to use ``pythonw`` to execute your applications. See `wxPython
downloads webpage <https://wxpython.org/pages/downloads/index.html>`__
for more information on this.

Using ``pyguitemp``
-------------------

There are several ways you can benefit from ``pyguitemp``, depending on
what you want to achieve. Check the
`documentation <https://imperialcollegelondon.github.io/python-gui-template/>`__
for full details.

-  Initialise your current directory with a skeleton for your GUI
   application using ``pyguitemp`` with
   ``python -m pyguitemp init my_app``.
-  Run ``pyguitemp`` with all its available expensions for your to have
   a look and explore the things you can do with it, uwing
   ``python -m pyguitemp run``.
-  Explore ``pyguitemp``\ ’s repo, flick trhough the code, learn how to
   do things, brings those which are useful to your own application, or
   clone the whole repo and customize the core classes and functions to
   fully suit your needs.

.. |GitHub| image:: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
   :target: https://github.com/ImperialCollegeLondon/python-gui-template
.. |Test and build| image:: https://github.com/ImperialCollegeLondon/python-gui-template/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/ImperialCollegeLondon/python-gui-template/actions/workflows/ci.yml
.. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/pyguitemp.svg
   :target: https://pypi.python.org/pypi/pyguitemp/
.. |PyPI status| image:: https://img.shields.io/pypi/status/pyguitemp.svg
   :target: https://pypi.python.org/pypi/pyguitemp/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/pyguitemp.svg
   :target: https://pypi.python.org/pypi/pyguitemp/
.. |PyPI license| image:: https://img.shields.io/pypi/l/pyguitemp.svg
   :target: https://pypi.python.org/pypi/pyguitemp/
.. |Website pyguitemp| image:: https://img.shields.io/website-up-down-green-red/http/shields.io.svg
   :target: https://imperialcollegelondon.github.io/python-gui-template/
.. |Windows| image:: https://svgshare.com/i/ZhY.svg
   :target: https://svgshare.com/i/ZhY.svg
.. |macOS| image:: https://svgshare.com/i/ZjP.svg
   :target: https://svgshare.com/i/ZjP.svg
.. |Linux| image:: https://svgshare.com/i/Zhy.svg
   :target: https://svgshare.com/i/Zhy.svg
