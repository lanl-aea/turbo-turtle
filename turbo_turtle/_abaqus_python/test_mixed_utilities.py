"""
.. warning::

   These tests are duplicates of the Python 3 tests in :meth:`turbo_turtle.tests.test_mixed_utilities`
"""
import os
import sys
import inspect
import unittest

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import _mixed_utilities


class TestUtilities(unittest.TestCase):
    """Python unittest's for :meth:`turbo_turtle._abaqus_python._mixed_utilities`"""

    def test_validate_element_type(self):
        tests = [
            (1, [None], [None]),
            (2, [None], [None, None]),
            (2, ["C3D8"], ["C3D8", "C3D8"])
        ]
        for length_part_name, original_element_type, expected in tests:
            element_type = _mixed_utilities.validate_element_type(length_part_name, original_element_type)
            self.assertEqual(element_type, expected)

    @unittest.expectedFailure
    def test_validate_element_type_exception1(self):
        element_type = _mixed_utilities.validate_element_type(1, ["C3D8", "C3D8"])

    def test_validate_element_type_exception1(self):
        with self.assertRaises(SystemExit):
            element_type = _mixed_utilities.validate_element_type_or_exit(1, ["C3D8", "C3D8"])

    @unittest.expectedFailure
    def test_validate_element_type_exception2(self):
        element_type = _mixed_utilities.validate_element_type(3, ["C3D8", "C3D8"])

    def test_validate_element_type_exception2(self):
        with self.assertRaises(SystemExit):
            element_type = _mixed_utilities.validate_element_type_or_exit(3, ["C3D8", "C3D8"])

    def test_remote_duplicate_items(self):
        tests = [
            (["thing1", "thing2"], ["thing1", "thing2"]),
            (["thing1", "thing2", "thing1"], ["thing1", "thing2"]),
        ]
        for string_list, expected in tests:
            unique = _mixed_utilities.remove_duplicate_items(string_list)
            self.assertEqual(unique, expected)
            # TODO: Figure out how to verify sys.stderr.write and print without mock module in Abaqus Python

    def test_intersection_of_lists(self):
        tests = [
            ([None], ["thing1", "thing2"], ["thing1", "thing2"]),
            (["thing1", "thing2"], ["thing1", "thing2"], ["thing1", "thing2"]),
            (["thing1"], ["thing1", "thing2"], ["thing1"]),
        ]
        for requested, available, expected in tests:
            intersection = _mixed_utilities.intersection_of_lists(requested, available)
            self.assertEqual(intersection, expected)

    def test_substitute_element_type(self):
        pass


if __name__ == '__main__':
    unittest.main()
