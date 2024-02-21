from unittest.mock import patch
from contextlib import nullcontext as does_not_raise

import pytest
import numpy

from turbo_turtle._abaqus_python import parsers


positive_float = {
    "zero": ("0.", 0., does_not_raise()),
    "one": ("1.", 1., does_not_raise()),
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
