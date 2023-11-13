import os
import sys
import inspect
import unittest

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import _utilities


class TestAbaqusUtilities(unittest.TestCase):

    def test_abaqus_constant(self):
        assert True


if __name__ == '__main__':
    unittest.main()
