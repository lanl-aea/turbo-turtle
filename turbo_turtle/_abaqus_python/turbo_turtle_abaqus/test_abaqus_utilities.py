"""
.. note::

   These are tests of the pure Abaqus Python utilities. The test file may make Abaqus Python specific imports.
"""

import os
import sys
import inspect
import unittest

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import _abaqus_utilities  # noqa: E402

import abaqusConstants  # noqa: E402


class TestAbaqusUtilities(unittest.TestCase):
    """Python unittest's for :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus._abaqus_utilities`"""

    def test_return_abaqus_constant(self):
        attribute = _abaqus_utilities.return_abaqus_constant("C3D8")
        assert attribute == abaqusConstants.C3D8

    @unittest.expectedFailure
    def test_return_abaqus_constant_exception(self):
        attribute = _abaqus_utilities.return_abaqus_constant("NotFound")
        assert attribute is None

    def test_return_abaqus_constant_or_exit(self):
        attribute = _abaqus_utilities.return_abaqus_constant_or_exit("C3D8")
        assert attribute == abaqusConstants.C3D8

    def test_return_abaqus_constant_or_exit_error(self):
        with self.assertRaises(SystemExit):
            _abaqus_utilities.return_abaqus_constant_or_exit("NotFound")

    def test_revolution_direction(self):
        assert abaqusConstants.ON == _abaqus_utilities.revolution_direction(1.0)
        assert abaqusConstants.OFF == _abaqus_utilities.revolution_direction(-1.0)


if __name__ == "__main__":
    unittest.main()
