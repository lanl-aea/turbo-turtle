"""Python 2/3 compatible coordinate handling for use in both Abaqus Python scripts and Turbo-Turtle Python 3 modules"""
import numpy


def lines_and_splines(coordinates, euclidean_distance):
    """Accept a [N, 2] numpy array of XY coordinates and return line point pairs and splines

    Array is broken into a list of [M, 2] arrays according to the following rules

    #. If neighboring points are farther apart than the euclidean distance, break the original array between them.
    #. If neighboring points have the same X or Y coordinate (horizontally or vertically aligned), break the original
       array between them. Uses ``numpy.isclose`` with the default tolerance for float comparison.

    After breaking into a list of arrays, the line pair list and spline list are generated from the following rules

    #. Line point pairs are returned for the end and beginning of adjacent arrays, and for the end of the last array and
       the beginning of the first array.
    #. Arrays of length 2 are converted to line pair coordinates
    #. Arrays greater than length 2 are kept intact as splines.

    :param numpy.array coordinates: [N, 2] array of XY coordinates.
    :param float euclidean_distance: If the distance between two points is greater than this, draw a straight line.

    :returns: list of line pairs and list of spline arrays
    :rtype: tuple
    """
    all_splines = _break_coordinates(coordinates, euclidean_distance)
    lines = _line_pairs(all_splines)
    lines.extend([(array[0], array[1]) for array in all_splines if len(array) == 2])
    splines = [array for array in all_splines if len(array) > 2]
    return lines, splines


def _break_coordinates(coordinates, euclidean_distance):
    """Accept a [N, 2] numpy array and break into a list of [M, 2] arrays

    This function follows this methodology to turn a [N, 2] numpy array into a list of [M, 2] arrays denoting
    individual lines or splines.

    #. If neighboring points are farther apart than the euclidean distance, break the original array between them.
    #. If neighboring points have the same X or Y coordinate (horizontally or vertically aligned), break the original
       array between them. Uses ``numpy.isclose`` with the default tolerance for float comparison.

    :param numpy.array coordinates: [N, 2] array of XY coordinates.
    :param float euclidean_distance: If the distance between two points is greater than this, draw a straight line.

    :return: Series of line and spline definitions
    :rtype: list
    """
    euclidean_distance_bools = _compare_euclidean_distance(coordinates, euclidean_distance)
    vertical_horizontal_bools = _compare_xy_values(coordinates)
    bools_from_or = _bool_via_or(euclidean_distance_bools, vertical_horizontal_bools)
    break_indices = numpy.where(bools_from_or)[0]
    all_splines = numpy.split(coordinates, break_indices, axis=0)
    return all_splines


def _compare_euclidean_distance(coordinates, euclidean_distance):
    """Compare the distance between coordinates in a 2D numpy array of XY data to a provided euclidean distance

    The distance comparison is performed as ``numpy_array_distance > euclidean_distance``. The distance between coordinates
    in the numpy array is computed such that the "current point" is compared to the previous point in the list. As such,
    a single ``False`` is always prepended to the beginning of the output ``euclidean_distance_bools`` list, because
    there is no such distance between the first point and one that comes before it.

    :param numpy.array coordinates: [N, 2] array of XY coordinates.
    :param float euclidean_distance: distance value to compare against

    :return: bools for the distance comparison
    :rtype: list of length N
    """
    calculated_euclidean_array = numpy.linalg.norm(coordinates[1:, :] - coordinates[0:-1, :], axis=1)
    euclidean_distance_bools = [False] + [this_euclidean_distance > euclidean_distance for this_euclidean_distance in
                                          calculated_euclidean_array]
    return euclidean_distance_bools


def _compare_xy_values(coordinates):
    """Check neighboring XY values in an [N, 2] array of coordinates for vertical or horizontal relationships

    This function loops through lists of coordinates checking to see if a "current point" and the previous point in the numpy
    array are vertical or hozitonal from one another. As such, a single ``False`` is always prepended to the beginning
    of the output ``vertical_horizontal_bools`` list, because there is no such vertical/horizontal relationship between
    the first point and one that comes before it.

    :param numpy.array coordinates: [N, 2] array of XY coordinates.

    :return: bools for vertical/horizontal relationship comparison
    :rtype: list of length N
    """
    vertical_horizontal_bools = [False] + [numpy.isclose(coords1[0], coords2[0]) or
                                           numpy.isclose(coords1[1], coords2[1]) for coords1, coords2 in
                                           zip(coordinates[1:, :], coordinates[0:-1, :])]
    return vertical_horizontal_bools


def _bool_via_or(bools_list_1, bools_list_2):
    """Compare two lists of bools using an ``or`` statement

    :param list bools_list_1: first set of bools
    :param list bools_list_2: second set of bools

    :return: bools resulting from ``or`` statment
    :rtype: list
    """
    bools_from_or = [a or b for a, b in zip(bools_list_1, bools_list_2)]
    return bools_from_or


def _line_pairs(all_splines):
    """Accept a list of [N, 2] arrays and return a list of paired coordinates to connect as lines

    Given a list of [N, 2] numpy arrays, create tuple pairs of coordinates between the end and beginning of subsequent
    arrays. Also return a pair from the last array's last coordinate to the first array's first coordinate.

    :param list all_splines: a list of 2D numpy arrays

    :returns: line pairs
    :rtype: list of tuples of [1, 2] arrays
    """
    line_pairs = [(spline1[-1], spline2[0]) for spline1, spline2 in zip(all_splines[0:-1], all_splines[1:])]
    line_pairs.append((all_splines[-1][-1], all_splines[0][0]))
    return line_pairs
