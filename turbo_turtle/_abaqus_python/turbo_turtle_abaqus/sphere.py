import os
import sys
import inspect

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
    inner_radius,
    outer_radius,
    output_file,
    input_file=parsers.sphere_defaults["input_file"],
    quadrant=parsers.sphere_defaults["quadrant"],
    revolution_angle=parsers.sphere_defaults["revolution_angle"],
    y_offset=parsers.sphere_defaults["y_offset"],
    model_name=parsers.sphere_defaults["model_name"],
    part_name=parsers.sphere_defaults["part_name"],
):
    """Wrap sphere function with file open and file write operations

    :param float inner_radius: inner radius (size of hollow)
    :param float outer_radius: outer radius (size of sphere)
    :param str output_file: output file name. Will be stripped of the extension and ``.cae`` will be used.
    :param str input_file: input file name. Will be stripped of the extension and ``.cae`` will be used.
    :param str quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param float revolution_angle: angle of rotation 0.-360.0 degrees. Provide 0 for a 2D axisymmetric model.
    :param float y_offset: vertical offset along the global Y-axis
    :param str model_name: name of the Abaqus model
    :param str part_name: name of the part to be created in the Abaqus model
    """
    import abaqus

    output_file = os.path.splitext(output_file)[0] + ".cae"

    # Preserve the (X, Y) center implementation, but use the simpler y-offset interface
    center = (0.0, y_offset)

    try:
        if input_file is not None:
            input_file = os.path.splitext(input_file)[0] + ".cae"
            # Avoid modifying the contents or timestamp on the input file.
            # Required to get conditional re-builds with a build system such as GNU Make, CMake, or SCons
            with _abaqus_utilities.AbaqusNamedTemporaryFile(input_file, suffix=".cae", dir="."):
                sphere(
                    inner_radius,
                    outer_radius,
                    quadrant=quadrant,
                    revolution_angle=revolution_angle,
                    center=center,
                    model_name=model_name,
                    part_name=part_name,
                )
                abaqus.mdb.saveAs(pathName=output_file)
        else:
            sphere(
                inner_radius,
                outer_radius,
                quadrant=quadrant,
                revolution_angle=revolution_angle,
                center=center,
                model_name=model_name,
                part_name=part_name,
            )
            abaqus.mdb.saveAs(pathName=output_file)
    except RuntimeError as err:
        _mixed_utilities.sys_exit(str(err))


def sphere(
    inner_radius,
    outer_radius,
    center=parsers.sphere_defaults["center"],
    quadrant=parsers.sphere_defaults["quadrant"],
    revolution_angle=parsers.sphere_defaults["revolution_angle"],
    model_name=parsers.sphere_defaults["model_name"],
    part_name=parsers.sphere_defaults["part_name"],
):
    """Create a hollow, spherical geometry from a sketch in the X-Y plane with upper (+X+Y), lower (+X-Y), or both
    quadrants.

    .. warning::

       The lower quadrant creation is currently broken

    :param float inner_radius: inner radius (size of hollow)
    :param float outer_radius: outer radius (size of sphere)
    :param tuple center: tuple of floats (X, Y) location for the center of the sphere
    :param str quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param float revolution_angle: angle of rotation 0.-360.0 degrees. Provide 0 for a 2D axisymmetric model.
    :param str model_name: name of the Abaqus model
    :param str part_name: name of the part to be created in the Abaqus model
    """
    import abaqus
    import abaqusConstants

    revolution_direction = _abaqus_utilities.revolution_direction(revolution_angle)
    revolution_angle = abs(revolution_angle)

    _abaqus_utilities._conditionally_create_model(model_name)

    _validate_sphere_quadrant(quadrant, parsers.sphere_quadrant_options)

    model = abaqus.mdb.models[model_name]

    arc_points = vertices.sphere(center, inner_radius, outer_radius, quadrant)
    inner_point1, inner_point2, outer_point1, outer_point2 = arc_points

    sketch = model.ConstrainedSketch(name="__profile__", sheetSize=200.0)
    if numpy.allclose(inner_point1, center) and numpy.allclose(inner_point2, center):
        inner_point1 = center
        inner_point2 = center
    else:
        sketch.ArcByCenterEnds(
            center=center, point1=inner_point1, point2=inner_point2, direction=abaqusConstants.CLOCKWISE
        )
    sketch.ArcByCenterEnds(center=center, point1=outer_point1, point2=outer_point2, direction=abaqusConstants.CLOCKWISE)
    sketch.Line(point1=outer_point1, point2=inner_point1)
    sketch.Line(point1=outer_point2, point2=inner_point2)
    centerline = sketch.ConstructionLine(point1=center, angle=90.0)
    sketch.assignCenterline(line=centerline)

    if numpy.isclose(revolution_angle, 0.0):
        part = model.Part(
            name=part_name, dimensionality=abaqusConstants.AXISYMMETRIC, type=abaqusConstants.DEFORMABLE_BODY
        )
        part.BaseShell(sketch=sketch)
    else:
        part = model.Part(name=part_name, dimensionality=abaqusConstants.THREE_D, type=abaqusConstants.DEFORMABLE_BODY)
        part.BaseSolidRevolve(sketch=sketch, angle=revolution_angle, flipRevolveDirection=revolution_direction)
    del sketch


def _validate_sphere_quadrant(quadrant, valid_quadrants):
    """Validate the user-provided sphere quadrant against a provided list of valid quadrants

    :param str quadrant: user provided sphere quadrant
    :param list valid_quadrants: valid quadrant to check against

    :raises RuntimError: if user provided quadrant is invalid
    """
    if quadrant not in valid_quadrants:
        error_message = "Error: Quadrant option must be one of: {}".format(valid_quadrants)
        raise RuntimeError(error_message)


def _gui_get_inputs():
    """Interactive Inputs

    Prompt the user for inputs with this interactive data entry function. When called, this function opens an Abaqus CAE
    GUI window with text boxes to enter the values given below. Note to developers - if you update this 'GUI-INPUTS'
    below, also update ``_mixed_settings._sphere_gui_help_string`` that gets used as the GUI ``label``.

    GUI-INPUTS
    ==========
    * Part Name - part name for the sphere being created.
    * Model Name - parts will be created in a new model with this name
    * Inner Radius - inner radius of the sphere
    * Outer Radius - outer radius of the sphere
    * Revolution Angle - revolution angle for a 3D part in degrees
    * Y-Offset - offset along the global y-axis
    * Quadrant - XY plane quadrant for drawing the sphere. Choose from 'both', 'upper', or 'lower'

    **IMPORTANT** - this function must return key-value pairs that will successfully unpack as ``**kwargs`` in
    ``sphere``

    :return: ``user_inputs`` - a dictionary of the following key-value pair types:

    * ``part_name``: ``str`` type, part name of the sphere
    * ``model_name``: ``str`` type, new model containing the part generated from the input file(s)
    * ``inner_radius``: ``float`` type, inner radius of the sphere
    * ``outer_radius``: ``float`` type, outer radius of the sphere
    * ``revolution_angle``: ``float`` type, revolution angle in degrees for 3D geometry
    * ``y_offset``: ``float`` type, offset along the y-axis
    * ``quadrant``: ``str`` type, XY plane quadrant for drawing the sphere

    :raises RuntimeError: if inner radius or  outer radius are not specified.
    """
    import abaqus

    fields = (
        ("Part Name:", parsers.sphere_defaults["part_name"]),
        ("Model Name:", parsers.sphere_defaults["model_name"]),
        ("Inner Radius:", ""),
        ("Outer Radius:", ""),
        ("Revolution Angle:", str(parsers.sphere_defaults["revolution_angle"])),
        ("Y-Offset:", str(parsers.sphere_defaults["y_offset"])),
        ("Quadrant:", parsers.sphere_defaults["quadrant"]),
    )

    part_name, model_name, inner_radius, outer_radius, revolution_angle, y_offset, quadrant = abaqus.getInputs(
        dialogTitle="Turbo Turtle Sphere",
        label=_mixed_settings._sphere_gui_help_string,
        fields=fields,
    )

    if part_name is not None:  # Will be None if the user hits the "cancel/esc" button
        # Preserve the (X, Y) center implementation, but use the simpler y-offset interface
        center = (0.0, float(y_offset))

        if not inner_radius or not outer_radius:
            error_message = "Error: You must specify an inner and outer radius for the sphere"
            raise RuntimeError(error_message)

        _validate_sphere_quadrant(quadrant, parsers.sphere_quadrant_options)

        user_inputs = {
            "inner_radius": float(inner_radius),
            "outer_radius": float(outer_radius),
            "center": center,
            "quadrant": quadrant,
            "revolution_angle": float(revolution_angle),
            "model_name": model_name,
            "part_name": part_name,
        }
    else:
        user_inputs = {}
    return user_inputs


def _gui():
    """Function with no inputs required for driving the plugin"""
    _abaqus_utilities.gui_wrapper(
        inputs_function=_gui_get_inputs, subcommand_function=sphere, post_action_function=_abaqus_utilities._view_part
    )


if __name__ == "__main__":
    if "caeModules" in sys.modules:  # All Abaqus CAE sessions immediately load caeModules
        _gui()
    else:
        parser = parsers.sphere_parser(basename=basename)
        try:
            args, unknown = parser.parse_known_args()
        except SystemExit as err:
            sys.exit(err.code)

        sys.exit(
            main(
                args.inner_radius,
                args.outer_radius,
                args.output_file,
                input_file=args.input_file,
                quadrant=args.quadrant,
                revolution_angle=args.revolution_angle,
                y_offset=args.y_offset,
                model_name=args.model_name,
                part_name=args.part_name,
            )
        )
