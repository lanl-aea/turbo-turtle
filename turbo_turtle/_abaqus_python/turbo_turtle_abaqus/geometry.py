import ast
import inspect
import os
import sys
import glob

import numpy


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import parsers  # noqa: E402
from turbo_turtle_abaqus import vertices  # noqa: E402
from turbo_turtle_abaqus import _mixed_utilities  # noqa: E402
from turbo_turtle_abaqus import _abaqus_utilities  # noqa: E402
from turbo_turtle_abaqus import _mixed_settings  # noqa: E402


def main(
    input_file,
    output_file,
    planar=parsers.geometry_defaults["planar"],
    model_name=parsers.geometry_defaults["model_name"],
    part_name=parsers.geometry_defaults["part_name"],
    unit_conversion=parsers.geometry_defaults["unit_conversion"],
    euclidean_distance=parsers.geometry_defaults["euclidean_distance"],
    delimiter=parsers.geometry_defaults["delimiter"],
    header_lines=parsers.geometry_defaults["header_lines"],
    revolution_angle=parsers.geometry_defaults["revolution_angle"],
    y_offset=parsers.geometry_defaults["y_offset"],
    rtol=parsers.geometry_defaults["rtol"],
    atol=parsers.geometry_defaults["atol"],
):
    """Create 2D planar, 2D axisymmetric, or 3D revolved geometry from an array of XY coordinates.

    This script takes an array of XY coordinates from a text file and creates a 2D sketch or 3D body of
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
    :param float y_offset: vertical offset along the global Y-axis. Offset should be provided in units *after* the unit
        conversion.
    :param float rtol: relative tolerance for vertical/horizontal line checks
    :param float atol: absolute tolerance for vertical/horizontal line checks

    :returns: writes ``{output_file}.cae``
    """
    import abaqus

    output_file = os.path.splitext(output_file)[0] + ".cae"
    try:
        geometry(
            input_file=input_file,
            planar=planar,
            model_name=model_name,
            part_name=part_name,
            revolution_angle=revolution_angle,
            delimiter=delimiter,
            header_lines=header_lines,
            euclidean_distance=euclidean_distance,
            unit_conversion=unit_conversion,
            y_offset=y_offset,
            rtol=rtol,
            atol=atol,
        )
    except RuntimeError as err:
        _mixed_utilities.sys_exit(str(err))
    abaqus.mdb.saveAs(pathName=output_file)


def geometry(
    input_file,
    planar,
    model_name,
    part_name,
    revolution_angle,
    delimiter,
    header_lines,
    euclidean_distance,
    unit_conversion,
    y_offset,
    rtol,
    atol,
):
    """Create 2D planar, 2D axisymmetric, or 3D revolved geometry from an array of XY coordinates.

    This function drive the geometry creation of 2D planar, 2D axisymetric, or 3D revolved bodies and operates on a new
    Abaqus moddel database object.

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
    :param float y_offset: vertical offset along the global Y-axis. Offset should be provided in units *after* the unit
        conversion.
    :param float rtol: relative tolerance for vertical/horizontal line checks
    :param float atol: absolute tolerance for vertical/horizontal line checks

    :raises RuntimeError: failure to create a sketch or part from a CSV file.
    """
    import abaqus

    _abaqus_utilities._conditionally_create_model(model_name)

    failed_parts = []  # List of Tuples keeping track of parts that failed and their input files

    part_name = _mixed_utilities.validate_part_name_or_exit(input_file, part_name)
    for file_name, new_part in zip(input_file, part_name):
        coordinates = _mixed_utilities.return_genfromtxt_or_exit(
            file_name, delimiter, header_lines, expected_dimensions=2, expected_columns=2
        )
        coordinates = vertices.scale_and_offset_coordinates(coordinates, unit_conversion, y_offset)
        lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance, rtol=rtol, atol=atol)
        try:
            draw_part_from_splines(
                lines,
                splines,
                planar=planar,
                model_name=model_name,
                part_name=new_part,
                euclidean_distance=euclidean_distance,
                revolution_angle=revolution_angle,
                rtol=rtol,
                atol=atol,
            )
        except abaqus.AbaqusException:
            failed_parts += [(new_part, file_name)]
    if failed_parts:
        error_message = [
            "Error: failed to create the following parts from input files. Check the XY coordinates "
            "for inadmissible Abaqus sketch connectivity. The ``turbo-turtle geometry-xyplot`` "
            "subcommand can plot points to aid in troubleshooting."
        ]
        error_message += ["    {}, {}".format(this_part, this_file) for this_part, this_file in failed_parts]
        raise RuntimeError("\n".join(error_message))


def draw_part_from_splines(
    lines,
    splines,
    planar=parsers.geometry_defaults["planar"],
    model_name=parsers.geometry_defaults["model_name"],
    part_name=parsers.geometry_defaults["part_name"],
    euclidean_distance=parsers.geometry_defaults["euclidean_distance"],
    revolution_angle=parsers.geometry_defaults["revolution_angle"],
    rtol=parsers.geometry_defaults["rtol"],
    atol=parsers.geometry_defaults["atol"],
):
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

    :param list lines: list of [2, 2] shaped arrays of (x, y) coordinates defining a line segment
    :param list splines: list of [N, 2] shaped arrays of (x, y) coordinates defining a spline
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param str model_name: name of the Abaqus model in which to create the part
    :param str part_name: name of the part being created
    :param float euclidean_distance: if the distance between two coordinates is greater than this, draw a straight line.
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries

    :returns: creates ``{part_name}`` within an Abaqus CAE database, not yet saved to local memory
    """
    import abaqus
    import abaqusConstants

    revolution_direction = _abaqus_utilities.revolution_direction(revolution_angle)
    revolution_angle = abs(revolution_angle)

    sketch = abaqus.mdb.models[model_name].ConstrainedSketch(name="__profile__", sheetSize=200.0)
    sketch.sketchOptions.setValues(viewStyle=abaqusConstants.AXISYM)
    sketch.setPrimaryObject(option=abaqusConstants.STANDALONE)
    sketch.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    sketch.FixedConstraint(entity=sketch.geometry[2])
    sketch.ConstructionLine(point1=(0.0, 0.0), point2=(1.0, 0.0))
    sketch.FixedConstraint(entity=sketch.geometry[3])

    for spline in splines:
        spline = tuple(map(tuple, spline))
        sketch.Spline(points=spline)
    for point1, point2 in lines:
        point1 = tuple(point1)
        point2 = tuple(point2)
        sketch.Line(point1=point1, point2=point2)
    if planar:
        part = abaqus.mdb.models[model_name].Part(
            name=part_name, dimensionality=abaqusConstants.TWO_D_PLANAR, type=abaqusConstants.DEFORMABLE_BODY
        )
        part.BaseShell(sketch=sketch)
    elif numpy.isclose(revolution_angle, 0.0):
        part = abaqus.mdb.models[model_name].Part(
            name=part_name, dimensionality=abaqusConstants.AXISYMMETRIC, type=abaqusConstants.DEFORMABLE_BODY
        )
        part.BaseShell(sketch=sketch)
    else:
        part = abaqus.mdb.models[model_name].Part(
            name=part_name, dimensionality=abaqusConstants.THREE_D, type=abaqusConstants.DEFORMABLE_BODY
        )
        part.BaseSolidRevolve(sketch=sketch, angle=revolution_angle, flipRevolveDirection=revolution_direction)
    sketch.unsetPrimaryObject()
    del abaqus.mdb.models[model_name].sketches["__profile__"]


def _gui_get_inputs():
    """Interactive Inputs

    Prompt the user for inputs with this interactive data entry function. When called, this function opens an Abaqus CAE
    GUI window with text boxes to enter the values given below. Note to developers - if you update this 'GUI-INPUTS'
    below, also update ``_mixed_settings._geometry_gui_help_string`` that gets used as the GUI ``label``.

    GUI-INPUTS
    ==========
    * Input File(s) - glob statement or comma separated list of files (NO SPACES) with points in x-y coordinates
    * Part Name(s) - part names for the parts being created. If ``None``, then part name is determined by the input
        files. This must either ``None``, a single part name, or a comma separated list of part names (NO SPACES)
    * Model Name - parts will be created in a new model with this name
    * Unit Conversion - unit conversion multiplication factor
    * Euclidean Distance - connect points with a straight line if the distance between them is larger than this
    * Planar Geometry Switch - switch to indicate that the 2D model is planar not axisymmetric (``True`` for planar)
    * Revolution Angle - revolution angle for a 3D part in degrees
    * Delimiter - delimiter character between columns in the input file(s)
    * Header Lines - number of header lines to skip in the input file(s)
    * Y-Offset - offset along the global y-axis
    * rtol - relative tolerance used by ``numpy.isclose``. If ``None``, use numpy defaults
    * atol - absolute tolerance used by ``numpy.isclose``. If ``None``, use numpy defaults

    **IMPORTANT** - this function must return key-value pairs that will successfully unpack as ``**kwargs`` in
    ``geometry``

    :return: ``user_inputs`` - a dictionary of the following key-value pair types:

    * ``input_file``: ``list`` type, input text files with points in x-y coordinates
    * ``part_name``: ``list`` type, part names, one for each input file, or ``None``
    * ``model_name``: ``str`` type, new model containing the part generated from the input file(s)
    * ``unit_conversion``: ``float`` type, unit conversion multiplication factor
    * ``euclidean_distance``: ``float`` type, distance between points for deciding to draw a straight line
    * ``planar``: ``bool`` type, switch for making 2D geometry planar, instead of axisymmetric
    * ``revolution_angle``: ``float`` type, revolution angle in degrees for 3D geometry
    * ``delimiter``: ``str`` type, delimiter character between columns in the input file(s)
    * ``header_lines``: ``int`` type, number of header lines to skip in the input file(s)
    * ``y_offset``: ``float`` type, offset along the y-axis
    * ``rtol``: ``float`` type, relative tolerance used by ``numpy.isclose``. If ``None``, use numpy defaults
    * ``atol``: ``float`` type, absolute tolerance used by ``numpy.isclose``. If ``None``, use numpy defaults

    :raises RuntimeError: if at least one input file is not specified
    """
    import abaqus

    default_input_files = "File1.csv,File2.csv OR *.csv"
    default_part_names = "Part-1,Part-2, OR None OR blank"

    fields = (
        ("Input File(s):", default_input_files),
        ("Part Name(s):", default_part_names),
        ("Model Name:", parsers.geometry_defaults["model_name"]),
        ("Unit Conversion:", str(parsers.geometry_defaults["unit_conversion"])),
        ("Euclidean Distance:", str(parsers.geometry_defaults["euclidean_distance"])),
        ("Planar Geometry Switch:", str(parsers.geometry_defaults["planar"])),
        ("Revolution Angle:", str(parsers.geometry_defaults["revolution_angle"])),
        ("Delimiter:", parsers.geometry_defaults["delimiter"]),
        ("Header Lines:", str(parsers.geometry_defaults["header_lines"])),
        ("Y-Offset:", str(parsers.geometry_defaults["y_offset"])),
        ("rtol:", str(parsers.geometry_defaults["rtol"])),
        ("atol:", str(parsers.geometry_defaults["atol"])),
    )

    (
        input_file_strings,
        part_name_strings,
        model_name,
        unit_conversion,
        euclidean_distance,
        planar,
        revolution_angle,
        delimiter,
        header_lines,
        y_offset,
        rtol,
        atol,
    ) = abaqus.getInputs(
        dialogTitle="Turbo Turtle Geometry",
        label=_mixed_settings._geometry_gui_help_string,
        fields=fields,
    )

    if input_file_strings is not None:  # Will be None if the user hits the "cancel/esc" button
        input_file = []
        if input_file_strings and input_file_strings != default_input_files:
            for this_input_file_string in input_file_strings.split(","):
                input_file += glob.glob(this_input_file_string)
        else:  # Catch an if the user fails to specify input files
            error_message = "Error: You must specify at least one input file"
            raise RuntimeError(error_message)

        if part_name_strings == "None" or part_name_strings == default_part_names or not part_name_strings:
            part_name = [None]
        else:
            part_name = part_name_strings.split(",")

        if rtol == "None" or not rtol:
            rtol = None
        else:
            rtol = float(rtol)

        if atol == "None" or not atol:
            atol = None
        else:
            atol = float(atol)

        user_inputs = {
            "model_name": model_name,
            "input_file": input_file,
            "part_name": part_name,
            "unit_conversion": float(unit_conversion),
            "euclidean_distance": float(euclidean_distance),
            "planar": ast.literal_eval(planar),
            "revolution_angle": float(revolution_angle),
            "delimiter": delimiter,
            "header_lines": int(header_lines),
            "y_offset": float(y_offset),
            "rtol": rtol,
            "atol": atol,
        }
    else:
        user_inputs = {}
    return user_inputs


def _gui():
    """Function with no inputs required for driving the plugin"""
    _abaqus_utilities.gui_wrapper(
        inputs_function=_gui_get_inputs, subcommand_function=geometry, post_action_function=_abaqus_utilities._view_part
    )


if __name__ == "__main__":
    if "caeModules" in sys.modules:  # All Abaqus CAE sessions immediately load caeModules
        _gui()
    else:
        parser = parsers.geometry_parser(basename=basename)
        try:
            args, unknown = parser.parse_known_args()
        except SystemExit as err:
            sys.exit(err.code)

        sys.exit(
            main(
                input_file=args.input_file,
                output_file=args.output_file,
                planar=args.planar,
                model_name=args.model_name,
                part_name=args.part_name,
                unit_conversion=args.unit_conversion,
                euclidean_distance=args.euclidean_distance,
                delimiter=args.delimiter,
                header_lines=args.header_lines,
                revolution_angle=args.revolution_angle,
                y_offset=args.y_offset,
                rtol=args.rtol,
                atol=args.atol,
            )
        )
