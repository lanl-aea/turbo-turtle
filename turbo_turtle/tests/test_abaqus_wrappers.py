import copy
import argparse
from unittest.mock import patch

import pytest

from turbo_turtle import _settings
from turbo_turtle import _abaqus_wrappers


image_namespace_sparse = {
    "input_file": "input_file",
    "output_file": "output_file",
    "x_angle": 0.,
    "y_angle": 0.,
    "z_angle": 0.,
    "image_size": [1, 2],
    "model_name": "model_name",
    "part_name": None,
    "color_map": "color_map"
}
image_namespace_full = copy.deepcopy(image_namespace_sparse)
image_namespace_full.update({"part_name": "part_name"}),
image_expected_options_sparse = [
    "command",
    "--input-file",
    "--output-file",
    "--x-angle",
    "--y-angle",
    "--z-angle",
    "--image-size",
    "--model-name",
    "--color-map"
]
wrapper_tests = {
    "image: no part-name": (
        "image",
        image_namespace_sparse,
        image_expected_options_sparse,
        ["--part-name"]
    ),
    "image: part-name": (
        "image",
        image_namespace_full,
        image_expected_options_sparse + ["--part-name"],
        []
    ),
}


@pytest.mark.parametrize("subcommand, namespace, expected_options, unexpected_options",
                         wrapper_tests.values(), ids=wrapper_tests.keys())
def test_image(subcommand, namespace, expected_options, unexpected_options):
    args = argparse.Namespace(**namespace)
    with patch("turbo_turtle._utilities.run_command") as mock_run:
        subcommand_wrapper = getattr(_abaqus_wrappers, subcommand)
        subcommand_wrapper(args, "/dummy/command/abaqus")
    mock_run.assert_called_once()
    command_string = mock_run.call_args[0][0]
    for option in expected_options:
        assert option in command_string
    for option in unexpected_options:
        assert option not in command_string
