"""
Contains the definition of the top window of the program, including the menu bar, the
toolbar (if any), the central widget, bottom progress bar and status area.

In particular, the progress bar and the status area are the kind of things that the
plugins will be importing - or at least wanting to update - regularly. They are defined
as global aobject singletons such that even though an instance is created once, such an
instance can be access directly from the class anywhere else where you import the class.
"""
from __future__ import annotations

from typing import List
import itertools
import wx

from .plugins import KNOWN_PLUGINS, PluginBase, MenuTool


class Window(wx.Frame):
    def __init__(
        self,
        parent,
        title: str,
        notebook_layout: bool = True,
        tab_style: int = wx.NB_TOP,
    ):
        super(Window, self).__init__(parent, title=title)

        if notebook_layout:
            self._make_notebook(tab_style)
        else:
            self._make_central_widget()
        self._make_status_bar()
        self._make_toolbar()
        self._make_menubar()

        self.Show(True)

    def _make_menubar(self) -> None:
        """Create the menu bar.

        An "Exit" entry in a "File" menu is created automatically. Any other entry is
        obtained from the plugins.
        """
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
        """

        Returns:

        """
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

    def _make_status_bar(self):
        """

        Returns:

        """
        self.CreateStatusBar()  # A StatusBar in the bottom of the window

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
        for tab in tabs:
            self.notebook.AddPage(*tab)

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

        if (n := len(widget)) != 1:
            raise ValueError(
                f"Exactly 1 central widget needs to be provided. {n} given."
            )


class BuiltInActions(PluginBase):
    """Actions and features builtin with the core window."""

    @staticmethod
    def menu_entries() -> List[MenuTool]:
        return [
            MenuTool(
                menu="File",
                id=wx.ID_EXIT,
                text="Exit",
                description="Terminate application",
            ),
        ]
