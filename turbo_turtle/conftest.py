import os
import pathlib

import pytest


display = os.environ.get("DISPLAY")
if not display:
    missing_display = True
else:
    missing_display = False


def pytest_addoption(parser):
    parser.addoption(
        "--abaqus-command",
        action="store",
        type=pathlib.Path,
        default=None,
        help="Abaqus command for system test CLI pass through",
    )
    parser.addoption(
        "--cubit-command",
        action="store",
        type=pathlib.Path,
        default=None,
        help="Cubit command for system test CLI pass through",
    )


@pytest.fixture
def abaqus_command(request):
    return request.config.getoption("--abaqus-command")


@pytest.fixture
def cubit_command(request):
    return request.config.getoption("--cubit-command")
