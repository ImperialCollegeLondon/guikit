from unittest.mock import MagicMock, patch


def test_run_app():
    class App:
        MainLoop = MagicMock()

    with patch("pyguitemp.scripts.MainApp", MagicMock(return_value=App)):
        from pyguitemp.scripts import MainApp, _run_app

        _run_app()

        MainApp.assert_called_once()
        App.MainLoop.assert_called_once()


def test_init_repo(tmpdir):
    with patch("pyguitemp.scripts.copytree", MagicMock()):
        from pathlib import Path

        from pyguitemp.scripts import _init_repo, copytree

        skeleton = Path(__file__).parent.parent / "pyguitemp" / "skeleton"
        _init_repo(tmpdir, "my_app")
        copytree.assert_called_once_with(skeleton, tmpdir / "my_app")


class TestRunSubCommand:
    def test_add_arguments(self):
        import argparse

        from pyguitemp.scripts import RunSubCommand

        command = RunSubCommand()
        parser = argparse.ArgumentParser()
        command.add_arguments(parser)
        assert set([a.dest for a in parser._actions]) == {"help"}

    def test_run(self):
        import argparse

        with patch("pyguitemp.scripts._run_app", MagicMock()):
            from pyguitemp.scripts import RunSubCommand, _run_app

            command = RunSubCommand()
            command.run(argparse.Namespace())
            _run_app.assert_called_once()


class TestInitSubCommand:
    def test_add_arguments(self):
        import argparse

        from pyguitemp.scripts import InitSubCommand

        command = InitSubCommand()
        parser = argparse.ArgumentParser()
        command.add_arguments(parser)
        assert set([a.dest for a in parser._actions]) == {"help", "name", "target"}

    def test_run(self):
        import argparse

        with patch("pyguitemp.scripts._init_repo", MagicMock()):
            from pyguitemp.scripts import InitSubCommand, _init_repo

            command = InitSubCommand()
            args = argparse.Namespace(target="", name="")
            command.run(args)
            _init_repo.assert_called_once()


def test_parse_args():

    with patch("argparse.ArgumentParser.parse_args", MagicMock()):
        from pyguitemp.scripts import _SUB_COMMANDS, _parse_args

        for command in _SUB_COMMANDS:
            command.add_arguments = MagicMock()

        _parse_args()

        for command in _SUB_COMMANDS:
            command.add_arguments.assert_called_once()


def test_main():
    class Namespace:
        command = "run"

    with patch("pyguitemp.scripts._parse_args", MagicMock(return_value=Namespace)):
        from pyguitemp.scripts import _SUB_COMMAND_BY_NAME, _parse_args, main

        _SUB_COMMAND_BY_NAME[Namespace.command].run = MagicMock()

        main()

        _parse_args.assert_called_once()
        _SUB_COMMAND_BY_NAME[Namespace.command].run.assert_called_once()
