import argparse
from unittest.mock import patch
from contextlib import nullcontext as does_not_raise

import pytest
import numpy

from turbo_turtle._abaqus_python import parsers


positive_float = {
    "zero": ("0.", 0., does_not_raise()),
    "one": ("1.", 1., does_not_raise()),
    "negative": ("-1.", None, pytest.raises(argparse.ArgumentTypeError)),
    "string": ("negative_one", None, pytest.raises(argparse.ArgumentTypeError)),
}


@pytest.mark.parametrize("input_string, expected_float, outcome",
                         positive_float.values(),
                         ids=positive_float.keys())
def test_positive_float(input_string, expected_float, outcome):
    with outcome:
        try:
            argument = parsers.positive_float(input_string)
            assert numpy.isclose(argument, expected_float)
        finally:
            pass


positive_int = {
    "zero": ("0", 0, does_not_raise()),
    "one": ("1", 1, does_not_raise()),
    "negative": ("-1", None, pytest.raises(argparse.ArgumentTypeError)),
    "string": ("negative_one", None, pytest.raises(argparse.ArgumentTypeError)),
}


@pytest.mark.parametrize("input_string, expected_int, outcome",
                         positive_int.values(),
                         ids=positive_int.keys())
def test_positive_int(input_string, expected_int, outcome):
    with outcome:
        try:
            argument = parsers.positive_int(input_string)
            assert argument == expected_int
        finally:
            pass
