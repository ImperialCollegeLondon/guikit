"""
Contains the definition of the top window of the program, including the menu bar, the
toolbar (if any), the central widget, bottom progress bar and status area.

In particular, the progress bar and the status area are the kind of things that the
plugins will be importing - or at least wanting to update - regularly. They are defined
as global aobject singletons such that even though an instance is created once, such an
instance can be access directly from the class anywhere else where you import the class.
"""
from __future__ import annotations

import itertools
from typing import Dict, List, Optional

import wx

from .logging import logger
from .plugins import KNOWN_PLUGINS, MenuTool, PluginBase, load_plugins


class StatusBar(wx.StatusBar):
    """
    Singleton class to manage the top level status and progress bar.

    It provides two fields:
        - field 0: Automatic display of menu and tools descriptions as well as custom
            status messages
        - field 1: Holds the progress bar. Do not use it for displaying text.

    Use 'StatusBar().SomeMethod` to manage the status bar messages and properties. See
    'wx.StatusBar' for more information about the options available.

    Use `StatusBar().progress_bar.SomeMethod` to manage the progress bar properties.
    See 'wx.Gauge' for more information about the options available.
    """

    _instance: Optional[StatusBar] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = wx.StatusBar.__new__(cls)
        return cls._instance

    def __init__(self, *args, progress_bar_width: int = 150, **kwargs):
        super(StatusBar, self).__init__(*args, **kwargs)
        self.SetFieldsCount(2, (-1, progress_bar_width))
        self.progress_bar = wx.Gauge(
            self,
            wx.ID_ANY,
            size=(progress_bar_width, 10),
            style=wx.GA_HORIZONTAL | wx.GA_SMOOTH,
        )
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, -1, ""), 1, wx.ALL)
        sizer.Add(self.progress_bar, 0, wx.ALL, 10)
        self.SetSizer(sizer)
        self.Layout()

    def SetStatusWidths(self, width: int):
        """Ensures that progress bar is resized if fields are resized.

        Args:
            width: Width of the progress bar.
        """
        super(StatusBar, self).SetStatusWidths((-1, width))
        self.progress_bar.SetSize(self.GetStatusWidth(1), 10)


class MainWindow(wx.Frame):
    def __init__(
        self,
        parent,
        title: str,
        notebook_layout: bool = True,
        tab_style: int = wx.NB_TOP,
    ):
        super(MainWindow, self).__init__(parent, title=title)
        self.notebook_layout = notebook_layout
        self.tab_style = tab_style
        self.SetStatusBar(StatusBar(self))

    def populate_window(self):
        """Adds menu items, tools and other widgets in plugins to the main window."""
        if self.notebook_layout:
            self._make_notebook(self.tab_style)
        else:
            self._make_central_widget()
        self._make_toolbar()
        self._make_menubar()
        self.SetInitialSize(wx.Size(800, 600))

    def _make_menubar(self) -> None:
        """Create the menu bar from the entries provided by the widgets."""
        # Collecting the menu entries
        entries = itertools.chain.from_iterable(
            [view().menu_entries() for view in KNOWN_PLUGINS]
        )

        # Creating the menus
        menus = dict()
        for entry in entries:
            if entry.menu not in menus:
                menus[entry.menu] = wx.Menu()

            menu_entry = menus[entry.menu].Append(
                entry.id, entry.text, entry.description, entry.kind
            )

            if entry.callback is not None:
                self.Bind(wx.EVT_MENU, entry.callback, menu_entry)

        # Creating the menubar.
        menu_bar = wx.MenuBar()
        for name, item in menus.items():
            menu_bar.Append(item, name)

        # Adding the MenuBar to the Frame content.
        self.SetMenuBar(menu_bar)

    def _make_toolbar(self):
        """Create the tool bar from the entries provided by the widgets."""
        # Collect tools
        tools = itertools.chain.from_iterable(
            [view().toolbar_items() for view in KNOWN_PLUGINS]
        )

        # Including the tools
        toolbar = self.CreateToolBar()
        for tool in tools:
            item = toolbar.AddTool(
                tool.id, tool.text, tool.bitmap, tool.short_help, tool.kind
            )

            if tool.callback is not None:
                self.Bind(wx.EVT_MENU, tool.callback, item)

        toolbar.Realize()

    def _make_notebook(self, tab_style: int = wx.NB_TOP) -> None:
        """Create the central widget of the window as a notebook.

        A notebook is created as the central widget and any other view provided by the
        plugins is added as new page. Finally, the first page is selected.

        Args:
            tab_style: integer indicating the position of the tabs. Valid values (OS
                dependent) are wx.NB_TOP, wx.NB_LEFT, wx.NB_RIGHT, wx.NB_BOTTOM,
                wx.NB_FIXEDWIDTH, wx.NB_MULTILINE and wx.NB_NOPAGETHEME.
        """
        self.notebook = wx.Notebook(self, style=tab_style)

        # Collect tabs
        tabs = itertools.chain.from_iterable(
            [view().tabs(self.notebook) for view in KNOWN_PLUGINS]
        )

        # Add tabs to notebook
        for tab in sorted(tabs, key=lambda x: x.order):
            self.notebook.AddPage(tab.page, tab.text, tab.select, tab.imageId)

        if self.notebook.PageCount > 0:
            self.notebook.SetSelection(0)

    def _make_central_widget(self) -> None:
        """Create the central widget of the window.

        Such a central widget is taken from the plugins. Exactly one central widget
        needs to be provided between all plugins.

        Raises:
            ValueError: If the number of central widgets found is not 1.
        """
        widget = [
            v for v in [view().central(self) for view in KNOWN_PLUGINS] if v is not None
        ]

        if len(widget) != 1:
            raise ValueError(
                f"Exactly 1 central widget needs to be provided. {len(widget)} given."
            )


class BuiltInActions(PluginBase):
    """Actions and features builtin with the core window."""

    def menu_entries(self) -> List[MenuTool]:
        return [
            MenuTool(
                menu="File",
                id=wx.ID_EXIT,
                text="Exit",
                description="Terminate application",
            ),
        ]


_tab_location: Dict[str, int] = {
    "top": wx.NB_TOP,
    "bottom": wx.NB_BOTTOM,
    "left": wx.NB_LEFT,
    "right": wx.NB_RIGHT,
}


class MainApp(wx.App):
    def __init__(
        self,
        *args,
        title: str,
        plugins_list: Optional[List[str]] = None,
        notebook_layout: bool = True,
        tab_style: str = "top",
        **kwargs,
    ):
        self.title = title
        self.plugins_list = plugins_list if plugins_list is not None else []
        self.notebook_layout = notebook_layout
        try:
            self.tab_style = _tab_location[tab_style]
        except KeyError:
            logger.warning(
                f"Invalid tab_style '{tab_style}'. Valid values are "
                f"{list(_tab_location.keys())}. Defaulting to 'top'"
            )
            self.tab_style = _tab_location["top"]

        super(MainApp, self).__init__(*args, **kwargs)

    def OnInit(self) -> bool:
        self.SetAppName(self.title)
        window = MainWindow(None, self.title, self.notebook_layout, self.tab_style)
        self.SetTopWindow(window)

        load_plugins(self.plugins_list)
        window.populate_window()
        window.Show(True)

        return True
