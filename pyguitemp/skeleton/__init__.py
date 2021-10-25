from pathlib import Path

from pyguitemp.logging import Logger

VERSION = "0.0.1"
APP_NAME = Path(__file__).parent.stem
logger = Logger(APP_NAME)
