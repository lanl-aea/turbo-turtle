import inspect
import os
import sys

import numpy


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import parsers
import lines_and_splines


def main(input_file, output_file,
         planar=parsers.geometry_default_planar,
         model_name=parsers.geometry_default_model_name,
         part_name=parsers.geometry_default_part_name,
         unit_conversion=parsers.geometry_default_unit_conversion,
         euclidean_distance=parsers.geometry_default_euclidean_distance,
         delimiter=parsers.geometry_default_delimiter,
         header_lines=parsers.geometry_default_header_lines,
         revolution_angle=parsers.geometry_default_revolution_angle):
    """This script takes an array of XY coordinates from a text file and creates a 2D sketch or 3D body of
    revolution about the global Y-axis. Note that 2D axisymmetric sketches and sketches for 3D bodies of revolution
    about the global Y-axis must lie entirely on the positive-X side of the global Y-axis. In general, a 2D sketch can
    lie in all four quadrants; this is referred to as a "planar" sketch and requires that the ``planar`` boolean
    arugment be set to ``True``. This script can accept multiple input files to create multiple parts in the same Abaqus
    model. The ``part_name`` parameter allows explicit naming of part(s) in the model. If omitted from the command line
    arguments, the default is to use the input file basename(s) as the part name(s).

    :param str input_file: input text file(s) with coordinates to draw
    :param str output_file: Abaqus CAE database to save the part(s)
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param str model_name: name of the Abaqus model in which to create the part
    :param list part_name: name(s) of the part(s) being created
    :param float unit_conversion: multiplication factor applies to all coordinates
    :param float euclidean_distance: if the distance between two coordinates is greater than this, draw a straight line.
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
        coordinates = read_file(file_name, delimiter, header_lines)
        coordinates = coordinates * unit_conversion
        try:
            draw_part_from_splines(coordinates, planar=planar, model_name=model_name, part_name=new_part,
                                   euclidean_distance=euclidean_distance, revolution_angle=revolution_angle)
        except:
            error_message = "Error: failed to create part '{}' from '{}'\n".format(new_part, file_name)
            sys.stderr.write(error_message)
            sys.exit(1)

    abaqus.mdb.saveAs(pathName=output_file)


def _validate_part_name(input_file, part_name):
    """Validate the structure of the ``part_name`` list to the following rules:

    * If ``part_name`` is ``[None]``, assign the base names of ``input_file`` to ``part_name``
    * Else if the length of ``part_name`` is not equal to the length of ``input_file``, exit with an error

    :param list input_file: input text file(s) with coordinates to draw
    :param list part_name: name(s) of part(s) being created

    :return: part name(s)
    :rtype: list
    """
    if part_name[0] is None:
        part_name = [os.path.splitext(os.path.basename(part_file))[0] for part_file in input_file]
    elif len(input_file) != len(part_name):
        error_message = "Error: The part name length '{}' must match the input file length '{}'\n".format(
            len(part_name), len(input_file))
        sys.stderr.write(error_message)
        sys.exit(1)
    return part_name


def read_file(file_name, delimiter=parsers.geometry_default_delimiter, header_lines=parsers.geometry_default_header_lines):
    """Parse a text file of XY coordinates into a numpy array

    If the resulting numpy array doesn't have shape [N, 2], return an error exit code

    :param str file_name: input text file with coordinates to draw
    :param str delimiter: character to use as a delimiter when reading the input file
    :param int header_lines: number of lines in the header to skip when reading the input file

    :return: 2D array of XY coordinates with shape [N, 2]
    :rtype: numpy.array
    """
    with open(file_name, 'r') as points_file:
        coordinates = numpy.genfromtxt(points_file, delimiter=delimiter, skip_header=header_lines)
    shape = coordinates.shape
    dimensions = len(shape)
    if dimensions != 2:
        sys.stderr.write("Expected two-dimensional coordinates. Found '{}' dimensions\n".format(dimensions))
        sys.exit(3)
    columns = shape[1]
    if columns != 2:
        sys.stderr.write("Expected coordinates with two columns: X,Y. Found '{}' columns\n".format(columns))
        sys.exit(4)
    return coordinates


def draw_part_from_splines(coordinates,
                           planar=parsers.geometry_default_planar,
                           model_name=parsers.geometry_default_model_name,
                           part_name=parsers.geometry_default_part_name,
                           euclidean_distance=parsers.geometry_default_euclidean_distance,
                           revolution_angle=parsers.geometry_default_revolution_angle):
    """Given a series of line/spline definitions, draw lines/splines in an Abaqus sketch and generate either a 2D part
    or a 3D body of revolution about the global Y-axis using the sketch. A 2D part can be either axisymmetric or planar
    depending on the ``planar`` and ``revolution_angle`` parameters.

    If ``planar`` is ``False`` and ``revolution_angle`` is equal (``numpy.isclose()``) to zero, this script will
    attempt to create a 2D axisymmetric model.

    If ``planar`` is ``False`` and ``revolution_angle`` is **not** zero, this script will attempt to create a 3D body of
    revolution about the global Y-axis.

    The default behavior of assuming ``planar=False`` implies that the sketch must lie entirely on the positive-X
    side of the global Y-axis, which is the constraint for both 2D axisymmetric and 3D revolved bodies.

    If ``planar`` is ``True``, this script will attempt to create a 2D planar model, which can be sketched in any/all
    four quadrants.

    **Note:** This function will always connect the first and last coordinates

    :param numpy.array coordinates: [N, 2] array of XY coordinates.
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param str model_name: name of the Abaqus model in which to create the part
    :param str part_name: name of the part being created
    :param float euclidean_distance: if the distance between two coordinates is greater than this, draw a straight line.
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries

    :returns: creates ``{part_name}`` within an Abaqus CAE database, not yet saved to local memory
    """
    import abaqus
    import abaqusConstants

    sketch = abaqus.mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    geometry, vertices, dimensions, constraints = sketch.geometry, sketch.vertices, sketch.dimensions, sketch.constraints
    sketch.sketchOptions.setValues(viewStyle=abaqusConstants.AXISYM)
    sketch.setPrimaryObject(option=abaqusConstants.STANDALONE)
    sketch.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    sketch.FixedConstraint(entity=geometry[2])
    sketch.ConstructionLine(point1=(0.0, 0.0), point2=(1.0, 0.0))
    sketch.FixedConstraint(entity=geometry[3])

    lines, splines = lines_and_splines.lines_and_splines(coordinates, euclidean_distance)
    for spline in splines:
        spline = tuple(map(tuple, spline))
        sketch.Spline(points=spline)
    for point1, point2 in lines:
        point1 = tuple(point1)
        point2 = tuple(point2)
        sketch.Line(point1=point1, point2=point2)
    if planar:
        p = abaqus.mdb.models[model_name].Part(name=part_name, dimensionality=abaqusConstants.TWO_D,
            type=abaqusConstants.DEFORMABLE_BODY)
        p = abaqus.mdb.models[model_name].parts[part_name]
        p.BaseShell(sketch=sketch)
    elif numpy.isclose(revolution_angle, 0.0):
        p = abaqus.mdb.models[model_name].Part(name=part_name, dimensionality=abaqusConstants.AXISYMMETRIC,
            type=abaqusConstants.DEFORMABLE_BODY)
        p = abaqus.mdb.models[model_name].parts[part_name]
        p.BaseShell(sketch=sketch)
    else:
        p = abaqus.mdb.models[model_name].Part(name=part_name, dimensionality=abaqusConstants.THREE_D,
            type=abaqusConstants.DEFORMABLE_BODY)
        p = abaqus.mdb.models[model_name].parts[part_name]
        p.BaseSolidRevolve(sketch=sketch, angle=revolution_angle, flipRevolveDirection=abaqus.OFF)
    sketch.unsetPrimaryObject()
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
        euclidean_distance=args.euclidean_distance,
        delimiter=args.delimiter,
        header_lines=args.header_lines,
        revolution_angle=args.revolution_angle
    ))
