from __future__ import annotations

import argparse
from abc import ABC, abstractmethod
from pathlib import Path
from shutil import copytree
from typing import Dict, List

from . import APP_NAME
from .config import APP_LONG_NAME, AUTO_PLUGINS, NOTEBOOK_LAYOUT, PLUGINS, TAB_STYLE
from .core import MainApp
from .logging import logger

logger.app_name = APP_NAME


def _run_app():
    """Runs pyguitemp as an application, loading all the plugins available."""
    app = MainApp(
        title=APP_LONG_NAME,
        plugins_list=PLUGINS + AUTO_PLUGINS,
        notebook_layout=NOTEBOOK_LAYOUT,
        tab_style=TAB_STYLE,
    )
    app.MainLoop()


def _init_repo(path: Path, name: str):
    """Initialises repository with the files/folders required to use pyguitemp.

    This is done by copying the skeleton repository structure within pyguitemp to the
    desired location.

    Args:
        path: Where the repository should be initialized. Default: current.
        name: Name of the application.
    """
    full_dir = path / name
    logger.info(f"Initialising '{name}' in `{full_dir}`...")
    copytree(Path(__file__).parent / "skeleton", full_dir)


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
        _run_app()


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


_SUB_COMMANDS: List[SubCommand] = [RunSubCommand(), InitSubCommand()]

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
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True
    for sub_command in _SUB_COMMANDS:
        sub_parser = subparsers.add_parser(
            sub_command.name, help=sub_command.description
        )
        sub_command.add_arguments(sub_parser)

    return parser.parse_args(argv)


def main(argv: List[str] = None):
    """Main entry point for pyguitemp, calling the relevant subcommands.

    Args:
        argv: List of input arguments, including subcommand.

    Returns:

    """
    args = _parse_args(argv)
    _SUB_COMMAND_BY_NAME[args.command].run(args)
