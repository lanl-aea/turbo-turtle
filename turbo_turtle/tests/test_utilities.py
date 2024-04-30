from unittest.mock import patch
from contextlib import nullcontext as does_not_raise
import subprocess

import pytest

from turbo_turtle import _utilities


def test_search_commands():
    """Test :meth:`turbo_turtle._utilities.search_command`"""
    with patch("shutil.which", return_value=None) as shutil_which:
        command_abspath = _utilities.search_commands(["notfound"])
        assert command_abspath is None

    with patch("shutil.which", return_value="found") as shutil_which:
        command_abspath = _utilities.search_commands(["found"])
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
    """Test :meth:`turbo_turtle._utilities.find_command`"""
    with patch("turbo_turtle._utilities.search_commands", return_value=found), outcome:
        try:
            command_abspath = _utilities.find_command(options)
            assert command_abspath == found
        finally:
            pass


def test_run_command():
    """Test :meth:`turbo_turtle._utilities.run_command`"""
    with patch("subprocess.check_output", side_effect=subprocess.CalledProcessError(1, "dummy", b"output")), \
         pytest.raises(SystemExit):
        _utilities.run_command("dummy")


def test_cubit_os_bin():
    with patch("platform.system", return_value="Darwin"):
        bin_directory = _utilities.cubit_os_bin()
        assert bin_directory == "MacOS"

    with patch("platform.system", return_value="Linux"):
        bin_directory = _utilities.cubit_os_bin()
        assert bin_directory == "bin"

    # TODO: Find the Windows bin directory name, update the function and the test.
    with patch("platform.system", return_value="Windows"):
        bin_directory = _utilities.cubit_os_bin()
        assert bin_directory == "bin"


construct_append_options = {
    "strings": (
        "--option-name",
        [["row1_column1", "row1_column2"], ["row2_column1", "row2_column2"]],
        "--option-name row1_column1 row1_column2 --option-name row2_column1 row2_column2"
    ),
    "strings: one row": (
        "--option-name",
        [["row1_column1", "row1_column2"]],
        "--option-name row1_column1 row1_column2"
    ),
    "ints": (
        "--int-tuple",
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "--int-tuple 1 2 3 --int-tuple 4 5 6 --int-tuple 7 8 9"
    ),
    "empty array": (
        "--empty",
        [[]],
        ""
    )
}


@pytest.mark.parametrize("option, array, expected",
                         construct_append_options.values(),
                         ids=construct_append_options.keys())
def test_construct_append_options(option, array, expected):
    option_string = _utilities.construct_append_options(option, array)
    assert option_string == expected
