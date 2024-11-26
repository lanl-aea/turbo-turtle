"""Python 2/3 compatible parsers for use in both Abaqus Python scripts and Turbo-Turtle Python 3 modules

Content *must* be compatible with Python 2 and 3. Content should be limited to those things necessary to construct the
CLI parser(s). Other content, such as project/package settings type variables, can be included to minimize the required
``sys.path`` modifications required in the Abaqus Python package/scripts. For now, that means this file does double duty
as the Abaqus Python package settings file and the parsers file.
"""

import os
import copy
import argparse


def positive_float(argument):
    """Type function for argparse - positive floats including zero

    Abaqus Python 2 and Python 3 compatible argparse type method:
    https://docs.python.org/3.9/library/argparse.html#type.

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


def positive_int(argument):
    """Type function for argparse - positive integers including zero

    Abaqus Python 2 and Python 3 compatible argparse type method:
    https://docs.python.org/3.9/library/argparse.html#type.

    :param str argument: string argument from argparse

    :returns: argument
    :rtype: int
    """
    MINIMUM_VALUE = 0
    try:
        argument = int(argument)
    except ValueError:
        raise argparse.ArgumentTypeError("invalid integer value: '{}'".format(argument))
    if not argument >= MINIMUM_VALUE:
        raise argparse.ArgumentTypeError("invalid positive integer: '{}'".format(argument))
    return argument


def construct_prog(basename):
    """Construct the Abaqus Python usage string

    :param str basename: Abaqus Python script basename

    :returns: program usage string
    :rtype: str
    """
    prog = "abaqus cae -noGui {} --".format(basename)
    return prog


geometry_defaults = {
    "unit_conversion": 1.0,
    "planar": False,
    "euclidean_distance": 4.0,
    "model_name": "Model-1",
    "part_name": [None],
    "delimiter": ",",
    "header_lines": 0,
    "revolution_angle": 360.0,
    "y_offset": 0.0,
    "rtol": None,
    "atol": None,
}
geometry_cli_help = "Create 2D or 3D part(s) from XY coordinate list input file(s)"
geometry_cli_description = (
    "Create a 2D planar, 2D axisymmetric, or 3D body of revolution (about the global Y-Axis) "
    "by sketching lines and splines in the XY plane. Line and spline definitions are formed "
    "by parsing an input file with [N, 2] array of XY coordinates."
)


def geometry_parser(basename="geometry.py", add_help=True, description=geometry_cli_description, cubit=False):
    """Return the geometry subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface
    :param bool cubit: Include the Cubit specific options and help language when True

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """
    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = (
            "or Cubit volume name(s). Cubit implementation converts hyphens to underscores for " "ACIS compatibility. "
        )
    part_name_help = "Part name(s) {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--input-file",
        type=str,
        nargs="+",
        required=True,
        help="Name of an input file(s) with points in x-y coordinate system",
    )
    required.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Name of the output model database file to save",
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--unit-conversion",
        type=positive_float,
        default=geometry_defaults["unit_conversion"],
        help="Unit conversion multiplication factor (default: %(default)s)",
    )
    optional.add_argument(
        "--euclidean-distance",
        type=positive_float,
        default=geometry_defaults["euclidean_distance"],
        # fmt: off
        help="Connect points with a straight line if the distance between them is larger than this "
             "in units *after* the unit conversion (default: %(default)s)",
        # fmt: on
    )
    optional.add_argument(
        "--planar",
        action="store_true",
        help="Switch to indicate that 2D model dimensionality is planar, not axisymmetric " "(default: %(default)s)",
    )
    optional.add_argument(
        "--model-name",
        type=str,
        default=geometry_defaults["model_name"],
        help="Model name in which to create the new part(s) (default: %(default)s)",
    )
    optional.add_argument(
        "--part-name",
        type=str,
        nargs="+",
        default=geometry_defaults["part_name"],
        help=part_name_help,
    )
    optional.add_argument(
        "--delimiter",
        type=str,
        default=geometry_defaults["delimiter"],
        help="Delimiter character between columns in the points file(s) (default: %(default)s)",
    )
    optional.add_argument(
        "--header-lines",
        type=positive_int,
        default=geometry_defaults["header_lines"],
        help="Number of header lines to skip when parsing the points files(s) (default: %(default)s)",
    )
    optional.add_argument(
        "--revolution-angle",
        type=float,
        default=geometry_defaults["revolution_angle"],
        help="Revolution angle for a 3D part in degrees (default: %(default)s)",
    )
    optional.add_argument(
        "--y-offset",
        type=float,
        default=geometry_defaults["y_offset"],
        help="Offset along the global Y-axis in units *after* the unit conversion (default: %(default)s)",
    )
    optional.add_argument(
        "--rtol",
        type=positive_float,
        default=geometry_defaults["rtol"],
        # fmt: off
        help="relative tolerance used by ``numpy.isclose``. If not provided, use numpy defaults "
             "(default: %(default)s)",
        # fmt: on
    )
    optional.add_argument(
        "--atol",
        type=positive_float,
        default=geometry_defaults["atol"],
        # fmt: off
        help="absolute tolerance used by ``numpy.isclose``. If not provided, use numpy defaults "
             "(default: %(default)s)",
        # fmt: on
    )
    return parser


geometry_xyplot_defaults = copy.deepcopy(geometry_defaults)
geometry_xyplot_defaults.update({"no_markers": False, "annotate": False, "scale": False})


cylinder_defaults = {
    "part_name": "Part-1",
    "y_offset": 0.0,
}
cylinder_cli_help = "Accept dimensions of a right circular cylinder and generate an axisymmetric revolved geometry"
cylinder_cli_description = (
    "Accept dimensions of a right circular cylinder and generate an axisymmetric revolved " "geometry."
)


def cylinder_parser(basename="cylinder.py", add_help=True, description=cylinder_cli_description, cubit=False):
    """Return the cylinder subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface
    :param bool cubit: Include the Cubit specific options and help language when True

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """

    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = (
            "or Cubit volume name. Cubit implementation converts hyphens to underscores for " "ACIS compatibility. "
        )
    part_name_help = "Part name {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--inner-radius",
        type=positive_float,
        required=True,
        help="Inner radius of hollow cylinder",
    )
    required.add_argument(
        "--outer-radius",
        type=positive_float,
        required=True,
        help="Outer radius of cylinder",
    )
    required.add_argument(
        "--height",
        type=positive_float,
        required=True,
        help="Height of the right circular cylinder",
    )
    required.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Name of the output model database file to save",
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--model-name",
        type=str,
        default=geometry_defaults["model_name"],
        help="Model name in which to create the new part(s) (default: %(default)s)",
    )
    optional.add_argument(
        "--part-name",
        type=str,
        default=cylinder_defaults["part_name"],
        help=part_name_help,
    )
    optional.add_argument(
        "--revolution-angle",
        type=float,
        default=geometry_defaults["revolution_angle"],
        help="Revolution angle for a 3D part in degrees (default: %(default)s)",
    )
    optional.add_argument(
        "--y-offset",
        type=float,
        default=cylinder_defaults["y_offset"],
        help="Offset along the global Y-axis (default: %(default)s)",
    )
    return parser


sphere_defaults = {
    "input_file": None,
    "quadrant": "both",
    "revolution_angle": 360.0,
    "y_offset": 0.0,
    "model_name": "Model-1",
    "part_name": "Part-1",
}
sphere_defaults["center"] = (0.0, sphere_defaults["y_offset"])
sphere_quadrant_options = ["both", "upper", "lower"]
sphere_cli_help = "Create a hollow, spherical geometry from a sketch in the X-Y plane"
sphere_cli_description = (
    "Create a hollow, spherical geometry from a sketch in the X-Y plane with upper (+X+Y), "
    "lower (+X-Y), or both quadrants."
)


def sphere_parser(basename="sphere.py", add_help=True, description=sphere_cli_description, cubit=False):
    """Return the sphere subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface
    :param bool cubit: Include the Cubit specific options and help language when True

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """

    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = (
            "or Cubit volume name. Cubit implementation converts hyphens to underscores for " "ACIS compatibility. "
        )
    part_name_help = "Part name {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--inner-radius",
        type=positive_float,
        required=True,
        help="Inner radius (hollow size)",
    )
    required.add_argument(
        "--outer-radius",
        type=positive_float,
        required=True,
        help="Outer radius (sphere size)",
    )
    required.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Model database to create",
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--input-file",
        type=str,
        default=sphere_defaults["input_file"],
        help="Model database to open (default: %(default)s)",
    )
    optional.add_argument(
        "--quadrant",
        type=str,
        choices=sphere_quadrant_options,
        default=sphere_defaults["quadrant"],
        help="XY plane quadrant: both, upper (I), lower (IV) (default: %(default)s)",
    )
    optional.add_argument(
        "--revolution-angle",
        type=float,
        default=sphere_defaults["revolution_angle"],
        help="Angle of revolution about the +Y axis (default: %(default)s)",
    )
    optional.add_argument(
        "--y-offset",
        type=float,
        default=sphere_defaults["y_offset"],
        help="Offset along the global Y-axis (default: %(default)s)",
    )
    optional.add_argument(
        "--model-name",
        type=str,
        default=sphere_defaults["model_name"],
        help="Model name (default: %(default)s)",
    )
    optional.add_argument(
        "--part-name",
        type=str,
        default=sphere_defaults["part_name"],
        help=part_name_help,
    )

    return parser


# TODO: These CLI lists will fail if a user tries to provide a negative number
partition_defaults = {
    "output_file": None,
    "center": [0.0, 0.0, 0.0],
    "xvector": [1.0, 0.0, 0.0],
    "zvector": [0.0, 0.0, 1.0],
    "model_name": "Model-1",
    "part_name": ["Part-1"],
    "big_number": 1e6,
}
partition_cli_help = "Partition hollow spheres into a turtle shell"
partition_cli_description = (
    "Partition hollow spheres into a turtle shell given a small number of locating, "
    "clocking, and partition plane angle parameters."
)


def partition_parser(basename="partition.py", add_help=True, description=partition_cli_description, cubit=False):
    """Return the partition subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface
    :param bool cubit: Include the Cubit specific options and help language when True

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """

    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = (
            "or Cubit volume name. Cubit implementation converts hyphens to underscores for " "ACIS compatibility. "
        )
    part_name_help = "Part name {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Model database to open (default: %(default)s)",
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--output-file",
        type=str,
        default=partition_defaults["output_file"],
        help="Model database to save to. Defaults to the specified --input-file",
    )
    optional.add_argument(
        "--center",
        nargs=3,
        type=float,
        default=partition_defaults["center"],
        help="Center of the sphere (default: %(default)s)",
    )
    optional.add_argument(
        "--xvector",
        nargs=3,
        type=float,
        default=partition_defaults["xvector"],
        help="Local x-axis vector defined in global coordinates (default: %(default)s)",
    )
    optional.add_argument(
        "--zvector",
        nargs=3,
        type=float,
        default=partition_defaults["zvector"],
        help="Local z-axis vector defined in global coordinates (default: %(default)s)",
    )
    optional.add_argument(
        "--model-name",
        type=str,
        default=partition_defaults["model_name"],
        help="Model name (default: %(default)s)",
    )
    optional.add_argument(
        "--part-name",
        type=str,
        nargs="+",
        default=partition_defaults["part_name"],
        help=part_name_help,
    )
    optional.add_argument(
        "--big-number",
        type=positive_float,
        default=partition_defaults["big_number"],
        help="Number larger than the outer radius of the part to partition (default: %(default)s)",
    )

    return parser


sets_defaults = {
    "face_sets": None,
    "edge_sets": None,
    "vertex_sets": None,
    "output_file": None,
    "model_name": "Model-1",
    "part_name": "Part-1",
}
sets_cli_help = "Create geometric sets from mask strings"
sets_cli_description = (
    "Create geometric sets from mask strings. Primarly intended for use in scripted workflows with stable geometry "
    "creation order and features because masks are fragile with respect to geometric changes. The recommended "
    "workflow is to perform manual set creation on a nominal geometry model, record the set masks/IDs reported by "
    "the third-party software, and write the CLI options into a scripted workflow file. Abaqus reports CAE "
    "operations in the ``abaqus.rpy`` replay file, e.g. ``grep -A 1 'mask=' abaqus.rpy``. Cubit IDs can be found in "
    "the model tree."
)


def sets_parser(basename="sets.py", add_help=True, description=sets_cli_description, cubit=False):
    """Return the sets subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """
    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = "unused by Cubit implementation."
    part_name_help = "Part name {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Model database input file",
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--output-file",
        type=str,
        default=sets_defaults["output_file"],
        help="Model database output file (default: %(default)s)",
    )
    optional.add_argument(
        "--model-name",
        type=str,
        default=sets_defaults["model_name"],
        help="Model name (default: %(default)s)",
    )
    optional.add_argument(
        "--part-name",
        type=str,
        default=sets_defaults["part_name"],
        help=part_name_help,
    )
    optional.add_argument(
        "--face-set",
        dest="face_sets",
        action="append",
        nargs=2,
        metavar=("name", "mask"),
        default=sets_defaults["face_sets"],
        help="Face (surface) set (name, mask) pairs. Repeat once per set (default: %(default)s)",
    )
    optional.add_argument(
        "--edge-set",
        dest="edge_sets",
        action="append",
        nargs=2,
        metavar=("name", "mask"),
        default=sets_defaults["edge_sets"],
        help="Edge set (name, mask) pairs. Repeat once per set (default: %(default)s)",
    )
    optional.add_argument(
        "--vertex-set",
        dest="vertex_sets",
        action="append",
        nargs=2,
        metavar=("name", "mask"),
        default=sets_defaults["vertex_sets"],
        help="Vertex set (name, mask) pairs. Repeat once per set (default: %(default)s)",
    )

    return parser


mesh_defaults = {
    "output_file": None,
    "model_name": "Model-1",
    "part_name": "Part-1",
    "global_seed": 1.0,
    "edge_seeds": None,
}
mesh_cli_help = "Mesh a part from a global seed and optional edge seeds"
# TODO: Write a more descriptive behavior message
mesh_cli_description = (
    "Mesh a part from a global seed and optional edge seeds. The edge seeds must be positive numbers. If "
    "the seed is an integer, the edge will be seeded by number. If it is a float, the edge will be seeded by size."
)


def mesh_parser(basename="mesh_module.py", add_help=True, description=mesh_cli_description, cubit=False):
    """Return the mesh subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """

    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = (
            "or Cubit volume name. Cubit implementation converts hyphens to underscores for " "ACIS compatibility. "
        )
    part_name_help = "Part name {}(default: %(default)s)".format(part_name_help_cubit)

    element_type_help_cubit = ""
    if cubit:
        element_type_help_cubit = (
            ". Applied as a Cubit meshing scheme if it matches 'tetmesh' or 'trimesh'. "
            "Otherwise ignored by Cubit implementation."
        )
    element_type_help = "Abaqus element type{}".format(element_type_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Model database input file",
    )
    required.add_argument(
        "--element-type",
        type=str,
        required=True,
        help=element_type_help,
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--output-file",
        type=str,
        default=mesh_defaults["output_file"],
        help="Model database output file (default: %(default)s)",
    )
    optional.add_argument(
        "--model-name",
        type=str,
        default=mesh_defaults["model_name"],
        help="Model name (default: %(default)s)",
    )
    optional.add_argument(
        "--part-name",
        type=str,
        default=mesh_defaults["part_name"],
        help=part_name_help,
    )
    optional.add_argument(
        "--global-seed",
        type=positive_float,
        default=mesh_defaults["global_seed"],
        help="The global mesh seed size. Positive float.",
    )
    optional.add_argument(
        "--edge-seed",
        dest="edge_seeds",
        action="append",
        nargs=2,
        metavar=("name", "number"),
        default=mesh_defaults["edge_seeds"],
        help="Edge seed (name, number) pairs. Repeat once per edge set. (default: %(default)s)",
    )

    return parser


merge_defaults = {"merged_model_name": "Model-1", "model_name": [None], "part_name": [None]}
merge_cli_help = "Merge parts from multiple model database files into a single model"
merge_cli_description = (
    "Supply multiple model database files, model names, and part names to merge the parts into a "
    "new model. Every model databse file is searched for every model/part name combination. "
    "If a part name is found in more than one model, return an error."
)


def merge_parser(basename="merge.py", add_help=True, description=merge_cli_description, cubit=False):
    """Return the merge subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """
    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = ". Unused by Cubit implementation. "
    part_name_help = "Part name(s) to search for within model(s){} (default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--input-file",
        type=str,
        nargs="+",
        required=True,
        help="Model database input file(s)",
    )
    required.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Model database file to save the merged model",
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--merged-model-name",
        type=str,
        default=merge_defaults["merged_model_name"],
        help="Model to create and merge parts into (default: %(default)s)",
    )
    optional.add_argument(
        "--model-name",
        type=str,
        nargs="+",
        default=merge_defaults["model_name"],
        help="Model name(s) to query in the input model database file(s) " "(default: %(default)s)",
    )
    optional.add_argument(
        "--part-name",
        type=str,
        nargs="+",
        default=merge_defaults["part_name"],
        help=part_name_help,
    )
    return parser


export_defaults = {
    "model_name": "Model-1",
    "part_name": ["Part-1"],
    "element_type": [None],
    "destination": os.getcwd(),
    "assembly": None,
}
export_output_type_choices = ["abaqus", "genesis", "genesis-normal", "genesis-hdf5"]
export_defaults["output_type"] = export_output_type_choices[0]
export_cli_help = "Export a part mesh as an orphan mesh"
# TODO: Write a more descriptive behavior message
export_cli_description = "Export a part mesh as an orphan mesh"


def export_parser(basename="export.py", add_help=True, description=export_cli_description, cubit=False):
    """Return the export subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """
    part_name_help_cubit = ""
    if cubit:
        part_name_help_cubit = (
            "or Cubit volume name(s). Cubit implementation converts hyphens to underscores for " "ACIS compatibility. "
        )
    part_name_help = "Part name(s) {}(default: %(default)s)".format(part_name_help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Model database input file",
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--model-name", type=str, default=export_defaults["model_name"], help="Model name (default: %(default)s)"
    )
    optional.add_argument(
        "--part-name",
        type=str,
        nargs="+",
        default=export_defaults["part_name"],
        help=part_name_help,
    )
    optional.add_argument(
        "--element-type",
        type=str,
        nargs="+",
        default=export_defaults["element_type"],
        # fmt: off
        help="List of element types, one per part name or one global replacement for every part name "
             "(default: %(default)s)",
        # fmt: off
    )
    optional.add_argument(
        "--destination",
        type=str,
        default=export_defaults["destination"],
        help="Write orphan mesh files to this output directory (default: PWD)",
    )
    optional.add_argument(
        "--assembly",
        type=str,
        default=export_defaults["assembly"],
        # fmt: off
        help="Assembly file for exporting the assembly keyword block. If a file is provided, but no "
             "assembly instances are found, instance all provided part names and export assembly "
             "block (default: %(default)s)",
        # fmt: on
    )
    if cubit:
        optional.add_argument(
            "--output-type",
            choices=export_output_type_choices,
            default=export_defaults["output_type"],
            # fmt: off
            help="Cubit output type. When 'abaqus' is selected, each part name is exported as an  "
                 "orphan mesh to a ``part_name``.inp file. When 'genesis' is selected all blocks "
                 "are output to a single file ``input_file``.g (default: %(default)s)",
            # fmt: on
        )

    return parser


image_defaults = {
    "x_angle": 0.0,
    "y_angle": 0.0,
    "z_angle": 0.0,
    "image_size": [1920, 1080],
    "model_name": "Model-1",
    "part_name": None,
}
image_cli_help = "Save an image of a model database file"
image_cli_description = "Save a part or assembly view image for a given Abaqus input file"
# One time dump from abaqus.session.viewports['Viewport: 1'].colorMappings.keys()) to stay Python 3 compatible
image_color_map_choices = [
    "Material",
    "Section",
    "Composite layup",
    "Composite ply",
    "Part",
    "Part instance",
    "Element set",
    "Averaging region",
    "Element type",
    "Default",
    "Assembly",
    "Part geometry",
    "Load",
    "Boundary condition",
    "Interaction",
    "Constraint",
    "Property",
    "Meshability",
    "Instance type",
    "Set",
    "Surface",
    "Internal set",
    "Internal surface",
    "Display group",
    "Selection group",
    "Skin",
    "Stringer",
    "Cell",
    "Face",
]


def image_parser(basename="image.py", add_help=True, description=image_cli_description, cubit=False):
    """Return the image subcommand parser

    :param str basename: Explicit script basename for the usage.
    :param bool add_help: ``add_help`` argument value for the ``argparse.ArgumentParser`` class interface
    :param str description: The ``description`` argument value for the ``argparse.ArgumentParser`` class interface

    :returns: argparse parser
    :rtype: argparse.ArgumentParser
    """
    help_cubit = ""
    if cubit:
        help_cubit = ". Unused by Cubit implementation."
    model_name_help = "Model name{} (default: %(default)s)".format(help_cubit)
    part_name_help = "Part name{} (default: %(default)s)".format(help_cubit)
    color_map_help = "Color map{} (default: %(default)s)".format(help_cubit)

    parser = argparse.ArgumentParser(add_help=add_help, description=description, prog=construct_prog(basename))

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Abaqus input file. Supports ``*.inp`` and ``*.cae``.",
    )
    required.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Output image from the Abaqus viewport. Supports ``*.png`` and ``*.svg``.",
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--x-angle",
        type=float,
        default=image_defaults["x_angle"],
        help="Viewer rotation about X-axis in degrees (default: %(default)s)",
    )
    optional.add_argument(
        "--y-angle",
        type=float,
        default=image_defaults["y_angle"],
        help="Viewer rotation about Y-axis in degrees (default: %(default)s)",
    )
    optional.add_argument(
        "--z-angle",
        type=float,
        default=image_defaults["z_angle"],
        help="Viewer rotation about Z-axis in degrees (default: %(default)s)",
    )
    optional.add_argument(
        "--image-size",
        nargs=2,
        type=positive_int,
        default=image_defaults["image_size"],
        help="Image size in pixels (width, height) (default: %(default)s)",
    )
    optional.add_argument(
        "--model-name",
        type=str,
        default=image_defaults["model_name"],
        help=model_name_help,
    )
    optional.add_argument(
        "--part-name",
        type=str,
        default=image_defaults["part_name"],
        help=part_name_help,
    )
    optional.add_argument(
        "--color-map",
        type=str,
        choices=image_color_map_choices,
        default=image_color_map_choices[0],
        help=color_map_help,
    )
    return parser
