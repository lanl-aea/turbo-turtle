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
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import _mixed_utilities  # noqa: E402


class TestMixedUtilities(unittest.TestCase):
    """Abaqus Python unittests for :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus._mixed_utilities`"""

    def test_validate_element_type(self):
        tests = [
            (1, [None], [None]),
            (2, [None], [None, None]),
            (2, ["C3D8"], ["C3D8", "C3D8"]),
        ]
        for length_part_name, original_element_type, expected in tests:
            element_type = _mixed_utilities.validate_element_type(length_part_name, original_element_type)
            self.assertEqual(element_type, expected)

    @unittest.expectedFailure
    def test_validate_element_type_exception1(self):
        element_type = _mixed_utilities.validate_element_type(1, ["C3D8", "C3D8"])
        assert element_type is None

    def test_validate_element_type_exception1_exit(self):
        with self.assertRaises(SystemExit):
            _mixed_utilities.validate_element_type_or_exit(1, ["C3D8", "C3D8"])

    @unittest.expectedFailure
    def test_validate_element_type_exception2(self):
        element_type = _mixed_utilities.validate_element_type(3, ["C3D8", "C3D8"])
        assert element_type is None

    def test_validate_element_type_exception2_exit(self):
        with self.assertRaises(SystemExit):
            _mixed_utilities.validate_element_type_or_exit(3, ["C3D8", "C3D8"])

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

    def test_element_type_regex(self):
        tests = [
            (
                "*element, type=C3D8\n*ELEMENT, TYPE=C3D8\n*Element, Type=C3D8\n",
                "C3D8R",
                "*element, type=C3D8R\n*ELEMENT, TYPE=C3D8R\n*Element, Type=C3D8R\n",
            ),
            (
                "*element, type=square4\n*ELEMENT, TYPE=SQUARE4\n*Element, Type=Square4\n",
                "CAX4",
                "*element, type=CAX4\n*ELEMENT, TYPE=CAX4\n*Element, Type=CAX4\n",
            ),
        ]
        for content, element_type, expected in tests:
            new_contents = _mixed_utilities._element_type_regex(content, element_type)
            self.assertEqual(new_contents, expected)

    def test_substitute_element_type(self):
        # TODO: Figure out how to mock file i/o with Python 2 unittest and no mock module
        pass


if __name__ == "__main__":
    unittest.main()
