import argparse
from unittest.mock import patch

import pytest

from turbo_turtle import _settings
from turbo_turtle import _abaqus_wrappers



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
    "part-name": (
        argparse.Namespace(
            input_file="input_file",
            output_file="output_file",
            x_angle=0.,
            y_angle=0.,
            z_angle=0.,
            image_size=[1, 2],
            model_name="model_name",
            part_name="part_name",
            color_map="color_map"
        ),
        expected_options_sparse + ["--part-name"]
    ),
    "no part-name": (
        argparse.Namespace(
            input_file="input_file",
            output_file="output_file",
            x_angle=0.,
            y_angle=0.,
            z_angle=0.,
            image_size=[1, 2],
            model_name="model_name",
            part_name=None,
            color_map="color_map"
        ),
        expected_options_sparse
    ),
}


@pytest.mark.parametrize("namespace, expected_options", image.values(), ids=image.keys())
def test_image(namespace, expected_options):
    with patch("turbo_turtle._utilities.run_command") as mock_run:
        _abaqus_wrappers.image(namespace, "command")
    mock_run.assert_called_once()
    command_string = mock_run.call_args[0][0]
    for option in expected_options:
        assert option in command_string
    if namespace.part_name is None:
        assert "--part-name" not in command_string
