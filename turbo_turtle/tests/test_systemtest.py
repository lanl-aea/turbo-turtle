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

try:
    version("turbo_turtle")
    installed = True
except PackageNotFoundError:
    # TODO: Recover from the SCons task definition?
    build_directory = _settings._project_root_abspath.parent / "build" / "systemtests"
    build_directory.mkdir(parents=True, exist_ok=True)
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


def character_delimited_list(non_string_list, character=" "):
    """Map a list of non-strings to a character delimited string

    :returns: string delimited by specified character
    :rtype: str
    """
    return character.join(map(str, non_string_list))


def setup_sphere_commands(model, angle, center, quadrant, element_type, element_replacement, cubit,
                          turbo_turtle_command=turbo_turtle_command):
    """Return the sphere/partition/mesh commands for system testing

    :returns: list of string commands
    :rtype: list
    """
    model = pathlib.Path(model).with_suffix(".cae")
    image = model.with_suffix(".png")
    if cubit:
        model = model.with_suffix(".cub")
        image = image.parent / f"{image.stem}-cubit{image.suffix}"
    assembly = model.stem + "_assembly.inp"
    center=character_delimited_list(center)
    xvector=character_delimited_list([1., 0., 0.])
    zvector=character_delimited_list([0., 0., 1.])
    commands = [
        f"{turbo_turtle_command} sphere --inner-radius 1 --outer-radius 2 --output-file {model} " \
            f"--model-name {model.stem} --part-name {model.stem} --quadrant {quadrant} " \
            f"--revolution-angle {angle} --center {center}",
        f"{turbo_turtle_command} partition --input-file {model} --output-file {model} " \
            f"--model-name {model.stem} --part-name {model.stem} --center {center} 0 " \
            f"--xvector {xvector} --zvector {zvector}",
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
    # TODO: Update as Cubit support is added for partition/mesh/image/export
    if cubit:
        commands = commands[0:3]
    if cubit:
        commands = [f"{command} --cubit" for command in commands]
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


def setup_cylinder_commands(model, revolution_angle, cubit,
                            turbo_turtle_command=turbo_turtle_command):
    model = pathlib.Path(model).with_suffix(".cae")
    if cubit:
        model = model.with_suffix(".cub")
    commands = [
        f"{turbo_turtle_command} cylinder --model-name {model.stem} --part-name {model.stem} " \
            f"--output-file {model} --revolution-angle {revolution_angle} " \
            f"--inner-radius 1 --outer-radius 2 --height 1"
    ]
    if cubit:
        commands = [f"{command} --cubit" for command in commands]
    return commands


def setup_merge_commands(part_name, turbo_turtle_command=turbo_turtle_command):
    sphere_options = ("merge-sphere.cae", 360., (0., 0.), "both", "C3D8", "C3D8R", False)
    commands = []
    commands.append(setup_sphere_commands(*sphere_options)[0])
    geometry_options = ("merge-multi-part",
                        [_settings._project_root_abspath / "tests" / "washer.csv",
                         _settings._project_root_abspath / "tests" / "vase.csv"],
                        360.0, False)
    commands.extend(setup_geometry_commands(*geometry_options))

    merge_command =  f"{turbo_turtle_command} merge --input-file merge-sphere.cae merge-multi-part.cae " \
                     f"--output-file merge.cae --merged-model-name merge " \
                     f"--model-name merge-multi-part merge-sphere"
    if part_name:
        merge_command += f" --part-name {part_name}"

    commands.append(merge_command)
    return commands

# Help/Usage sign-of-life
commands_list = [f"{turbo_turtle_command} -h"]
commands_list.extend([f"{turbo_turtle_command} {subcommand} -h" for subcommand in subcommand_list])

# Legacy geometry system tests requires a series of commands before the temp directory is removed
# TODO: Decide if we should package or drop the legacy geometry tests
name='Turbo-Turtle-Tests'
legacy_geometry_file = _settings._project_root_abspath / "tests" / "legacy_geometry.py"
commands_list.append([
    f"abq2023 cae -noGui {legacy_geometry_file}",
    f"{turbo_turtle_command} partition --input-file {name}.cae --output-file {name}.cae --model-name {name} --part-name seveneigths-sphere --center 0 0 0 --xvector 1 0 0 --zvector 0 0 1",
    f"{turbo_turtle_command} image --input-file {name}.cae --model-name {name} --output-file seveneigths-sphere.png --part-name seveneigths-sphere",
    f"{turbo_turtle_command} partition --input-file {name}.cae --output-file {name}.cae --model-name {name} --part-name swiss-cheese --center 0 0 0 --xvector 1 0 0 --zvector 0 0 1",
    f"{turbo_turtle_command} image --input-file {name}.cae --model-name {name} --output-file swiss-cheese.png --part-name swiss-cheese",
])

# Sphere/partition/mesh
system_tests = (
    # model/part,         angle,   center, quadrant, element_type, element_replacement, cubit
    # Abaqus CAE
    ("sphere.cae",         360., (0., 0.),  "both",  "C3D8",       "C3D8R", False),
    ("axisymmetric.cae",     0., (0., 0.),  "both",  "CAX4",       "CAX4R", False),
    ("quarter-sphere.cae",  90., (0., 0.),  "both",  "C3D8",       "C3D8R", False),
    ("offset-sphere.cae",  360., (1., 1.),  "both",  "C3D8",       "C3D8R", False),
    ("eigth-sphere.cae",    90., (0., 0.), "upper",  "C3D8",       "C3D8R", False),
    ("half-sphere.cae",    360., (0., 0.), "upper",  "C3D8",       "C3D8R", False),
    # Cubit
    # TODO: Add element type and replacement when the mesh/export subcommands support Cubit
    ("sphere.cae",         360., (0., 0.),  "both",    None,          None, True),
    ("axisymmetric.cae",     0., (0., 0.),  "both",    None,          None, True),
    ("quarter-sphere.cae",  90., (0., 0.),  "both",    None,          None, True),
    ("offset-sphere.cae",  360., (1., 1.),  "both",    None,          None, True),
    ("eigth-sphere.cae",    90., (0., 0.), "upper",    None,          None, True),
    ("half-sphere.cae",    360., (0., 0.), "upper",    None,          None, True)
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
    # model/part,   angle, cubit
    ("cylinder_3d", 360., False),
    ("cylinder_2d",   0., False),
    ("cylinder_3d", 360., True),
    ("cylinder_2d",   0., True)
)
for test in system_tests:
    commands_list.append(setup_cylinder_commands(*test))

# Merge tests
for part_name in ("washer vase merge-sphere", ""):
    commands_list.append(setup_merge_commands(part_name))


@pytest.mark.systemtest
@pytest.mark.parametrize("commands", commands_list)
def test_shell_commands(commands):
    """Run the system tests.

    Executes with a temporary directory that is cleaned up after each test execution.

    :param str command: the full command string for the system test
    """
    if isinstance(commands, str):
        commands = [commands]
    if installed:
        with tempfile.TemporaryDirectory() as temp_directory:
            run_commands(commands, temp_directory)
    else:
        run_commands(commands, build_directory)


def run_commands(commands, build_directory):
    for command in commands:
        command = command.split(" ")
        result = subprocess.check_output(command, env=env, cwd=build_directory).decode('utf-8')
