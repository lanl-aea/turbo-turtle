"""Python 2/3 compatible coordinate handling for use in both Abaqus Python scripts and Turbo-Turtle Python 3 modules"""

import cmath

import numpy


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


def cylinder(inner_radius, outer_radius, height, y_offset=0.0):
    """Return a :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices.lines_and_splines` compatible vertex
    array

    :param float inner_radius: Radius of the hollow center
    :param float outer_radius: Outer radius of the cylinder
    :param float height: Height of the cylinder

    :returns: vertex coordinate array
    :rtype: numpy.array
    """
    coordinates = (
        (inner_radius, height / 2.0 + y_offset),  # fmt: skip # noqa: E241
        (outer_radius, height / 2.0 + y_offset),  # fmt: skip # noqa: E241
        (outer_radius, -height / 2.0 + y_offset),
        (inner_radius, -height / 2.0 + y_offset),
    )
    return numpy.array(coordinates)


def cylinder_lines(inner_radius, outer_radius, height, y_offset=0.0):
    """Return the line coordinate pairs defining a cylinder

    :param float inner_radius: Radius of the hollow center
    :param float outer_radius: Outer radius of the cylinder
    :param float height: Height of the cylinder

    :returns: list of line segment coordinate pairs
    :rtype: list of (numpy.array, numpy.array) tuples
    """
    coordinates = cylinder(inner_radius, outer_radius, height, y_offset=y_offset)
    euclidean_distance = min(inner_radius, height) / 2.0
    lines, splines = lines_and_splines(coordinates, euclidean_distance)
    return lines


def sphere(center, inner_radius, outer_radius, quadrant):
    """Return the inner and outer radii vertices defining a 2D sketh of a sphere for revolution

    :param tuple center: tuple of floats (X, Y) location for the center of the sphere
    :param float inner_radius: inner radius (size of hollow)
    :param float outer_radius: outer radius (size of sphere)
    :param str quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both

    :returns: [4, 2] inner/outer radii in (x, y) coordinates defining inner/outer circular arc segments
    :rtype: numpy.array
    """
    inner_radius = abs(inner_radius)
    outer_radius = abs(outer_radius)

    if quadrant == "both":
        start_angle = -numpy.pi / 2.0
        end_angle = numpy.pi / 2.0
    elif quadrant == "upper":
        start_angle = 0.0
        end_angle = numpy.pi / 2.0
    elif quadrant == "lower":
        start_angle = -numpy.pi / 2.0
        end_angle = 0.0

    radius_list = (inner_radius, inner_radius, outer_radius, outer_radius)
    angle_list = (end_angle, start_angle, end_angle, start_angle)
    points = numpy.array(center) + numpy.array(rectalinear_coordinates(radius_list, angle_list))
    return points


def scale_and_offset_coordinates(coordinates, unit_conversion=1.0, y_offset=0.0):
    """Scale and offset XY coordinates in a 2 column numpy array

    First multiply by the unit conversion. Then offset the Y coordinates (2nd column) by adding the y offset

    :param numpy.array coordinates: [N, 2] array of XY coordinates.
    :param float unit_conversion: multiplication factor applies to all coordinates
    :param float y_offset: vertical offset along the global Y-axis. Offset should be provided in units *after* the unit
        conversion.
    """
    coordinates = coordinates * unit_conversion
    coordinates[:, 1] += y_offset
    return coordinates


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
    all_splines = _break_coordinates(coordinates, euclidean_distance, rtol=rtol, atol=atol)
    lines = _line_pairs(all_splines)
    lines.extend([numpy.stack((array[0], array[1])) for array in all_splines if len(array) == 2])
    splines = [array for array in all_splines if len(array) > 2]
    return lines, splines


def ordered_lines_and_splines(coordinates, euclidean_distance, rtol=None, atol=None):
    """Return a single, closed loop list of [M, 2] arrays with lines (length 2) and splines (length >2)"""
    all_splines = _break_coordinates(coordinates, euclidean_distance, rtol=rtol, atol=atol)
    lines_and_splines = [all_splines[0]]
    for spline1, spline2 in zip(all_splines[0:-1], all_splines[1:]):
        lines_and_splines.append(numpy.stack((spline1[-1], spline2[0])))
        lines_and_splines.append(spline2)
    lines_and_splines.append(numpy.stack((all_splines[-1][-1], all_splines[0][0])))
    # Eliminate points after creating line connections
    lines_and_splines = [array for array in lines_and_splines if len(array) > 1]
    return lines_and_splines


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

    The distance comparison is performed as ``numpy_array_distance > euclidean_distance``. The distance between
    coordinates in the numpy array is computed such that the "current point" is compared to the previous point in the
    list. As such, a single ``False`` is always prepended to the beginning of the output ``euclidean_distance_bools``
    list, because there is no such distance between the first point and one that comes before it.

    :param numpy.array coordinates: [N, 2] array of XY coordinates.
    :param float euclidean_distance: distance value to compare against

    :return: bools for the distance comparison
    :rtype: list of length N
    """
    calculated_euclidean_array = numpy.linalg.norm(coordinates[1:, :] - coordinates[0:-1, :], axis=1)
    euclidean_distance_bools = [False] + [
        this_euclidean_distance > euclidean_distance for this_euclidean_distance in calculated_euclidean_array
    ]
    return euclidean_distance_bools


def _compare_xy_values(coordinates, rtol=None, atol=None):
    """Check neighboring XY values in an [N, 2] array of coordinates for vertical or horizontal relationships

    This function loops through lists of coordinates checking to see if a "current point" and the previous point in the
    numpy array are vertical or hozitonal from one another. As such, a single ``False`` is always prepended to the
    beginning of the output ``vertical_horizontal_bools`` list, because there is no such vertical/horizontal
    relationship between the first point and one that comes before it.

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
    vertical_horizontal_bools = [False] + [
        numpy.isclose(coords1[0], coords2[0], **isclose_kwargs)  # noqa: W504
        or numpy.isclose(coords1[1], coords2[1], **isclose_kwargs)  # noqa: W503
        for coords1, coords2 in zip(coordinates[1:, :], coordinates[0:-1, :])
    ]
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
    :rtype: list of [2, 2] numpy arrays
    """
    zipped_splines = zip(all_splines[0:-1], all_splines[1:])
    line_pairs = [numpy.stack((spline1[-1], spline2[0])) for spline1, spline2 in zipped_splines]
    line_pairs.append((all_splines[-1][-1], all_splines[0][0]))
    return line_pairs


def normalize_vector(vector):
    """Normalize a cartesian vector

    :param list vector: List of three floats defining a cartesian vector

    :returns: normalized
    :rtype: numpy.array
    """
    numpy.array(vector)
    norm = numpy.linalg.norm(vector)
    if numpy.isclose(norm, 0.0):
        return vector
    return vector / norm


def midpoint_vector(first, second, third=None):
    """Calculate the vector between two vectors (summation / 2)

    :param numpy.array first: First vector
    :param numpy.array second: Second vector

    :returns: Vector midway between first and second vector
    :rtype: numpy.array
    """
    first = numpy.array(first)
    second = numpy.array(second)
    summation = first + second
    midpoint = summation / 2.0
    if third is not None:
        third = numpy.array(third)
        summation = summation + third
        midpoint = summation / 3.0
    return midpoint


def is_parallel(first, second, rtol=None, atol=None):
    """Compute cross product. If it is near zero, return True. Else False.

    :param numpy.array first: First vector
    :param numpy.array second: Second vector

    :returns: boolean answering "are these vectors parallel?"
    :rtype: bool
    """
    first = numpy.array(first)
    second = numpy.array(second)
    kwargs = {}
    if rtol is not None:
        kwargs.update({"rtol": rtol})
    if atol is not None:
        kwargs.update({"atol": atol})
    return numpy.allclose(numpy.cross(first, second), 0.0, **kwargs)


def any_parallel(first, options, rtol=None, atol=None):
    """If the first vector is parellel to any of the options, return True

    :param numpy.array first: First vector
    :param list options: List of vectors to compare against the first vector

    :returns: boolean answering "is the first vector parallel to any of the option vectors?"
    :rtype: bool
    """
    for second in options:
        if is_parallel(first, second, rtol=rtol, atol=atol):
            return True
    return False


def datum_planes(xvector, zvector):
    """Calculate the sphere partitioning datum plane normal vectors on a local coordinate system

    The x- and z-vectors must be orthogonal. They will be normalized prior to calculating the normalized plane normal
    vectors.

    :param list xvector: List of three (3) floats defining the local x-axis vector in global coordinate space
    :param list zvector: List of three (3) floats defining the local z-axis vector in global coordinate space

    :returns: list of normalized local plane normal vectors [9, 3] - (3) xy/yz/zx planes, (6) +/- 45 degrees from
        xy/yz/zx planes
    :rtype: list
    """
    dot = numpy.dot(xvector, zvector)
    if not numpy.isclose(dot, 0.0):
        raise RuntimeError("Provided x-vector '{}' and z-vector '{}' are not orthogonal".format(xvector, zvector))

    xvector = normalize_vector(xvector)
    zvector = normalize_vector(zvector)

    xy_plane = zvector
    yz_plane = xvector
    yvector = numpy.cross(zvector, xvector)
    zx_plane = yvector

    primary_planes = [xy_plane, yz_plane, zx_plane]

    midpoints = [
        midpoint_vector(xvector,  yvector),  # fmt: skip # noqa: E201,E241
        midpoint_vector(xvector, -yvector),  # fmt: skip # noqa: E201,E241
        midpoint_vector(yvector,  zvector),  # fmt: skip # noqa: E201,E241
        midpoint_vector(yvector, -zvector),  # fmt: skip # noqa: E201,E241
        midpoint_vector(zvector,  xvector),  # fmt: skip # noqa: E201,E241
        midpoint_vector(zvector, -xvector),  # fmt: skip # noqa: E201,E241
    ]
    midpoints = [normalize_vector(midpoint) for midpoint in midpoints]

    return primary_planes + midpoints


def fortyfive_vectors(xvector, zvector):
    """Return the normalized (1, 1, 1) vector variants of a local coordinate system defined by the x- and z-vector"""

    dot = numpy.dot(xvector, zvector)
    if not numpy.isclose(dot, 0.0):
        raise RuntimeError("Provided x-vector '{}' and z-vector '{}' are not orthogonal".format(xvector, zvector))

    xvector = normalize_vector(xvector)
    zvector = normalize_vector(zvector)
    yvector = numpy.cross(zvector, xvector)

    fortyfives = [
        midpoint_vector( xvector,  yvector,  zvector),  # 0  # fmt: skip # noqa: E201,E241
        midpoint_vector(-xvector,  yvector,  zvector),  # 1  # fmt: skip # noqa: E201,E241
        midpoint_vector(-xvector,  yvector, -zvector),  # 2  # fmt: skip # noqa: E201,E241
        midpoint_vector( xvector,  yvector, -zvector),  # 3  # fmt: skip # noqa: E201,E241
        midpoint_vector( xvector, -yvector,  zvector),  # 4  # fmt: skip # noqa: E201,E241
        midpoint_vector(-xvector, -yvector,  zvector),  # 5  # fmt: skip # noqa: E201,E241
        midpoint_vector(-xvector, -yvector, -zvector),  # 6  # fmt: skip # noqa: E201,E241
        midpoint_vector( xvector, -yvector, -zvector),  # 7  # fmt: skip # noqa: E201,E241
    ]
    fortyfives = [normalize_vector(vector) for vector in fortyfives]

    return fortyfives


def pyramid_surfaces(center, xvector, zvector, big_number):
    """Return the pyramid surfaces defined by the center and vertices of a cube

    Returns arrays of [N, 2] coordinates defining 12 triangular surfaces and 6 square surfaces defining the 4 edge
    pyramids from the center of a cube to the cube vertices.

    :returns: list of numpy arrays, where each numpy array is an [N, 3] list of coordinates defining a surface
    :rtype: list of numpy.array
    """
    vectors = fortyfive_vectors(xvector, zvector)
    fortyfive_vertices = [center + vector * big_number for vector in vectors]
    # TODO: Figure out how to cleanup these coordinate pairs such that they are independent from the fortyfives indices
    surface_coordinates = [
        # +Y surfaces
        numpy.array([center, fortyfive_vertices[0], fortyfive_vertices[1]]),  # 0:    +Y +Z
        numpy.array([center, fortyfive_vertices[1], fortyfive_vertices[2]]),  # 1: -X +Y
        numpy.array([center, fortyfive_vertices[2], fortyfive_vertices[3]]),  # 2:    +Y -Z
        numpy.array([center, fortyfive_vertices[3], fortyfive_vertices[0]]),  # 3: +X +Y
        # -Y surfaces
        numpy.array([center, fortyfive_vertices[4], fortyfive_vertices[5]]),  # 4:    -Y +Z
        numpy.array([center, fortyfive_vertices[5], fortyfive_vertices[6]]),  # 5: -X -Y
        numpy.array([center, fortyfive_vertices[6], fortyfive_vertices[7]]),  # 6:    -Y -Z
        numpy.array([center, fortyfive_vertices[7], fortyfive_vertices[4]]),  # 7: +X -Y
        # +X surfaces
        numpy.array([center, fortyfive_vertices[0], fortyfive_vertices[4]]),  # 8: +X    +Z
        numpy.array([center, fortyfive_vertices[3], fortyfive_vertices[7]]),  # 9: +X    -Z
        # -X surfaces
        numpy.array([center, fortyfive_vertices[1], fortyfive_vertices[5]]),  # 10: -X    +Z
        numpy.array([center, fortyfive_vertices[2], fortyfive_vertices[6]]),  # 11: -X    -Z
        # +/- normal to Y
        numpy.array(fortyfive_vertices[0:4]),  # 12: +Y
        numpy.array(fortyfive_vertices[4:]),  # 13: -Y
        # +/- normal to X
        numpy.array(
            [fortyfive_vertices[0], fortyfive_vertices[3], fortyfive_vertices[7], fortyfive_vertices[4]]  # 14: +X
        ),
        numpy.array(
            [fortyfive_vertices[1], fortyfive_vertices[2], fortyfive_vertices[6], fortyfive_vertices[5]]  # 15: -X
        ),
        # +/- normal to Z
        numpy.array(
            [fortyfive_vertices[0], fortyfive_vertices[1], fortyfive_vertices[5], fortyfive_vertices[4]]  # 16: +Z
        ),
        numpy.array(
            [fortyfive_vertices[2], fortyfive_vertices[3], fortyfive_vertices[7], fortyfive_vertices[6]]  # 17: -Z
        ),
    ]
    return surface_coordinates
