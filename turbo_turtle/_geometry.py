import argparse
import inspect
import os
import sys
import numpy

default_unit_conversion = 1.0
default_planar = False
default_euclidian_distance = 4.0
default_model_name = "Model-1"
default_part_name = [None]
default_delimiter = ","
default_header_lines = 0
default_revolution_angle = 360.0


def main(input_file, output_file, planar=default_planar, model_name=default_model_name, 
         part_name=default_part_name, unit_conversion=default_unit_conversion,
         euclidian_distance=default_euclidian_distance, delimiter=default_delimiter, 
         header_lines=default_header_lines, revolution_angle=default_revolution_angle):
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
    for file_name, new_part in zip(input_file, part_name):
        try:
            numpy_points_array = read_file(file_name, delimiter, header_lines)
            numpy_points_array = numpy_points_array * unit_conversion
            all_splines = points_to_splines(numpy_points_array, euclidian_distance)
            draw_part_from_splines(all_splines, planar, model_name, new_part, revolution_angle)
        except:
            sys.stderr.write("Error: failed to create part {} from {}".format(new_part, file_name))
            exit(1)
    
    output_file = os.path.splitext(output_file)[0] + ".cae"
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
    if part_name[0] is None:
        part_name = [os.path.splitext(os.path.basename(part_file))[0] for part_file in input_file]
    elif len(input_file) != len(part_name):
        error_message = "The part name length '{}' must match the input file length '{}'\n".format(
            len(part_name), len(input_file))
        sys.stderr.write(error_message)
        sys.exit(1)
    return part_name


def read_file(file_name, delimiter=default_delimiter, header_lines=default_header_lines):
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


def points_to_splines(numpy_points_array, euclidian_distance=default_euclidian_distance):
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
    # Extract the x-y points from the points input file
    x_points = numpy_points_array[:, 0]
    y_points = numpy_points_array[:, 1]

    # Need to find where the inner and outer splines start and end
    # Looking for two points that have the same x-value or y-value
    # TODO: remove this 90-degree assumption and add a parameter for an arbitrary angle between lines
    all_splines = []
    new_spline_counter = 0
    for II, (xval, yval) in enumerate(zip(x_points, y_points)):
        if II == 0:
            this_spline = ()
            new_spline_counter += 1
            this_spline += ((xval, yval), )  # Need to append the first point no matter what
        else:
            calculated_euclidian_distance = ((xval - x_points[II-1]) ** 2 + (yval - y_points[II-1]) ** 2) ** 0.5
            # Start the next spline if adjacent points have same xval or yval (i.e. 90-degrees)
            if xval == this_spline[-1][0] or yval == this_spline[-1][-1]:
                all_splines.append(this_spline)
                this_spline = ()
                new_spline_counter += 1
                this_spline += ((xval, yval), )
            # If the euclidian distance between two points is too large, then that must be a straight line
            # Straight line means start a new spline tuple
            elif calculated_euclidian_distance > euclidian_distance:
                all_splines.append(this_spline)
                this_spline = ()
                new_spline_counter += 1
                this_spline += ((xval, yval), )
            else:
                this_spline += ((xval, yval), )  # All else, append 1st spline
            if II == len(x_points)-1:
                all_splines.append(this_spline)
    return all_splines


def draw_part_from_splines(all_splines, planar=default_planar, model_name=default_model_name, 
                           part_name=default_part_name, revolution_angle=default_revolution_angle):
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
    session.viewports['Viewport: 1'].setValues(displayedObject=p)


def get_parser():
    file_name = inspect.getfile(lambda:None)
    basename = os.path.basename(file_name)
    prog = "abaqus cae -noGui {} --".format(basename)
    cli_description = "Abaqus Python script for creating 2D or 3D part(s) from an x-y coordinate system input file(s)"
    parser = argparse.ArgumentParser(description=cli_description, prog=prog)
        
    parser.add_argument("--input-file", type=str, nargs="+", required=True,
                        help="Name of an input file(s) with points in x-y coordinate system")
    parser.add_argument("--unit-conversion", type=float, default=default_unit_conversion,
                        help="Unit conversion multiplication factor (default: %(default)s)")
    parser.add_argument("--euclidian_distance", type=float, default=default_euclidian_distance,
                        help="Connect points with a straight line is the distance between is larger than this (default: %(default)s)")
    parser.add_argument("--planar", action='store_true',
                        help="Switch to indicate that 2D model dimensionality is planar, not axisymmetric (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=default_model_name,
                        help="Abaqus model name in which to create the new part(s) (default: %(default)s)")
    parser.add_argument("--part-name", type=str, nargs="+", default=default_part_name,
                        help="Abaqus part name(s) (default: %(default)s)")
    parser.add_argument("--output-file", type=str, required=True,
                        help="Name of the output Abaqus CAE file to save (default: %(default)s)")
    parser.add_argument("--delimiter", type=str, default=default_delimiter,
                        help="Delimiter character between columns in the points file(s) (default: %(default)s)")
    parser.add_argument("--header-lines", type=int, default=default_header_lines,
                        help="Number of header lines to skip when parsing the points files(s) (default: %(default)s)")
    parser.add_argument("--revolution-angle", type=float, default=default_revolution_angle,
                        help="Revolution angle for a 3D part in degrees (default: %(default)s)")
    return parser


if __name__ == "__main__":
    parser = get_parser()
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
