"""
Contains all the custom machinery for dealing with logging in the program. It should
allow for new handlers to be added if any plugin requires it.
"""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from . import APP_NAME


def app_dir(app_name: str = APP_NAME) -> Path:
    """Finds the application data directory for the current platform.

    If it does not exists, it creates the required directory tree.

    Returns:
        The path to the root app directory.
    """
    if sys.platform == "win32":
        path = Path.home() / "AppData" / "Local" / app_name
    elif sys.platform == "darwin":
        path = Path.home() / "Library" / "Application Support" / app_name
    else:
        path = Path.home() / f".{app_name}"

    _create_tree(path)
    return path


def _create_tree(path: Path) -> None:
    """Creates the app directory tree.

    Args:
        path: Where the directory tree must be created
    """
    os.makedirs(str(path), exist_ok=True)
    os.makedirs(str(path / "logs"), exist_ok=True)


class Logger:
    def __init__(self, app_name: str = APP_NAME):
        self._logger: Optional[logging.Logger] = None
        self.app_name = app_name

    @property
    def logger(self) -> logging.Logger:
        """Interface to the underlying logger.

        The logger is created automatically the first time it is used.

        Returns:
            A Logger object.
        """
        if not isinstance(self._logger, logging.Logger):
            self._logger = logging.getLogger("root")
            self._logger.setLevel(logging.DEBUG)

            self.set_console_handler()
            self.set_file_handler()

        return self._logger

    def __getattr__(self, item):
        return getattr(self.logger, item)

    def set_console_handler(self):
        """Sets a handler to print the log to the terminal."""
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create and add formatter to handle
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s(%(lineno)d): %("
            "message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
        ch.setFormatter(formatter)

        # add ch to logger
        self._logger.addHandler(ch)

    def set_file_handler(self):
        """Sets a handler to print the log to a file in the app directory."""
        filename = (
            app_dir(self.app_name)
            / "logs"
            / f"{datetime.now().strftime('%Y%m%d_%H-%M-%S')}.log"
        )
        ch = logging.FileHandler(str(filename))
        ch.setLevel(logging.INFO)

        # create and add formatter to handle
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y/%m/%d %H:%M:%S"
        )
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)


logger = Logger()
"""Global logger for the application"""
