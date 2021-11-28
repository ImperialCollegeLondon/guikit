import wx

from guikit.plugins import MenuTool, PluginBase


class MenuEntryPlugin(PluginBase):
    def menu_entries(self):
        save = MenuTool(
            menu="File",
            text="Save data",
            description="Save selected data into disk",
            callback=save_data,
        )
        load = MenuTool(
            menu="File",
            text="Load data",
            description="Load new data from disk",
            callback=load_data,
        )
        return [save, load]


def save_data(_):
    dial = wx.MessageDialog(
        None,
        "You click the 'Save data' menu entry",
        "Saving data...",
        wx.OK | wx.STAY_ON_TOP | wx.CENTRE,
    )
    dial.ShowModal()


def load_data(_):
    dial = wx.MessageDialog(
        None,
        "You click the 'Load data' menu entry",
        "Loading data...",
        wx.OK | wx.STAY_ON_TOP | wx.CENTRE,
    )
    dial.ShowModal()
