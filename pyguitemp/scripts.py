from __future__ import annotations

import argparse
import importlib
import inspect
from abc import ABC, abstractmethod
from pathlib import Path
from shutil import copytree
from typing import Dict, List

from . import APP_NAME
from . import config as dconfig
from .core import MainApp
from .logging import logger
from .plugins import collect_builtin_extensions

logger.app_name = APP_NAME


def run():
    """Runs guikit as an application, loading all the plugins available."""
    frame = inspect.stack()[1]
    caller_file = Path(frame[0].f_code.co_filename)
    config_file = caller_file.parent / "config.py"

    if not config_file.exists():
        raise RuntimeError(f"Configuration file '{config_file}' not found!")

    config = importlib.import_module(f"{caller_file.parent.stem}.config")

    title = config.APP_LONG_NAME if "APP_LONG_NAME" in dir(config) else "My App"
    plug = config.PLUGINS if "PLUGINS" in dir(config) else []
    autoplugins = config.AUTO_PLUGINS if "AUTO_PLUGINS" in dir(config) else []
    nb_layout = (
        config.NOTEBOOK_LAYOUT
        if "NOTEBOOK_LAYOUT" in dir(config)
        else dconfig.NOTEBOOK_LAYOUT
    )
    tab_style = config.TAB_STYLE if "TAB_STYLE" in dir(config) else dconfig.TAB_STYLE

    all_plugins = plug + [p for p in autoplugins if p not in plug]

    app = MainApp(
        title=title,
        plugins_list=all_plugins,
        notebook_layout=nb_layout,
        tab_style=tab_style,
    )
    app.MainLoop()


def _init_repo(path: Path, name: str):
    """Initialises repository with the files/folders required to use guikit.

    This is done by copying the skeleton repository structure within guikit to the
    desired location.

    Args:
        path: Where the repository should be initialized. Default: current.
        name: Name of the application.
    """
    full_dir = path / name
    logger.info(f"Initialising '{name}' in `{full_dir}`...")
    copytree(Path(__file__).parent / "skeleton", full_dir)


def _list_plugins() -> None:
    """Lists all plugins available in guikit that the user can copy."""
    plug = [ext.split(".")[-1] for ext in collect_builtin_extensions()]
    for p in plug:
        print(p)


def _copy_plugin(name: List[str], target: Path) -> None:
    """Lists all plugins available in guikit that the user can copy.

    Args:
        name: List of plugins to copy.
        target: Root destination for the plugins.
    """
    available = [ext.split(".")[-1] for ext in collect_builtin_extensions()]
    root = Path(__file__).parent / "extensions"

    for p in name:
        if p not in available:
            raise ValueError(
                f"Plugin '{p}' unknown. Run with '-l' flag for a list of valid values"
            )

        logger.info(f"Copying '{p}' into `{target}`...")
        copytree(root / p, target / p)


class SubCommand(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    @abstractmethod
    def run(self, args: argparse.Namespace):
        pass


class RunSubCommand(SubCommand):
    def __init__(self):
        super().__init__("run", f"Run '{APP_NAME}' as a standalone app.")

    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    def run(self, args: argparse.Namespace):
        run()


class InitSubCommand(SubCommand):
    def __init__(self):
        super().__init__(
            "init", "Initialises the current directory with an skeleton of a GUI app"
        )

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "name",
            type=str,
            help="Name of the app. To be used as package name.",
        )
        parser.add_argument(
            "-t",
            "--target",
            default=".",
            type=str,
            help="Target location for the app. Default: Current directory.",
        )

    def run(self, args: argparse.Namespace):
        _init_repo(Path(args.target).absolute(), args.name)


class PluginSubCommand(SubCommand):
    def __init__(self):
        super().__init__(
            "plugin", "Brings exisitng plugins in guikit to the application."
        )

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="Lists the plugins available.",
        )
        parser.add_argument(
            "-n",
            "--name",
            default="",
            type=str,
            help="Lists of comma-separated names of the plugins to copy.",
        )
        parser.add_argument(
            "-t",
            "--target",
            default=".",
            type=str,
            help="Target location for the plugin. Default: Current directory.",
        )

    def run(self, args: argparse.Namespace):
        if args.list:
            _list_plugins()
        elif args.name != "":
            name = args.name.split(",")
            target = Path(args.target).absolute()
            _copy_plugin(name, target)
        else:
            print("Nothing to do...")


_SUB_COMMANDS: List[SubCommand] = [
    RunSubCommand(),
    InitSubCommand(),
    PluginSubCommand(),
]

_SUB_COMMAND_BY_NAME: Dict[str, SubCommand] = {
    sub_command.name: sub_command for sub_command in _SUB_COMMANDS
}


def _parse_args(argv: List[str] = None) -> argparse.Namespace:
    """Parse the input arguments list populating the relevant subcommands

    Args:
        argv: List of arguments

    Returns:
        The namespace containing the relevant sub command information and arguments.
    """
    parser = argparse.ArgumentParser(prog=APP_NAME)
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True
    for sub_command in _SUB_COMMANDS:
        sub_parser = subparsers.add_parser(
            sub_command.name, help=sub_command.description
        )
        sub_command.add_arguments(sub_parser)

    return parser.parse_args(argv)


def main(argv: List[str] = None):
    """Main entry point for guikit, calling the relevant subcommands.

    Args:
        argv: List of input arguments, including subcommand.

    Returns:

    """
    args = _parse_args(argv)
    _SUB_COMMAND_BY_NAME[args.command].run(args)
