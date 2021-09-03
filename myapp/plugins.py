"""
Contains all the machinery to register and load plugins.
"""
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import List, Type, Callable, Optional
import wx


KNOWN_PLUGINS: List[Type[PluginBase]] = []
"""List of plugins registered as subclasses of PluginBase."""


@dataclass
class MenuTool:
    """Compiles the information required to add menu and toolbar items."""

    menu: str = ""
    id: int = wx.ID_ANY
    text: str = ""
    description: str = ""
    short_help: str = ""
    callback: Optional[Callable[[wx.Event], None]] = None
    kind: wx.ItemKind = wx.ITEM_NORMAL
    bitmap: Optional[wx.Bitmap] = None


@dataclass
class Tab:
    """Compiles the information required to define add tabs."""

    page: wx.Window
    text: str
    select: bool = False
    imageId: int = wx.NO_IMAGE


class PluginBase(ABC):
    """
    Base class that defines the required API that all the views of the different plugins
    will need to provide.
    """

    def __init_subclass__(cls: Type[PluginBase]):
        if cls not in KNOWN_PLUGINS:
            KNOWN_PLUGINS.append(cls)

    @staticmethod
    def menu_entries() -> List[MenuTool]:
        """Return a list of menu entries provided by this plugin.

        The items of the list must be MenuTool objects.

        Returns:
            A list of MenuTool objects provided by this plugin to be added to the
            application menu bar.
        """
        return []

    @staticmethod
    def toolbar_items() -> List[MenuTool]:
        """Return a list of toolbar items provided by this plugin.

        The items of the list must be MenuTool objects.

        Returns:
            A list of MenuTool objects provided by this plugin to be added to the
            application toolbar.
        """
        return []

    @staticmethod
    def tabs(parent) -> List[Tab]:
        """Create and return the list of tabs provided by this plugin.

        The elements of the list must be Tab objects.

        Args:
            parent: The application notebook, to be used as parent during the creation
            of the tabs.

        Returns:
            A list of Tab objects provided by this plugin to be added to the application
            notebook.
        """
        return []

    @staticmethod
    def central(parent) -> Optional[wx.Window]:
        """Central widget provided by this plugin.

        Args:
            parent: The main window, to be used as parent during the creation of the
            widget.

        Returns:
            None (if no central widget provided) or any object derived from
            wx.MainWindow (pretty much, any widget).
        """
        return None
