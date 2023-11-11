import pytest
import numpy

from turbo_turtle._abaqus_python import lines_and_splines


compare_xy_values = {
    "horizontal": (
        numpy.array([[0, 0], [1, 0]]), [False, True]
    ),
    "vertical": (
        numpy.array([[0, 0], [0, 1]]), [False, True]
    ),
    "x=y": (
        numpy.array([[0, 0], [1, 1]]), [False, False]
    ),
}


@pytest.mark.parametrize("coordinates, expected",
                         compare_xy_values.values(),
                         ids=compare_xy_values.keys())
def test_compare_xy_values(coordinates, expected):
    bools = lines_and_splines._compare_xy_values(coordinates)
    assert bools == expected
