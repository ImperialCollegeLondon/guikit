"""
Contains the definition of the top window of the program, including the menu bar, the
toolbar (if any), the central widget, bottom progress bar and status area.

In particular, the progress bar and the status area are the kind of things that the
plugins will be importing - or at least wanting to update - regularly. They are defined
as global aobject singletons such that even though an instance is created once, such an
instance can be access directly from the class anywhere else where you import the class.
"""
from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from typing import List, Mapping, Type, Union

from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QMainWindow,
    QProgressBar,
    QStatusBar,
    QTabWidget,
    QWidget,
)

if sys.platform == "darwin":
    # There is an issue with pyside2 and MacOS BigSur. This hack sorts it
    # https://stackoverflow.com/a/64878899/3778792
    import os

    os.environ["QT_MAC_WANTS_LAYER"] = "1"


class ViewBase(ABC):
    """
    Base class that defines the required API that all the views of the different plugins
    will need to provide.
    """

    def __init_subclass__(cls: Type[ViewBase]):
        if cls not in KNOWN_VIEWS:
            KNOWN_VIEWS.append(cls)

    @abstractmethod
    def menu_entries(
        self,
    ) -> Mapping[str, Union[List[QAction], Mapping[str, List[QAction]]]]:
        """Return a dictionary with the menu elements provided by this view.

        Menus group all commands that we can use in an application.

        Returns:
            The dictionary might have deeply nested dictionaries which will define
            submenus. Submenus will be created if not already present. The value of the
            final entries must always be a list of QAction. Eg:

            {
                "Menu": [<QAction>, <QAction>],
                "Edit": {
                            "Tools": [<QAction>, <QAction>]
                        }
            }
        """

    @abstractmethod
    def toolbar_items(self) -> Mapping[str, List[QAction]]:
        """Return a dictionary with the toolbar elements provided by this view.

        Toolbars provide a quick access to the most frequently used commands.

        Returns:
            Contrary to menus, where there might be multiple submenus, there can be no
            nesting for toolbars. The value of the final entries must always be a list
            of QAction. Eg:

            {
                "Menu": [<QAction>, <QAction>],
                "Edit": [<QAction>, <QAction>]
            }
        """

    @abstractmethod
    def tabs(self) -> Mapping[str, QWidget]:
        """Return a dictionary with the tabs provided by this view.

        Tabs are the central part of the GUI and serve to group different parts of the
        software in a logical way. Within each tab there can be entry fields, tables,
        plots, text areas, buttons, etc.

        They key of the dictionary will be the text of the tab and the value, the widget
        displayed within the tab. Eg. the following dictionary will result in two tabs
        being displayed.

        {
            "Settings": <QWidget>,
            "Output": <QWidget>
        }
        """


KNOWN_VIEWS: List[Type[ViewBase]] = []
"""List of views registered as subclasses of ViewBase."""


class Status(QStatusBar):
    def __init__(self):
        super(Status, self).__init__()
        self.progress_bar: QProgressBar = QProgressBar()
        self.addPermanentWidget(self.progress_bar)


status: Status
"""Global variable giving access to the status and progress bars"""


class MainWindow(QMainWindow):
    def __init__(self, name: str):
        super().__init__()
        self.setWindowTitle(name)
        self.setMinimumSize(800, 600)

        # The lower status and progress bar
        global status
        status = Status()
        self.setStatusBar(status)

        # Add Menu Bar
        menu_entries = [view().menu_entries() for view in KNOWN_VIEWS]
        if len(menu_entries) > 0:
            self._populate_menu(menu_entries)

        # Add toolbars
        tools = [view().toolbar_items() for view in KNOWN_VIEWS]
        if len(tools) > 0:
            self._populate_toolbars(tools)

        # Central widget
        tabs = [view().tabs() for view in KNOWN_VIEWS]
        self.notebook = QTabWidget()
        self._populate_notebook(tabs)
        self.setCentralWidget(self.notebook)

        self.statusBar().showMessage("Loading complete!")

    def _populate_notebook(self, tabs: List[Mapping[str, QWidget]]) -> None:
        """Populate the notebook from tabs coming from all the plugins.

        Args:
            tabs: A list with the mapping of names and tab widgets.
        """
        for t in tabs:
            for name, widget in t.items():
                self.notebook.addTab(widget, name)

    def _populate_toolbars(self, tools: List[Mapping[str, List[QAction]]]) -> None:
        """Create and populate the toolbars.

        Args:
            tools: A list with the mapping of toolbar names and actions.
        """
        for t in tools:
            for name, actions in t.items():
                bar = self.addToolBar(name)
                bar.addActions(actions)

    def _populate_menu(
        self,
        entries: List[Mapping[str, Union[List[QAction], Mapping[str, List[QAction]]]]],
    ) -> None:
        """Add entries to the menu bar.

        Only one level of submenus is accepted.

        Args:
            entries: A list with the (possibly nested) mapping of menu entries names
                and actions.
        """
        for entry in entries:
            for menu_name, items in entry.items():
                menu = self.menuBar().addMenu(menu_name)
                if isinstance(items, dict):
                    for submenu, subitems in items.items():
                        subbar = menu.addMenu(submenu)
                        subbar.addActions(subitems)
                elif isinstance(items, list):
                    menu.addActions(items)


class DefaultMenu(ViewBase):
    def toolbar_items(self) -> Mapping[str, List[QAction]]:
        return {}

    def tabs(self) -> Mapping[str, QWidget]:
        return {}

    def menu_entries(
        self,
    ) -> Mapping[str, Union[List[QAction], Mapping[str, List[QAction]]]]:
        exit_app = QAction("Exit")
        exit_app.triggered.connect(QApplication.instance().closeAllWindows)

        documentation = QAction("Documentation")
        about = QAction("About")
        return {"File": [exit_app], "Help": [documentation, about]}
