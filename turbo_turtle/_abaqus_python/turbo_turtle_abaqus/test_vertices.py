"""
.. warning::

   These tests are duplicates of the Python 3 tests in :meth:`turbo_turtle.tests.test_vertices`
"""

import os
import sys
import math
import inspect
import unittest

import numpy

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import vertices  # noqa: E402


class TestVertices(unittest.TestCase):
    """Python unittest's for :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices`"""

    def test_compare_xy_values(self):
        tests = [
            (numpy.array([[0, 0], [1, 0]]), [False, True], None, None),
            (numpy.array([[0, 0], [0, 1]]), [False, True], None, None),
            (numpy.array([[0, 0], [1, 1]]), [False, False], None, None),
            (numpy.array([[100, 0], [100 + 100 * 5e-6, 1]]), [False, True], None, None),
            (numpy.array([[100, 0], [100 + 100 * 5e-6, 1]]), [False, False], 1e-6, None),
        ]
        for coordinates, expected, rtol, atol in tests:
            bools = vertices._compare_xy_values(coordinates, rtol=rtol, atol=atol)
            assert bools == expected

    def test_compare_euclidean_distance(self):
        tests = [
            (numpy.array([[0, 0], [1, 0]]), 0.1, [False, True]),
            (numpy.array([[0, 0], [1, 0]]), 10.0, [False, False]),
            (numpy.array([[0, 0], [1, 0]]), 1.0, [False, False]),
        ]
        for coordinates, euclidean_distance, expected in tests:
            bools = vertices._compare_euclidean_distance(coordinates, euclidean_distance)
            assert bools == expected

    def test_bool_via_or(self):
        tests = [
            ([True, True], [False, False], [True, True]),
            ([False, False], [False, False], [False, False]),
            ([True, True], [True, True], [True, True]),
            ([True, False], [False, True], [True, True]),
            ([False, True], [True, False], [True, True]),
        ]
        for bool_list_1, bool_list_2, expected in tests:
            bools = vertices._bool_via_or(bool_list_1, bool_list_2)
            assert bools == expected

    def test_break_coordinates(self):
        tests = [
            (
                numpy.array([[1.0, -0.5], [2.0, -0.5], [2.0, 0.5], [1.0, 0.5]]),
                4,
                [
                    numpy.array([[1.0, -0.5]]),
                    numpy.array([[2.0, -0.5]]),
                    numpy.array([[2.0, 0.5]]),
                    numpy.array([[1.0, 0.5]]),
                ],
            ),
            (
                numpy.array(
                    [
                        [5.1, -5.0],  # fmt: skip # noqa: E201,E202,E203
                        [5.0, -4.8],  # fmt: skip # noqa: E201,E202,E203
                        [4.5, -4.0],  # fmt: skip # noqa: E201,E202,E203
                        [4.1, -3.0],  # fmt: skip # noqa: E201,E202,E203
                        [4.0, -2.5],  # fmt: skip # noqa: E201,E202,E203
                        [4.0,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                        [4.1,  3.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [4.5,  4.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [5.0,  4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                        [5.1,  5.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [3.0,  5.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [3.0, -4.0],  # fmt: skip # noqa: E201,E202,E203
                        [0.0, -4.0],  # fmt: skip # noqa: E201,E202,E203
                        [0.0, -5.0],
                    ]
                ),  # noqa: E201,E202,E203
                4,
                [
                    numpy.array(
                        [
                            [5.1, -5.0],  # noqa: E201,E202,E203,E241
                            [5.0, -4.8],  # noqa: E201,E202,E203,E241
                            [4.5, -4.0],  # noqa: E201,E202,E203,E241
                            [4.1, -3.0],  # noqa: E201,E202,E203,E241
                            [4.0, -2.5],
                        ]
                    ),  # noqa: E201,E202,E203,E241
                    numpy.array(
                        [
                            [4.0, 2.5],  # noqa: E201,E202,E203,E241
                            [4.1, 3.0],  # noqa: E201,E202,E203,E241
                            [4.5, 4.0],  # noqa: E201,E202,E203,E241
                            [5.0, 4.8],  # noqa: E201,E202,E203,E241
                            [5.1, 5.0],
                        ]
                    ),  # noqa: E201,E202,E203,E241
                    numpy.array([[3.0,  5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[3.0, -4.0]]),  # noqa: E201,E202,E203,E241
                    numpy.array([[0.0, -4.0]]),  # noqa: E201,E202,E203,E241
                    numpy.array([[0.0, -5.0]]),
                ],
            ),  # noqa: E201,E202,E203,E241
        ]
        for coordinates, euclidean_distance, expected in tests:
            all_splines = vertices._break_coordinates(coordinates, euclidean_distance)
            for spline, expectation in zip(all_splines, expected):
                assert numpy.allclose(spline, expectation)

    def test_line_pairs(self):
        tests = [
            (
                [
                    numpy.array([[1.0, -0.5]]),
                    numpy.array([[2.0, -0.5]]),
                    numpy.array([[2.0,  0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241,E501
                    numpy.array([[1.0,  0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241,E501
                ],
                [
                    (numpy.array([1.0, -0.5]), numpy.array([2.0, -0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([2.0, -0.5]), numpy.array([2.0,  0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([2.0,  0.5]), numpy.array([1.0,  0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([1.0,  0.5]), numpy.array([1.0, -0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
                ],
            ),
            (
                [
                    numpy.array(
                        [
                            [5.1, -5.0],  # noqa: E201,E202,E203,E241
                            [5.0, -4.8],  # noqa: E201,E202,E203,E241
                            [4.5, -4.0],  # noqa: E201,E202,E203,E241
                            [4.1, -3.0],  # noqa: E201,E202,E203,E241
                            [4.0, -2.5],  # noqa: E201,E202,E203,E241
                        ]
                    ),
                    numpy.array(
                        [
                            [4.0, 2.5],  # noqa: E201,E202,E203,E241
                            [4.1, 3.0],  # noqa: E201,E202,E203,E241
                            [4.5, 4.0],  # noqa: E201,E202,E203,E241
                            [5.0, 4.8],  # noqa: E201,E202,E203,E241
                            [5.1, 5.0],  # noqa: E201,E202,E203,E241
                        ]
                    ),
                    numpy.array([[3.0,  5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[3.0, -4.0]]),  # noqa: E201,E202,E203,E241
                    numpy.array([[0.0, -4.0]]),  # noqa: E201,E202,E203,E241
                    numpy.array([[0.0, -5.0]]),  # noqa: E201,E202,E203,E241
                ],
                [
                    (numpy.array([4.0, -2.5]), numpy.array([4.0,  2.5])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([5.1,  5.0]), numpy.array([3.0,  5.0])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([3.0,  5.0]), numpy.array([3.0, -4.0])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([3.0, -4.0]), numpy.array([0.0, -4.0])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([0.0, -4.0]), numpy.array([0.0, -5.0])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([0.0, -5.0]), numpy.array([5.1, -5.0])),  # fmt: skip # noqa: E201,E202,E203,E241
                ],
            ),
        ]
        for all_splines, expected in tests:
            line_pairs = vertices._line_pairs(all_splines)
            for pair, expectation in zip(line_pairs, expected):
                assert len(pair) == len(expectation)
                assert numpy.allclose(pair[0], expectation[0])
                assert numpy.allclose(pair[1], expectation[1])

    def test_scale_and_offset_coordinates(self):
        tests = [
            (
                numpy.array(
                    [
                        [
                            0.0,
                            0.0
                        ],
                        [1.0, 1.0],
                    ]
                ),
                1.0,
                0.0,
                numpy.array(
                    [
                        [
                            0.0,
                            0.0
                        ],
                        [1.0, 1.0],
                    ]
                ),
            ),
            (
                numpy.array(
                    [
                        [
                            0.0,
                            0.0
                        ],
                        [1.0, 1.0],
                    ]
                ),
                2.0,
                0.0,
                numpy.array(
                    [
                        [
                            0.0,
                            0.0
                        ],
                        [2.0, 2.0],
                    ]
                ),
            ),
            (
                numpy.array(
                    [
                        [
                            0.0,
                            0.0
                        ],
                        [1.0, 1.0],
                    ]
                ),
                1.0,
                1.0,
                numpy.array(
                    [
                        [
                            0.0,
                            1.0
                        ],
                        [1.0, 2.0],
                    ]
                ),
            ),
            (
                numpy.array(
                    [
                        [
                            0.0,
                            0.0
                        ],
                        [1.0, 1.0],
                    ]
                ),
                2.0,
                1.0,
                numpy.array(
                    [
                        [
                            0.0,
                            1.0
                        ],
                        [2.0, 3.0],
                    ]
                ),
            ),
        ]
        for coordinates, unit_conversion, y_offset, expected in tests:
            new_coordinates = vertices.scale_and_offset_coordinates(coordinates, unit_conversion, y_offset)
            assert numpy.allclose(new_coordinates, expected)

    def test_lines_and_splines(self):
        tests = [
            (
                numpy.array([[1.0, -0.5], [2.0, -0.5], [2.0, 0.5], [1.0, 0.5]]),
                4,
                [
                    numpy.array([[1.0, -0.5], [2.0, -0.5]]),
                    numpy.array([[2.0, -0.5], [2.0,  0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[2.0,  0.5], [1.0,  0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[1.0,  0.5], [1.0, -0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
                ],
                [],
            ),
            (
                numpy.array(
                    [
                        [5.1, -5.0],  # noqa: E201,E202,E203,E241
                        [5.0, -4.8],  # noqa: E201,E202,E203,E241
                        [4.5, -4.0],  # noqa: E201,E202,E203,E241
                        [4.1, -3.0],  # noqa: E201,E202,E203,E241
                        [4.0, -2.5],  # noqa: E201,E202,E203,E241
                        [4.0,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                        [4.1,  3.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [4.5,  4.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [5.0,  4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                        [5.1,  5.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [3.0,  5.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [3.0, -4.0],  # noqa: E201,E202,E203,E241
                        [0.0, -4.0],  # noqa: E201,E202,E203,E241
                        [0.0, -5.0],  # noqa: E201,E202,E203,E241
                    ]
                ),
                4,
                [
                    numpy.array([[4.0, -2.5], [4.0,  2.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[5.1,  5.0], [3.0,  5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[3.0,  5.0], [3.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[3.0, -4.0], [0.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[0.0, -4.0], [0.0, -5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[0.0, -5.0], [5.1, -5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                ],
                [
                    numpy.array(
                        [
                            [5.1, -5.0],  # noqa: E201,E202,E203,E241
                            [5.0, -4.8],  # noqa: E201,E202,E203,E241
                            [4.5, -4.0],  # noqa: E201,E202,E203,E241
                            [4.1, -3.0],  # noqa: E201,E202,E203,E241
                            [4.0, -2.5],  # noqa: E201,E202,E203,E241
                        ]
                    ),
                    numpy.array(
                        [
                            [4.0, 2.5],  # noqa: E201,E202,E203,E241
                            [4.1, 3.0],  # noqa: E201,E202,E203,E241
                            [4.5, 4.0],  # noqa: E201,E202,E203,E241
                            [5.0, 4.8],  # noqa: E201,E202,E203,E241
                            [5.1, 5.0],  # noqa: E201,E202,E203,E241
                        ]
                    ),
                ],
            ),
        ]
        for coordinates, euclidean_distance, expected_lines, expected_splines in tests:
            lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance)
            assert len(lines) == len(expected_lines)
            for line, expectation in zip(lines, expected_lines):
                assert numpy.allclose(line, expectation)
            assert len(splines) == len(expected_splines)
            for spline, expectation in zip(splines, expected_splines):
                assert numpy.allclose(spline, expectation)

    def test_ordered_lines_and_splines(self):
        tests = [
            (
                numpy.array([[1.0, -0.5], [2.0, -0.5], [2.0, 0.5], [1.0, 0.5]]),
                4,
                [
                    numpy.array([[1.0, -0.5], [2.0, -0.5]]),
                    numpy.array([[2.0, -0.5], [2.0,  0.5]]),  # fmt: skip # noqa: E241
                    numpy.array([[2.0,  0.5], [1.0,  0.5]]),  # fmt: skip # noqa: E241
                    numpy.array([[1.0,  0.5], [1.0, -0.5]]),  # fmt: skip # noqa: E241
                ],
            ),
            (
                numpy.array(
                    [
                        [5.1, -5.0],  # noqa: E201,E202,E241
                        [5.0, -4.8],  # noqa: E201,E202,E203,E241
                        [4.5, -4.0],  # noqa: E201,E202,E241
                        [4.1, -3.0],  # noqa: E201,E202,E241
                        [4.0, -2.5],  # noqa: E201,E202,E203,E241
                        [4.0,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                        [4.1,  3.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [4.5,  4.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [5.0,  4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                        [5.1,  5.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [3.0,  5.0],  # fmt: skip # noqa: E201,E202,E203,E241
                        [3.0, -4.0],  # noqa: E201,E202,E203,E241
                        [0.0, -4.0],  # noqa: E201,E202,E203,E241
                        [0.0, -5.0],  # noqa: E201,E202,E203,E241
                    ]
                ),
                4,
                [
                    numpy.array(
                        [
                            [5.1, -5.0],  # noqa: E201,E202,E203,E241
                            [5.0, -4.8],  # noqa: E201,E202,E203,E241
                            [4.5, -4.0],  # noqa: E201,E202,E203,E241
                            [4.1, -3.0],  # noqa: E201,E202,E203,E241
                            [4.0, -2.5],  # noqa: E201,E202,E203,E241
                        ]
                    ),
                    numpy.array(
                        [
                            [4.0, -2.5],
                            [4.0,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                        ]
                    ),
                    numpy.array(
                        [
                            [4.0, 2.5],  # noqa: E201,E202,E203,E241
                            [4.1, 3.0],  # noqa: E201,E202,E203,E241
                            [4.5, 4.0],  # noqa: E201,E202,E203,E241
                            [5.0, 4.8],  # noqa: E201,E202,E203,E241
                            [5.1, 5.0],  # noqa: E201,E202,E203,E241
                        ]
                    ),
                    numpy.array([[5.1,  5.0], [3.0,  5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[3.0,  5.0], [3.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[3.0, -4.0], [0.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[0.0, -4.0], [0.0, -5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([[0.0, -5.0], [5.1, -5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
                ],
            ),
        ]
        for coordinates, euclidean_distance, expected_lines_and_splines in tests:
            lines_and_splines = vertices.ordered_lines_and_splines(coordinates, euclidean_distance)
            assert len(lines_and_splines) == len(expected_lines_and_splines)
            for curve, expectation in zip(lines_and_splines, expected_lines_and_splines):
                assert numpy.allclose(curve, expectation)

    # TODO: flesh out when we figure out how to patch in Abaqus Python 2
    def test_lines_and_splines_passthrough(self):
        pass

    # TODO: flesh out when we figure out how to patch in Abaqus Python 2
    def test_break_coordinates_passthrough(self):
        pass

    def test_cylinder(self):
        tests = [
            (1.0, 2.0, 1.0, None, numpy.array([[1.0, 0.5], [2.0, 0.5], [2.0, -0.5], [1.0, -0.5]])),
            (1.0, 2.0, 1.0, 0.5, numpy.array([[1.0, 1.0], [2.0, 1.0], [2.0, 0.0], [1.0, 0.0]])),
        ]
        for inner_radius, outer_radius, height, y_offset, expected in tests:
            kwargs = {}
            if y_offset is not None:
                kwargs = {"y_offset": y_offset}
            coordinates = vertices.cylinder(inner_radius, outer_radius, height, **kwargs)
            assert numpy.allclose(coordinates, expected)

    def test_cylinder_lines(self):
        tests = [
            (
                1.0,
                2.0,
                1.0,
                None,
                [
                    (numpy.array([1.0,  0.5]), numpy.array([2.0,  0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([2.0,  0.5]), numpy.array([2.0, -0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([2.0, -0.5]), numpy.array([1.0, -0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
                    (numpy.array([1.0, -0.5]), numpy.array([1.0,  0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
                ],
            ),
            (
                1.0,
                2.0,
                1.0,
                0.5,
                [
                    (numpy.array([1.0, 1.0]), numpy.array([2.0, 1.0])),
                    (numpy.array([2.0, 1.0]), numpy.array([2.0, 0.0])),
                    (numpy.array([2.0, 0.0]), numpy.array([1.0, 0.0])),
                    (numpy.array([1.0, 0.0]), numpy.array([1.0, 1.0])),
                ],
            ),
        ]
        for inner_radius, outer_radius, height, y_offset, expected in tests:
            kwargs = {}
            if y_offset is not None:
                kwargs = {"y_offset": y_offset}
            lines = vertices.cylinder_lines(inner_radius, outer_radius, height, **kwargs)
            for line, expected_line in zip(lines, expected):
                assert numpy.allclose(line, expected_line)

    def test_rectalinear_coordinates(self):
        number = math.sqrt(2.0**2 / 2.0)
        tests = [
            (
                (1, 1, 1, 1),
                (0, math.pi / 2, math.pi, 2 * math.pi),
                ((1, 0), (0, 1), (-1, 0), (1, 0)),
            ),
            (
                (2, 2, 2, 2),
                (math.pi / 4, math.pi * 3 / 4, math.pi * 5 / 4, math.pi * 7 / 4),
                ((number, number), (-number, number), (-number, -number), (number, -number)),
            ),
        ]
        for radius_list, angle_list, expected in tests:
            coordinates = vertices.rectalinear_coordinates(radius_list, angle_list)
            assert numpy.allclose(coordinates, expected)

    def test_normalize_vector(self):
        one_over_root_three = 1.0 / math.sqrt(3.0)
        tests = [
            ((0.0, 0.0, 0.0), numpy.array([0.0, 0.0, 0.0])),
            ((1.0, 0.0, 0.0), numpy.array([1.0, 0.0, 0.0])),
            ((0.0, 1.0, 0.0), numpy.array([0.0, 1.0, 0.0])),
            ((0.0, 0.0, 1.0), numpy.array([0.0, 0.0, 1.0])),
            ((1.0, 1.0, 1.0), numpy.array([one_over_root_three, one_over_root_three, one_over_root_three])),
            ((2.0, 2.0, 2.0), numpy.array([one_over_root_three, one_over_root_three, one_over_root_three])),
        ]
        for vector, expected in tests:
            normalized = vertices.normalize_vector(vector)
            assert numpy.allclose(normalized, expected)

    def test_midpoint_vector(self):
        tests = [
            ([1.0, 0, 0], [0, 1.0, 0], numpy.array([0.5, 0.5, 0.0])),
            ([1.0, 0, 0], [0, -1.0, 0], numpy.array([0.5, -0.5, 0.0])),
            ([0, 1.0, 0], [0, 0, 1.0], numpy.array([0, 0.5, 0.5])),
            ([0, 1.0, 0], [0, 0, -1.0], numpy.array([0, 0.5, -0.5])),
            ([1.0, 1.0, 1.0], [-1.0, 1.0, 1.0], numpy.array([0, 1.0, 1.0])),
        ]
        for first, second, expected in tests:
            midpoint = vertices.midpoint_vector(first, second)
            assert numpy.allclose(midpoint, expected)

    def test_is_parallel(self):
        tests = [
            ((1.0, 1.0, 1.0), (1.0, 1.0, 1.0), True),
            ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), False),
            ((0.0, 1.0, 0.0), (0.0, 2.0, 0.0), True),
        ]
        for first, second, expected in tests:
            boolean = vertices.is_parallel(first, second)
            assert boolean == expected

    def test_any_parallel(self):
        tests = [
            ((1.0, 1.0, 1.0), [(1.0, 1.0, 1.0), (1.0, 0.0, 0.0)], True),
            ((1.0, 0.0, 0.0), [(0.0, 0.0, 1.0), (0.0, 1.0, 0.0)], False),
            ((0.0, 1.0, 0.0), [(2.0, 0.0, 0.0), (0.0, 2.0, 0.0)], True),
        ]
        for first, options, expected in tests:
            boolean = vertices.any_parallel(first, options)
            assert boolean == expected

    def test_datum_planes(self):
        norm = math.sqrt(0.5)
        tests = [
            (
                (1.0, 0.0, 0.0),
                (0.0, 0.0, 1.0),
                [
                    numpy.array([  0.0,   0.0,   1.0]),  # fmt: skip # noqa: E201,E202,E203,E241 # XY plane
                    numpy.array([  1.0,   0.0,   0.0]),  # fmt: skip # noqa: E201,E202,E203,E241 # YZ plane
                    numpy.array([  0.0,   1.0,   0.0]),  # fmt: skip # noqa: E201,E202,E203,E241 # ZX plane
                    numpy.array([ norm,  norm,   0.0]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([ norm, -norm,   0.0]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([  0.0,  norm,  norm]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([  0.0,  norm, -norm]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([ norm,   0.0,  norm]),  # fmt: skip # noqa: E201,E202,E203,E241
                    numpy.array([-norm,   0.0,  norm]),  # fmt: skip # noqa: E201,E202,E203,E241
                ],
            ),
        ]
        for xvector, zvector, expected in tests:
            planes = vertices.datum_planes(xvector, zvector)
            for plane, expectation in zip(planes, expected):
                assert numpy.allclose(plane, expectation)

    def test_fortyfive_vectors(self):
        over_root_three = 1.0 / math.sqrt(3.0)
        tests = [
            (
                numpy.array([1.0, 0.0, 0.0]),
                numpy.array([0.0, 0.0, 1.0]),
                [
                    numpy.array([ over_root_three,  over_root_three,  over_root_three]),  # fmt: skip # noqa: E201,E202,E203,E241,E501
                    numpy.array([-over_root_three,  over_root_three,  over_root_three]),  # fmt: skip # noqa: E201,E202,E203,E241,E501
                    numpy.array([-over_root_three,  over_root_three, -over_root_three]),  # fmt: skip # noqa: E201,E202,E203,E241,E501
                    numpy.array([ over_root_three,  over_root_three, -over_root_three]),  # fmt: skip # noqa: E201,E202,E203,E241,E501
                    numpy.array([ over_root_three, -over_root_three,  over_root_three]),  # fmt: skip # noqa: E201,E202,E203,E241,E501
                    numpy.array([-over_root_three, -over_root_three,  over_root_three]),  # fmt: skip # noqa: E201,E202,E203,E241,E501
                    numpy.array([-over_root_three, -over_root_three, -over_root_three]),  # fmt: skip # noqa: E201,E202,E203,E241,E501
                    numpy.array([ over_root_three, -over_root_three, -over_root_three]),  # fmt: skip # noqa: E201,E202,E203,E241,E501
                ],
            ),
        ]
        for xvector, zvector, expected in tests:
            fortyfive_vectors = vertices.fortyfive_vectors(xvector, zvector)
            for vector, expectation in zip(fortyfive_vectors, expected):
                assert numpy.allclose(vector, expectation)
