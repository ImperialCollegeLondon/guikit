"""
The entry point of the program. It launches the main application - i.e. it starts
whatever represents de mainloop in the chosen GUI toolkit.
"""
from . import APP_NAME
from .plugins import collect_builtin_extensions
from .core import MainApp
import wx

app = MainApp(
    title=APP_NAME,
    plugins_list=collect_builtin_extensions(),
    notebook_layout=True,
    tab_style=wx.NB_TOP,
)
app.MainLoop()
