Welcome to PyGUItemp documentation!
===================================

This little tool serves to facilitate getting started building a GUI for
your software. It takes care of most of the boilerplate code that you
need to build a GUI - making some opinionated decisions about the
general layout of the application - so you can focus on adding the
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

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   howtos/howtos_index
   technical/api/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
