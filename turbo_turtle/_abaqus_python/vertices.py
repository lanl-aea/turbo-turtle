"""Python 2/3 compatible coordinate handling for use in both Abaqus Python scripts and Turbo-Turtle Python 3 modules"""
import math
import numpy
import cmath


def rectalinear_coordinates(radius_list, angle_list):
    """Calculate 2D rectalinear XY coordinates from 2D polar coordinates

    :param list radius: length N list of polar coordinate radius
    :param list angle: length N list of polar coordinate angle measured from the positive X-axis in radians

    :returns coords: length N tuple of tuple(X, Y) rectalinear coordinates
    :rtype: list
    """
    numbers = (cmath.rect(radius, angle) for radius, angle in zip(radius_list, angle_list))
    coordinates = tuple((number.real, number.imag) for number in numbers)
    return coordinates


def cylinder(inner_radius, outer_radius, height):
    """Return a :meth:`turbo_turtle._abaqus_python.geometry.draw_part_from_splines` compatible vertex array

    :param float inner_radius: Radius of the hollow center
    :param float outer_radius: Outer radius of the cylinder
    :param float height: Height of the cylinder
    """
    coordinates = (
        (inner_radius, height),
        (outer_radius, height),
        (outer_radius, 0.),
        (inner_radius, 0.)
    )
    return numpy.array(coordinates)


def lines_and_splines(coordinates, euclidean_distance, rtol=None, atol=None):
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
    :param float rtol: relative tolerance used by ``numpy.isclose``. If None, use the numpy default.
    :param float atol: absolute tolerance used by ``numpy.isclose``. If None, use the numpy default.

    :returns: list of line pairs and list of spline arrays
    :rtype: tuple
    """
    all_splines = _break_coordinates(coordinates, euclidean_distance)
    lines = _line_pairs(all_splines)
    lines.extend([(array[0], array[1]) for array in all_splines if len(array) == 2])
    splines = [array for array in all_splines if len(array) > 2]
    return lines, splines


def _break_coordinates(coordinates, euclidean_distance, rtol=None, atol=None):
    """Accept a [N, 2] numpy array and break into a list of [M, 2] arrays

    This function follows this methodology to turn a [N, 2] numpy array into a list of [M, 2] arrays denoting
    individual lines or splines.

    #. If neighboring points are farther apart than the euclidean distance, break the original array between them.
    #. If neighboring points have the same X or Y coordinate (horizontally or vertically aligned), break the original
       array between them. Uses ``numpy.isclose`` with the default tolerance for float comparison.

    :param numpy.array coordinates: [N, 2] array of XY coordinates.
    :param float euclidean_distance: If the distance between two points is greater than this, draw a straight line.
    :param float rtol: relative tolerance used by ``numpy.isclose``. If None, use the numpy default.
    :param float atol: absolute tolerance used by ``numpy.isclose``. If None, use the numpy default.

    :return: Series of line and spline definitions
    :rtype: list
    """
    euclidean_distance_bools = _compare_euclidean_distance(coordinates, euclidean_distance)
    vertical_horizontal_bools = _compare_xy_values(coordinates, rtol=rtol, atol=atol)
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


def _compare_xy_values(coordinates, rtol=None, atol=None):
    """Check neighboring XY values in an [N, 2] array of coordinates for vertical or horizontal relationships

    This function loops through lists of coordinates checking to see if a "current point" and the previous point in the numpy
    array are vertical or hozitonal from one another. As such, a single ``False`` is always prepended to the beginning
    of the output ``vertical_horizontal_bools`` list, because there is no such vertical/horizontal relationship between
    the first point and one that comes before it.

    :param numpy.array coordinates: [N, 2] array of XY coordinates.
    :param float rtol: relative tolerance used by ``numpy.isclose``. If None, use the numpy default.
    :param float atol: absolute tolerance used by ``numpy.isclose``. If None, use the numpy default.

    :return: bools for vertical/horizontal relationship comparison
    :rtype: list of length N
    """
    isclose_kwargs = {}
    if rtol is not None:
        isclose_kwargs.update({"rtol": rtol})
    if atol is not None:
        isclose_kwargs.update({"atol": atol})
    vertical_horizontal_bools = [False] + [numpy.isclose(coords1[0], coords2[0], **isclose_kwargs) or
                                           numpy.isclose(coords1[1], coords2[1], **isclose_kwargs) for
                                           coords1, coords2 in zip(coordinates[1:, :], coordinates[0:-1, :])]
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


def polar_vector(radius, polar_angle, azimuthal_angle):
    """Calculate the rectalinear coordinates of a vector defined in polar coordinates, where the polar axis is the
    Y-axis

    .. math::

       x = radius * sin(polar_angle) * cos(azimuthal_angle)

    .. math::

       y = radius * cos(polar_angle)

    .. math::

       z = - radius * sin(polar_angle) * sin(azimuthal_angle)

    :param float radius: Radial distance
    :param float polar_angle: Polar angle measured from the local y-axix (polar axis) in radians
    :param float azimuthal_angle: Azimuthal angle measure from the local x-axis in radians

    :returns: rectalinear vector [1, 3]
    :rtype: numpy.array
    """
    return numpy.array([
          radius * math.sin(polar_angle) * math.cos(azimuthal_angle),
          radius * math.cos(polar_angle),
        - radius * math.sin(polar_angle) * math.sin(azimuthal_angle)
    ])


def calculate_datum_planes(center, xpoint, zpoint, polar_angle, azimuthal_angle):
    """Calculate the parititioning datum plane normal vectors on the partitioning local coordinate system

    :param list center: List of three (3) floats defining the location of the datum coordinate system in global
        coordinate space
    :param list xpoint: List of three (3) floats defining the local x-axis vector in global coordinate space
    :param list zpoint: List of three (3) floats defining the local z-axis vector in global coordinate space
    :param float polar_angle: Polar angle measured from the local y-axix (polar axis) in degrees
    :param float azimuthal_angle: Azimuthal angle measure from the local x-axis in degrees

    :returns: list of local plane normal vectors [7, 3] - xz plane, (2) +/- azimuthal planes, (4) polar planes
    """
    xpoint = numpy.array(xpoint)
    zpoint = numpy.array(zpoint)

    xz_plane = numpy.cross(xpoint, zpoint)

    azimuthal_radians = math.radians(azimuthal_angle)
    polar_radians = math.radians(polar_angle)

    azimuthal_normal = math.pi - azimuthal_radians
    positive_azimuthal = polar_vector(1., 0.,  azimuthal_normal)
    negative_azimuthal = polar_vector(1., 0., -azimuthal_normal)

    first_vector  = polar_vector(1., polar_radians,  azimuthal_radians)
    second_vector = polar_vector(1., polar_radians, -azimuthal_radians)
    third_vector  = polar_vector(1., polar_radians,  azimuthal_radians + math.pi)
    fourth_vector = polar_vector(1., polar_radians, -azimuthal_radians + math.pi)

    first_polar = numpy.cross(first_vector, second_vector)
    second_polar = numpy.cross(second_vector, third_vector)
    third_polar = numpy.cross(third_vector, fourth_vector)
    fourth_polar = numpy.cross(fourth_vector, first_vector)

    return [xz_plane, positive_azimuthal, negative_azimuthal, first_polar, second_polar, third_polar, fourth_polar]
