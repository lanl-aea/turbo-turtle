"""Define the project's custom pytest options and CLI extensions."""

import os
import pathlib

import matplotlib
import pytest

matplotlib.use("Agg")
display = os.environ.get("DISPLAY")
if not display:
    missing_display = True
else:
    missing_display = False


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add the custom pytest options to the pytest command-line parser."""
    parser.addoption(
        "--abaqus-command",
        action="append",
        default=None,
        help="Abaqus command for system test CLI pass through",
    )
    parser.addoption(
        "--cubit-command",
        action="append",
        default=None,
        help="Cubit command for system test CLI pass through",
    )


@pytest.fixture
def abaqus_command(request: pytest.FixtureRequest) -> pathlib.Path:
    """Return the argument of custom pytest ``--abaqus-command`` command-line option.

    Returns an empty list if the getopts default ``None`` is provided (no command line argument specified)
    """
    command_list = request.config.getoption("--abaqus-command")
    if command_list is None:
        command_list = []
    return command_list


@pytest.fixture
def cubit_command(request: pytest.FixtureRequest) -> pathlib.Path:
    """Return the argument of custom pytest ``--cubit-command`` command-line option.

    Returns an empty list if the getopts default ``None`` is provided (no command line argument specified)
    """
    command_list = request.config.getoption("--cubit-command")
    if command_list is None:
        command_list = []
    return command_list
