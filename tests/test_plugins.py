from unittest.mock import MagicMock, patch


class TestPluginBase:
    def test_plugin_registration(self, plugin):
        from guikit.plugins import KNOWN_PLUGINS

        assert plugin in KNOWN_PLUGINS

    def test_menu_entries(self, empty_plugin):
        """Dummy tests to check default outputs"""
        assert empty_plugin().menu_entries() == []

    def test_toolbar_items(self, empty_plugin):
        """Dummy tests to check default outputs"""
        assert empty_plugin().toolbar_items() == []

    def test_tabs(self, empty_plugin):
        """Dummy tests to check default outputs"""
        assert empty_plugin().tabs() == []

    def test_central(self, empty_plugin):
        """Dummy tests to check default outputs"""
        assert empty_plugin().central() is None


def test_collect_plugins():
    from pathlib import Path

    from guikit.plugins import collect_plugins

    this_file = Path(__file__)
    plugins = collect_plugins(this_file.parent)
    assert f"{this_file.parent.stem}.{this_file.stem}" in plugins

    plugins = collect_plugins(this_file.parent, package="some_package")
    assert f"some_package.{this_file.parent.stem}.{this_file.stem}" in plugins

    plugins = collect_plugins(this_file.parent, add_to_path=True)
    assert f"{this_file.stem}" in plugins


def test_collect_builtin_extensions():
    with patch("guikit.plugins.collect_plugins", MagicMock()):
        from guikit.plugins import collect_builtin_extensions, collect_plugins

        collect_builtin_extensions()
        collect_plugins.assert_called_once()


def test_load_plugins(caplog):
    with patch("importlib.import_module", MagicMock()):
        from importlib import import_module

        from guikit.plugins import load_plugins

        plugins = ["guikit.extensions.about_dialog"]
        load_plugins(plugins)
        import_module.assert_called()

    plugins.append("Wrong plugin")
    load_plugins(plugins)
    assert "Plugin 'Wrong plugin' could not be loaded." in caplog.messages[-1]
