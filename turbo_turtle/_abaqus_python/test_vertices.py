"""
.. warning::

   These tests are duplicates of the Python 3 tests in :meth:`turbo_turtle.tests.test_mixed_utilities`
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

    def test_compare_euclidean_distance(self):
        tests = [
            (numpy.array([[0, 0], [1, 0]]), 0.1, [False, True]),
            (numpy.array([[0, 0], [1, 0]]), 10., [False, False]),
            (numpy.array([[0, 0], [1, 0]]), 1.0, [False, False])
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
            ([False, True], [True, False], [True, True])
        ]
        for bool_list_1, bool_list_2, expected in tests:
            bools = vertices._bool_via_or(bool_list_1, bool_list_2)
            assert bools == expected

    def test_break_coordinates(self):
        tests = [
            (numpy.array([[1.0, -0.5], [2.0, -0.5], [2.0, 0.5], [1.0, 0.5]]),
             4,
             [numpy.array([[1.0, -0.5]]), numpy.array([[2.0, -0.5]]), numpy.array([[2.0, 0.5]]), numpy.array([[1.0, 0.5]])]),
            (numpy.array([[ 5.1, -5. ],
                          [ 5. , -4.8],
                          [ 4.5, -4. ],
                          [ 4.1, -3. ],
                          [ 4. , -2.5],
                          [ 4. ,  2.5],
                          [ 4.1,  3. ],
                          [ 4.5,  4. ],
                          [ 5. ,  4.8],
                          [ 5.1,  5. ],
                          [ 3. ,  5. ],
                          [ 3. , -4. ],
                          [ 0. , -4. ],
                          [ 0. , -5. ]]),
             4,
             [numpy.array([[ 5.1, -5. ],
                           [ 5. , -4.8],
                           [ 4.5, -4. ],
                           [ 4.1, -3. ],
                           [ 4. , -2.5]]),
              numpy.array([[ 4. ,  2.5],
                           [ 4.1,  3. ],
                           [ 4.5,  4. ],
                           [ 5. ,  4.8],
                           [ 5.1,  5. ]]),
              numpy.array([[ 3.0,  5.0]]),
              numpy.array([[ 3.0, -4.0]]),
              numpy.array([[ 0.0, -4.0]]),
              numpy.array([[ 0.0, -5.0]])])
        ]
        for coordinates, euclidean_distance, expected in tests:
            all_splines = vertices._break_coordinates(coordinates, euclidean_distance)
            for spline, expectation in zip(all_splines, expected):
                assert numpy.allclose(spline, expectation)

    def test_line_pairs(self):
        tests = [
            (
                [numpy.array([[1.0, -0.5]]), numpy.array([[2.0, -0.5]]), numpy.array([[2.0, 0.5]]), numpy.array([[1.0, 0.5]])],
                [(numpy.array([1.0, -0.5]), numpy.array([2.0, -0.5])),
                 (numpy.array([2.0, -0.5]), numpy.array([2.0,  0.5])),
                 (numpy.array([2.0,  0.5]), numpy.array([1.0,  0.5])),
                 (numpy.array([1.0,  0.5]), numpy.array([1.0, -0.5]))]
            ),
            (
                [numpy.array([[ 5.1, -5. ],
                              [ 5. , -4.8],
                              [ 4.5, -4. ],
                              [ 4.1, -3. ],
                              [ 4. , -2.5]]),
                 numpy.array([[ 4. ,  2.5],
                              [ 4.1,  3. ],
                              [ 4.5,  4. ],
                              [ 5. ,  4.8],
                              [ 5.1,  5. ]]),
                 numpy.array([[ 3.0,  5.0]]),
                 numpy.array([[ 3.0, -4.0]]),
                 numpy.array([[ 0.0, -4.0]]),
                 numpy.array([[ 0.0, -5.0]])],
                [(numpy.array([ 4. , -2.5]), numpy.array([ 4. ,  2.5])),
                 (numpy.array([ 5.1,  5. ]), numpy.array([ 3.0,  5.0])),
                 (numpy.array([ 3.0,  5.0]), numpy.array([ 3.0, -4.0])),
                 (numpy.array([ 3.0, -4.0]), numpy.array([ 0.0, -4.0])),
                 (numpy.array([ 0.0, -4.0]), numpy.array([ 0.0, -5.0])),
                 (numpy.array([ 0.0, -5.0]), numpy.array([ 5.1, -5. ]))]
            )
        ]
        for all_splines, expected in tests:
            line_pairs = vertices._line_pairs(all_splines)
            for pair, expectation in zip(line_pairs, expected):
                assert len(pair) == len(expectation)
                assert numpy.allclose(pair[0], expectation[0])
                assert numpy.allclose(pair[1], expectation[1])

    def test_lines_and_splines(self):
        tests = [
            (
                numpy.array([[1.0, -0.5], [2.0, -0.5], [2.0, 0.5], [1.0, 0.5]]),
                4,
                [(numpy.array([1.0, -0.5]), numpy.array([2.0, -0.5])),
                 (numpy.array([2.0, -0.5]), numpy.array([2.0,  0.5])),
                 (numpy.array([2.0,  0.5]), numpy.array([1.0,  0.5])),
                 (numpy.array([1.0,  0.5]), numpy.array([1.0, -0.5]))],
                []
            ),
            (
                numpy.array([[ 5.1, -5. ],
                             [ 5. , -4.8],
                             [ 4.5, -4. ],
                             [ 4.1, -3. ],
                             [ 4. , -2.5],
                             [ 4. ,  2.5],
                             [ 4.1,  3. ],
                             [ 4.5,  4. ],
                             [ 5. ,  4.8],
                             [ 5.1,  5. ],
                             [ 3. ,  5. ],
                             [ 3. , -4. ],
                             [ 0. , -4. ],
                             [ 0. , -5. ]]),
                4,
                [(numpy.array([ 4. , -2.5]), numpy.array([ 4. ,  2.5])),
                 (numpy.array([ 5.1,  5. ]), numpy.array([ 3.0,  5.0])),
                 (numpy.array([ 3.0,  5.0]), numpy.array([ 3.0, -4.0])),
                 (numpy.array([ 3.0, -4.0]), numpy.array([ 0.0, -4.0])),
                 (numpy.array([ 0.0, -4.0]), numpy.array([ 0.0, -5.0])),
                 (numpy.array([ 0.0, -5.0]), numpy.array([ 5.1, -5. ]))],
                [numpy.array([[ 5.1, -5. ],
                              [ 5. , -4.8],
                              [ 4.5, -4. ],
                              [ 4.1, -3. ],
                              [ 4. , -2.5]]),
                 numpy.array([[ 4. ,  2.5],
                              [ 4.1,  3. ],
                              [ 4.5,  4. ],
                              [ 5. ,  4.8],
                              [ 5.1,  5. ]])]
            )
        ]
        for coordinates, euclidean_distance, expected_lines, expected_splines in tests:
            lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance)
            for pair, expectation in zip(lines, expected_lines):
                assert len(pair) == len(expectation)
                assert numpy.allclose(pair[0], expectation[0])
                assert numpy.allclose(pair[1], expectation[1])
            assert len(splines) == len(expected_splines)
            for spline, expectation in zip(splines, expected_splines):
                assert numpy.allclose(spline, expectation)

    def test_cylinder(self):
        tests = [
            (1., 2., 1., None, numpy.array([[1., 0.5], [2., 0.5], [2., -0.5], [1., -0.5]])),
            (1., 2., 1., 0.5, numpy.array([[1., 1.], [2., 1.], [2., 0.], [1., 0.]]))
        ]
        for inner_radius, outer_radius, height, y_offset, expected in tests:
            kwargs = {}
            if y_offset is not None:
                kwargs = {"y_offset": y_offset}
            coordinates = vertices.cylinder(inner_radius, outer_radius, height, **kwargs)
            assert numpy.allclose(coordinates, expected)

    def test_rectalinear_coordinates(self):
        number = math.sqrt(2.**2 / 2.)
        tests = [
            ((1, 1, 1, 1), (0, math.pi / 2, math.pi, 2 * math.pi), ((1, 0), (0, 1), (-1, 0), (1, 0))),
            ((2, 2, 2, 2), (math.pi / 4, math.pi * 3 / 4, math.pi * 5 / 4, math.pi * 7 / 4),
             ((number, number), (-number, number), (-number, -number), (number, -number)))
        ]
        for radius_list, angle_list, expected in tests:
            coordinates = vertices.rectalinear_coordinates(radius_list, angle_list)
            assert numpy.allclose(coordinates, expected)

    def test_normalize_vector(self):
        one_over_root_three = 1. / math.sqrt(3.)
        tests = [
            ((0., 0., 0.), numpy.array([0., 0., 0.])),
            ((1., 0., 0.), numpy.array([1., 0., 0.])),
            ((0., 1., 0.), numpy.array([0., 1., 0.])),
            ((0., 0., 1.), numpy.array([0., 0., 1.])),
            ((1., 1., 1.), numpy.array([one_over_root_three, one_over_root_three, one_over_root_three])),
            ((2., 2., 2.), numpy.array([one_over_root_three, one_over_root_three, one_over_root_three])),
        ]
        for vector, expected in tests:
            normalized = vertices.normalize_vector(vector)
            assert numpy.allclose(normalized, expected)
