"""
The entry point of the program. It launches the main application - i.e. it starts
whatever represents the mainloop in the chosen GUI toolkit.
"""
from pyguitemp.core import MainApp

from .config import APP_LONG_NAME, AUTO_PLUGINS, NOTEBOOK_LAYOUT, PLUGINS, TAB_STYLE

app = MainApp(
    title=APP_LONG_NAME,
    plugins_list=PLUGINS + AUTO_PLUGINS,
    notebook_layout=NOTEBOOK_LAYOUT,
    tab_style=TAB_STYLE,
)
app.MainLoop()
