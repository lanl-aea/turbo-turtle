from unittest.mock import patch
from contextlib import nullcontext as does_not_raise

import pytest

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


def test_search_commands():
    with patch("shutil.which", return_value=None) as shutil_which:
        command_abspath = main._search_commands(["notfound"])
        assert command_abspath is None

    with patch("shutil.which", return_value="found") as shutil_which:
        command_abspath = main._search_commands(["found"])
        assert command_abspath == "found"


find_command = {
    "first": (
        ["first", "second"], "first", does_not_raise()
    ),
    "second": (
        ["first", "second"], "second", does_not_raise()
    ),
    "none": (
        ["first", "second"], None, pytest.raises(FileNotFoundError)
    ),
}


@pytest.mark.parametrize("options, found, outcome",
                         find_command.values(),
                         ids=find_command.keys())
def test_find_command(options, found, outcome):
    with patch("turbo_turtle.main._search_commands", return_value=found), outcome:
        try:
            command_abspath = main._find_command(options)
            assert command_abspath == found
        finally:
            pass
