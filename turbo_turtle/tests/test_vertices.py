"""
.. warning::

   These are tests of a mixed Python 2/3 compatible module. When updating, be sure to update the Abaqus Python tests to
   match.
"""
from unittest.mock import patch
import pytest
import numpy
import math

from turbo_turtle._abaqus_python.turbo_turtle_abaqus import vertices


compare_xy_values = {
    "horizontal": (
        numpy.array([[0, 0], [1, 0]]), [False, True], None, None
    ),
    "vertical": (
        numpy.array([[0, 0], [0, 1]]), [False, True], None, None
    ),
    "x=y": (
        numpy.array([[0, 0], [1, 1]]), [False, False], None, None
    ),
    "inside default rtol": (
        numpy.array([[100, 0], [100 + 100 * 5e-6, 1]]), [False, True], None, None
    ),
    "adjust rtol": (
        numpy.array([[100, 0], [100 + 100 * 5e-6, 1]]), [False, False], 1e-6, None
    ),
}


@pytest.mark.parametrize("coordinates, expected, rtol, atol",
                         compare_xy_values.values(),
                         ids=compare_xy_values.keys(),)
def test_compare_xy_values(coordinates, expected, rtol, atol):
    bools = vertices._compare_xy_values(coordinates, rtol=rtol, atol=atol)
    assert bools == expected


compare_euclidean_distance = {
    "longer": (
        numpy.array([[0, 0], [1, 0]]), 0.1, [False, True]
    ),
    "shorter": (
        numpy.array([[0, 0], [1, 0]]), 10., [False, False]
    ),
    "equal": (
        numpy.array([[0, 0], [1, 0]]), 1.0, [False, False]
    ),
}


@pytest.mark.parametrize("coordinates, euclidean_distance, expected",
                         compare_euclidean_distance.values(),
                         ids=compare_euclidean_distance.keys(),)
def test_compare_euclidean_distance(coordinates, euclidean_distance, expected):
    bools = vertices._compare_euclidean_distance(coordinates, euclidean_distance)
    assert bools == expected


bool_via_or = {
    "all true vs all false": (
        [True, True],
        [False, False],
        [True, True]
    ),
    "all false": (
        [False, False],
        [False, False],
        [False, False],
    ),
    "all true": (
        [True, True],
        [True, True],
        [True, True],
    ),
    "true/false mirror": (
        [True, False],
        [False, True],
        [True, True]
    ),
    "true/false mirror 2": (
        [False, True],
        [True, False],
        [True, True]
    ),
}


@pytest.mark.parametrize("bool_list_1, bool_list_2, expected",
                         bool_via_or.values(),
                         ids=bool_via_or.keys(),)
def test_bool_via_or(bool_list_1, bool_list_2, expected):
    bools = vertices._bool_via_or(bool_list_1, bool_list_2)
    assert bools == expected


break_coordinates = {
    "washer": (
        numpy.array([[1.0, -0.5], [2.0, -0.5], [2.0, 0.5], [1.0, 0.5]]),
        4,
        [numpy.array([[1.0, -0.5]]), numpy.array([[2.0, -0.5]]), numpy.array([[2.0, 0.5]]), numpy.array([[1.0, 0.5]])]
    ),
    "vase": (
        numpy.array(
            [
                [ 5.1, -5. ],  # fmt: skip # noqa: E201,E202
                [ 5. , -4.8],  # fmt: skip # noqa: E201,E202,E203
                [ 4.5, -4. ],  # fmt: skip # noqa: E201,E202
                [ 4.1, -3. ],  # fmt: skip # noqa: E201,E202
                [ 4. , -2.5],  # fmt: skip # noqa: E201,E202,E203
                [ 4. ,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4.1,  3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4.5,  4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 5. ,  4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 5.1,  5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 3. ,  5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 3. , -4. ],  # fmt: skip # noqa: E201,E202,E203
                [ 0. , -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 0. , -5. ],  # fmt: skip # noqa: E201,E202,E203,E241
            ]
        ),
        4,
        [
            numpy.array(
                [
                    [ 5.1, -5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 5. , -4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.5, -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.1, -3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4. , -2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                ]
            ),
            numpy.array(
                [
                    [ 4. ,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.1,  3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.5,  4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 5. ,  4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 5.1,  5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                ]
            ),
            numpy.array([[ 3.0,  5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 3.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 0.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 0.0, -5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
        ]
    )
}


@pytest.mark.parametrize("coordinates, euclidean_distance, expected",
                         break_coordinates.values(),
                         ids=break_coordinates.keys(),)
def test_break_coordinates(coordinates, euclidean_distance, expected):
    all_splines = vertices._break_coordinates(coordinates, euclidean_distance)
    for spline, expectation in zip(all_splines, expected):
        assert numpy.allclose(spline, expectation)


line_pairs = {
    "washer": (
        [numpy.array([[1.0, -0.5]]), numpy.array([[2.0, -0.5]]), numpy.array([[2.0, 0.5]]), numpy.array([[1.0, 0.5]])],
        [
            (numpy.array([1.0, -0.5]), numpy.array([2.0, -0.5])),
            (numpy.array([2.0, -0.5]), numpy.array([2.0,  0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
            (numpy.array([2.0,  0.5]), numpy.array([1.0,  0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
            (numpy.array([1.0,  0.5]), numpy.array([1.0, -0.5])),  # fmt: skip # noqa: E201,E202,E203,E241
        ]
    ),
    "vase": (
        [
            numpy.array(
                [
                    [ 5.1, -5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 5. , -4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.5, -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.1, -3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4. , -2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                ]
            ),
            numpy.array(
                [
                    [ 4. ,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.1,  3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.5,  4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 5. ,  4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 5.1,  5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                ]
            ),
            numpy.array([[ 3.0,  5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 3.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 0.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 0.0, -5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
        ],
        [
            (numpy.array([ 4. , -2.5]), numpy.array([ 4. ,  2.5])),  # fmt: skip # noqa: E201,E202,E203,E241
            (numpy.array([ 5.1,  5. ]), numpy.array([ 3.0,  5.0])),  # fmt: skip # noqa: E201,E202,E203,E241
            (numpy.array([ 3.0,  5.0]), numpy.array([ 3.0, -4.0])),  # fmt: skip # noqa: E201,E202,E203,E241
            (numpy.array([ 3.0, -4.0]), numpy.array([ 0.0, -4.0])),  # fmt: skip # noqa: E201,E202,E203,E241
            (numpy.array([ 0.0, -4.0]), numpy.array([ 0.0, -5.0])),  # fmt: skip # noqa: E201,E202,E203,E241
            (numpy.array([ 0.0, -5.0]), numpy.array([ 5.1, -5. ])),  # fmt: skip # noqa: E201,E202,E203,E241
        ]
    ),
}


@pytest.mark.parametrize("all_splines, expected",
                         line_pairs.values(),
                         ids=line_pairs.keys(),)
def test_line_pairs(all_splines, expected):
    line_pairs = vertices._line_pairs(all_splines)
    for pair, expectation in zip(line_pairs, expected):
        assert len(pair) == len(expectation)
        assert numpy.allclose(pair[0], expectation[0])
        assert numpy.allclose(pair[1], expectation[1])


scale_and_offset_coordinates = {
    "no modifications": (
        numpy.array([[0., 0.,], [1., 1.]]),
        1.,
        0.,
        numpy.array([[0., 0.,], [1., 1.]])
    ),
    "scale": (
        numpy.array([[0., 0.,], [1., 1.]]),
        2.,
        0.,
        numpy.array([[0., 0.,], [2., 2.]])
    ),
    "offset": (
        numpy.array([[0., 0.,], [1., 1.]]),
        1.,
        1.,
        numpy.array([[0., 1.,], [1., 2.]])
    ),
    "both": (
        numpy.array([[0., 0.,], [1., 1.]]),
        2.,
        1.,
        numpy.array([[0., 1.,], [2., 3.]])
    ),
}


@pytest.mark.parametrize("coordinates, unit_conversion, y_offset, expected",
                         scale_and_offset_coordinates.values(),
                         ids=scale_and_offset_coordinates.keys(),)
def test_scale_and_offset_coordinates(coordinates, unit_conversion, y_offset, expected):
    new_coordinates = vertices.scale_and_offset_coordinates(coordinates, unit_conversion, y_offset)
    assert numpy.allclose(new_coordinates, expected)


the_real_mccoy = {
    "washer": (
        numpy.array([[1.0, -0.5], [2.0, -0.5], [2.0, 0.5], [1.0, 0.5]]),
        4,
        [
            numpy.array([[1.0, -0.5], [2.0, -0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[2.0, -0.5], [2.0,  0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[2.0,  0.5], [1.0,  0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[1.0,  0.5], [1.0, -0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
        ],
        []
    ),
    "vase": (
        numpy.array(
            [
                [ 5.1, -5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 5. , -4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4.5, -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4.1, -3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4. , -2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4. ,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4.1,  3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4.5,  4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 5. ,  4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 5.1,  5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 3. ,  5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 3. , -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 0. , -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 0. , -5. ],  # fmt: skip # noqa: E201,E202,E203,E241
            ]
        ),
        4,
        [
            numpy.array([[ 4. , -2.5], [ 4. ,  2.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 5.1,  5. ], [ 3.0,  5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 3.0,  5.0], [ 3.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 3.0, -4.0], [ 0.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 0.0, -4.0], [ 0.0, -5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 0.0, -5.0], [ 5.1, -5. ]]),  # fmt: skip # noqa: E201,E202,E203,E241
        ],
        [
            numpy.array(
                [
                    [ 5.1, -5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 5. , -4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.5, -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.1, -3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4. , -2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                ]
            ),
            numpy.array(
               [
                   [ 4. ,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                   [ 4.1,  3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                   [ 4.5,  4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                   [ 5. ,  4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                   [ 5.1,  5. ],  # fmt: skip # noqa: E201,E202,E203,E241
               ]
            )
        ]
    )
}


@pytest.mark.parametrize("coordinates, euclidean_distance, expected_lines, expected_splines",
                         the_real_mccoy.values(),
                         ids=the_real_mccoy.keys(),)
def test_lines_and_splines(coordinates, euclidean_distance, expected_lines, expected_splines):
    """Test :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices.lines_and_splines`"""
    lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance)
    assert len(lines) == len(expected_lines)
    for line, expectation in zip(lines, expected_lines):
        assert numpy.allclose(line, expectation)
    assert len(splines) == len(expected_splines)
    for spline, expectation in zip(splines, expected_splines):
        assert numpy.allclose(spline, expectation)


ordered_lines_and_splines = {
    "washer": (
        numpy.array([[1.0, -0.5], [2.0, -0.5], [2.0, 0.5], [1.0, 0.5]]),
        4,
        [
            numpy.array([[1.0, -0.5], [2.0, -0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[2.0, -0.5], [2.0,  0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[2.0,  0.5], [1.0,  0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[1.0,  0.5], [1.0, -0.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
        ],
    ),
    "vase": (
        numpy.array(
            [
                [ 5.1, -5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 5. , -4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4.5, -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4.1, -3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4. , -2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4. ,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4.1,  3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 4.5,  4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 5. ,  4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 5.1,  5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 3. ,  5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 3. , -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 0. , -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                [ 0. , -5. ],  # fmt: skip # noqa: E201,E202,E203,E241
            ]
        ),
        4,
        [
            numpy.array(
                [
                    [ 5.1, -5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 5. , -4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.5, -4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.1, -3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4. , -2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                ]
            ),
            numpy.array([[ 4. , -2.5], [ 4. ,  2.5]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array(
                [
                    [ 4. ,  2.5],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.1,  3. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 4.5,  4. ],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 5. ,  4.8],  # fmt: skip # noqa: E201,E202,E203,E241
                    [ 5.1,  5. ],  # fmt: skip # noqa: E201,E202,E203,E241
                ]
            ),
            numpy.array([[ 5.1,  5. ], [ 3.0,  5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 3.0,  5.0], [ 3.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 3.0, -4.0], [ 0.0, -4.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 0.0, -4.0], [ 0.0, -5.0]]),  # fmt: skip # noqa: E201,E202,E203,E241
            numpy.array([[ 0.0, -5.0], [ 5.1, -5. ]]),  # fmt: skip # noqa: E201,E202,E203,E241
        ]
    )
}


@pytest.mark.parametrize("coordinates, euclidean_distance, expected_lines_and_splines",
                         ordered_lines_and_splines.values(),
                         ids=ordered_lines_and_splines.keys(),)
def test_ordered_lines_and_splines(coordinates, euclidean_distance, expected_lines_and_splines):
    lines_and_splines = vertices.ordered_lines_and_splines(coordinates, euclidean_distance)
    assert len(lines_and_splines) == len(expected_lines_and_splines)
    for curve, expectation in zip(lines_and_splines, expected_lines_and_splines):
        assert numpy.allclose(curve, expectation)


def test_lines_and_splines_passthrough():
    with (
        patch(
            "turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices._break_coordinates",
            return_value=[]
        ) as mock_break_coordinates,
        patch("turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices._line_pairs", return_value=[]),
    ):
        all_splines = vertices.lines_and_splines([], 4.0, rtol=1e-5, atol=1e-9)
        assert all_splines == ([], [])
        mock_break_coordinates.assert_called_once_with([], 4.0, rtol=1e-5, atol=1e-9)


def test_break_coordinates_passthrough():
    with (
        patch("turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices._compare_xy_values") as mock_xy_values,
        patch("turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices._compare_euclidean_distance"),
        patch("turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices._bool_via_or"),
        patch("numpy.where"),
        patch("numpy.split"),
    ):
        vertices._break_coordinates([], 4.0, rtol=1e-5, atol=1e-9)
        mock_xy_values.assert_called_once_with([], rtol=1e-5, atol=1e-9)


cylinder = {
    "no offset": (
        1., 2., 1., None, numpy.array([[1., 0.5], [2., 0.5], [2., -0.5], [1., -0.5]])
    ),
    "offset half height": (
        1., 2., 1., 0.5, numpy.array([[1., 1.], [2., 1.], [2., 0.], [1., 0.]])
    )
}


@pytest.mark.parametrize("inner_radius, outer_radius, height, y_offset, expected",
                         cylinder.values(),
                         ids=cylinder.keys(),)
def test_cylinder(inner_radius, outer_radius, height, y_offset, expected):
    """Test :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices.cylinder`"""
    kwargs = {}
    if y_offset is not None:
        kwargs = {"y_offset": y_offset}
    coordinates = vertices.cylinder(inner_radius, outer_radius, height, **kwargs)
    assert numpy.allclose(coordinates, expected)


cylinder_lines = {
    "no offset": (
        1., 2., 1., None,
        [
            (numpy.array([1.,  0.5]), numpy.array([2.,  0.5])),  # fmt: skip # noqa: E241
            (numpy.array([2.,  0.5]), numpy.array([2., -0.5])),  # fmt: skip # noqa: E241
            (numpy.array([2., -0.5]), numpy.array([1., -0.5])),
            (numpy.array([1., -0.5]), numpy.array([1.,  0.5])),  # fmt: skip # noqa: E241
        ],
    ),
    "offset half height": (
        1., 2., 1., 0.5,
        [
            (numpy.array([1., 1.]), numpy.array([2., 1.])),
            (numpy.array([2., 1.]), numpy.array([2., 0.])),
            (numpy.array([2., 0.]), numpy.array([1., 0.])),
            (numpy.array([1., 0.]), numpy.array([1., 1.])),
        ],
    )
}


@pytest.mark.parametrize("inner_radius, outer_radius, height, y_offset, expected",
                         cylinder_lines.values(),
                         ids=cylinder_lines.keys(),)
def test_cylinder_lines(inner_radius, outer_radius, height, y_offset, expected):
    """Test :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices.cylinder_lines`"""
    kwargs = {}
    if y_offset is not None:
        kwargs = {"y_offset": y_offset}
    lines = vertices.cylinder_lines(inner_radius, outer_radius, height, **kwargs)
    for line, expected_line in zip(lines, expected):
        assert numpy.allclose(line, expected_line)


number = math.sqrt(2.**2 / 2.)
rectalinear_coordinates = {
    "unit circle": (
        (1, 1, 1, 1), (0, math.pi / 2, math.pi, 2 * math.pi), ((1, 0), (0, 1), (-1, 0), (1, 0))
    ),
    "forty-fives": (
        (2, 2, 2, 2), (math.pi / 4, math.pi * 3 / 4, math.pi * 5 / 4, math.pi * 7 / 4),
        ((number, number), (-number, number), (-number, -number), (number, -number))
    )
}


@pytest.mark.parametrize("radius_list, angle_list, expected",
                         rectalinear_coordinates.values(),
                         ids=rectalinear_coordinates.keys(),)
def test_rectalinear_coordinates(radius_list, angle_list, expected):
    """Test :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices.rectalinear_coordinates`"""
    coordinates = vertices.rectalinear_coordinates(radius_list, angle_list)
    assert numpy.allclose(coordinates, expected)


one_over_root_three = 1. / math.sqrt(3.)
normalize_vector = {
    "zero": (
        (0., 0., 0.), numpy.array([0., 0., 0.])
    ),
    "unit x-axis": (
        (1., 0., 0.), numpy.array([1., 0., 0.])
    ),
    "unit y-axis": (
        (0., 1., 0.), numpy.array([0., 1., 0.])
    ),
    "unit z-axis": (
        (0., 0., 1.), numpy.array([0., 0., 1.])
    ),
    "unit equal": (
        (1., 1., 1.), numpy.array([one_over_root_three, one_over_root_three, one_over_root_three])
    ),
    "twice unit equal": (
        (2., 2., 2.), numpy.array([one_over_root_three, one_over_root_three, one_over_root_three])
    ),
}


@pytest.mark.parametrize("vector, expected",
                         normalize_vector.values(),
                         ids=normalize_vector.keys(),)
def test_normalize_vector(vector, expected):
    normalized = vertices.normalize_vector(vector)
    assert numpy.allclose(normalized, expected)


midpoint_vector = {
    "+x+y": (
        [1., 0, 0], [0, 1., 0], numpy.array([0.5, 0.5, 0.])
    ),
    "+x-y": (
        [1., 0, 0], [0, -1., 0], numpy.array([0.5, -0.5, 0.])
    ),
    "+y+z": (
        [0, 1., 0], [0, 0, 1.], numpy.array([0, 0.5, 0.5])
    ),
    "+y-z": (
        [0, 1., 0], [0, 0, -1.], numpy.array([0, 0.5, -0.5])
    ),
    "111,-111": (
        [1., 1., 1.], [-1., 1., 1.], numpy.array([0, 1., 1.])
    ),
}


@pytest.mark.parametrize("first, second, expected",
                         midpoint_vector.values(),
                         ids=midpoint_vector.keys(),)
def test_midpoint_vector(first, second, expected):
    midpoint = vertices.midpoint_vector(first, second)
    assert numpy.allclose(midpoint, expected)


is_parallel = {
    "identical": (
        (1., 1., 1.), (1., 1., 1.), True
    ),
    "orthogonal": (
        (1., 0., 0.), (0., 0., 1.), False
    ),
    "multiple": (
        (0., 1., 0.), (0., 2., 0.), True
    ),
}


@pytest.mark.parametrize("first, second, expected",
                         is_parallel.values(),
                         ids=is_parallel.keys(),)
def test_is_parallel(first, second, expected):
    boolean = vertices.is_parallel(first, second)
    assert boolean == expected


any_parallel = {
    "identical": (
        (1., 1., 1.), [(1., 1., 1.), (1., 0., 0.)], True
    ),
    "orthogonal": (
        (1., 0., 0.), [(0., 0., 1.), (0., 1., 0.)], False
    ),
    "multiple": (
        (0., 1., 0.), [(2., 0., 0.), (0., 2., 0.)], True
    ),
}


@pytest.mark.parametrize("first, options, expected",
                         any_parallel.values(),
                         ids=any_parallel.keys(),)
def test_any_parallel(first, options, expected):
    boolean = vertices.any_parallel(first, options)
    assert boolean == expected


norm = math.sqrt(0.5)
datum_planes = {
    "globally aligned 45-degrees": (
        (1., 0., 0.), (0., 0., 1.),
        [
            numpy.array([0., 0., 1.]),  # XY plane
            numpy.array([1., 0., 0.]),  # YZ plane
            numpy.array([0., 1., 0.]),  # ZX plane
            numpy.array([ norm,  norm, 0.]),  # fmt: skip # noqa: E201,E241
            numpy.array([ norm, -norm, 0.]),  # fmt: skip # noqa: E201,E241
            numpy.array([ 0., norm,  norm]),  # fmt: skip # noqa: E201,E241
            numpy.array([ 0., norm, -norm]),  # fmt: skip # noqa: E201,E241
            numpy.array([  norm, 0., norm]),  # fmt: skip # noqa: E201,E241
            numpy.array([ -norm, 0., norm]),  # fmt: skip # noqa: E201,E241
        ]
    ),
}


@pytest.mark.parametrize("xvector, zvector, expected",
                         datum_planes.values(),
                         ids=datum_planes.keys(),)
def test_datum_planes(xvector, zvector, expected):
    planes = vertices.datum_planes(xvector, zvector)
    for plane, expectation in zip(planes, expected):
        assert numpy.allclose(plane, expectation)


over_root_three = 1. / math.sqrt(3.)
fortyfive_vectors = {
    "cartesian aligned": (
        numpy.array([1., 0., 0.]), numpy.array([0., 0., 1.]),
        [
            numpy.array([ over_root_three,  over_root_three,  over_root_three]),  # fmt: skip # noqa: E201,E241
            numpy.array([-over_root_three,  over_root_three,  over_root_three]),  # fmt: skip # noqa: E201,E241
            numpy.array([-over_root_three,  over_root_three, -over_root_three]),  # fmt: skip # noqa: E201,E241
            numpy.array([ over_root_three,  over_root_three, -over_root_three]),  # fmt: skip # noqa: E201,E241
            numpy.array([ over_root_three, -over_root_three,  over_root_three]),  # fmt: skip # noqa: E201,E241
            numpy.array([-over_root_three, -over_root_three,  over_root_three]),  # fmt: skip # noqa: E201,E241
            numpy.array([-over_root_three, -over_root_three, -over_root_three]),  # fmt: skip # noqa: E201,E241
            numpy.array([ over_root_three, -over_root_three, -over_root_three]),  # fmt: skip # noqa: E201,E241
        ]
    ),
}


@pytest.mark.parametrize("xvector, zvector, expected",
                         fortyfive_vectors.values(),
                         ids=fortyfive_vectors.keys(),)
def test_fortyfive_vectors(xvector, zvector, expected):
    fortyfive_vectors = vertices.fortyfive_vectors(xvector, zvector)
    for vector, expectation in zip(fortyfive_vectors, expected):
        assert numpy.allclose(vector, expectation)
