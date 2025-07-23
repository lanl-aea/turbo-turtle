import os
import sys
import inspect

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import parsers  # noqa: E402
from turbo_turtle_abaqus import vertices  # noqa: E402
from turbo_turtle_abaqus import geometry  # noqa: E402
from turbo_turtle_abaqus import _abaqus_utilities  # noqa: E402
from turbo_turtle_abaqus import _mixed_utilities  # noqa: E402
from turbo_turtle_abaqus import _mixed_settings  # noqa: E402


def main(
    inner_radius,
    outer_radius,
    height,
    output_file,
    model_name=parsers.geometry_defaults["model_name"],
    part_name=parsers.cylinder_defaults["part_name"],
    revolution_angle=parsers.geometry_defaults["revolution_angle"],
    y_offset=parsers.cylinder_defaults["y_offset"],
):
    """Accept dimensions of a right circular cylinder and generate an axisymmetric revolved geometry

    Centroid of cylinder is located on the global coordinate origin by default.

    :param float inner_radius: Radius of the hollow center
    :param float outer_radius: Outer radius of the cylinder
    :param float height: Height of the cylinder
    :param str output_file: Abaqus CAE database to save the part(s)
    :param str model_name: name of the Abaqus model in which to create the part
    :param list part_name: name(s) of the part(s) being created
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries
    :param float y_offset: vertical offset along the global Y-axis
    """
    import abaqus

    output_file = os.path.splitext(output_file)[0] + ".cae"
    try:
        cylinder(inner_radius, outer_radius, height, y_offset, model_name, part_name, revolution_angle)
    except RuntimeError as err:
        _mixed_utilities.sys_exit(str(err))
    abaqus.mdb.saveAs(pathName=output_file)


def cylinder(inner_radius, outer_radius, height, y_offset, model_name, part_name, revolution_angle):
    """Accept dimensions of a right circular cylinder and generate an axisymmetric revolved geometry

    This function drives the geometry creation of a cylinder whose axis of symmetry is located on the global coordinate
    origin by default, and always on the global Y-axis.

    :param float inner_radius: Radius of the hollow center
    :param float outer_radius: Outer radius of the cylinder
    :param float height: Height of the cylinder
    :param float y_offset: vertical offset along the global Y-axis
    :param str model_name: name of the Abaqus model in which to create the part
    :param list part_name: name(s) of the part(s) being created
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries
    """
    _abaqus_utilities._conditionally_create_model(model_name)

    lines = vertices.cylinder_lines(inner_radius, outer_radius, height, y_offset)
    geometry.draw_part_from_splines(
        lines, [], planar=False, model_name=model_name, part_name=part_name, revolution_angle=revolution_angle
    )


def _gui_get_inputs():
    """Interactive Inputs

    Prompt the user for inputs with this interactive data entry function. When called, this function opens an Abaqus CAE
    GUI window with text boxes to enter the values given below. Note to developers - if you update this 'GUI-INPUTS'
    below, also update ``_mixed_settings._cylinder_gui_help_string`` that gets used as the GUI ``label``.

    GUI-INPUTS
    ==========
    * Part Name - part name for the cylinder being created.
    * Model Name - parts will be created in a new model with this name
    * Inner Radius - inner radius of the cylinder
    * Outer Radius - outer radius of the cylinder
    * Height - height of the cylinder
    * Revolution Angle - revolution angle for a 3D part in degrees
    * Y-Offset - offset along the global y-axis

    **IMPORTANT** - this function must return key-value pairs that will successfully unpack as ``**kwargs`` in
    ``cylinder``

    :return: ``user_inputs`` - a dictionary of the following key-value pair types:

    * ``part_name``: ``str`` type, part name of the cylinder
    * ``model_name``: ``str`` type, new model containing the part generated from the input file(s)
    * ``inner_radius``: ``float`` type, inner radius of the cylinder
    * ``outer_radius``: ``float`` type, outer radius of the cylinder
    * ``height``: ``float`` type, height of the cylinder
    * ``revolution_angle``: ``float`` type, revolution angle in degrees for 3D geometry
    * ``y_offset``: ``float`` type, offset along the y-axis

    :raises RuntimeError: if inner radius, outer radius, or height are not specified.
    """
    import abaqus

    fields = (
        ("Part Name:", parsers.cylinder_defaults["part_name"]),
        ("Model Name:", parsers.geometry_defaults["model_name"]),
        ("Inner Radius:", ""),
        ("Outer Radius:", ""),
        ("Height:", ""),
        ("Revolution Angle:", str(parsers.geometry_defaults["revolution_angle"])),
        ("Y-Offset:", str(parsers.cylinder_defaults["y_offset"])),
    )

    part_name, model_name, inner_radius, outer_radius, height, revolution_angle, y_offset = abaqus.getInputs(
        dialogTitle="Turbo Turtle Cylinder",
        label=_mixed_settings._cylinder_gui_help_string,
        fields=fields,
    )

    if part_name is not None:  # Will be None if the user hits the "cancel/esc" button
        if not inner_radius or not outer_radius or not height:
            error_message = "Error: You must specify an inner and outer radius and a height for the cylinder"
            raise RuntimeError(error_message)

        user_inputs = {
            "inner_radius": float(inner_radius),
            "outer_radius": float(outer_radius),
            "height": float(height),
            "y_offset": float(y_offset),
            "model_name": model_name,
            "part_name": part_name,
            "revolution_angle": float(revolution_angle),
        }
    else:
        user_inputs = {}
    return user_inputs


def _gui():
    """Function with no inputs required for driving the plugin"""
    _abaqus_utilities.gui_wrapper(
        inputs_function=_gui_get_inputs, subcommand_function=cylinder, post_action_function=_abaqus_utilities._view_part
    )


if __name__ == "__main__":
    if "caeModules" in sys.modules:  # All Abaqus CAE sessions immediately load caeModules
        _gui()
    else:
        parser = parsers.cylinder_parser(basename=basename)
        try:
            args, unknown = parser.parse_known_args()
        except SystemExit as err:
            sys.exit(err.code)

        sys.exit(
            main(
                inner_radius=args.inner_radius,
                outer_radius=args.outer_radius,
                height=args.height,
                output_file=args.output_file,
                model_name=args.model_name,
                part_name=args.part_name,
                revolution_angle=args.revolution_angle,
                y_offset=args.y_offset,
            )
        )
