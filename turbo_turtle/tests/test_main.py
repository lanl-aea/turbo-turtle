from unittest.mock import patch

from turbo_turtle import main
from turbo_turtle import _settings


def test_docs():
    with patch("webbrowser.open") as mock_webbrowser_open, \
         patch("sys.exit") as mock_exit, \
         patch("pathlib.Path.exists", return_value=True):
        main._docs()
        # Make sure the correct type is passed to webbrowser.open
        mock_webbrowser_open.assert_called_with(str(_settings._installed_docs_index))
        mock_exit.assert_not_called()

    with patch("webbrowser.open") as mock_webbrowser_open, \
         patch("sys.exit") as mock_exit, \
         patch("pathlib.Path.exists", return_value=True):
        main._docs(print_local_path=True)
        mock_webbrowser_open.assert_not_called()
        mock_exit.assert_not_called()

    # Test the "unreachable" exit code used as a sign-of-life that the installed package structure assumptions in
    # _settings.py are correct.
    with patch("webbrowser.open") as mock_webbrowser_open, \
         patch("sys.exit") as mock_exit, \
         patch("pathlib.Path.exists", return_value=False):
        main._docs(print_local_path=True)
        mock_webbrowser_open.assert_not_called()
        mock_exit.assert_called()


def test_check_for_command():
    with patch("shutil.which", return_value=None) as shutil_which, \
         patch("sys.exit") as sys_exit:
        command_abspath = main._check_for_command("notfound")
        sys_exit.assert_called_once_with(2)

    with patch("shutil.which", return_value="found") as shutil_which, \
         patch("sys.exit") as sys_exit:
        command_abspath = main._check_for_command("found")
        assert command_abspath == "found"
        sys_exit.assert_not_called()
