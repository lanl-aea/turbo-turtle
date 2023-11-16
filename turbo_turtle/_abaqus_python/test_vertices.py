"""
.. warning::

   These tests are duplicates of the Python 3 tests in :meth:`turbo_turtle.tests.test_mixed_utilities`
"""
import os
import sys
import inspect
import unittest

import numpy

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import vertices 


class TestVertices(unittest.TestCase):
    """Python unittest's for :meth:`turbo_turtle._abaqus_python.vertices`"""

    def test_compare_xy_values(self):
        tests = [
            (numpy.array([[0, 0], [1, 0]]), [False, True], None, None),
            (numpy.array([[0, 0], [0, 1]]), [False, True], None, None),
            (numpy.array([[0, 0], [1, 1]]), [False, False], None, None),
            (numpy.array([[100, 0], [100 + 100*5e-6, 1]]), [False, True], None, None),
            (numpy.array([[100, 0], [100 + 100*5e-6, 1]]), [False, False], 1e-6, None),
        ]
        for coordinates, expected, rtol, atol in tests:
            bools = vertices._compare_xy_values(coordinates, rtol=rtol, atol=atol)
            assert bools == expected
