import os
import shlex
import pathlib
import tempfile
import subprocess
from importlib.metadata import version, PackageNotFoundError

import pytest
import numpy

from turbo_turtle import _settings
from turbo_turtle import _utilities
from turbo_turtle._main import get_parser
from turbo_turtle.conftest import missing_display


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
    turbo_turtle_command = "python -m turbo_turtle._main"
    package_parent_path = _settings._project_root_abspath.parent
    key = "PYTHONPATH"
    if key in env:
        env[key] = f"{package_parent_path}:{env[key]}"
    else:
        env[key] = f"{package_parent_path}"


def setup_sphere_commands(model, inner_radius, outer_radius, angle, y_offset, quadrant, element_type, element_replacement, cubit, output_type,
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
    center=f"0. {y_offset} 0."
    xvector=_utilities.character_delimited_list([1., 0., 0.])
    zvector=_utilities.character_delimited_list([0., 0., 1.])
    commands = [
        f"{turbo_turtle_command} sphere --inner-radius {inner_radius} --outer-radius {outer_radius} --output-file {model} " \
            f"--model-name {model.stem} --part-name {model.stem} --quadrant {quadrant} " \
            f"--revolution-angle {angle} --y-offset {y_offset}",
        f"{turbo_turtle_command} partition --input-file {model} --output-file {model} " \
            f"--model-name {model.stem} --part-name {model.stem} --center {center} " \
            f"--xvector {xvector} --zvector {zvector}",
        f"{turbo_turtle_command} mesh --input-file {model} --output-file {model} " \
            f"--model-name {model.stem} --part-name {model.stem} --global-seed 0.15 " \
            f"--element-type {element_type}",
        f"{turbo_turtle_command} image --input-file {model} --output-file {image} " \
            f"--model-name {model.stem} --part-name {model.stem}",
        f"{turbo_turtle_command} export --input-file {model} " \
            f"--model-name {model.stem} --part-name {model.stem} " \
            f"--element-type {element_replacement} --destination . " \
            f"--assembly {assembly} --output-type {output_type}",
    ]
    # Skip the image subcommand when DISPLAY is not found
    # Skip the image subcommand when running the Genesis variations. We don't need duplicate images of the cubit meshes
    # TODO: Update as Cubit support is added for partition/mesh/image/export
    if (cubit and missing_display) or (cubit and output_type.lower() == "genesis"):
        commands.pop(3)
    # Skip the partition/mesh/image/export
    if inner_radius == 0:
        commands = [commands[0]]
    if cubit:
        commands = [f"{command} --backend cubit" for command in commands]
    return commands


def setup_geometry_xyplot_commands(model, input_file):
    part_name = _utilities.character_delimited_list(csv.stem for csv in input_file)
    input_file = _utilities.character_delimited_list(input_file)
    commands =[
        f"{turbo_turtle_command} geometry-xyplot --input-file {input_file} --output-file {model}.png " \
        f"--part-name {part_name}"
    ]
    return commands


def setup_geometry_commands(model, input_file, revolution_angle, y_offset, cubit,
                            turbo_turtle_command=turbo_turtle_command):
    model = pathlib.Path(model).with_suffix(".cae")
    if cubit:
        model = model.with_suffix(".cub")
    part_name = " ".join(csv.stem for csv in input_file)
    input_file = _utilities.character_delimited_list(input_file)
    commands = [
        f"{turbo_turtle_command} geometry --input-file {input_file} --model-name {model.stem} " \
            f"--part-name {part_name} --output-file {model} --revolution-angle {revolution_angle} " \
            f"--y-offset {y_offset}",
    ]
    if cubit:
        commands = [f"{command} --backend cubit" for command in commands]
    return commands


def setup_sets_command(model, input_file, revolution_angle, face_sets, cubit,
                       turbo_turtle_command=turbo_turtle_command):
    model = pathlib.Path(model).with_suffix(".cae")
    if cubit:
        model = model.with_suffix(".cub")
    commands = setup_geometry_commands(
        model, input_file, revolution_angle, 0., cubit,
        turbo_turtle_command=turbo_turtle_command
    )
    face_sets = _utilities.construct_append_options("--face-set", face_sets)
    sets_command = f"{turbo_turtle_command} sets --input-file {model} --model-name ${model.stem} " \
                   f"--part-name {model.stem} --output-file {model} {face_sets}"
    commands.append(sets_command)


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
        commands = [f"{command} --backend cubit" for command in commands]
    return commands


def setup_merge_commands(part_name, cubit, turbo_turtle_command=turbo_turtle_command):
    commands = []

    sphere_model = pathlib.Path("merge-sphere.cae")
    sphere_element_type = "C3D8"
    sphere_element_replacement = "C3D8R"
    geometry_model = pathlib.Path("merge-multi-part")
    output_file = pathlib.Path("merge.cae")
    if cubit:
        sphere_model = sphere_model.with_suffix(".cub")
        sphere_element_type = None
        sphere_element_replacement = "HEX20"
        geometry_model = geometry_model.with_suffix(".cub")
        output_file = output_file.with_suffix(".cub")

    # Create sphere file
    sphere_options = (str(sphere_model), 1., 2., 360., 0., "both", sphere_element_type, sphere_element_replacement, cubit, "abaqus")
    commands.append(setup_sphere_commands(*sphere_options)[0])

    # Create washer/vase combined file
    geometry_options = (str(geometry_model),
                        [_settings._project_root_abspath / "tests" / "washer.csv",
                         _settings._project_root_abspath / "tests" / "vase.csv"],
                        360.0, 0., cubit)
    commands.extend(setup_geometry_commands(*geometry_options))

    # Run the actual merge command
    merge_command =  f"{turbo_turtle_command} merge --input-file {sphere_model} {geometry_model} " \
                     f"--output-file {output_file} --merged-model-name merge " \
                     f"--model-name merge-multi-part merge-sphere"
    if part_name:
        merge_command += f" --part-name {part_name}"
    if cubit:
        merge_command = f"{merge_command} --backend cubit"
    commands.append(merge_command)

    return commands

# Help/Usage sign-of-life
commands_list = []
commands_list.append(
    [f"{turbo_turtle_command} -h"] + [f"{turbo_turtle_command} {subcommand} -h" for subcommand in subcommand_list]
)

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
    # model/part, inner_radius, outer_radius, angle, y-offset, quadrant, element_type, element_replacement, cubit, output_type
    # Abaqus CAE
    ("sphere.cae",               1.,     2., 360.,       0.,  "both",  "C3D8",       "C3D8R", False, "abaqus"),
    ("solid-sphere.cae",         0.,     2., 360.,       0.,  "both",  "C3D8",       "C3D8R", False, "abaqus"),
    ("axisymmetric.cae",         1.,     2.,   0.,       0.,  "both",  "CAX4",       "CAX4R", False, "abaqus"),
    ("quarter-sphere.cae",       1.,     2.,  90.,       0.,  "both",  "C3D8",       "C3D8R", False, "abaqus"),
    ("offset-sphere.cae",        1.,     2., 360.,       1.,  "both",  "C3D8",       "C3D8R", False, "abaqus"),
    ("eigth-sphere.cae",         1.,     2.,  90.,       0., "upper",  "C3D8",       "C3D8R", False, "abaqus"),
    ("half-sphere.cae",          1.,     2., 360.,       0., "upper",  "C3D8",       "C3D8R", False, "abaqus"),
    # Cubit: for Abaqus INP
    ("sphere.cae",               1.,     2., 360.,       0.,  "both",    None,       "C3D8R", True, "abaqus"),
    ("solid-sphere.cae",         0.,     2., 360.,       0.,  "both",    None,       "C3D8R", True, "abaqus"),
    ("axisymmetric.cae",         1.,     2.,   0.,       0.,  "both",    None,       "CAX4R", True, "abaqus"),
    ("quarter-sphere.cae",       1.,     2.,  90.,       0.,  "both",    None,       "C3D8R", True, "abaqus"),
    ("offset-sphere.cae",        1.,     2., 360.,       1.,  "both",    None,       "C3D8R", True, "abaqus"),
    ("eigth-sphere.cae",         1.,     2.,  90.,       0., "upper",    None,       "C3D8R", True, "abaqus"),
    ("half-sphere.cae",          1.,     2., 360.,       0., "upper",    None,       "C3D8R", True, "abaqus"),
    # Cubit "element type" is really a "meshing scheme"
    ("sphere-tets.cae",          1.,     2., 360.,     0., "both", "tetmesh",       None, True, "abaqus"),
    ("axisymmetric-tri.cae",     1.,     2.,   0.,     0., "both", "trimesh",       None, True, "abaqus"),
    # Cubit: for Genesis INP
    ("sphere-genesis.cae",         1.,   2., 360., 0.,  "both",   None,  "HEX", True, "genesis"),
    ("solid-sphere-genesis.cae",   0.,   2., 360., 0.,  "both",   None,  "HEX", True, "genesis"),
    ("axisymmetric-genesis.cae",   1.,   2.,   0., 0.,  "both",   None, "QUAD", True, "genesis"),
    ("quarter-sphere-genesis.cae", 1.,   2.,  90., 0.,  "both",   None,  "HEX", True, "genesis"),
    ("offset-sphere-genesis.cae",  1.,   2., 360., 1.,  "both",   None,  "HEX", True, "genesis"),
    ("eigth-sphere-genesis.cae",   1.,   2.,  90., 0., "upper",   None,  "HEX", True, "genesis"),
    ("half-sphere-genesis.cae",    1.,   2., 360., 0., "upper",   None,  "HEX", True, "genesis"),
    # Cubit "element type" is really a "meshing scheme"
    ("sphere-tets-genesis.cae",     1.,   2., 360., 0., "both", "tetmesh",   "TRI", True, "genesis"),
    ("axisymmetric-tri-genesis.cae",1.,   2.,   0., 0., "both", "trimesh", "TETRA", True, "genesis"),
)
for test in system_tests:
    commands_list.append(setup_sphere_commands(*test))

# Geometry XY Plot tests
system_tests = (
    # model/part,                                                  input_file
    ("washer",     [_settings._project_root_abspath / "tests" / "washer.csv"]),
    ("vase",       [_settings._project_root_abspath / "tests" / "vase.csv"]),
    ("multi-part", [_settings._project_root_abspath / "tests" / "washer.csv",
                    _settings._project_root_abspath / "tests" / "vase.csv"]),
)
for test in system_tests:
    commands_list.append(setup_geometry_xyplot_commands(*test))


# Geometry tests
system_tests = (
    # model/part,                                                           input_file, angle, y-offset, cubit
    # Abaqus
    ("washer",              [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0, 0., False),
    ("offset-washer",       [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0, 1., False),
    ("washer-axisymmetric", [_settings._project_root_abspath / "tests" / "washer.csv"],   0.0, 0., False),
    ("vase",                [_settings._project_root_abspath / "tests" / "vase.csv"],   360.0, 0., False),
    ("vase-axisymmetric",   [_settings._project_root_abspath / "tests" / "vase.csv"],     0.0, 0., False),
    ("multi-part-3D",       [_settings._project_root_abspath / "tests" / "washer.csv",
                             _settings._project_root_abspath / "tests" / "vase.csv"],   360.0, 0., False),
    ("multi-part-2D",       [_settings._project_root_abspath / "tests" / "washer.csv",
                             _settings._project_root_abspath / "tests" / "vase.csv"],     0.0, 0., False),
    # Cubit
    ("washer",              [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0, 0., True),
    ("offset-washer",       [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0, 1., True),
    ("washer-axisymmetric", [_settings._project_root_abspath / "tests" / "washer.csv"],   0.0, 0., True),
    ("vase",                [_settings._project_root_abspath / "tests" / "vase.csv"],   360.0, 0., True),
    ("vase-axisymmetric",   [_settings._project_root_abspath / "tests" / "vase.csv"],     0.0, 0., True),
    ("multi-part-3D",       [_settings._project_root_abspath / "tests" / "washer.csv",
                             _settings._project_root_abspath / "tests" / "vase.csv"],   360.0, 0., True),
    ("multi-part-2D",       [_settings._project_root_abspath / "tests" / "washer.csv",
                             _settings._project_root_abspath / "tests" / "vase.csv"],     0.0, 0., True),
)
for test in system_tests:
    commands_list.append(setup_geometry_commands(*test))

# Sets tests
system_tests = (
    # model/part,                                                           input_file, angle,                                face_sets, cubit
    # Abaqus
    ("vase",                [_settings._project_root_abspath / "tests" / "vase.csv"],   360.0, [["top", "[#4 ]"], ["bottom", "[#40 ]"]], False),
)

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
    commands_list.append(setup_merge_commands(part_name, cubit=False))
    commands_list.append(setup_merge_commands(part_name, cubit=True))

# SCons extensions tests
# TODO: Use a turbo-turtle fetch command
# https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/145
# System tests as SCons tasks
sconstruct = _settings._project_root_abspath / "tests/SConstruct"
commands_list.append(f"scons . --sconstruct {sconstruct} --turbo-turtle-command='{turbo_turtle_command}'")
# User manual example SCons tasks
sconstruct_files = [
    [
        _settings._project_root_abspath / "tutorials/SConstruct",
        _settings._project_root_abspath / "tutorials/SConscript"
    ]
]
for files in sconstruct_files:
    space_delimited_files = ' '.join([str(path) for path in files])
    scons_test_commands = [
        f"{turbo_turtle_command} fetch SConstruct SConscript",
        # FIXME: Figure out why this command fails on the CI server, but not in local user tests
        # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/159
        #f"scons . --turbo-turtle-command='{turbo_turtle_command}'"
    ]
    commands_list.append(scons_test_commands)


@pytest.mark.systemtest
@pytest.mark.parametrize("number, commands", enumerate(commands_list))
def test_shell_commands(number, commands):
    """Run the system tests.

    Executes with a temporary directory that is cleaned up after each test execution.

    :param int number: the command number. Used during local testing to separate command directories.
    :param str command: the full command string for the system test
    """
    if isinstance(commands, str):
        commands = [commands]
    if installed:
        with tempfile.TemporaryDirectory() as temp_directory:
            run_commands(commands, temp_directory)
    else:
        command_directory = build_directory / f"commands{number}"
        command_directory.mkdir(parents=True, exist_ok=True)
        run_commands(commands, command_directory)


def run_commands(commands, build_directory):
    for command in commands:
        command = shlex.split(command)
        result = subprocess.check_output(command, env=env, cwd=build_directory).decode('utf-8')
