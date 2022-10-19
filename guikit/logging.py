"""
Contains all the custom machinery for dealing with logging in the program. It should
allow for new handlers to be added if any plugin requires it.
"""
import logging
from datetime import datetime
from typing import Optional

from platformdirs import user_log_path

from . import APP_NAME


class Logger:
    def __init__(self, app_name: str = APP_NAME, app_author: Optional[str] = None):
        self._logger: Optional[logging.Logger] = None
        self.app_name = app_name
        self.app_author = app_author

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
        log_path = user_log_path(self.app_name, self.app_author)
        log_path.mkdir(parents=True, exist_ok=True)

        filename = log_path / f"{datetime.now().strftime('%Y%m%d_%H-%M-%S')}.log"
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
