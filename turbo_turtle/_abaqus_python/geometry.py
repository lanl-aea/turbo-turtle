import inspect
import os
import sys

import numpy


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import parsers


def main(input_file, output_file,
         planar=parsers.geometry_default_planar,
         model_name=parsers.geometry_default_model_name,
         part_name=parsers.geometry_default_part_name,
         unit_conversion=parsers.geometry_default_unit_conversion,
         euclidian_distance=parsers.geometry_default_euclidian_distance,
         delimiter=parsers.geometry_default_delimiter,
         header_lines=parsers.geometry_default_header_lines,
         revolution_angle=parsers.geometry_default_revolution_angle):
    """This script takes a series of points in x-y coordinates from a text file and creates a 2D sketch or 3D body of
    revolution about the global Y-axis. Note that 2D axisymmetric sketches and sketches for 3D bodies of revolution
    about the global Y-axis must lie entirely on the positive-X side of the global Y-axis. In general, a 2D sketch can
    lie in all four quadrants; this is referred to as a "planar" sketch and requires that the ``planar`` boolean
    arugment be set to ``True``. This script can accept multiple input files to create multiple parts in the same Abaqus
    model. The ``part_name`` parameter allows explicit naming of part(s) in the model. If omitted from the command line
    arguments, the default is to use the input file basename(s) as the part name(s).

    :param str input_file: input text file(s) with points to draw
    :param str output_file: Abaqus CAE database to save the part(s)
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param str model_name: name of the Abaqus model in which to create the part
    :param list part_name: name(s) of the part(s) being created
    :param float unit_conversion: multiplication factor applies to all points
    :param float euclidian_distance: if the distance between two points is greater than this, draw a straight line.
        Distance should be provided in units *after* the unit conversion
    :param str delimiter: character to use as a delimiter when reading the input file
    :param int header_lines: number of lines in the header to skip when reading the input file
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries

    :returns: writes ``{output_file}.cae``
    """
    import abaqus
    import abaqusConstants

    abaqus.mdb.Model(name=model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
    part_name = _validate_part_name(input_file, part_name)
    output_file = os.path.splitext(output_file)[0] + ".cae"
    for file_name, new_part in zip(input_file, part_name):
        numpy_points_array = read_file(file_name, delimiter, header_lines)
        numpy_points_array = numpy_points_array * unit_conversion
        all_splines = points_to_splines(numpy_points_array, euclidian_distance)
        try:
            draw_part_from_splines(all_splines, planar, model_name, new_part, revolution_angle)
        except:
            error_message = "Error: failed to create part '{}' from '{}'\n".format(new_part, file_name)
            sys.stderr.write(error_message)
            sys.exit(1)

    abaqus.mdb.saveAs(pathName=output_file)


def _validate_part_name(input_file, part_name):
    """Validate the structure of the ``part_name`` list to the following rules:

    * If ``part_name`` is ``[None]``, assign the base names of ``input_file`` to ``part_name``
    * Else if the length of ``part_name`` is not equal to the length of ``input_file``, exit with an error

    :param list input_file: input text file(s) with points to draw
    :param list part_name: name(s) of part(s) being created

    :return: part name(s)
    :rtype: list
    """
    print(part_name)
    if part_name[0] is None or part_name[0] == 'None':
        part_name = [os.path.splitext(os.path.basename(part_file))[0] for part_file in input_file]
    elif len(input_file) != len(part_name):
        error_message = "Error: The part name length '{}' must match the input file length '{}'\n".format(
            len(part_name), len(input_file))
        sys.stderr.write(error_message)
        sys.exit(1)
    return part_name


def read_file(file_name, delimiter=parsers.geometry_default_delimiter, header_lines=parsers.geometry_default_header_lines):
    """Parse a text file of points into a numpy array

    :param str file_name: input text file with points to draw
    :param str delimiter: character to use as a delimiter when reading the input file
    :param int header_lines: number of lines in the header to skip when reading the input file

    :return: array of points
    :rtype: numpy.array
    """
    with open(file_name, 'r') as points_file:
        numpy_points_array = numpy.genfromtxt(points_file, delimiter=delimiter, skip_header=header_lines)
    return numpy_points_array


def points_to_splines(numpy_points_array, euclidian_distance=parsers.geometry_default_euclidian_distance):
    """Read a text file of points in x-y coordinates and generate a list of lines and splines to draw.

    This function follows this methodology to turn a large list of points into a list of lists denoting individual lines
    or splines:

    #. Start looping through points in the ``numpy_points_array``, and append points to a list
    #. When two neighboring points have the same ``x`` or ``y`` value (i.e. a vertical or horizonal line), assume that a
       spline cannot be drawn and start populating a new spline list after storing these points
    #. If two points are closer together than the ``euclidian_distance`` parameter, draw a straight line between them
    #. If only a single point exists between splines/lines, do not draw a spline, and connect to the previous and next
       line/spline with a straight line.
    #. Store lists of points to be considered splines so long as exceptions in Step 3, 4, and 5 are not met.
    #. Neighboring splines that are not connected will be connected with a straight line
    #. It is assumed that the downstream function used to generate the geometry will connect start and end points

    :param numpy.array numpy_points_array: array of points
    :param float euclidian_distance: if the distance between two points is greater than this, draw a straight line.
        Distance should be provided in units *after* the unit conversion

    :return: Series of line and spline definitions
    :rtype: list
    """
    x_points = numpy_points_array[:, 0]
    y_points = numpy_points_array[:, 1]

    euclidian_distance_bools = _compare_euclidian_distance(euclidian_distance, numpy_points_array)
    vertical_horizontal_bools = _compare_xy_values(numpy_points_array)
    bools_from_or = _bool_via_or(euclidian_distance_bools, vertical_horizontal_bools)
    break_indices = numpy.where(bools_from_or)[0]
    all_splines = numpy.split(numpy_points_array, break_indices, axis=0)
    return all_splines


def _compare_euclidian_distance(euclidian_distance, numpy_points_array):
    """Compare the distance between points in a numpy array of x-y data to a provided euclidian distance

    The distance comparison is performed as ``numpy_array_distance > euclidian_distance``. The distance between points
    in the numpy array is computed such that the "current point" is compared to the previous point in the list. As such,
    a single ``False`` is always prepended to the beginning of the output ``euclidian_distance_bools`` list, because
    there is no such distance between the first point and one that comes before it.

    :param float euclidian_distance: distance value to compare against
    :param numpy.array numpy_points_array: array of points

    :return: bools for the distance comparison
    :rtype: list
    """
    calculated_euclidian_array = numpy.linalg.norm(numpy_points_array[1:, :] - numpy_points_array[0:-1, :], axis=1)
    euclidian_distance_bools = [False] + [this_euclidian_distance > euclidian_distance for this_euclidian_distance in
                                          calculated_euclidian_array]
    return euclidian_distance_bools


def _compare_xy_values(numpy_points_array):
    """Check neighboring x and y values in a numpy array of points for vertical or horizontal relationships

    This function loops through lists of points checking to see if a "current point" and the previous point in the numpy
    array are vertical or hozitonal from one another. As such, a single ``False`` is always prepended to the beginning
    of the output ``vertical_horizontal_bools`` list, because there is no such vertical/horizontal relationship between
    the first point and one that comes before it.

    :param numpy.array numpy_points_array: array of points

    :return: bools for vertical/horizontal relationship comparison
    :rtype: list
    """
    vertical_horizontal_bools = [False] + [numpy.isclose(coords1[0], coords2[0]) or
                                           numpy.isclose(coords1[1], coords2[1]) for coords1, coords2 in
                                           zip(numpy_points_array[1:, :], numpy_points_array[0:-1, :])]
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


def draw_part_from_splines(all_splines, planar=parsers.geometry_default_planar, model_name=parsers.geometry_default_model_name,
                           part_name=parsers.geometry_default_part_name, revolution_angle=parsers.geometry_default_revolution_angle):
    """Given a series of line/spline definitions, draw lines/splines in an Abaqus sketch and generate either a 2D part
    or a 3D body of revolution about the global Y-axis using the sketch. A 2D part can be either axisymmetric or planar
    depending on the ``planar`` and ``revolution_angle`` parameters.

    If ``planar`` is ``False`` and ``revolution_angle`` is equal (or ``numpy.isclose()``) to zero, this script will
    attempt to create a 2D axisymmetric model.

    If ``planar`` is ``False`` and ``revolution_angle`` is **not** zero, this script will attempt to create a 3D body of
    revolution about the global Y-axis.

    The default behavior of assuming ``planar=False`` implies that the sketch must lie entirely on the positive-X
    side of the global Y-axis, which is the constraint for both 2D axisymmetric and 3D revolved bodies.

    If ``planar`` is ``True``, this script will attempt to create a 2D planar model, which can be sketched in any/all
    four quadrants.

    **Note:** This function will connect the start and end points defined in ``all_splines``, which is a list of lists
    defining straight lines and splines. This is noted in the parser function
    :meth:`turbo_turtle._geometry.points_to_splines`.

    :param list all_splines: list of lists containing straight line and spline definitions
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param str model_name: name of the Abaqus model in which to create the part
    :param str part_name: name of the part being created
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries

    :returns: creates ``{part_name}`` within an Abaqus CAE database, not yet saved to local memory
    """
    import abaqus
    import abaqusConstants

    sketch1 = abaqus.mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    geometry, vertices, dimensions, constraints = sketch1.geometry, sketch1.vertices, sketch1.dimensions, sketch1.constraints
    sketch1.sketchOptions.setValues(viewStyle=abaqusConstants.AXISYM)
    sketch1.setPrimaryObject(option=abaqusConstants.STANDALONE)
    sketch1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    sketch1.FixedConstraint(entity=geometry[2])
    sketch1.ConstructionLine(point1=(0.0, 0.0), point2=(1.0, 0.0))
    sketch1.FixedConstraint(entity=geometry[3])

    # Draw splines through any spline list that has more than two poits
    for II, this_spline in enumerate(all_splines):
        this_spline = tuple(map(tuple, this_spline))
        if len(this_spline) != 1:
            sketch1.Spline(points=this_spline)
        if II != 0:
            sketch1.Line(point1=all_splines[II-1][-1], point2=this_spline[0])
    sketch1.Line(point1=all_splines[0][0], point2=all_splines[-1][-1])
    if planar:
        p = abaqus.mdb.models[model_name].Part(name=part_name, dimensionality=abaqusConstants.TWO_D,
            type=abaqusConstants.DEFORMABLE_BODY)
        p = abaqus.mdb.models[model_name].parts[part_name]
        p.BaseShell(sketch=sketch1)
    elif numpy.isclose(revolution_angle, 0.0):
        p = abaqus.mdb.models[model_name].Part(name=part_name, dimensionality=abaqusConstants.AXISYMMETRIC,
            type=abaqusConstants.DEFORMABLE_BODY)
        p = abaqus.mdb.models[model_name].parts[part_name]
        p.BaseShell(sketch=sketch1)
    else:
        p = abaqus.mdb.models[model_name].Part(name=part_name, dimensionality=abaqusConstants.THREE_D,
            type=abaqusConstants.DEFORMABLE_BODY)
        p = abaqus.mdb.models[model_name].parts[part_name]
        p.BaseSolidRevolve(sketch=sketch1, angle=revolution_angle, flipRevolveDirection=abaqus.OFF)
    sketch1.unsetPrimaryObject()
    p = abaqus.mdb.models[model_name].parts[part_name]
    del abaqus.mdb.models[model_name].sketches['__profile__']


if __name__ == "__main__":

    parser = parsers.geometry_parser(basename=basename)
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit as err:
        sys.exit(err.code)

    sys.exit(main(
        input_file=args.input_file,
        output_file=args.output_file,
        planar=args.planar,
        model_name=args.model_name,
        part_name=args.part_name,
        unit_conversion=args.unit_conversion,
        euclidian_distance=args.euclidian_distance,
        delimiter=args.delimiter,
        header_lines=args.header_lines,
        revolution_angle=args.revolution_angle
    ))
