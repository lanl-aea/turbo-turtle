import inspect
import os
import sys

import numpy


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import parsers
import vertices
import _mixed_utilities


def main(input_file, output_file,
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
         atol=parsers.geometry_defaults["atol"]):
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
    import abaqusConstants

    abaqus.mdb.Model(name=model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
    output_file = os.path.splitext(output_file)[0] + ".cae"
    geometry(input_file=input_file, planar=planar, model_name=model_name, part_name=part_name,
             revolution_angle=revolution_angle, delimiter=delimiter, header_lines=header_lines,
             euclidean_distance=euclidean_disance, unit_conversion=unit_conversion, y_offset=y_offset,
             rtol=rtol, atol=atol)
    abaqus.mdb.saveAs(pathName=output_file)


def geometry(input_file, planar, model_name, part_name, revolution_angle, delimiter, header_lines,
             euclidean_distance, unit_conversion, y_offset, rtol, atol):
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
    """
    part_name = _mixed_utilities.validate_part_name_or_exit(input_file, part_name)
    for file_name, new_part in zip(input_file, part_name):
        coordinates = _mixed_utilities.return_genfromtxt_or_exit(file_name, delimiter, header_lines,
                                                                 expected_dimensions=2, expected_columns=2)
        lines, splines = vertices.modified_lines_and_splines(coordinates, euclidean_distance, unit_conversion, y_offset,
                                                             rtol=rtol, atol=atol)
        try:
            draw_part_from_splines(lines, splines, planar=planar, model_name=model_name, part_name=new_part,
                                   euclidean_distance=euclidean_distance, revolution_angle=revolution_angle,
                                   rtol=rtol, atol=atol)
        except:
            message = "Error: failed to create part '{}' from '{}'. Check the XY coordinates for " \
                      "inadmissible Abaqus sketch connectivity. The ``turbo-turtle geometry-xyplot`` " \
                      "subcommand can plot points to aid in troubleshooting.\n".format(new_part, file_name)
            _mixed_utilities.sys_exit(message)


def draw_part_from_splines(lines, splines,
                           planar=parsers.geometry_defaults["planar"],
                           model_name=parsers.geometry_defaults["model_name"],
                           part_name=parsers.geometry_defaults["part_name"],
                           euclidean_distance=parsers.geometry_defaults["euclidean_distance"],
                           revolution_angle=parsers.geometry_defaults["revolution_angle"],
                           rtol=parsers.geometry_defaults["rtol"],
                           atol=parsers.geometry_defaults["atol"]):
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

    sketch = abaqus.mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
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


def _gui_post_action(center, xvector, zvector, model_name, part_name):
    """Action performed after running partition

    After partitioning, this funciton resets the viewport - if the last partition action hits the an AbaqusException
    except statement in the ``partition`` function, the user will otherwise be left in a sketch view that is hard to
    exit from. An example of this is partioning a half-sphere; half of the partitioning actions are expected to fail,
    since there is no geometry to partition on the open-end of the half-sphere.

    This function is designed to have the exact same arguments as 
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.partition.partition`
    """
    import abaqus

    part_object = abaqus.mdb.models[model_name].parts[part_name[-1]]
    session.viewports['Viewport: 1'].setValues(displayedObject=part_object)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.fitView()


def geometry_gui():
    """Function with no inputs required for driving the plugin
    """
    gui_wrapper(inputs_function=_gui_get_inputs,
                subcommand_function=geometry,
                post_action_function=_gui_post_action)


if __name__ == "__main__":
    if 'caeModules' in sys.modules:  # All Abaqus CAE sessions immediately load caeModules
        geometry_gui()
    else:
    parser = parsers.partition_parser(basename=basename)
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
            revolution_angle=args.revolution_angle,
            y_offset=args.y_offset,
            rtol=args.rtol,
            atol=args.atol
        ))
