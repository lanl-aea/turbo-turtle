import os
import pathlib
import tempfile
import subprocess
from importlib.metadata import version, PackageNotFoundError

import pytest
import numpy

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


def character_delimited_list(non_string_list, character=" "):
    """Map a list of non-strings to a character delimited string

    :returns: string delimited by specified character
    :rtype: str
    """
    return character.join(map(str, non_string_list))


def setup_sphere_commands(model, angle, center, quadrant, element_type, element_replacement,
                          turbo_turtle_command=turbo_turtle_command):
    """Return the sphere/partition/mesh commands for system testing

    :returns: list of string commands
    :rtype: list
    """
    model = pathlib.Path(model)
    image = model.with_suffix(".png")
    assembly = model.stem + "_assembly.inp"
    center_three_dimensions = numpy.array(center + (0,))
    center=character_delimited_list(center)
    xpoint=character_delimited_list(center_three_dimensions + numpy.array([1, 0, 0]))
    zpoint=character_delimited_list(center_three_dimensions + numpy.array([0, 0, 1]))
    commands = [
        f"{turbo_turtle_command} sphere --inner-radius 1 --outer-radius 2 --output-file {model} " \
            f"--model-name {model.stem} --part-name {model.stem} --quadrant {quadrant} " \
            f"--revolution-angle {angle} --center {center}",
        f"{turbo_turtle_command} partition --input-file {model} --output-file {model} " \
            f"--model-name {model.stem} --part-name {model.stem} --center {center} 0 " \
            f"--xpoint {xpoint} --zpoint {zpoint} --plane-angle 45",
        f"{turbo_turtle_command} mesh --input-file {model} --output-file {model} " \
            f"--model-name {model.stem} --part-name {model.stem} --global-seed 0.15 " \
            f"--element-type {element_type}",
        f"{turbo_turtle_command} image --input-file {model} --output-file {image} " \
            f"--model-name {model.stem} --part-name {model.stem}",
        f"{turbo_turtle_command} export --input-file {model} " \
            f"--model-name {model.stem} --part-name {model.stem} " \
            f"--element-type {element_replacement} --destination . " \
            f"--assembly {assembly}",
    ]
    return commands


def setup_geometry_commands(model, input_file, revolution_angle, cubit,
                            turbo_turtle_command=turbo_turtle_command):
    model = pathlib.Path(model).with_suffix(".cae")
    if cubit:
        model = model.with_suffix(".cub")
    part_name = " ".join(csv.stem for csv in input_file)
    input_file = character_delimited_list(input_file)
    commands = [
        f"{turbo_turtle_command} geometry --input-file {input_file} --model-name {model.stem} " \
            f"--part-name {part_name} --output-file {model} --revolution-angle {revolution_angle}",
    ]
    if cubit:
        commands = [f"{command} --cubit" for command in commands]
    return commands


def setup_cylinder_commands(model, revolution_angle,
                            turbo_turtle_command=turbo_turtle_command):
    model = pathlib.Path(model).with_suffix(".cae")
    commands = [
        f"{turbo_turtle_command} cylinder --model-name {model.stem} --part-name {model.stem} " \
            f"--output-file {model} --revolution-angle {revolution_angle} " \
            f"--inner-radius 1 --outer-radius 2 --height 1"
    ]
    return commands


# Help/Usage sign-of-life
commands_list = [f"{turbo_turtle_command} -h"]
commands_list.extend([f"{turbo_turtle_command} {subcommand} -h" for subcommand in subcommand_list])

# Legacy geometry system tests requires a series of commands before the temp directory is removed
# TODO: Decide if we should package or drop the legacy geometry tests
name='Turbo-Turtle-Tests'
commands_list.append([
    f"abq2023 cae -noGui {legacy_geometry_file}",
    f"{turbo_turtle_command} partition --input-file {name}.cae --output-file {name}.cae --model-name {name} --part-name seveneigths-sphere --center 0 0 0 --xpoint 1 0 0 --zpoint 0 0 1 --plane-angle 45",
    f"{turbo_turtle_command} image --input-file {name}.cae --model-name {name} --output-file seveneigths-sphere.png --part-name seveneigths-sphere",
    f"{turbo_turtle_command} partition --input-file {name}.cae --output-file {name}.cae --model-name {name} --part-name swiss-cheese --center 0 0 0 --xpoint 1 0 0 --zpoint 0 0 1 --plane-angle 45",
    f"{turbo_turtle_command} image --input-file {name}.cae --model-name {name} --output-file swiss-cheese.png --part-name swiss-cheese",
])

# Sphere/partition/mesh
system_tests = (
    # model/part,         angle,   center, quadrant, element_type, element_replacement
    ("sphere.cae",         360., (0., 0.),  "both",  "C3D8",       "C3D8R"),
    ("axisymmetric.cae",     0., (0., 0.),  "both",  "CAX4",       "CAX4R"),
    ("quarter-sphere.cae",  90., (0., 0.),  "both",  "C3D8",       "C3D8R"),
    ("offset-sphere.cae",  360., (1., 1.),  "both",  "C3D8",       "C3D8R"),
    ("eigth-sphere.cae",    90., (0., 0.), "upper",  "C3D8",       "C3D8R"),
    ("half-sphere.cae",    360., (0., 0.), "upper",  "C3D8",       "C3D8R")
)
for test in system_tests:
    commands_list.append(setup_sphere_commands(*test))

# Geometry tests
system_tests = (
    # model/part,                                                           input_file, angle, cubit
    # Abaqus
    ("washer",              [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0, False),
    ("washer-axisymmetric", [_settings._project_root_abspath / "tests" / "washer.csv"],   0.0, False),
    ("vase",                [_settings._project_root_abspath / "tests" / "vase.csv"],   360.0, False),
    ("vase-axisymmetric",   [_settings._project_root_abspath / "tests" / "vase.csv"],     0.0, False),
    ("multi-part-3D",       [_settings._project_root_abspath / "tests" / "washer.csv",
                             _settings._project_root_abspath / "tests" / "vase.csv"],   360.0, False),
    ("multi-part-2D",       [_settings._project_root_abspath / "tests" / "washer.csv",
                             _settings._project_root_abspath / "tests" / "vase.csv"],     0.0, False),
    # Cubit
    ("washer",              [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0, True),
    ("washer-axisymmetric", [_settings._project_root_abspath / "tests" / "washer.csv"],   0.0, True),
    ("vase",                [_settings._project_root_abspath / "tests" / "vase.csv"],   360.0, True),
    ("vase-axisymmetric",   [_settings._project_root_abspath / "tests" / "vase.csv"],     0.0, True),
    ("multi-part-3D",       [_settings._project_root_abspath / "tests" / "washer.csv",
                             _settings._project_root_abspath / "tests" / "vase.csv"],   360.0, True),
    ("multi-part-2D",       [_settings._project_root_abspath / "tests" / "washer.csv",
                             _settings._project_root_abspath / "tests" / "vase.csv"],     0.0, True),
)
for test in system_tests:
    commands_list.append(setup_geometry_commands(*test))

# Cylinder tests
system_tests = (
    # model/part,   angle
    ("cylinder_3d", 360.),
    ("cylinder_2d",   0.)
)
for test in system_tests:
    commands_list.append(setup_cylinder_commands(*test))

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
