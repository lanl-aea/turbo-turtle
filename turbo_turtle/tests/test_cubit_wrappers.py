import copy
import argparse
from unittest.mock import patch

import pytest

from turbo_turtle import _settings
from turbo_turtle import _cubit_wrappers


cubit_command = "/dummy/command/cubit"

geometry_keywords = {
    "planar": False,
    "part_name": ["part_name"],
    "unit_conversion": 1.,
    "euclidean_distance": 1.,
    "delimiter": ",",
    "header_lines": 0,
    "revolution_angle": 360.,
    "y_offset": 0.
}
geometry_namespace = copy.deepcopy(geometry_keywords)
geometry_namespace.update({"input_file": ["input_file"], "output_file": "output_file"})

wrapper_tests = {
    "geometry": (
        "geometry",
        geometry_namespace,
        (["input_file"], "output_file"),
        geometry_keywords
    ),
}


@pytest.mark.parametrize("subcommand, namespace, positional, keywords",
                         wrapper_tests.values(), ids=wrapper_tests.keys())
def test_cubit_wrappers(subcommand, namespace, positional, keywords):
    args = argparse.Namespace(**namespace)
    with patch(f"turbo_turtle._cubit_python.{subcommand}") as mock_function:
        subcommand_wrapper = getattr(_cubit_wrappers, subcommand)
        subcommand_wrapper(args, cubit_command)
    mock_function.assert_called_once_with(*positional, **keywords)
