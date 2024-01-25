"""Python 2/3 compatible parsers for use in both Abaqus Python scripts and Turbo-Turtle Python 3 modules

Content *must* be compatible with Python 2 and 3. Content should be limited to those things necessary to construct the
CLI parser(s). Other content, such as project/package settings type variables, can be included to minimize the required
``sys.path`` modifications required in the Abaqus Python package/scripts. For now, that means this file does double duty
as the Abaqus Python package settings file and the parsers file.
"""
import os
import argparse


def positive_float(argument):
    """Type function for argparse - positive floats

    Abaqus Python 2 and Python 3 compatible argparse type method:
    https://docs.python.org/3.8/library/argparse.html#type.

    :param str argument: string argument from argparse

    :returns: argument
    :rtype: float
    """
    MINIMUM_VALUE = 0.0
    try:
        argument = float(argument)
    except ValueError:
        raise argparse.ArgumentTypeError("invalid float value: '{}'".format(argument))
    if not argument >= MINIMUM_VALUE:
        raise argparse.ArgumentTypeError("invalid positive float: '{}'".format(argument))
    return argument


def construct_prog(basename):
    """Construct the Abaqus Python usage string

    :param str basename: Abaqus Python script basename

    :returns: program usage string
    :rtype: str
    """
    prog = "abaqus cae -noGui {} --".format(basename)
    return prog


geometry_default_unit_conversion = 1.0
geometry_default_planar = False
geometry_default_euclidean_distance = 4.0
geometry_default_model_name = "Model-1"
geometry_default_part_name = [None]
geometry_default_delimiter = ","
geometry_default_header_lines = 0
geometry_default_revolution_angle = 360.0
geometry_default_y_offset = 0.
geometry_default_rtol = None
geometry_default_atol = None
geometry_cli_help = "Create 2D or 3D part(s) from XY coordinate list input file(s)"
geometry_cli_description = "Create a 2D planar, 2D axisymmetric, or 3D body of revolution (about the global Y-Axis) by " \
                           "sketching lines and splines in the XY plane. Line and spline definitions are formed by " \
                           "parsing an input file with [N, 2] array of XY coordinates."

def geometry_parser(basename="geometry.py", add_help=True, description=geometry_cli_description, cubit=False):
    """Return the geometry subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str sphere_cli_description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface
    :param bool cubit: Include the Cubit specific options and help language when True

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """
    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = "or Cubit volume name(s). Cubit implementation converts hyphens to underscores for " \
                               "ACIS compatibility. "
    part_name_help = "Abaqus part name(s) {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    parser.add_argument("--input-file", type=str, nargs="+", required=True,
                        help="Name of an input file(s) with points in x-y coordinate system")
    parser.add_argument("--unit-conversion", type=positive_float, default=geometry_default_unit_conversion,
                        help="Unit conversion multiplication factor (default: %(default)s)")
    parser.add_argument("--euclidean-distance", type=positive_float, default=geometry_default_euclidean_distance,
                        help="Connect points with a straight line if the distance between them is larger than this " \
                             "in units *after* the unit conversion (default: %(default)s)")
    parser.add_argument("--planar", action='store_true',
                        help="Switch to indicate that 2D model dimensionality is planar, not axisymmetric " \
                             "(default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=geometry_default_model_name,
                        help="Abaqus model name in which to create the new part(s) (default: %(default)s)")
    parser.add_argument("--part-name", type=str, nargs="+", default=geometry_default_part_name,
                        help=part_name_help)
    parser.add_argument("--output-file", type=str, required=True,
                        help="Name of the output Abaqus CAE file to save (default: %(default)s)")
    parser.add_argument("--delimiter", type=str, default=geometry_default_delimiter,
                        help="Delimiter character between columns in the points file(s) (default: %(default)s)")
    parser.add_argument("--header-lines", type=int, default=geometry_default_header_lines,
                        help="Number of header lines to skip when parsing the points files(s) (default: %(default)s)")
    parser.add_argument("--revolution-angle", type=float, default=geometry_default_revolution_angle,
                        help="Revolution angle for a 3D part in degrees (default: %(default)s)")
    parser.add_argument("--y-offset", type=float, default=geometry_default_y_offset,
                        help="Offset along the global Y-axis in units *after* the unit conversion (default: %(default)s)")
    parser.add_argument("--rtol", type=float, default=geometry_default_rtol,
                        help="relative tolerance used by ``numpy.isclose``. If not provided, use numpy defaults " \
                             "(default: %(default)s)")
    parser.add_argument("--atol", type=float, default=geometry_default_atol,
                        help="absolute tolerance used by ``numpy.isclose``. If not provided, use numpy defaults " \
                             "(default: %(default)s)")
    return parser


cylinder_default_part_name = "Part-1"
cylinder_default_y_offset = 0.
cylinder_cli_help = "Accept dimensions of a right circular cylinder and generate an axisymmetric revolved geometry"
cylinder_cli_description = "Accept dimensions of a right circular cylinder and generate an axisymmetric revolved " \
                           "geometry."


def cylinder_parser(basename="cylinder.py", add_help=True, description=cylinder_cli_description, cubit=False):
    """Return the cylinder subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str sphere_cli_description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface
    :param bool cubit: Include the Cubit specific options and help language when True

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """

    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = "or Cubit volume name. Cubit implementation converts hyphens to underscores for " \
                               "ACIS compatibility. "
    part_name_help = "Abaqus part name {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    parser.add_argument("--inner-radius", type=positive_float, required=True,
                        help="Inner radius of hollow cylinder")
    parser.add_argument("--outer-radius", type=positive_float, required=True,
                        help="Outer radius of cylinder")
    parser.add_argument("--height", type=positive_float, required=True,
                        help="Height of the right circular cylinder")
    parser.add_argument("--output-file", type=str, required=True,
                        help="Name of the output Abaqus CAE file to save (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=geometry_default_model_name,
                        help="Abaqus model name in which to create the new part(s) (default: %(default)s)")
    parser.add_argument("--part-name", type=str, default=cylinder_default_part_name,
                        help=part_name_help)
    parser.add_argument("--revolution-angle", type=float, default=geometry_default_revolution_angle,
                        help="Revolution angle for a 3D part in degrees (default: %(default)s)")
    parser.add_argument("--y-offset", type=float, default=cylinder_default_y_offset,
                        help="Offset along the global Y-axis (default: %(default)s)")
    return parser


sphere_default_input_file = None
sphere_default_quadrant = "both"
sphere_default_revolution_angle = 360.
sphere_default_y_offset = 0.
sphere_default_center = (0., sphere_default_y_offset)
sphere_default_model_name = "Model-1"
sphere_default_part_name = "Part-1"
sphere_quadrant_options = ["both", "upper", "lower"]
sphere_cli_help = "Create a hollow, spherical geometry from a sketch in the X-Y plane"
sphere_cli_description = "Create a hollow, spherical geometry from a sketch in the X-Y plane with upper (+X+Y), " \
                         "lower (+X-Y), or both quadrants."


def sphere_parser(basename="sphere.py", add_help=True, description=sphere_cli_description, cubit=False):
    """Return the sphere subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str sphere_cli_description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface
    :param bool cubit: Include the Cubit specific options and help language when True

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """

    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = "or Cubit volume name. Cubit implementation converts hyphens to underscores for " \
                               "ACIS compatibility. "
    part_name_help = "Abaqus part name {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--inner-radius', type=positive_float, required=True,
                               help="Inner radius (hollow size)")
    requiredNamed.add_argument('--outer-radius', type=positive_float, required=True,
                               help="Outer radius (sphere size)")
    requiredNamed.add_argument('--output-file', type=str, required=True,
                               help="Abaqus model database to create")

    parser.add_argument('--input-file', type=str, default=sphere_default_input_file,
                        help="Abaqus model database to open (default: %(default)s)")
    parser.add_argument("--quadrant", type=str, choices=sphere_quadrant_options, default=sphere_default_quadrant,
                        help="XY plane quadrant: both, upper (I), lower (IV) (default: %(default)s)")
    parser.add_argument('--revolution-angle', type=float, default=sphere_default_revolution_angle,
                        help="Angle of revolution about the +Y axis (default: %(default)s)")
    parser.add_argument('--y-offset', type=float, default=sphere_default_y_offset,
                        help="Offset along the global Y-axis (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default=sphere_default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument('--part-name', type=str, default=sphere_default_part_name,
                        help=part_name_help)

    return parser


# TODO: These CLI lists will fail if a user tries to provide a negative number
partition_default_output_file = None
partition_default_center = [0.0, 0.0, 0.0]
partition_default_xvector = [1.0, 0.0, 0.0]
partition_default_zvector = [0.0, 0.0, 1.0]
partition_default_model_name = "Model-1"
partition_default_part_name = ["Part-1"]
partition_default_big_number = 1e6
partition_cli_help = "Partition hollow spheres into a turtle shell"
partition_cli_description = "Partition hollow spheres into a turtle shell given a small number of locating, " \
                            "clocking, and partition plane angle parameters."


def partition_parser(basename="partition.py", add_help=True, description=partition_cli_description, cubit=False):
    """Return the partition subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str sphere_cli_description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface
    :param bool cubit: Include the Cubit specific options and help language when True

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """

    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = "or Cubit volume name. Cubit implementation converts hyphens to underscores for " \
                               "ACIS compatibility. "
    part_name_help = "Abaqus part name {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--input-file', type=str, default=sphere_default_input_file,
                               help="Abaqus model database to open (default: %(default)s)")

    parser.add_argument('--output-file', type=str, default=partition_default_output_file,
                        help="Abaqus model database to save to. Defaults to the specified --input-file")
    parser.add_argument('--center', nargs=3, type=float, default=partition_default_center,
                        help="Center of the sphere (default: %(default)s)")
    parser.add_argument('--xvector', nargs=3, type=float, default=partition_default_xvector,
                        help="Local x-axis vector defined in global coordinates (default: %(default)s)")
    parser.add_argument('--zvector', nargs=3, type=float, default=partition_default_zvector,
                        help="Local z-axis vector defined in global coordinates (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default=partition_default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument('--part-name', type=str, nargs='+', default=partition_default_part_name,
                        help=part_name_help)
    parser.add_argument('--big-number', type=float, default=partition_default_big_number,
                        help="Number larger than the outer radius of the part to partition (default: %(default)s)")

    return parser


mesh_default_output_file = None
mesh_default_model_name = "Model-1"
mesh_default_part_name = "Part-1"
mesh_default_global_seed = 1.0
mesh_cli_help = "Mesh an Abaqus part from a global seed"
# TODO: Write a more descriptive behavior message
mesh_cli_description = "Mesh an Abaqus part from a global seed"


def mesh_parser(basename="mesh.py", add_help=True, description=mesh_cli_description, cubit=False):
    """Return the mesh subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str sphere_cli_description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """

    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = "or Cubit volume name. Cubit implementation converts hyphens to underscores for " \
                               "ACIS compatibility. "
    part_name_help = "Abaqus part name {}(default: %(default)s)".format(part_name_help_cubit)

    element_type_help_cubit = ""
    if cubit:
        element_type_help_cubit = ". Applied as a Cubit meshing scheme if it matches 'tetmesh' or 'trimesh'. " \
                                  "Otherwise ignored by Cubit implementation."
    element_type_help = "Abaqus element type{}".format(element_type_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    parser.add_argument("--input-file", type=str, required=True,
                        help="Abaqus CAE input file")
    parser.add_argument("--element-type", type=str, required=True,
                        help=element_type_help)
    parser.add_argument("--output-file", type=str, default=mesh_default_output_file,
                        help="Abaqus CAE output file (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=mesh_default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument("--part-name", type=str, default=mesh_default_part_name,
                        help=part_name_help)
    parser.add_argument("--global-seed", type=positive_float, default=mesh_default_global_seed,
                        help="The global mesh seed size. Positive float.")

    return parser


merge_cli_help = "Merge parts from multiple Abaqus CAE files into a single model"
merge_cli_description = "Supply multiple Abaqus CAE files, model names, and part names to merge the parts into a " \
                        "new model. Every CAE file is searched for every model/part name combination. If a part name " \
                        "is found in more than one model, return an error."
merge_default_merged_model_name = "Model-1"
merge_default_model_name = [None]
merge_default_part_name = [None]


def merge_parser(basename="merge.py", add_help=True, description=merge_cli_description, cubit=False):
    """Return the merge subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str sphere_cli_description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """
    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = ". Unused by Cubit implementation. "
    part_name_help = "Abaqus part name(s) to search for within model(s){} (default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    parser.add_argument("--input-file", type=str, nargs="+", required=True,
                        help="Abaqus CAE input file(s)")
    parser.add_argument("--output-file", type=str, required=True,
                        help="Abaqus CAE file to save the merged model")
    parser.add_argument("--merged-model-name", type=str, default=merge_default_merged_model_name,
                        help="Model to create and merge parts into (default: %(default)s)")
    parser.add_argument("--model-name", type=str, nargs="+", default=merge_default_model_name,
                        help="Abaqus model name(s) to query in the input CAE file(s) (default: %(default)s)")
    parser.add_argument("--part-name", type=str, nargs="+", default=merge_default_part_name,
                        help=part_name_help)
    return parser


export_default_model_name = "Model-1"
export_default_part_name = ["Part-1"]
export_default_element_type = [None]
export_default_destination = os.getcwd()
export_default_assembly = None
export_output_type_choices = ["abaqus", "genesis", "genesis-normal", "genesis-hdf5"]
export_default_output_type = export_output_type_choices[0]
export_cli_help = "Export an Abaqus part mesh as an orphan mesh"
# TODO: Write a more descriptive behavior message
export_cli_description = "Export an Abaqus part mesh as an orphan mesh"


def export_parser(basename="export.py", add_help=True, description=export_cli_description, cubit=False):
    """Return the export subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str sphere_cli_description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """
    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = "or Cubit volume name(s). Cubit implementation converts hyphens to underscores for " \
                               "ACIS compatibility. "
    part_name_help = "Abaqus part name(s) {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    parser.add_argument("--input-file", type=str, required=True,
                        help="Abaqus CAE input file")
    parser.add_argument("--model-name", type=str, default=export_default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument("--part-name", type=str, nargs='+', default=export_default_part_name,
                        help=part_name_help)
    parser.add_argument("--element-type", type=str, nargs='+', default=export_default_element_type,
                        help="List of element types, one per part name or one global replacement for every part name " \
                             "(default: %(default)s)")
    parser.add_argument("--destination", type=str, default=export_default_destination,
                        help="Write orphan mesh files to this output directory (default: PWD)")
    parser.add_argument("--assembly", type=str, default=export_default_assembly,
                        help="Assembly file for exporting the assembly keyword block. If a file is provided, but no " \
                             "assembly instances are found, instance all provided part names and export assembly " \
                             "block (default: %(default)s)")
    if cubit:
        parser.add_argument("--output-type", choices=export_output_type_choices, default=export_default_output_type,
                            help="Cubit output type. When 'abaqus' is selected, each part name is exported as an  " \
                                 "orphan mesh to a ``part_name``.inp file. When 'genesis' is selected all blocks " \
                                 "are output to a single file ``input_file``.g (default: %(default)s)")

    return parser


image_default_x_angle = 0.
image_default_y_angle = 0.
image_default_z_angle = 0.
image_default_image_size = [1920, 1080]
image_default_model_name = "Model-1"
image_default_part_name = None
image_cli_help = "Save an image of an Abaqus model"
image_cli_description = "Save a part or assembly view image for a given Abaqus input file"
# One time dump from session.viewports['Viewport: 1'].colorMappings.keys()) to stay Python 3 compatible
image_color_map_choices = [
    'Material', 'Section', 'Composite layup', 'Composite ply', 'Part', 'Part instance',
    'Element set', 'Averaging region', 'Element type', 'Default', 'Assembly', 'Part geometry', 'Load', 'Boundary condition',
    'Interaction', 'Constraint', 'Property', 'Meshability', 'Instance type', 'Set', 'Surface', 'Internal set',
    'Internal surface', 'Display group', 'Selection group', 'Skin', 'Stringer', 'Cell', 'Face'
]


def image_parser(basename="image.py", add_help=True, description=image_cli_description, cubit=False):
    """Return the image subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str sphere_cli_description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """
    help_cubit = ""
    if cubit:
        help_cubit = ". Unused by Cubit implementation."
    model_name_help = "Abaqus model name{} (default: %(default)s)".format(help_cubit)
    part_name_help = "Abaqus part name{} (default: %(default)s)".format(help_cubit)
    color_map_help = "Color map{} (default: %(default)s)".format(help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    parser.add_argument('--input-file', type=str, required=True,
                         help='Abaqus input file. Supports ``*.inp`` and ``*.cae``.')
    parser.add_argument('--output-file', type=str, required=True,
                        help='Output image from the Abaqus viewport. Supports ``*.png`` and ``*.svg``.')
    parser.add_argument('--x-angle', type=float, default=image_default_x_angle,
                        help='Viewer rotation about X-axis in degrees (default: %(default)s)')
    parser.add_argument('--y-angle', type=float, default=image_default_y_angle,
                        help='Viewer rotation about Y-axis in degrees (default: %(default)s)')
    parser.add_argument('--z-angle', type=float, default=image_default_z_angle,
                        help='Viewer rotation about Z-axis in degrees (default: %(default)s)')
    parser.add_argument('--image-size', nargs=2, type=int, default=image_default_image_size,
                        help="Image size in pixels (width, height) (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default=image_default_model_name,
                        help=model_name_help)
    parser.add_argument('--part-name', type=str, default=image_default_part_name,
                        help=part_name_help)
    parser.add_argument('--color-map', type=str, choices=image_color_map_choices, default=image_color_map_choices[0],
                        help=color_map_help)
    return parser
