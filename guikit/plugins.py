"""
Contains all the machinery to register and load plugins.
"""
from __future__ import annotations

import importlib
import inspect
import sys
from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional, Type

import wx

from .logging import logger

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
    order: int = 0


class PluginBase(ABC):
    """
    Base class that defines the required API that all the views of the different plugins
    will need to provide.
    """

    def __init_subclass__(cls: Type[PluginBase]):
        if cls not in KNOWN_PLUGINS:
            KNOWN_PLUGINS.append(cls)

    def menu_entries(self) -> List[MenuTool]:
        """Return a list of menu entries provided by this plugin.

        The items of the list must be MenuTool objects.

        Returns:
            A list of MenuTool objects provided by this plugin to be added to the
            application menu bar.
        """
        return []

    def toolbar_items(self) -> List[MenuTool]:
        """Return a list of toolbar items provided by this plugin.

        The items of the list must be MenuTool objects.

        Returns:
            A list of MenuTool objects provided by this plugin to be added to the
            application toolbar.
        """
        return []

    def tabs(self, parent=None) -> List[Tab]:
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

    def central(self, parent=None) -> Optional[wx.Window]:
        """Central widget provided by this plugin.

        Args:
            parent: The main window, to be used as parent during the creation of the
            widget.

        Returns:
            None (if no central widget provided) or any object derived from
            wx.MainWindow (pretty much, any widget).
        """
        return None


def collect_plugins(
    path: Path, package: Optional[str] = None, add_to_path: bool = False
) -> List[str]:
    """Collects the plugins from the given location.

    This function collects the modules and packages available in chosen location. If
    they are not directly importable by Python (i.e. they are not in the path), either
    the name of the containing package should be supplied or the add_to_path flag must
    be set to True.

    Eg. If path = "/some/location/with/tools/mytool", and "mytool" is an importable
    package with "import mytool", plugins within "mytool" folder will be included with
    no extra arguments.

    If "mytool" is not importable but "tools" is, i.e. 'import tools.mytool' works,
    then you should add "package='tools'".

    If neither "mytool" nor anything else in its path is importable, then the path can
    be added to the module's import path, sys.path, so the plugins within can be
    imported as "import plugin".

    Args:
        path: Directory to explore.
        package: Package in which the directory is contained.
        add_to_path: If the directory should be added to the import path.

    Returns:
        List of modules and packages to be imported in the form
        "package.subpackage.plugin", where "plugin" can be a module (a python file) or
        a package itself (a folder containing a __init__.py file).
    """
    if add_to_path:
        sys.path.insert(1, str(path))
        pkg = ""
    else:
        pkg = f"{path.stem}." if package is None else f"{package}.{path.stem}."

    plugin_names = []
    for p in path.glob("*.py"):
        if not p.stem.startswith("__"):
            plugin_names.append(f"{pkg}{p.stem}")

    for p in path.glob("*/"):
        if p.is_dir() and (p / "__init__.py").exists():
            plugin_names.append(f"{pkg}{p.stem}")

    return plugin_names


def collect_builtin_extensions():
    """Search for plugins to be loaded in the "extensions" subfolder.

    These plugins can be single modules (simple_plugin.py) or more complex modules
    defined as packages (i.e. they are folders with a __init__.py file).

    Returns:
        A list of plugins names to be loaded.
    """
    frame = inspect.stack()[1]
    caller_file = Path(frame[0].f_code.co_filename)
    extensions = caller_file.parent / "extensions"
    return collect_plugins(extensions, caller_file.parent.stem)


def load_plugins(plugin_list: List[str]):
    """Loads the plugins of the list.

    Args:
        plugin_list: A list of plugins to be loaded.
    """
    for plugin in plugin_list:
        try:
            importlib.import_module(plugin)
        except ModuleNotFoundError as err:
            logger.warning(f"Plugin '{err.name}' could not be loaded. {err}")
