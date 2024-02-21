import pytest

from turbo_turtle._abaqus_python import parsers


def test_positive_float():
    assert(parsers.positive_float("1.") == 1.)
    assert(parsers.positive_float("0.") == 0.)
