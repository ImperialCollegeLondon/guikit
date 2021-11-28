import wx

from guikit.plugins import PluginBase, Tab


class NotebookPlugin(PluginBase):
    def tabs(self, parent):
        text1 = Tab(
            page=wx.TextCtrl(parent, style=wx.TE_MULTILINE),
            text="Text area",
        )
        text2 = Tab(
            page=wx.TextCtrl(parent, style=wx.TE_MULTILINE),
            text="A second text area",
        )
        return [text1, text2]
