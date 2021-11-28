import pytest
import wx


@pytest.fixture()
def window():
    app = wx.App()
    frame = wx.Frame(None)
    yield frame
    wx.CallAfter(frame.Close)
    app.MainLoop()


@pytest.fixture()
def main_window():
    from guikit.core import MainWindow

    app = wx.App()
    frame = MainWindow(None, "My App")
    yield frame
    wx.CallAfter(frame.Close)
    app.MainLoop()


@pytest.fixture()
def plugin():
    from typing import List

    import wx

    from guikit.plugins import MenuTool, PluginBase

    class ExamplePlugin(PluginBase):
        def central(self, parent=None) -> wx.Window:
            return wx.TextCtrl(parent, style=wx.TE_MULTILINE)

        def toolbar_items(self) -> List[MenuTool]:
            return [
                MenuTool(
                    id=wx.ID_STOP,
                    text="Exit",
                    short_help="Terminate application",
                    bitmap=wx.ArtProvider.GetBitmap(
                        wx.ART_QUIT, wx.ART_TOOLBAR, wx.Size(50, 50)
                    ),
                ),
            ]

    return ExamplePlugin


@pytest.fixture()
def empty_plugin():
    from guikit.plugins import PluginBase

    class EmptyPlugin(PluginBase):
        pass

    return EmptyPlugin
