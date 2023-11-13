import os
import sys
import inspect
import unittest

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import _utilities


class TestUtilities(unittest.TestCase):
    """Python unittest's for :meth:`turbo_turtle._abaqus_python._abaqus_utilities`"""

    def test_validate_element_type(self):
        tests = [
            (1, [None], [None]),
            (2, [None], [None, None]),
            (2, ["C3D8"], ["C3D8", "C3D8"])
        ]
        for length_part_name, original_element_type, expected in tests:
            element_type = _utilities.validate_element_type(length_part_name, original_element_type)
            assert element_type == expected

    @unittest.expectedFailure
    def test_validate_element_type_exception1(self):
        element_type = _utilities.validate_element_type(1, ["C3D8", "C3D8"])

    def test_validate_element_type_exception1(self):
        with self.assertRaises(SystemExit):
            element_type = _utilities.validate_element_type_or_exit(1, ["C3D8", "C3D8"])

    @unittest.expectedFailure
    def test_validate_element_type_exception2(self):
        element_type = _utilities.validate_element_type(3, ["C3D8", "C3D8"])

    def test_validate_element_type_exception2(self):
        with self.assertRaises(SystemExit):
            element_type = _utilities.validate_element_type_or_exit(3, ["C3D8", "C3D8"])


if __name__ == '__main__':
    unittest.main()