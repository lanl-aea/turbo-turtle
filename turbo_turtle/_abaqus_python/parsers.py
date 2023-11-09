"""Python 2/3 compatible parsers for use in both the Abaqus Python scripts and the Turbo-Turtle Python 3 wrappers

Content *must* be compatible with Python 2 and 3. Content should be limited to those things necessary to construct the
CLI parser(s). Other content, such as project/package settings type variables, can be included to minimize the required
``sys.path`` modifications required in the Abaqus Python package/scripts. For now, that means this file does double duty
as the Abaqus Python package settings file and the parsers file.
"""
import os
import argparse


def construct_prog(basename):
    """Construct the Abaqus Python usage string

    :param str basename: Abaqus Python script basename

    :returns: program usage string
    :rtype: str
    """
    prog = "abaqus cae -noGui {} --".format(basename)
    return prog


def create_parser(add_help, description, basename):
    """Handle the parser instantiation with or without the help message

    :param bool add_help: Use a parser with a help message when True
    :param str description: Description to add to a parser with a help message
    :param str basename: File basename to use in the usage string of a parser with a help message

    :returns: parser
    :rtype: argparse.ArgumentParser
    """
    if add_help:
        parser = argparse.ArgumentParser(description=description, prog=construct_prog(basename))
    else:
        parser = argparse.ArgumentParser(add_help=add_help)
    return parser


geometry_default_unit_conversion = 1.0
geometry_default_planar = False
geometry_default_euclidian_distance = 4.0
geometry_default_model_name = "Model-1"
geometry_default_part_name = [None]
geometry_default_delimiter = ","
geometry_default_header_lines = 0
geometry_default_revolution_angle = 360.0
geometry_cli_help = "Abaqus Python script for creating 2D or 3D part(s) from an x-y coordinate system input file(s)"
geometry_cli_description = "Create a 2D planar, 2D axisymmetric, or 3D body of revolution (about the global Y-Axis) by " \
                           "sketching lines and splines in the X-Y plane. Line and spline definitions are formed by " \
                           "parsing an input text file of points in X-Y space."

def geometry_parser(basename="_geometry.py", add_help=True, description=geometry_cli_description):

    parser = create_parser(add_help=add_help, description=description, basename=basename)

    parser.add_argument("--input-file", type=str, nargs="+", required=True,
                        help="Name of an input file(s) with points in x-y coordinate system")
    parser.add_argument("--unit-conversion", type=float, default=geometry_default_unit_conversion,
                        help="Unit conversion multiplication factor (default: %(default)s)")
    parser.add_argument("--euclidian_distance", type=float, default=geometry_default_euclidian_distance,
                        help="Connect points with a straight line is the distance between is larger than this (default: %(default)s)")
    parser.add_argument("--planar", action='store_true',
                        help="Switch to indicate that 2D model dimensionality is planar, not axisymmetric (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=geometry_default_model_name,
                        help="Abaqus model name in which to create the new part(s) (default: %(default)s)")
    parser.add_argument("--part-name", type=str, nargs="+", default=geometry_default_part_name,
                        help="Abaqus part name(s) (default: %(default)s)")
    parser.add_argument("--output-file", type=str, required=True,
                        help="Name of the output Abaqus CAE file to save (default: %(default)s)")
    parser.add_argument("--delimiter", type=str, default=geometry_default_delimiter,
                        help="Delimiter character between columns in the points file(s) (default: %(default)s)")
    parser.add_argument("--header-lines", type=int, default=geometry_default_header_lines,
                        help="Number of header lines to skip when parsing the points files(s) (default: %(default)s)")
    parser.add_argument("--revolution-angle", type=float, default=geometry_default_revolution_angle,
                        help="Revolution angle for a 3D part in degrees (default: %(default)s)")
    return parser


cylinder_default_part_name = "Part-1" 
cylinder_cli_help = "Accept dimensions of a right circular cylinder and generate an axisymmetric revolved geometry"
cylinder_cli_description = "Accept dimensions of a right circular cylinder and generate an axisymmetric revolved geometry"


def cylinder_parser(basename="_cylinder.py", add_help=True, description=cylinder_cli_description):

    parser = create_parser(add_help=add_help, description=description, basename=basename)

    parser.add_argument("--inner-radius", type=float, required=True,
                        help="Inner radius of hollow cylinder")
    parser.add_argument("--outer-radius", type=float, required=True,
                        help="Outer radius of cylinder")
    parser.add_argument("--height", type=float, required=True,
                        help="Height of the right circular cylinder")
    parser.add_argument("--output-file", type=str, required=True,
                        help="Name of the output Abaqus CAE file to save (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=geometry_default_model_name,
                        help="Abaqus model name in which to create the new part(s) (default: %(default)s)")
    parser.add_argument("--part-name", type=str, default=cylinder_default_part_name,
                        help="Abaqus part name(s) (default: %(default)s)")
    parser.add_argument("--revolution-angle", type=float, default=geometry_default_revolution_angle,
                        help="Revolution angle for a 3D part in degrees (default: %(default)s)")
    return parser


sphere_default_input_file = None
sphere_default_quadrant = "both"
sphere_default_angle = 360.
sphere_default_center = (0., 0.)
sphere_default_model_name = "Model-1"
sphere_default_part_name = "sphere"
sphere_cli_help = "Create a hollow, spherical geometry from a sketch in the X-Y plane"
sphere_cli_description = "Create a hollow, spherical geometry from a sketch in the X-Y plane with upper (+X+Y), " \
                         "lower (+X-Y), or both quadrants."


def sphere_parser(basename="_sphere.py", add_help=True, description=sphere_cli_description):

    parser = create_parser(add_help=add_help, description=description, basename=basename)

    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--inner-radius', type=float, required=True,
                               help="Inner radius (hollow size)")
    requiredNamed.add_argument('--outer-radius', type=float, required=True,
                               help="Outer radius (sphere size)")
    requiredNamed.add_argument('--output-file', type=str, required=True,
                               help="Abaqus model database to create")

    parser.add_argument('--input-file', type=str, default=sphere_default_input_file,
                        help="Abaqus model database to open (default: %(default)s)")
    parser.add_argument("--quadrant", type=str, choices=("both", "upper", "lower"), default=sphere_default_quadrant,
                        help="XY plane quadrant: both, upper (I), lower (IV) (default: %(default)s)")
    parser.add_argument('--angle', type=float, default=sphere_default_angle,
                        help="Angle of revolution about the +Y axis (default: %(default)s)")
    parser.add_argument('--center', nargs=2, type=float, default=sphere_default_center,
                        help="Center of the sphere (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default=sphere_default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument('--part-name', type=str, default=sphere_default_part_name,
                        help="Abaqus part name (default: %(default)s)")

    return parser


# TODO: These CLI lists will fail if a user tries to provide a negative number
partition_default_center = [0.0, 0.0, 0.0]
partition_default_xpoint = [1.0, 0.0, 0.0]
partition_default_zpoint = [0.0, 0.0, 1.0]
partition_default_plane_angle = 45.0
partition_default_partitions_x = [0.0, 0.0]
partition_default_partitions_y = [0.0, 0.0]
partition_default_partitions_z = [0.0, 0.0]
partition_cli_help = "Partition a spherical shape into a turtle shell"
partition_cli_description = "Partition a spherical shape into a turtle shell given a small number of locating parameters."


def partition_parser(basename="_partition.py", add_help=True, description=partition_cli_description):

    parser = create_parser(add_help=add_help, description=description, basename=basename)

    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--model-name', type=str, required=True,
                        help="Abaqus model name")
    requiredNamed.add_argument('--part-name', type=str, required=True,
                        help="Abaqus part name")
    requiredNamed.add_argument('--input-file', type=str, required=True,
                        help="Abaqus model database to open")

    parser.add_argument('--output-file', type=str, default=None,
                        help="Abaqus model database to save to. Defaults to the specified --input-file")
    parser.add_argument('--xpoint', nargs=3, type=float, default=partition_default_xpoint,
                        help="Point on the x-axis (default: %(default)s)")
    parser.add_argument('--center', nargs=3, type=float, default=partition_default_center,
                        help="Center of the sphere (default: %(default)s)")
    parser.add_argument('--zpoint', nargs=3, type=float, default=partition_default_zpoint,
                        help="Point on the z-axis (default: %(default)s)")
    parser.add_argument('--plane-angle', type=float, default=partition_default_plane_angle,
                        help="Angle for non-principal partitions (default: %(default)s)")
    parser.add_argument('--x-partitions', type=float, nargs='+', default=partition_default_partitions_x,
                        help="Create a partition offset from the x-principal-plane (default: %(default)s)")
    parser.add_argument('--y-partitions', type=float, nargs='+', default=partition_default_partitions_y,
                        help="Create a partition offset from the y-principal-plane (default: %(default)s)")
    parser.add_argument('--z-partitions', type=float, nargs='+', default=partition_default_partitions_z,
                        help="Create a partition offset from the z-principal-plane (default: %(default)s)")

    return parser


mesh_default_output_file = None
mesh_default_model_name = "Model-1"
mesh_default_part_name = "Part-1"
mesh_default_global_seed = 1.0
mesh_cli_help = "Mesh an Abaqus part from a global seed"
# TODO: Write a more descriptive behavior message
mesh_cli_description = "Mesh an Abaqus part from a global seed"


def mesh_parser(basename="_mesh.py", add_help=True, description=mesh_cli_description):

    parser = create_parser(add_help=add_help, description=description, basename=basename)

    parser.add_argument("--input-file", type=str, required=True,
                        help="Abaqus CAE input file")
    parser.add_argument("--element-type", type=str, required=True,
                        help="Abaqus element type")
    parser.add_argument("--output-file", type=str, default=mesh_default_output_file,
                        help="Abaqus CAE output file (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=mesh_default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument("--part-name", type=str, default=mesh_default_part_name,
                        help="Abaqus part name (default: %(default)s)")
    parser.add_argument("--global-seed", type=float, default=mesh_default_global_seed,
                        help="The global mesh seed size. Positive float.")

    return parser


export_default_model_name = "Model-1"
export_default_part_name = ["Part-1"]
export_default_element_type = [None]
export_default_destination = os.getcwd()
export_cli_help = "Export an Abaqus part mesh as an orphan mesh"
# TODO: Write a more descriptive behavior message
export_cli_description = "Export an Abaqus part mesh as an orphan mesh"


def export_parser(basename="_export.py", add_help=True, description=export_cli_description):

    parser = create_parser(add_help=add_help, description=description, basename=basename)

    parser.add_argument("--input-file", type=str, required=True,
                        help="Abaqus CAE input file")
    parser.add_argument("--model-name", type=str, default=export_default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument("--part-name", type=str, nargs='+', default=export_default_part_name,
                        help="List of Abaqus part names (default: %(default)s)")
    parser.add_argument("--element-type", type=str, nargs='+', default=export_default_element_type,
                        help="List of element types, one per part name or one global replacement for every part name " \
                             "(default: %(default)s)")
    parser.add_argument("--destination", type=str, default=export_default_destination,
                        help="Write orphan mesh files to this output directory (default: PWD)")

    return parser


image_default_x_angle = 0.
image_default_y_angle = 0.
image_default_z_angle = 0.
image_default_image_size = (1920, 1080)
image_default_model_name = "Model-1"
image_default_part_name = "Part-1"
image_cli_help = "Save an image of an Abaqus model"
image_cli_description = "Save an assembly view image (colored by material) for a given Abaqus input file"


def image_parser(basename="_image.py", add_help=True, description=image_cli_description):

    parser = create_parser(add_help=add_help, description=description, basename=basename)

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
                        help="Image size in pixels (X, Y) (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default=image_default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument('--part-name', type=str, default=image_default_part_name,
                        help="Abaqus part name (default: %(default)s)")

    return parser
