import os
import tempfile
import subprocess
from importlib.metadata import version, PackageNotFoundError

import pytest

from turbo_turtle import _settings
from turbo_turtle.main import get_parser


parser = get_parser()
subcommand_list = parser._subparsers._group_actions[0].choices.keys()


env = os.environ.copy()
turbo_turtle_command = "turbo-turtle"
legacy_geometry_file = "legacy_geometry.py"

try:
    version("turbo_turtle")
    installed = True
except PackageNotFoundError:
    installed = False

# If executing in repository, add package to PYTHONPATH and change the root command
if not installed:
    turbo_turtle_command = "python -m turbo_turtle.main"
    legacy_geometry_file = _settings._project_root_abspath.parent / legacy_geometry_file
    package_parent_path = _settings._project_root_abspath.parent
    key = "PYTHONPATH"
    if key in env:
        env[key] = f"{package_parent_path}:{env[key]}"
    else:
        env[key] = f"{package_parent_path}"

commands_list = [f"{turbo_turtle_command} -h"]
commands_list.extend([f"{turbo_turtle_command} {subcommand} -h" for subcommand in subcommand_list])
# Legacy geometry system tests requires a series of commands before the temp directory is removed
name='Turbo-Turtle-Tests'
commands_list.append([
    f"abq2023 cae -noGui {legacy_geometry_file}",
    f"{turbo_turtle_command} partition --input-file {name}.cae --output-file {name}.cae --model-name {name} --part-name seveneigths-sphere --center 0 0 0 --xpoint 1 0 0 --zpoint 0 0 1 --plane-angle 45",
    f"{turbo_turtle_command} image --input-file {name}.cae --model-name {name} --output-file seveneigths-sphere.png --part-name seveneigths-sphere",
    f"{turbo_turtle_command} partition --input-file {name}.cae --output-file {name}.cae --model-name {name} --part-name swiss-cheese --center 0 0 0 --xpoint 1 0 0 --zpoint 0 0 1 --plane-angle 45",
    f"{turbo_turtle_command} image --input-file {name}.cae --model-name {name} --output-file swiss-cheese.png --part-name swiss-cheese",
])

@pytest.mark.systemtest
@pytest.mark.parametrize("commands", commands_list)
def test_run_tutorial(commands):
    """Run the system tests.

    Executes with a temporary directory that is cleaned up after each test execution.

    :param str command: the full command string for the system test
    """
    if isinstance(commands, str):
        commands = [commands]
    with tempfile.TemporaryDirectory() as temp_directory:
        for command in commands:
            command = command.split(" ")
            result = subprocess.check_output(command, env=env, cwd=temp_directory).decode('utf-8')
