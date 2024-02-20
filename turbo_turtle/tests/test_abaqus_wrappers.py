import copy
import argparse
from unittest.mock import patch

import pytest

from turbo_turtle import _settings
from turbo_turtle import _abaqus_wrappers


namespace_sparse = {
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
namespace_full = copy.deepcopy(namespace_sparse)
namespace_full.update({"part_name": "part_name"}),
expected_options_sparse = [
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
image = {
    "no part-name": (
        namespace_sparse,
        expected_options_sparse,
        ["--part-name"]
    ),
    "part-name": (
        namespace_full,
        expected_options_sparse + ["--part-name"],
        []
    ),
}


@pytest.mark.parametrize("namespace, expected_options, unexpected_options", image.values(), ids=image.keys())
def test_image(namespace, expected_options, unexpected_options):
    args = argparse.Namespace(**namespace)
    with patch("turbo_turtle._utilities.run_command") as mock_run:
        _abaqus_wrappers.image(args, "command")
    mock_run.assert_called_once()
    command_string = mock_run.call_args[0][0]
    for option in expected_options:
        assert option in command_string
    for option in unexpected_options:
        assert option not in command_string
