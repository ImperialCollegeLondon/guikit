class TestStatusBar:
    def test_set_status_widths(self, window):
        import wx
        from myapp.core import StatusBar

        bar = StatusBar(window)
        assert isinstance(bar.progress_bar, wx.Gauge)

        expected = [300, -1, 300]
        bar.SetStatusWidths(expected)
        assert all([bar.GetStatusWidth(i) == v for i, v in enumerate(expected)])
        assert bar.progress_bar.GetSize()[0] == expected[-1]


class TestMainWindow:
    def test_populate_window(self):
        assert False

    def test__make_menubar(self):
        assert False

    def test__make_toolbar(self):
        assert False

    def test__make_notebook(self):
        assert False

    def test__make_central_widget(self):
        assert False


class TestBuiltInActions:
    def test_menu_entries(self):
        from myapp.core import BuiltInActions
        from myapp.plugins import MenuTool

        entries = BuiltInActions().menu_entries()
        assert len(entries) > 0
        assert all([isinstance(item, MenuTool) for item in entries])
        assert entries[0].menu == "File"


class TestMainApp:
    def test_on_init(self):
        assert False
