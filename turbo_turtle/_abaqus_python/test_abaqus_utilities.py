import os
import sys
import inspect
import unittest

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import _abaqus_utilities

import abaqusConstants


class TestAbaqusUtilities(unittest.TestCase):

    def test_return_abaqus_constant(self):
        attribute = _abaqus_utilities.return_abaqus_constant("C3D8")
        assert attribute == abaqusConstants.C3D8

    @unittest.expectedFailure
    def test_return_abaqus_constant_exception(self):
        attribute = _abaqus_utilities.return_abaqus_constant("NotFound")

    def test_return_abaqus_constant_or_exit(self):
        attribute = _abaqus_utilities.return_abaqus_constant_or_exit("C3D8")
        assert attribute == abaqusConstants.C3D8

    def test_return_abaqus_constant_or_exit_error(self):
        with self.assertRaises(SystemExit):
            attribute = _abaqus_utilities.return_abaqus_constant_or_exit("NotFound")


if __name__ == '__main__':
    unittest.main()
