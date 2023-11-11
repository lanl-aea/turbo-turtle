import pytest
import numpy

from turbo_turtle._abaqus_python import lines_and_splines


compare_xy_values = {
    "horizontal": (
        numpy.array([[0, 0], [1, 0]]), [False, True]
    ),
    "vertical": (
        numpy.array([[0, 0], [0, 1]]), [False, True]
    ),
    "x=y": (
        numpy.array([[0, 0], [1, 1]]), [False, False]
    ),
}


@pytest.mark.parametrize("coordinates, expected",
                         compare_xy_values.values(),
                         ids=compare_xy_values.keys())
def test_compare_xy_values(coordinates, expected):
    bools = lines_and_splines._compare_xy_values(coordinates)
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
                         ids=compare_euclidean_distance.keys())
def test_compare_euclidean_distance(coordinates, euclidean_distance, expected):
    bools = lines_and_splines._compare_euclidean_distance(coordinates, euclidean_distance)
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
                         ids=bool_via_or.keys())
def test_bool_via_or(bool_list_1, bool_list_2, expected):
    bools = lines_and_splines._bool_via_or(bool_list_1, bool_list_2)
    assert bools == expected


break_coordinates = {
    "washer": (
        numpy.array([[1.0, -0.5], [2.0, -0.5], [2.0, 0.5], [1.0, 0.5]]),
        4,
        [numpy.array([[1.0, -0.5]]), numpy.array([[2.0, -0.5]]), numpy.array([[2.0, 0.5]]), numpy.array([[1.0, 0.5]])]
    ),
    "vase": (
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
         numpy.array([[ 0.0, -5.0]])]
    )
}


@pytest.mark.parametrize("coordinates, euclidean_distance, expected",
                         break_coordinates.values(),
                         ids=break_coordinates.keys())
def test_break_coordinates(coordinates, euclidean_distance, expected):
    all_splines = lines_and_splines._break_coordinates(coordinates, euclidean_distance)
    for spline, expectation in zip(all_splines, expected):
        assert numpy.allclose(spline, expectation)
