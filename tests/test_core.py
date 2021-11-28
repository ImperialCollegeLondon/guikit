from unittest.mock import MagicMock, patch

import pytest


class TestStatusBar:
    def test_set_status_widths(self, window):
        import wx

        from guikit.core import StatusBar

        bar = StatusBar(window)
        assert isinstance(bar.progress_bar, wx.Gauge)

        expected = 300
        bar.SetStatusWidths(expected)
        assert bar.GetStatusWidth(1) == expected
        assert bar.progress_bar.GetSize()[0] == expected


class TestMainWindow:
    def test_populate_window(self, main_window):
        main_window._make_notebook = MagicMock()
        main_window._make_toolbar = MagicMock()
        main_window._make_menubar = MagicMock()
        main_window._make_central_widget = MagicMock()

        main_window.populate_window()
        main_window._make_menubar.assert_called_once()
        main_window._make_toolbar.assert_called_once()
        main_window._make_notebook.assert_called_once()
        main_window._make_central_widget.assert_not_called()

        main_window.notebook_layout = False
        main_window.populate_window()
        main_window._make_central_widget.assert_called_once()

    def test__make_menubar(self, main_window):
        main_window._make_menubar()
        menus = main_window.GetMenuBar().GetMenus()
        assert len(menus) > 0
        assert menus[0][1] == "File"

    @pytest.mark.xfail
    def test__make_toolbar(self, main_window):
        main_window._make_toolbar()
        assert main_window.GetToolBar().GetToolsCount() == 0

    @pytest.mark.xfail
    def test__make_notebook(self, main_window):
        import wx

        main_window._make_notebook()
        assert isinstance(main_window.notebook, wx.Notebook)
        assert main_window.notebook.PageCount == 0

    @pytest.mark.xfail
    def test__make_central_widget(self, main_window):
        import wx

        from guikit.plugins import PluginBase

        with pytest.raises(ValueError):
            main_window._make_central_widget()

        class SomePlugin(PluginBase):
            def central(self, parent):
                return wx.TextCtrl(parent, style=wx.TE_MULTILINE)

        main_window._make_central_widget()

        class SomeOtherPlugin(PluginBase):
            def central(self, parent):
                return wx.TextCtrl(parent, style=wx.TE_MULTILINE)

        with pytest.raises(ValueError):
            main_window._make_central_widget()


class TestBuiltInActions:
    def test_menu_entries(self):
        from guikit.core import BuiltInActions
        from guikit.plugins import MenuTool

        entries = BuiltInActions().menu_entries()
        assert len(entries) > 0
        assert all([isinstance(item, MenuTool) for item in entries])
        assert entries[0].menu == "File"


class TestMainApp:
    def test_on_init(self, caplog):
        import wx

        with patch("guikit.core.MainWindow.Show", MagicMock()):
            from guikit.core import MainApp, MainWindow

            app = MainApp(title="Some App", tab_style="a corner")
            assert "Invalid tab_style" in caplog.messages[-1]
            assert app.tab_style == wx.NB_TOP
            assert isinstance(app.GetTopWindow(), MainWindow)

            wx.CallAfter(app.GetTopWindow().Close)
            app.MainLoop()
