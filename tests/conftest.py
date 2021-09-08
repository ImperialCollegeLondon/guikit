import wx
import pytest


@pytest.fixture()
def window():
    app = wx.App()
    frame = wx.Frame(None)
    yield frame
    wx.CallAfter(frame.Close)
    app.MainLoop()
