"""
The entry point of the program. It launches the main application - i.e. it starts
whatever represents the mainloop in the chosen GUI toolkit.
"""
import wx

from . import APP_NAME
from .core import MainApp
from .logging import logger
from .plugins import collect_builtin_extensions

logger.app_name = APP_NAME

app = MainApp(
    title=APP_NAME,
    plugins_list=collect_builtin_extensions(),
    notebook_layout=True,
    tab_style=wx.NB_TOP,
)
app.MainLoop()
