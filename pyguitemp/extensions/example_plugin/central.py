import wx

from pyguitemp.plugins import PluginBase


class CentralPlugin(PluginBase):
    def central(self, parent):
        return wx.TextCtrl(parent, style=wx.TE_MULTILINE)
