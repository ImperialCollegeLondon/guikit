import wx

from guikit.plugins import MenuTool, PluginBase


class ToolbarPlugin(PluginBase):
    def toolbar_items(self):
        save = MenuTool(
            menu="File",
            text="Save data",
            description="Save selected data into disk",
            short_help="Save selected data into disk",
            bitmap=wx.ArtProvider.GetBitmap(
                wx.ART_FILE_SAVE, wx.ART_TOOLBAR, wx.Size(50, 50)
            ),
            callback=save_data,
        )
        load = MenuTool(
            menu="File",
            text="Load data",
            description="Load new data from disk",
            short_help="Load new data from disk",
            bitmap=wx.ArtProvider.GetBitmap(
                wx.ART_FILE_OPEN, wx.ART_TOOLBAR, wx.Size(50, 50)
            ),
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
