import copy
import argparse
from unittest.mock import patch

import pytest

from turbo_turtle import _abaqus_wrappers


command = "/dummy/command"

geometry_namespace_sparse = {
    "input_file": ["input_file"],
    "output_file": "output_file",
    "unit_conversion": 1.0,
    "euclidean_distance": 1.0,
    "planar": None,
    "model_name": "model_name",
    "part_name": [None],
    "delimiter": ",",
    "header_lines": 0,
    "revolution_angle": 360.0,
    "y_offset": 0.0,
    "rtol": None,
    "atol": None,
}
geometry_namespace_full = copy.deepcopy(geometry_namespace_sparse)
geometry_namespace_full.update({"planar": True, "part_name": ["part_name"], "rtol": 1.0e-9, "atol": 1.0e-9}),
geometry_expected_options_sparse = [
    "--input-file",
    "--output-file",
    "--unit-conversion",
    "--euclidean-distance",
    "--model-name",
    "--delimiter",
    "--header-lines",
    "--revolution-angle",
    "--y-offset",
]
geometry_unexpected_options_sparse = ["--planar", "--part-name", "--atol", "--rtol"]

cylinder_namespace = {
    "inner_radius": 1.0,
    "outer_radius": 2.0,
    "height": 1.0,
    "output_file": "output_file",
    "model_name": "model_name",
    "part_name": "part_name",
    "revolution_angle": 360.0,
    "y_offset": 0.0,
}
cylinder_expected_options = [
    command,
    "--inner-radius",
    "--outer-radius",
    "--height",
    "--output-file",
    "--model-name",
    "--part-name",
    "--revolution-angle",
    "--y-offset",
]

sphere_namespace_sparse = {
    "inner_radius": 1.0,
    "outer_radius": 2.0,
    "output_file": "output_file",
    "input_file": None,
    "quadrant": "both",
    "revolution_angle": 360.0,
    "y_offset": 0.0,
    "model_name": "model_name",
    "part_name": "part_name",
}
sphere_namespace_full = copy.deepcopy(sphere_namespace_sparse)
sphere_namespace_full.update({"input_file": "input_file"}),
sphere_expected_options_sparse = [
    command,
    "--inner-radius",
    "--outer-radius",
    "--output-file",
    "--quadrant",
    "--revolution-angle",
    "--y-offset",
    "--model-name",
    "--part-name",
]
sphere_unexpected_options_sparse = ["--input-file"]

partition_namespace_sparse = {
    "input_file": "input_file",
    "output_file": None,
    "center": (0.0, 0.0, 0.0),
    "xvector": (0.0, 0.0, 0.0),
    "zvector": (0.0, 0.0, 0.0),
    "model_name": "model_name",
    "part_name": ["part_name"],
    "big_number": 0.0,
}
partition_namespace_full = copy.deepcopy(partition_namespace_sparse)
partition_namespace_full.update({"output_file": "output_file"}),
partition_expected_options_sparse = [
    command,
    "--input-file",
    "--center",
    "--xvector",
    "--zvector",
    "--model-name",
    "--part-name",
    "--big-number",
]
partition_unexpected_options_sparse = ["--output-file"]

sets_namespace_sparse = {
    "input_file": "input_file",
    "output_file": None,
    "model_name": "model_name",
    "part_name": "part_name",
    "face_sets": None,
    "edge_sets": None,
    "vertex_sets": None,
}
sets_namespace_full = copy.deepcopy(sets_namespace_sparse)
sets_namespace_full.update(
    {
        "output_file": "output_file",
        "face_sets": [["name1", "2"]],
        "edge_sets": [["name2", "4"]],
        "vertex_sets": [["name3", "6"]],
    }
)
sets_expected_options_sparse = [command, "--input-file", "--model-name", "--part-name"]
sets_unexpected_options_sparse = ["--output-file", "--face-set", "--edge-set", "--vertex-set"]

mesh_namespace_sparse = {
    "input_file": "input_file",
    "element_type": "element_type",
    "output_file": None,
    "model_name": "model_name",
    "part_name": "part_name",
    "global_seed": "global_seed",
    "edge_seeds": None,
}
mesh_namespace_full = copy.deepcopy(mesh_namespace_sparse)
mesh_namespace_full.update({"output_file": "output_file", "edge_seeds": [["name", "1"]]}),
mesh_expected_options_sparse = [
    command,
    "--input-file",
    "--element-type",
    "--model-name",
    "--part-name",
    "--global-seed",
]
mesh_unexpected_options_sparse = ["--output-file", "--edge-seed"]

merge_namespace_sparse = {
    "input_file": ["input_file"],
    "output_file": "output_file",
    "merged_model_name": "merged_model_name",
    "model_name": [None],
    "part_name": [None],
}
merge_namespace_full = copy.deepcopy(merge_namespace_sparse)
merge_namespace_full.update(
    {
        "model_name": ["model_name"],
        "part_name": ["part_name"],
    }
),
merge_expected_options_sparse = [
    "--input-file",
    "--output-file",
    "--merged-model-name",
]
merge_unexpected_options_sparse = ["--model-name", "--part-name"]

export_namespace_sparse = {
    "input_file": "input_file",
    "model_name": "model_name",
    "part_name": ["part_name"],
    "element_type": [None],
    "destination": ".",
    "assembly": None,
}
export_namespace_full = copy.deepcopy(export_namespace_sparse)
export_namespace_full.update(
    {
        "element_type": ["element_type"],
        "assembly": True,
    }
),
export_expected_options_sparse = ["--input-file", "--model-name", "--part-name", "--destination"]
export_unexpected_options_sparse = ["--element-type", "--assembly"]

image_namespace_sparse = {
    "input_file": "input_file",
    "output_file": "output_file",
    "x_angle": 0.0,
    "y_angle": 0.0,
    "z_angle": 0.0,
    "image_size": [1, 2],
    "model_name": "model_name",
    "part_name": None,
    "color_map": "color_map",
}
image_namespace_full = copy.deepcopy(image_namespace_sparse)
image_namespace_full.update({"part_name": "part_name"}),
image_expected_options_sparse = [
    command,
    "--input-file",
    "--output-file",
    "--x-angle",
    "--y-angle",
    "--z-angle",
    "--image-size",
    "--model-name",
    "--color-map",
]
image_unexpected_options_sparse = ["--part-name"]

wrapper_tests = {
    "cylinder": ("cylinder", cylinder_namespace, cylinder_expected_options, []),
    "geometry: sparse": (
        "geometry",
        geometry_namespace_sparse,
        geometry_expected_options_sparse,
        geometry_unexpected_options_sparse,
    ),
    "geometry: full": (
        "geometry",
        geometry_namespace_full,
        geometry_expected_options_sparse + geometry_unexpected_options_sparse,
        [],
    ),
    "sphere: sparse": (
        "sphere",
        sphere_namespace_sparse,
        sphere_expected_options_sparse,
        sphere_unexpected_options_sparse,
    ),
    "sphere: full": (
        "sphere",
        sphere_namespace_full,
        sphere_expected_options_sparse + sphere_unexpected_options_sparse,
        [],
    ),
    "partition: sparse": (
        "partition",
        partition_namespace_sparse,
        partition_expected_options_sparse,
        partition_unexpected_options_sparse,
    ),
    "partition: full": (
        "partition",
        partition_namespace_full,
        partition_expected_options_sparse + partition_unexpected_options_sparse,
        [],
    ),
    "sets: sparse": (
        "sets",
        sets_namespace_sparse,
        sets_expected_options_sparse,
        sets_unexpected_options_sparse,
    ),
    "sets: full": (
        "sets",
        sets_namespace_full,
        sets_expected_options_sparse + sets_unexpected_options_sparse,
        [],
    ),
    "mesh: sparse": (
        "mesh",
        mesh_namespace_sparse,
        mesh_expected_options_sparse,
        mesh_unexpected_options_sparse,
    ),
    "mesh: full": (
        "mesh",
        mesh_namespace_full,
        mesh_expected_options_sparse + mesh_unexpected_options_sparse,
        [],
    ),
    "merge: sparse": (
        "merge",
        merge_namespace_sparse,
        merge_expected_options_sparse,
        merge_unexpected_options_sparse,
    ),
    "merge: full": (
        "merge",
        merge_namespace_full,
        merge_expected_options_sparse + merge_unexpected_options_sparse,
        [],
    ),
    "export: sparse": (
        "export",
        export_namespace_sparse,
        export_expected_options_sparse,
        export_unexpected_options_sparse,
    ),
    "export: full": (
        "export",
        export_namespace_full,
        export_expected_options_sparse + export_unexpected_options_sparse,
        [],
    ),
    "image: sparse": (
        "image",
        image_namespace_sparse,
        image_expected_options_sparse,
        image_unexpected_options_sparse,
    ),
    "image: full": (
        "image",
        image_namespace_full,
        image_expected_options_sparse + image_unexpected_options_sparse,
        [],
    ),
}


@pytest.mark.parametrize(
    "subcommand, namespace, expected_options, unexpected_options",
    wrapper_tests.values(),
    ids=wrapper_tests.keys(),
)
def test_abaqus_wrappers(subcommand, namespace, expected_options, unexpected_options):
    args = argparse.Namespace(**namespace)
    with patch("turbo_turtle._utilities.run_command") as mock_run:
        subcommand_wrapper = getattr(_abaqus_wrappers, subcommand)
        subcommand_wrapper(args, command)
    mock_run.assert_called_once()
    command_string = mock_run.call_args[0][0]
    for option in expected_options:
        assert option in command_string
    for option in unexpected_options:
        assert option not in command_string


def trim_namespace(original, pop_keys):
    """Create a modified dictionary deepcopy by removing the provided keys

    :returns: Modified dictionary deepcopy with pop keys removed
    :rtype: dict
    """
    modified = copy.deepcopy(original)
    for key in pop_keys:
        if key in modified:
            modified.pop(key)
    return modified


def test_trim_namespace():
    original = {"keep": "keep", "pop": "pop"}
    modified = trim_namespace(original, ("pop",))
    assert modified == {"keep": "keep"}


geometry_positional = ("input_file", "output_file")
geometry_unused = ("model_name",)
geometry_keywords = trim_namespace(geometry_namespace_sparse, geometry_positional + geometry_unused)

cylinder_positional = ("inner_radius", "outer_radius", "height", "output_file")
cylinder_unused = ("model_name",)
cylinder_keywords = trim_namespace(cylinder_namespace, cylinder_positional + cylinder_unused)

sphere_positional = ("inner_radius", "outer_radius", "output_file")
sphere_unused = ("model_name",)
sphere_keywords = trim_namespace(sphere_namespace_sparse, sphere_positional + sphere_unused)

partition_positional = ("input_file",)
partition_unused = ("model_name",)
partition_keywords = trim_namespace(partition_namespace_sparse, partition_positional + partition_unused)

mesh_positional = ("input_file", "element_type")
mesh_unused = ("model_name",)
mesh_keywords = trim_namespace(mesh_namespace_sparse, mesh_positional + mesh_unused)

merge_positional = ("input_file", "output_file")
merge_unused = ("model_name", "merged_model_name", "part_name")
merge_keywords = trim_namespace(merge_namespace_sparse, merge_positional + merge_unused)

export_namespace_cubit = copy.deepcopy(export_namespace_sparse)
export_namespace_cubit["output_type"] = "output_type"
export_positional = ("input_file",)
export_unused = ("model_name", "assembly")
export_keywords = trim_namespace(export_namespace_cubit, export_positional + export_unused)

image_positional = ("input_file", "output_file", "command")
image_unused = ("model_name", "part_name", "color_map")
image_keywords = trim_namespace(image_namespace_sparse, image_positional + image_unused)

cubit_wrapper_tests = {
    "geometry": ("geometry", geometry_namespace_sparse, (["input_file"], "output_file"), geometry_keywords),
    "cylinder": ("cylinder", cylinder_namespace, (1.0, 2.0, 1.0, "output_file"), cylinder_keywords),
    "sphere": ("sphere", sphere_namespace_sparse, (1.0, 2.0, "output_file"), sphere_keywords),
    "partition": ("partition", partition_namespace_sparse, ("input_file",), partition_keywords),
    "mesh": ("mesh", mesh_namespace_sparse, ("input_file", "element_type"), mesh_keywords),
    "merge": ("merge", merge_namespace_sparse, (["input_file"], "output_file"), merge_keywords),
    "export": ("export", export_namespace_cubit, ("input_file",), export_keywords),
    "image": ("image", image_namespace_sparse, ("input_file", "output_file", command), image_keywords),
}


@pytest.mark.parametrize(
    "subcommand, namespace, positional, keywords",
    cubit_wrapper_tests.values(),
    ids=cubit_wrapper_tests.keys(),
)
def test_cubit_wrappers(subcommand, namespace, positional, keywords):
    args = argparse.Namespace(**namespace)
    with (
        patch("turbo_turtle._utilities.import_cubit"),
        patch(f"turbo_turtle._cubit_python.{subcommand}") as mock_function,
    ):
        from turbo_turtle import _cubit_wrappers

        subcommand_wrapper = getattr(_cubit_wrappers, subcommand)
        subcommand_wrapper(args, command)
    mock_function.assert_called_once()
    call_positional = mock_function.call_args[0]
    call_keywords = mock_function.call_args[1]
    assert call_positional == positional
    assert call_keywords == keywords


geometry_keywords = trim_namespace(geometry_namespace_sparse, geometry_positional)
cylinder_keywords = trim_namespace(cylinder_namespace, cylinder_positional)
sphere_keywords = trim_namespace(sphere_namespace_sparse, sphere_positional)
partition_keywords = trim_namespace(partition_namespace_sparse, partition_positional)
mesh_keywords = trim_namespace(mesh_namespace_sparse, mesh_positional)
merge_keywords = trim_namespace(merge_namespace_sparse, merge_positional)
export_keywords = trim_namespace(export_namespace_cubit, export_positional)
image_keywords = trim_namespace(image_namespace_sparse, image_positional + image_unused)
gmsh_wrapper_tests = {
    "geometry": (
        "geometry",
        geometry_namespace_sparse,
        (["input_file"], "output_file"),
        geometry_keywords,
    ),
    "cylinder": (
        "cylinder",
        cylinder_namespace,
        (1.0, 2.0, 1.0, "output_file"),
        cylinder_keywords,
    ),
    "sphere": (
        "sphere",
        sphere_namespace_sparse,
        (1.0, 2.0, "output_file"),
        sphere_keywords,
    ),
    "partition": (
        "partition",
        partition_namespace_sparse,
        ("input_file",),
        partition_keywords,
    ),
    "mesh": (
        "mesh",
        mesh_namespace_sparse,
        ("input_file", "element_type"),
        mesh_keywords,
    ),
    "merge": (
        "merge",
        merge_namespace_sparse,
        (["input_file"], "output_file"),
        merge_keywords,
    ),
    "export": (
        "export",
        export_namespace_cubit,
        ("input_file",),
        export_keywords,
    ),
    "image": (
        "image",
        image_namespace_sparse,
        ("input_file", "output_file"),
        image_keywords,
    ),
}


@pytest.mark.parametrize(
    "subcommand, namespace, positional, keywords",
    gmsh_wrapper_tests.values(),
    ids=gmsh_wrapper_tests.keys(),
)
def test_gmsh_wrappers(subcommand, namespace, positional, keywords):
    args = argparse.Namespace(**namespace)
    implemented = ["geometry", "cylinder", "sphere", "mesh", "image"]
    if subcommand in implemented:
        with (
            patch("turbo_turtle._utilities.import_gmsh"),
            patch(f"turbo_turtle._gmsh_python.{subcommand}") as mock_function,
        ):
            from turbo_turtle import _gmsh_wrappers

            subcommand_wrapper = getattr(_gmsh_wrappers, subcommand)
            subcommand_wrapper(args, command)
        mock_function.assert_called_once()
        call_positional = mock_function.call_args[0]
        call_keywords = mock_function.call_args[1]
        assert call_positional == positional
        assert call_keywords == keywords
    else:
        with (
            patch("turbo_turtle._utilities.import_gmsh"),
            patch(f"turbo_turtle._gmsh_python.{subcommand}") as mock_function,
            pytest.raises(RuntimeError),
        ):
            from turbo_turtle import _gmsh_wrappers

            subcommand_wrapper = getattr(_gmsh_wrappers, subcommand)
            subcommand_wrapper(args, command)
