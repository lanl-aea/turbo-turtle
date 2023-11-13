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


if __name__ == '__main__':
    unittest.main()
