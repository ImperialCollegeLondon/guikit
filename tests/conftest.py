import wx
import pytest


@pytest.fixture()
def window():
    app = wx.App()
    frame = wx.Frame(None)
    yield frame
    wx.CallAfter(frame.Close)
    app.MainLoop()


@pytest.fixture()
def main_window():
    from myapp.core import MainWindow

    app = wx.App()
    frame = MainWindow(None, "My App")
    yield frame
    wx.CallAfter(frame.Close)
    app.MainLoop()


@pytest.fixture()
def menu_tool():
    import wx
    from myapp.plugins import MenuTool

    return (
        MenuTool(
            id=wx.ID_STOP,
            text="Exit",
            short_help="Terminate application",
            bitmap=wx.ArtProvider.GetBitmap(
                wx.ART_QUIT, wx.ART_TOOLBAR, wx.Size(50, 50)
            ),
        ),
    )
