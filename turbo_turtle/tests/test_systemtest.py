import os
import tempfile
import subprocess
from importlib.metadata import version, PackageNotFoundError

import pytest

from turbo_turtle import _settings


env = os.environ.copy()
turbo_turtle_command = "turbo-turtle"

try:
    version("turbo_turtle")
    installed = True
except PackageNotFoundError:
    installed = False

# If executing in repository, add package to PYTHONPATH and change the root command
if not installed:
    turbo_turtle_command = "python -m turbo_turtle.main"
    package_parent_path = _settings._project_root_abspath.parent
    key = "PYTHONPATH"
    if key in env:
        env[key] = f"{package_parent_path}:{env[key]}"
    else:
        env[key] = f"{package_parent_path}"

@pytest.mark.systemtest
@pytest.mark.parametrize("command", [
    f"{turbo_turtle_command} -h",
    f"{turbo_turtle_command} docs -h",
    f"{turbo_turtle_command} geometry -h",
    f"{turbo_turtle_command} cylinder -h",
    f"{turbo_turtle_command} sphere -h",
    f"{turbo_turtle_command} partition -h",
    f"{turbo_turtle_command} mesh -h",
    f"{turbo_turtle_command} image -h",
    f"{turbo_turtle_command} merge -h",
    f"{turbo_turtle_command} export -h",
])
def test_run_tutorial(command):
    """Run the system tests.

    Executes with a temporary directory that is cleaned up after each test execution.

    :param str command: the full command string for the system test
    """
    with tempfile.TemporaryDirectory() as temp_directory:
        command = command.split(" ")
        result = subprocess.check_output(command, env=env, cwd=temp_directory).decode('utf-8')
