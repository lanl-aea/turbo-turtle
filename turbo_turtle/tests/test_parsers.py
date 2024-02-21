import pytest
import numpy

from turbo_turtle._abaqus_python import parsers


def test_positive_float():
    assert numpy.isclose(parsers.positive_float("1."), 1.)
    assert numpy.isclose(parsers.positive_float("0."), 0.)
