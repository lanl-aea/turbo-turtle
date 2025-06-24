import math
from contextlib import nullcontext as does_not_raise

import numpy
import pytest

cubit = pytest.importorskip("cubit", reason="Could not import Cubit")

from turbo_turtle import _cubit_python  # noqa: E402


pytestmark = pytest.mark.cubit_python


cubit_command_or_exception = {
    "good command": ("reset aprepro", does_not_raise()),
    "bad command": ("definitetlynotacubitcommand", pytest.raises(RuntimeError)),
}


@pytest.mark.parametrize(
    "command, outcome",
    cubit_command_or_exception.values(),
    ids=cubit_command_or_exception.keys(),
)
def test_cubit_command_or_exception(command, outcome):
    with outcome:
        try:
            success = _cubit_python.cubit_command_or_exception(command)
            assert success is True
        finally:
            pass


create_curve_from_coordinates = {
    "float": (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.5, 0.0, 0.0),
        1.0,
    ),
    "int": (
        (0, 0, 0),
        (1, 0, 0),
        (0.5, 0.0, 0.0),
        1.0,
    ),
}


@pytest.mark.parametrize(
    "point1, point2, center, length",
    create_curve_from_coordinates.values(),
    ids=create_curve_from_coordinates.keys(),
)
def test_create_curve_from_coordinates(point1, point2, center, length):
    curve = _cubit_python.create_curve_from_coordinates(point1, point2)
    assert curve.dimension() == 1
    assert numpy.isclose(curve.length(), length)
    assert numpy.allclose(curve.center_point(), center)


create_spline_from_coordinates = {
    "too few points": (
        numpy.array([[0.0, 0.0, 0.0]]),
        pytest.raises(RuntimeError),
    ),
    "two points": (
        numpy.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]),
        does_not_raise(),
    ),
    "three points": (
        numpy.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
        does_not_raise(),
    ),
    "four points": (
        numpy.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]),
        does_not_raise(),
    ),
}


@pytest.mark.parametrize(
    "coordinates, outcome",
    create_spline_from_coordinates.values(),
    ids=create_spline_from_coordinates.keys(),
)
def test_create_spline_from_coordinates(coordinates, outcome):
    with outcome:
        try:
            curve = _cubit_python.create_spline_from_coordinates(coordinates)
            assert curve.dimension() == 1
        finally:
            pass


quarter_arc_length = 2.0 * math.pi / 4.0
create_arc_from_coordinates = {
    "float": (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        quarter_arc_length,
    ),
    "int": (
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        quarter_arc_length,
    ),
}


@pytest.mark.parametrize(
    "center, point1, point2, length",
    create_arc_from_coordinates.values(),
    ids=create_arc_from_coordinates.keys(),
)
def test_create_arc_from_coordinates(center, point1, point2, length):
    curve = _cubit_python.create_arc_from_coordinates(center, point1, point2)
    assert numpy.isclose(curve.length(), length)


create_surface_from_coordinates = {
    "too few points": (
        numpy.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]),
        pytest.raises(RuntimeError),
    ),
    "three points": (
        numpy.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
        does_not_raise(),
    ),
    "four points": (
        numpy.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]),
        does_not_raise(),
    ),
}


@pytest.mark.parametrize(
    "coordinates, outcome",
    create_surface_from_coordinates.values(),
    ids=create_surface_from_coordinates.keys(),
)
def test_create_surface_from_coordinates(coordinates, outcome):
    with outcome:
        try:
            surface = _cubit_python.create_surface_from_coordinates(coordinates)
            assert len(surface.surfaces()) == 1
            assert len(surface.curves()) == coordinates.shape[0]
            assert len(surface.vertices()) == coordinates.shape[0]
        finally:
            pass
