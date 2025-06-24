import os
import shlex
import string
import typing
import pathlib
import tempfile
import subprocess
from importlib.metadata import version, PackageNotFoundError

import pytest

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


def setup_sphere_commands(
    model,
    inner_radius,
    outer_radius,
    angle,
    y_offset,
    quadrant,
    element_type,
    element_replacement,
    backend,
    output_type,
) -> typing.List[string.Template]:
    """Return the sphere/partition/mesh commands for system testing

    :returns: list of string or string template commands
    """
    model = pathlib.Path(model).with_suffix(".cae")
    image = model.with_suffix(".png")
    # TODO: Merge Gmsh sphere system tests when partition/mesh/image subcommands are implemented
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/217
    if backend == "cubit":
        model = model.with_suffix(".cub")
        image = image.parent / f"{image.stem}-cubit{image.suffix}"
    assembly = model.stem + "_assembly.inp"
    center = f"0. {y_offset} 0."
    xvector = _utilities.character_delimited_list([1.0, 0.0, 0.0])
    zvector = _utilities.character_delimited_list([0.0, 0.0, 1.0])
    backend_option = f"--backend {backend}" if backend is not None else ""

    commands = [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            f"--inner-radius {inner_radius} --outer-radius {outer_radius} --output-file {model} "
            f"--model-name {model.stem} --part-name {model.stem} --quadrant {quadrant} "
            f"--revolution-angle {angle} --y-offset {y_offset} {backend_option}"
        ),
        string.Template(
            "${turbo_turtle_command} partition --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            f"--input-file {model} --output-file {model} "
            f"--model-name {model.stem} --part-name {model.stem} --center {center} "
            f"--xvector {xvector} --zvector {zvector} {backend_option}"
        ),
        string.Template(
            "${turbo_turtle_command} mesh --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            f"--input-file {model} --output-file {model} "
            f"--model-name {model.stem} --part-name {model.stem} --global-seed 0.15 "
            f"--element-type {element_type} {backend_option}"
        ),
        string.Template(
            "${turbo_turtle_command} image --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            f"--input-file {model} --output-file {image} "
            f"--model-name {model.stem} --part-name {model.stem} {backend_option}"
        ),
        string.Template(
            "${turbo_turtle_command} export --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            f"--input-file {model} --model-name {model.stem} --part-name {model.stem} "
            f"--element-type {element_replacement} --destination . "
            f"--assembly {assembly} --output-type {output_type} {backend_option}"
        ),
    ]
    # Skip the image subcommand when DISPLAY is not found
    # Skip the image subcommand when running the Genesis variations. We don't need duplicate images of the cubit meshes
    if (backend == "cubit" and missing_display) or (backend == "cubit" and output_type.lower() == "genesis"):
        commands.pop(3)
    # Skip the partition/mesh/image/export
    if inner_radius == 0:
        commands = [commands[0]]
    return pytest.param(commands, marks=getattr(pytest.mark, backend))


def setup_geometry_xyplot_commands(model, input_file, backend) -> typing.List[string.Template]:
    part_name = _utilities.character_delimited_list(csv.stem for csv in input_file)
    input_file = _utilities.character_delimited_list(input_file)
    commands = [
        string.Template(
            "${turbo_turtle_command} geometry-xyplot "
            "--abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            f"--input-file {input_file} --output-file {model}.png --part-name {part_name} "
            f"--backend {backend}"
        )
    ]
    return pytest.param(commands, marks=getattr(pytest.mark, backend))


def setup_geometry_commands(
    model,
    input_file,
    revolution_angle,
    y_offset,
    backend,
) -> typing.List[string.Template]:
    model = pathlib.Path(model).with_suffix(".cae")
    if backend == "cubit":
        model = model.with_suffix(".cub")
    if backend == "gmsh":
        model = model.with_suffix(".step")
    part_name = " ".join(csv.stem for csv in input_file)
    input_file = _utilities.character_delimited_list(input_file)
    backend_option = f"--backend {backend}" if backend is not None else ""
    commands = [
        string.Template(
            "${turbo_turtle_command} geometry --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            f"--input-file {input_file} --model-name {model.stem} "
            f"--part-name {part_name} --output-file {model} --revolution-angle {revolution_angle} "
            f"--y-offset {y_offset} {backend_option}"
        )
    ]
    return pytest.param(commands, marks=getattr(pytest.mark, backend))


def setup_sets_commands(
    model,
    input_file,
    revolution_angle,
    face_sets,
    edge_sets,
    edge_seeds,
    element_type,
    backend,
) -> typing.List[string.Template]:
    model = pathlib.Path(model).with_suffix(".cae")
    if backend == "cubit":
        model = model.with_suffix(".cub")
    part_name = " ".join(csv.stem for csv in input_file)
    commands = setup_geometry_commands(model, input_file, revolution_angle, 0.0, backend).values[0]
    if face_sets is not None:
        face_sets = _utilities.construct_append_options("--face-set", face_sets)
    else:
        face_sets = ""
    if edge_sets is not None:
        edge_sets = _utilities.construct_append_options("--edge-set", edge_sets)
    else:
        edge_sets = ""
    if edge_seeds is not None:
        edge_seeds = _utilities.construct_append_options("--edge-seed", edge_seeds)
    else:
        edge_seeds = ""
    backend_option = f"--backend {backend}" if backend is not None else ""
    sets_commands = [
        string.Template(
            "${turbo_turtle_command} sets --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            f"--input-file {model} --model-name {model.stem} "
            f"--part-name {part_name} --output-file {model} {face_sets} {edge_sets} {backend_option}"
        ),
        string.Template(
            "${turbo_turtle_command} mesh --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            f"--input-file {model} --model-name {model.stem} "
            f"--part-name {part_name} --output-file {model} --global-seed 1. --element-type {element_type} "
            f"{edge_seeds} {backend_option}"
        ),
    ]
    commands.extend(sets_commands)
    return pytest.param(commands, marks=getattr(pytest.mark, backend))


def setup_cylinder_commands(model, revolution_angle, backend) -> typing.List[string.Template]:
    model = pathlib.Path(model).with_suffix(".cae")
    if backend == "cubit":
        model = model.with_suffix(".cub")
    if backend == "gmsh":
        model = model.with_suffix(".step")
    backend_option = f"--backend {backend}" if backend is not None else ""
    commands = [
        string.Template(
            "${turbo_turtle_command} cylinder --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            f"--model-name {model.stem} --part-name {model.stem} "
            f"--output-file {model} --revolution-angle {revolution_angle} "
            f"--inner-radius 1 --outer-radius 2 --height 1 {backend_option}"
        )
    ]
    return pytest.param(commands, marks=getattr(pytest.mark, backend))


def setup_merge_commands(part_name, backend) -> typing.List[string.Template]:
    commands = []

    sphere_model = pathlib.Path("merge-sphere.cae")
    sphere_element_type = "C3D8"
    sphere_element_replacement = "C3D8R"
    geometry_model = pathlib.Path("merge-multi-part")
    output_file = pathlib.Path("merge.cae")
    if backend == "cubit":
        sphere_model = sphere_model.with_suffix(".cub")
        sphere_element_type = None
        sphere_element_replacement = "HEX20"
        geometry_model = geometry_model.with_suffix(".cub")
        output_file = output_file.with_suffix(".cub")

    # Create sphere file
    sphere_options = (
        str(sphere_model),
        1.0,
        2.0,
        360.0,
        0.0,
        "both",
        sphere_element_type,
        sphere_element_replacement,
        backend,
        "abaqus",
    )
    commands.append(setup_sphere_commands(*sphere_options).values[0][0])

    # Create washer/vase combined file
    geometry_options = (
        str(geometry_model),
        [
            _settings._project_root_abspath / "tests" / "washer.csv",
            _settings._project_root_abspath / "tests" / "vase.csv",
        ],
        360.0,
        0.0,
        backend,
    )
    commands.extend(setup_geometry_commands(*geometry_options).values[0])

    # Run the actual merge command
    part_name = f"--part-name {part_name}" if part_name else ""
    backend_option = f"--backend {backend}" if backend is not None else ""
    merge_command = string.Template(
        "${turbo_turtle_command} merge --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
        f"--input-file {sphere_model} {geometry_model} "
        f"--output-file {output_file} --merged-model-name merge "
        f"--model-name merge-multi-part merge-sphere {part_name} {backend_option}"
    )
    commands.append(merge_command)

    return pytest.param(commands, marks=getattr(pytest.mark, backend))


commands_list = []
# Legacy geometry system tests requires a series of commands before the temp directory is removed
# TODO: Decide if we should package or drop the legacy geometry tests
name = "Turbo-Turtle-Tests"
legacy_geometry_file = _settings._project_root_abspath / "tests" / "legacy_geometry.py"
commands_list.append(
    pytest.param(
        [
            string.Template(f"${{abaqus_command}} cae -noGui {legacy_geometry_file}"),
            string.Template(
                "${turbo_turtle_command} partition --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
                f"--input-file {name}.cae --output-file {name}.cae --model-name {name} "
                f"--part-name seveneigths-sphere --center 0 0 0 --xvector 1 0 0 --zvector 0 0 1"
            ),
            string.Template(
                "${turbo_turtle_command} image --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
                f"--input-file {name}.cae --model-name {name} "
                f"--output-file seveneigths-sphere.png --part-name seveneigths-sphere"
            ),
            string.Template(
                "${turbo_turtle_command} partition --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
                f"--input-file {name}.cae --output-file {name}.cae --model-name {name} --part-name swiss-cheese "
                "--center 0 0 0 --xvector 1 0 0 --zvector 0 0 1"
            ),
            string.Template(
                "${turbo_turtle_command} image --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
                f"--input-file {name}.cae --model-name {name} --output-file swiss-cheese.png --part-name swiss-cheese"
            ),
        ],
        marks=pytest.mark.abaqus,
    )
)

# Sphere/partition/mesh
system_tests = (
    # model/part, inner_radius, outer_radius, angle, y-offset, quadrant, element_type, element_replacement,  backend, output_type  # noqa: E501
    # Abaqus CAE
    ("sphere.cae",                   1., 2.,   360.,       0.,   "both",       "C3D8",             "C3D8R", "abaqus", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("solid-sphere.cae",             0., 2.,   360.,       0.,   "both",       "C3D8",             "C3D8R", "abaqus", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("axisymmetric.cae",             1., 2.,     0.,       0.,   "both",       "CAX4",             "CAX4R", "abaqus", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("quarter-sphere.cae",           1., 2.,    90.,       0.,   "both",       "C3D8",             "C3D8R", "abaqus", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("offset-sphere.cae",            1., 2.,   360.,       1.,   "both",       "C3D8",             "C3D8R", "abaqus", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("eigth-sphere.cae",             1., 2.,    90.,       0.,  "upper",       "C3D8",             "C3D8R", "abaqus", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("half-sphere.cae",              1., 2.,   360.,       0.,  "upper",       "C3D8",             "C3D8R", "abaqus", "abaqus"),  # fmt: skip # noqa: E241,E501
    # Cubit: for Abaqus INP
    ("sphere.cae",                   1., 2.,   360.,       0.,   "both",         None,             "C3D8R",  "cubit", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("solid-sphere.cae",             0., 2.,   360.,       0.,   "both",         None,             "C3D8R",  "cubit", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("axisymmetric.cae",             1., 2.,     0.,       0.,   "both",         None,             "CAX4R",  "cubit", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("quarter-sphere.cae",           1., 2.,    90.,       0.,   "both",         None,             "C3D8R",  "cubit", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("offset-sphere.cae",            1., 2.,   360.,       1.,   "both",         None,             "C3D8R",  "cubit", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("eigth-sphere.cae",             1., 2.,    90.,       0.,  "upper",         None,             "C3D8R",  "cubit", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("half-sphere.cae",              1., 2.,   360.,       0.,  "upper",         None,             "C3D8R",  "cubit", "abaqus"),  # fmt: skip # noqa: E241,E501
    # Cubit "element type" is really a "meshing scheme"
    ("sphere-tets.cae",              1., 2.,   360.,       0.,   "both",    "tetmesh",                None,  "cubit", "abaqus"),  # fmt: skip # noqa: E241,E501
    ("axisymmetric-tri.cae",         1., 2.,     0.,       0.,   "both",    "trimesh",                None,  "cubit", "abaqus"),  # fmt: skip # noqa: E241,E501
    # Cubit: for Genesis INP
    ("sphere-genesis.cae",           1., 2.,   360.,       0.,   "both",         None,               "HEX",  "cubit", "genesis"),  # fmt: skip # noqa: E241,E501
    ("solid-sphere-genesis.cae",     0., 2.,   360.,       0.,   "both",         None,               "HEX",  "cubit", "genesis"),  # fmt: skip # noqa: E241,E501
    ("axisymmetric-genesis.cae",     1., 2.,     0.,       0.,   "both",         None,              "QUAD",  "cubit", "genesis"),  # fmt: skip # noqa: E241,E501
    ("quarter-sphere-genesis.cae",   1., 2.,    90.,       0.,   "both",         None,               "HEX",  "cubit", "genesis"),  # fmt: skip # noqa: E241,E501
    ("offset-sphere-genesis.cae",    1., 2.,   360.,       1.,   "both",         None,               "HEX",  "cubit", "genesis"),  # fmt: skip # noqa: E241,E501
    ("eigth-sphere-genesis.cae",     1., 2.,    90.,       0.,  "upper",         None,               "HEX",  "cubit", "genesis"),  # fmt: skip # noqa: E241,E501
    ("half-sphere-genesis.cae",      1., 2.,   360.,       0.,  "upper",         None,               "HEX",  "cubit", "genesis"),  # fmt: skip # noqa: E241,E501
    # Cubit "element type" is really a "meshing scheme"
    ("sphere-tets-genesis.cae",      1., 2.,   360.,       0.,   "both",    "tetmesh",               "TRI",  "cubit", "genesis"),  # fmt: skip # noqa: E241,E501
    ("axisymmetric-tri-genesis.cae", 1., 2.,     0.,       0.,   "both",    "trimesh",             "TETRA",  "cubit", "genesis"),  # fmt: skip # noqa: E241,E231,E501
)
for test in system_tests:
    commands_list.append(setup_sphere_commands(*test))

# Geometry XY Plot tests
system_tests = (
    # model/part,                                                  input_file, backend
    ("washer",     [_settings._project_root_abspath / "tests" / "washer.csv"], "abaqus"),  # fmt: skip # noqa: E241
    ("vase",       [_settings._project_root_abspath / "tests" / "vase.csv"],   "abaqus"),  # fmt: skip # noqa: E241
    ("multi-part", [_settings._project_root_abspath / "tests" / "washer.csv",
                    _settings._project_root_abspath / "tests" / "vase.csv"],   "abaqus"),  # fmt: skip # noqa: E241
)
for test in system_tests:
    commands_list.append(setup_geometry_xyplot_commands(*test))


# Geometry tests
system_tests = (
    # model/part,                                                           input_file, angle, y-offset, backend
    # Abaqus
    ("washer",              [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0,       0., "abaqus"),  # fmt: skip # noqa: E241,E501
    ("offset-washer",       [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0,       1., "abaqus"),  # fmt: skip # noqa: E241,E501
    ("washer-axisymmetric", [_settings._project_root_abspath / "tests" / "washer.csv"],   0.0,       0., "abaqus"),  # fmt: skip # noqa: E241,E501
    ("vase",                [_settings._project_root_abspath / "tests" / "vase.csv"],   360.0,       0., "abaqus"),  # fmt: skip # noqa: E241,E501
    ("vase-axisymmetric",   [_settings._project_root_abspath / "tests" / "vase.csv"],     0.0,       0., "abaqus"),  # fmt: skip # noqa: E241,E501
    ("multi-part-3D",       [_settings._project_root_abspath / "tests" / "washer.csv",  # fmt: skip # noqa: E241
                             _settings._project_root_abspath / "tests" / "vase.csv"],   360.0,       0., "abaqus"),  # fmt: skip # noqa: E241,E501
    ("multi-part-2D",       [_settings._project_root_abspath / "tests" / "washer.csv",  # fmt: skip # noqa: E241
                             _settings._project_root_abspath / "tests" / "vase.csv"],     0.0,       0., "abaqus"),  # fmt: skip # noqa: E241,E501
    # Cubit
    ("washer",              [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0,       0., "cubit"),  # fmt: skip # noqa: E241,E501
    ("offset-washer",       [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0,       1., "cubit"),  # fmt: skip # noqa: E241,E501
    ("washer-axisymmetric", [_settings._project_root_abspath / "tests" / "washer.csv"],   0.0,       0., "cubit"),  # fmt: skip # noqa: E241,E501
    ("vase",                [_settings._project_root_abspath / "tests" / "vase.csv"],   360.0,       0., "cubit"),  # fmt: skip # noqa: E241,E501
    ("vase-axisymmetric",   [_settings._project_root_abspath / "tests" / "vase.csv"],     0.0,       0., "cubit"),  # fmt: skip # noqa: E241,E501
    ("multi-part-3D",       [_settings._project_root_abspath / "tests" / "washer.csv",  # fmt: skip # noqa: E241
                             _settings._project_root_abspath / "tests" / "vase.csv"],   360.0,       0., "cubit"),  # fmt: skip # noqa: E241,E501
    ("multi-part-2D",       [_settings._project_root_abspath / "tests" / "washer.csv",  # fmt: skip # noqa: E241
                             _settings._project_root_abspath / "tests" / "vase.csv"],     0.0,       0., "cubit"),  # fmt: skip # noqa: E241,E501
    # Gmsh
    ("washer",              [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0,       0., "gmsh"),  # fmt: skip # noqa: E241,E501
    ("offset-washer",       [_settings._project_root_abspath / "tests" / "washer.csv"], 360.0,       1., "gmsh"),  # fmt: skip # noqa: E241,E501
    ("washer-axisymmetric", [_settings._project_root_abspath / "tests" / "washer.csv"],   0.0,       0., "gmsh"),  # fmt: skip # noqa: E241,E501
    ("vase",                [_settings._project_root_abspath / "tests" / "vase.csv"],   360.0,       0., "gmsh"),  # fmt: skip # noqa: E241,E501
    ("vase-axisymmetric",   [_settings._project_root_abspath / "tests" / "vase.csv"],     0.0,       0., "gmsh"),  # fmt: skip # noqa: E241,E501
    ("multi-part-3D",       [_settings._project_root_abspath / "tests" / "washer.csv",  # fmt: skip # noqa: E241
                             _settings._project_root_abspath / "tests" / "vase.csv"],   360.0,       0., "gmsh"),  # fmt: skip # noqa: E241,E501
    ("multi-part-2D",       [_settings._project_root_abspath / "tests" / "washer.csv",  # fmt: skip # noqa: E241
                             _settings._project_root_abspath / "tests" / "vase.csv"],     0.0,       0., "gmsh"),  # fmt: skip # noqa: E241,E501
)
for test in system_tests:
    commands_list.append(setup_geometry_commands(*test))

# Sets/mesh tests
system_tests = (
    # model/part, input_file, angle, face_sets, edge_sets, edge seeds, element_type, backend
    # Abaqus
    # TODO: Pick some Abaqus edge sets for the system tests
    (
        "vase",
        [_settings._project_root_abspath / "tests" / "vase.csv"],
        360.0,
        [["top", "'[#4 ]'"], ["bottom", "'[#40 ]'"]],
        None,
        None,
        "C3D8R",
        "abaqus",
    ),
    (
        "vase-axisymmetric",
        [_settings._project_root_abspath / "tests" / "vase.csv"],
        0.0,
        None,
        [["top", "'[#10 ]'"], ["bottom", "'[#1 ]'"]],
        [["top", "5"], ["bottom", "0.5"]],
        "CAX4",
        "abaqus",
    ),
    # Cubit
    (
        "vase",
        [_settings._project_root_abspath / "tests" / "vase.csv"],
        360.0,
        [["top", "4"], ["bottom", "7"], ["outer", "'2 3 8'"]],
        [["top_outer", "13"]],
        [["top_outer", "1.000001"]],
        "C3D8R",
        "cubit",
    ),
    (
        "vase-axisymmetric",
        [_settings._project_root_abspath / "tests" / "vase.csv"],
        0.0,
        None,
        [["top", "2"], ["bottom", "6"], ["outer", "'1 7 8'"]],
        [["top", "1.000001"]],
        "CAX4",
        "cubit",
    ),
)
for test in system_tests:
    commands_list.append(setup_sets_commands(*test))

# Cylinder tests
system_tests = (
    # model/part,   angle, backend
    ("cylinder_3d",  360., "abaqus"),  # fmt: skip # noqa: E241
    ("cylinder_2d",    0., "abaqus"),  # fmt: skip # noqa: E241
    ("cylinder_3d",  360., "cubit"),  # fmt: skip # noqa: E241
    ("cylinder_2d",    0., "cubit"),  # fmt: skip # noqa: E241
    ("cylinder_3d",  360., "gmsh"),  # fmt: skip # noqa: E241
    ("cylinder_2d",    0., "gmsh"),  # fmt: skip # noqa: E241
)
for test in system_tests:
    commands_list.append(setup_cylinder_commands(*test))

# TODO: Merge Gmsh sphere system tests when partition/mesh/image subcommands are implemented
# https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/217
gmsh_sphere_2D = [
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 1. --outer-radius 2. --output-file sphere.step --revolution-angle=0. --backend gmsh"
        )
    ],
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 1. --outer-radius 2. --output-file sphere.step --revolution-angle=0. "
            "--backend gmsh --quadrant upper"
        ),
    ],
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 1. --outer-radius 2. --output-file sphere.step --revolution-angle=0. "
            "--backend gmsh --quadrant lower"
        ),
    ],
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 0. --outer-radius 1. --output-file sphere.step --revolution-angle=0. --backend gmsh"
        ),
    ],
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 0. --outer-radius 1. --output-file sphere.step --revolution-angle=0. "
            "--backend gmsh --quadrant upper"
        ),
    ],
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 0. --outer-radius 1. --output-file sphere.step --revolution-angle=0. "
            "--backend gmsh --quadrant lower"
        ),
    ],
]
for test in gmsh_sphere_2D:
    test.append(
        string.Template(
            "${turbo_turtle_command} mesh --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--input-file sphere.step --output-file sphere.msh --global-seed 1. --element-type unused "
            "--backend gmsh"
        )
    )
    if not missing_display:
        test.append(
            string.Template(
                "${turbo_turtle_command} image --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
                "--input-file sphere.step --output-file sphere.step.png --x-angle 0 --y-angle 0 --backend gmsh"
            )
        )
        test.append(
            string.Template(
                "${turbo_turtle_command} image --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
                "--input-file sphere.msh --output-file sphere.msh.png --x-angle 0 --y-angle 0 --backend gmsh"
            )
        )
    commands_list.append(pytest.param(test, marks=pytest.mark.gmsh))
gmsh_sphere_3D = [
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 1. --outer-radius 2. --output-file sphere.step --revolution-angle=360. "
            "--backend gmsh"
        ),
    ],
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 1. --outer-radius 2. --output-file sphere.step --revolution-angle=360. "
            "--backend gmsh --quadrant upper"
        ),
    ],
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 1. --outer-radius 2. --output-file sphere.step --revolution-angle=360. "
            "--backend gmsh --quadrant lower"
        ),
    ],
    # TODO: Fix solid sphere revolve
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/218
    # [  # fmt: skip # noqa: E265
    #    string.Template(
    #        "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
    #        "--inner-radius 0. --outer-radius 1. --output-file sphere.step --revolution-angle=360. "
    #        "--backend gmsh"
    #    )
    # ],  # fmt: skip # noqa: E265
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 0. --outer-radius 1. --output-file sphere.step --revolution-angle=360. "
            "--backend gmsh --quadrant upper"
        )
    ],
    [
        string.Template(
            "${turbo_turtle_command} sphere --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--inner-radius 0. --outer-radius 1. --output-file sphere.step --revolution-angle=360. "
            "--backend gmsh --quadrant lower"
        )
    ],
]
for test in gmsh_sphere_3D:
    test.append(
        string.Template(
            "${turbo_turtle_command} mesh --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
            "--input-file sphere.step --output-file sphere.msh --global-seed 1. --element-type unused "
            "--backend gmsh"
        )
    )
    if not missing_display:
        test.append(
            string.Template(
                "${turbo_turtle_command} image --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
                "--input-file sphere.step --output-file sphere.step.png --x-angle 45 --y-angle -45 "
                "--backend gmsh"
            )
        )
        test.append(
            string.Template(
                "${turbo_turtle_command} image --abaqus-command ${abaqus_command} --cubit-command ${cubit_command} "
                "--input-file sphere.msh --output-file sphere.msh.png --x-angle 45 --y-angle -45 --backend gmsh"
            )
        )
    commands_list.append(pytest.param(test, marks=pytest.mark.gmsh))

# Merge tests
for part_name in ("washer vase merge-sphere", ""):
    commands_list.append(setup_merge_commands(part_name, backend="abaqus"))
    commands_list.append(setup_merge_commands(part_name, backend="cubit"))

# SCons extensions tests
# System tests as SCons tasks
# TODO: Decide how to handle this system test which requires both Abaqus and Cubit.
# Separate the SConstruct file into Abaqus/Cubit halves? Dedicated, non-matrixed construction environment?
sconstruct = _settings._project_root_abspath / "tests/SConstruct"
commands_list.append(
    pytest.param(
        [
            string.Template(
                f"scons . --sconstruct={sconstruct} --turbo-turtle-command='${{turbo_turtle_command}}' "
                "--abaqus-command=${abaqus_command} --backend=abaqus"
            )
        ],
        marks=pytest.mark.abaqus,
    )
)
commands_list.append(
    pytest.param(
        [
            string.Template(
                f"scons . --sconstruct={sconstruct} --turbo-turtle-command='${{turbo_turtle_command}}' "
                "--cubit-command=${cubit_command} --backend=cubit"
            )
        ],
        marks=pytest.mark.cubit,
    )
)
# User manual example SCons tasks
sconstruct_files = [
    [
        _settings._project_root_abspath / "tutorials/SConstruct",
        _settings._project_root_abspath / "tutorials/SConscript",
    ]
]
for files in sconstruct_files:
    space_delimited_files = " ".join([str(path) for path in files])
    scons_test_commands = [
        string.Template("${turbo_turtle_command} fetch SConstruct SConscript"),
        # FIXME: Figure out why this command fails on the CI server, but not in local user tests
        # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/159
        # f"scons . --turbo-turtle-command="{turbo_turtle_command}""  # fmt: skip # noqa: E265
    ]
    commands_list.append(scons_test_commands)


@pytest.mark.systemtest
@pytest.mark.require_third_party
@pytest.mark.parametrize("commands", commands_list)
def test_require_third_party(abaqus_command, cubit_command, commands: list) -> None:
    """Run system tests that require third-party software

    Executes with a temporary directory that is cleaned up after each test execution.

    Accepts custom pytest CLI options to specify abaqus and cubit commands

    .. code-block::

       pytest --abaqus-command /my/system/abaqus --cubit-command /my/system/cubit

    :param abaqus_command: string absolute path to Abaqus executable
    :param cubit_command: string absolute path to Cubit executable
    :param command: the full list of command string(s) for the system test
    """
    test_project_shell_commands(abaqus_command, cubit_command, commands)


def run_commands(commands, build_directory, template_substitution={}) -> None:
    for command in commands:
        if isinstance(command, string.Template):
            command = command.substitute(template_substitution)
        command = shlex.split(command)
        subprocess.check_output(command, env=env, cwd=build_directory).decode("utf-8")


# Help/Usage sign-of-life
project_only_commands_list = [string.Template("${turbo_turtle_command} -h")]
project_only_commands_list.extend(
    [string.Template(f"${{turbo_turtle_command}} {subcommand} -h") for subcommand in subcommand_list]
)
project_only_commands_list.append(string.Template("${turbo_turtle_command} fetch"))


@pytest.mark.systemtest
@pytest.mark.parametrize("commands", project_only_commands_list)
def test_project_shell_commands(abaqus_command, cubit_command, commands: list) -> None:
    """Run the system tests.

    Executes with a temporary directory that is cleaned up after each test execution.

    Accepts custom pytest CLI options to specify abaqus and cubit commands

    .. code-block::

       pytest --abaqus-command /my/system/abaqus --cubit-command /my/system/cubit

    :param abaqus_command: string absolute path to Abaqus executable
    :param cubit_command: string absolute path to Cubit executable
    :param command: the full list of command string(s) for the system test
    """
    template_substitution = {
        "turbo_turtle_command": turbo_turtle_command,
        "abaqus_command": abaqus_command,
        "cubit_command": cubit_command,
    }
    if isinstance(commands, str) or isinstance(commands, string.Template):
        commands = [commands]
    if installed:
        with tempfile.TemporaryDirectory() as temp_directory:
            run_commands(commands, temp_directory, template_substitution=template_substitution)
    else:
        with tempfile.TemporaryDirectory(dir=build_directory, ignore_cleanup_errors=True) as temp_directory:
            run_commands(commands, temp_directory, template_substitution=template_substitution)
