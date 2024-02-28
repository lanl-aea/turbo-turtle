from unittest.mock import patch

import pytest

from turbo_turtle import main
from turbo_turtle import _settings


def test_docs():
    """Test the docs subcommand behavior"""
    with patch("webbrowser.open") as mock_webbrowser_open, \
         patch("pathlib.Path.exists", return_value=True):
        main._docs()
        # Make sure the correct type is passed to webbrowser.open
        mock_webbrowser_open.assert_called_with(str(_settings._installed_docs_index))

    with patch("webbrowser.open") as mock_webbrowser_open, \
         patch("pathlib.Path.exists", return_value=True):
        main._docs(print_local_path=True)
        mock_webbrowser_open.assert_not_called()

    # Test the "unreachable" exit code used as a sign-of-life that the installed package structure assumptions in
    # _settings.py are correct.
    with patch("webbrowser.open") as mock_webbrowser_open, \
         patch("pathlib.Path.exists", return_value=False), \
         pytest.raises(SystemExit):
        main._docs(print_local_path=True)
        mock_webbrowser_open.assert_not_called()

def test_print_abaqus_module():
    """Test the print-abaqus-module subcommand behavior"""
    fake_subcommand = "fake_subcommand"
    expected_output = f"{_settings._abaqus_python_abspath}/{fake_subcommand}.py"
    returned_output = main._print_abaqus_module_location(fake_subcommand)
    assert expected_output == returned_output
