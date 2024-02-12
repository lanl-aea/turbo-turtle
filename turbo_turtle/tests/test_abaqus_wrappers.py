import argparse

from unittest.mock import patch

from turbo_turtle import _settings
from turbo_turtle import _abaqus_wrappers


def test_image():
    args = argparse.Namespace(
        input_file="input_file",
        output_file="output_file",
        x_angle=0.,
        y_angle=0.,
        z_angle=0.,
        image_size=[1, 2],
        model_name="model_name",
        part_name="part_name",
        color_map="color_map"
    )
    expected_cli_options = [
        "command",
        "--input-file",
        "--output-file",
        "--x-angle",
        "--y-angle",
        "--z-angle",
        "--image-size",
        "--model-name",
        "--part-name",
        "--color-map"
    ]
    with patch("turbo_turtle._utilities.run_command") as mock_run:
        _abaqus_wrappers.image(args, "command")
    mock_run.assert_called_once()
    for option in expected_cli_options:
        assert option in mock_run.call_args[0][0]
