from contextlib import nullcontext as does_not_raise

import numpy
import pytest
cubit = pytest.importorskip("cubit", reason="Could not import Cubit")

from turbo_turtle import _cubit_python


cubit_command_or_exception = {
    "good command": ("reset aprepro", does_not_raise()),
    "bad command": ("definitetlynotacubitcommand", pytest.raises(RuntimeError)),
}


@pytest.mark.parametrize("command, outcome",
                         cubit_command_or_exception.values(),
                         ids=cubit_command_or_exception.keys())
def test_cubit_command_or(command, outcome):
    with outcome:
        try:
            success = _cubit_python.cubit_command_or_exception(command)
            assert success is True
        finally:
            pass

    if not isinstance(outcome, does_not_raise):
        exit_outcome = pytest.raises(SystemExit)
    else:
        exit_outcome = outcome
    with exit_outcome:
        try:
            success = _cubit_python.cubit_command_or_exit(command)
            assert success is True
        finally:
            pass


create_curve_from_coordinates = {
    "float": ((0., 0., 0.), (1., 0., 0.), (0.5, 0., 0.), 1.0),
    "int": ((0, 0, 0), (1, 0, 0), (0.5, 0., 0.), 1.0),
}


@pytest.mark.parametrize("point1, point2, center, length",
                         create_curve_from_coordinates.values(),
                         ids=create_curve_from_coordinates.keys())
def test_create_curve_from_coordinates(point1, point2, center, length):
    curve = _cubit_python._create_curve_from_coordinates(point1, point2)
    assert numpy.isclose(curve.length(), length)
    assert numpy.allclose(curve.center_point(), center)
