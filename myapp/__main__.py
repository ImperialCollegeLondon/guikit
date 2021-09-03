"""
The entry point of the program. It launches the main application - i.e. it starts
whatever represents de mainloop in the chosen GUI toolkit.
"""
from myapp import APP_NAME
from myapp.core import MainApp
import wx

app = MainApp(title=APP_NAME, notebook_layout=True, tab_style=wx.NB_TOP)
app.MainLoop()
