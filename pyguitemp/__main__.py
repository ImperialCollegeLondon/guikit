"""
The entry point of the program. It launches the main application - i.e. it starts
whatever represents the mainloop in the chosen GUI toolkit.
"""
from . import APP_NAME
from .logging import logger
from .core import MainApp
from .config import PLUGINS, AUTO_PLUGINS, APP_LONG_NAME, NOTEBOOK_LAYOUT, TAB_STYLE

logger.app_name = APP_NAME

app = MainApp(
    title=APP_LONG_NAME,
    plugins_list=PLUGINS + AUTO_PLUGINS,
    notebook_layout=NOTEBOOK_LAYOUT,
    tab_style=TAB_STYLE,
)
app.MainLoop()
