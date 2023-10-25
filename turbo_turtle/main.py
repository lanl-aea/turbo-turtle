import sys
import pathlib
import argparse
import subprocess

from turbo_turtle import _settings
from turbo_turtle import __version__


# TODO: write a Python 2/3 compatible parser and argument handler
def _sphere_parser():

    default_input_file = None
    default_quadrant = "both"
    default_angle = 360.
    default_center = (0., 0.)
    default_model_name = "Model-1"
    default_part_name = "sphere"

    parser = argparse.ArgumentParser(add_help=False)

    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--inner-radius', type=float, required=True,
                               help="Inner radius (hollow size)")
    requiredNamed.add_argument('--outer-radius', type=float, required=True,
                               help="Outer radius (sphere size)")
    requiredNamed.add_argument('--output-file', type=str, required=True,
                               help="Abaqus model database to create")

    parser.add_argument('--abaqus-command', type=str, default=_settings._default_abaqus_command,
                        help='Abaqus executable absolute or relative path (default: %(default)s)')
    parser.add_argument('--input-file', type=str, default=default_input_file,
                        help="Abaqus model database to open (default: %(default)s)")
    parser.add_argument("--quadrant", type=str, choices=("both", "upper", "lower"), default=default_quadrant,
                        help="XY plane quadrant: both, upper (I), lower (IV) (default: %(default)s)")
    parser.add_argument('--angle', type=float, default=default_angle,
                        help="Angle of revolution about the +Y axis (default: %(default)s)")
    parser.add_argument('--center', nargs=2, type=float, default=default_center,
                        help="Center of the sphere (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default=default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument('--part-name', type=str, default=default_part_name,
                        help="Abaqus part name (default: %(default)s)")

    return parser


def _sphere(args):
    """Python 3 wrapper around the Abaqus Python sphere CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._project_root_abspath / "_sphere.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--inner-radius {args.inner_radius} --outer-radius {args.outer_radius} "
    command += f"--output-file {args.output_file} "
    if args.input_file is not None:
        command += f"--input-file {args.input_file} "
    command += f"--quadrant {args.quadrant} --angle {args.angle} "
    command += f"--center {' '.join(map(str, args.center))} "
    command += f"--model-name {args.model_name} --part-name {args.part_name}"
    command = command.split()
    stdout = subprocess.check_output(command)


# TODO: write a Python 2/3 compatible parser and argument handler
def _partition_parser():
    """Get parser object for partition subcommand command line options

    :return: parser
    :rtype: ArgumentParser
    """

    default_center = [0.0, 0.0, 0.0]
    default_xpoint = [1.0, 0.0, 0.0]
    default_zpoint = [0.0, 0.0, 1.0]
    default_plane_angle = 45.0
    default_partitions_x = [0.0, 0.0]
    default_partitions_y = [0.0, 0.0]
    default_partitions_z = [0.0, 0.0]

    parser = argparse.ArgumentParser(add_help=False)

    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--model-name', type=str, required=True,
                               help="Abaqus model name")
    requiredNamed.add_argument('--part-name', type=str, required=True,
                               help="Abaqus part name")
    requiredNamed.add_argument('--input-file', type=str, required=True,
                               help="Abaqus model database to open")

    parser.add_argument('--output-file', type=str, default=None,
                        help="Abaqus model database to save to. Defaults to the specified --input-file")
    parser.add_argument('--abaqus-command', type=str, default=_settings._default_abaqus_command,
                        help='Abaqus executable absolute or relative path (default: %(default)s)')

    parser.add_argument('--xpoint', nargs=3, type=float, default=default_xpoint,
                        help="Point on the x-axis (default: %(default)s)")
    parser.add_argument('--center', nargs=3, type=float, default=default_center,
                        help="Center of the sphere (default: %(default)s)")
    parser.add_argument('--zpoint', nargs=3, type=float, default=default_zpoint,
                        help="Point on the z-axis (default: %(default)s)")
    parser.add_argument('--plane-angle', type=float, default=default_plane_angle,
                        help="Angle for non-principal partitions (default: %(default)s)")
    parser.add_argument('--x-partitions', type=float, nargs='+', default=default_partitions_x,
                        help="Create a partition offset from the x-principal-plane (default: %(default)s)")
    parser.add_argument('--y-partitions', type=float, nargs='+', default=default_partitions_y,
                        help="Create a partition offset from the y-principal-plane (default: %(default)s)")
    parser.add_argument('--z-partitions', type=float, nargs='+', default=default_partitions_z,
                        help="Create a partition offset from the z-principal-plane (default: %(default)s)")
    return parser


def _partition(args):
    """Python 3 wrapper around the Abaqus Python partition CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._project_root_abspath / "_partition.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    if args.output_file is not None:
        command += f"--output-file {args.output_file} "
    command += f"--model-name {args.model_name} --part-name {args.part_name} "
    command += f"--xpoint {' '.join(map(str, args.xpoint))} "
    command += f"--center {' '.join(map(str, args.center))} "
    command += f"--zpoint {' '.join(map(str, args.zpoint))} "
    command += f"--plane-angle {args.plane_angle} "
    command += f"--x-partitions {' '.join(map(str, args.x_partitions))} "
    command += f"--y-partitions {' '.join(map(str, args.y_partitions))} "
    command += f"--z-partitions {' '.join(map(str, args.z_partitions))} "
    command = command.split()
    stdout = subprocess.check_output(command)


def _mesh_parser():

    default_output_file = None
    default_model_name = "Model-1"
    default_part_name = "Part-1"
    default_global_seed = 1.0

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("--input-file", type=str, required=True,
                        help="Abaqus CAE input file")
    parser.add_argument("--element-type", type=str, required=True,
                        help="Abaqus element type")
    parser.add_argument('--abaqus-command', type=str, default=_settings._default_abaqus_command,
                        help='Abaqus executable absolute or relative path (default: %(default)s)')
    parser.add_argument("--output-file", type=str, default=default_output_file,
                        help="Abaqus CAE output file (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument("--part-name", type=str, default=default_part_name,
                        help="Abaqus part name (default: %(default)s)")
    parser.add_argument("--global-seed", type=float, default=default_global_seed,
                        help="The global mesh seed size. Positive float.")

    return parser


def _mesh(args):
    """Python 3 wrapper around the Abaqus Python mesh CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._project_root_abspath / "_mesh.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    command += f"--element-type {args.element_type} "
    if args.output_file is not None:
        command += f"--output-file {args.output_file} "
    command += f"--model-name {args.model_name} --part-name {args.part_name} "
    command += f"--global-seed {args.global_seed}"
    command = command.split()
    stdout = subprocess.check_output(command)


def _export_parser():

    default_output_file = None
    default_model_name = "Model-1"
    default_part_name = "Part-1"

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("--input-file", type=str, required=True,
                        help="Abaqus CAE input file")
    parser.add_argument("--output-file", type=str, default=default_output_file,
                        help="Abaqus INP output file (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument("--part-name", type=str, default=default_part_name,
                        help="Abaqus part name (default: %(default)s)")
    parser.add_argument('--abaqus-command', type=str, default=_settings._default_abaqus_command,
                        help='Abaqus executable absolute or relative path (default: %(default)s)')

    return parser


def _export(args):
    """Python 3 wrapper around the Abaqus Python export CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._project_root_abspath / "_mesh.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    if args.output_file is not None:
        command += f"--output-file {args.output_file} "
    command += f"--model-name {args.model_name} --part-name {args.part_name}"
    command = command.split()
    stdout = subprocess.check_output(command)


def _image_parser():

    default_x_angle = 0.
    default_y_angle = 0.
    default_z_angle = 0.
    default_image_size = (1920, 1080)
    default_model_name = "Model-1"
    default_part_name = "Part-1"

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--input-file', type=str, required=True,
                         help='Abaqus input file. Supports ``*.inp`` and ``*.cae``.')
    parser.add_argument('--output-file', type=str, required=True,
                        help='Output image from the Abaqus viewport. Supports ``*.png`` and ``*.svg``.')
    parser.add_argument('--abaqus-command', type=str, default=_settings._default_abaqus_command,
                        help='Abaqus executable absolute or relative path (default: %(default)s)')
    parser.add_argument('--x-angle', type=float, default=default_x_angle,
                        help='Viewer rotation about X-axis in degrees (default: %(default)s)')
    parser.add_argument('--y-angle', type=float, default=default_y_angle,
                        help='Viewer rotation about Y-axis in degrees (default: %(default)s)')
    parser.add_argument('--z-angle', type=float, default=default_z_angle,
                        help='Viewer rotation about Z-axis in degrees (default: %(default)s)')
    parser.add_argument('--image-size', nargs=2, type=int, default=default_image_size,
                        help="Image size in pixels (X, Y) (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default=default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument('--part-name', type=str, default=default_part_name,
                        help="Abaqus part name (default: %(default)s)")

    return parser


def _image(args):
    """Python 3 wrapper around the Abaqus Python image CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._project_root_abspath / "_image.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--input-file {args.input_file} "
    command += f"--output-file {args.output_file} "
    command += f"--x-angle {args.x_angle} "
    command += f"--y-angle {args.y_angle} "
    command += f"--z-angle {args.z_angle} "
    command += f"--image-size {' '.join(map(str, args.image_size))} "
    command += f"--model-name {args.model_name} --part-name {args.part_name}"
    command = command.split()
    stdout = subprocess.check_output(command)


def _docs_parser():
    """Get parser object for docs subcommand command line options

    :return: parser
    :rtype: ArgumentParser
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-p", "--print-local-path",
                        action="store_true",
                        help="Print the path to the locally installed documentation index file. " \
                             "As an alternative to the docs sub-command, open index.html in a web browser " \
                             "(default: %(default)s)")
    return parser


def _docs(print_local_path=False):
    """Open or print the package's installed documentation

    Exits with a non-zero exit code if the installed index file is not found.

    :param bool print_local_path: If True, print the index file path instead of opening with a web browser
    """

    if not _settings._installed_docs_index.exists():
        # This should only be reached if the package installation structure doesn't match the assumptions in
        # _settings.py. It is used by the Conda build tests as a sign-of-life that the assumptions are correct.
        print("Could not find package documentation HTML index file", file=sys.stderr)
        sys.exit(1)

    if print_local_path:
        print(_settings._installed_docs_index, file=sys.stdout)
    else:
        import webbrowser
        webbrowser.open(str(_settings._installed_docs_index))


def get_parser():
    """Get parser object for command line options

    :return: parser
    :rtype: ArgumentParser
    """
    main_description = \
        "Common geometry, partition, and meshing utilities. Currently a thin Python 3 driver for Abaqus CAE utilities."
    main_parser = argparse.ArgumentParser(
        description=main_description,
        prog=_settings._project_name_short
    )
    main_parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"{_settings._project_name_short} {__version__}"
    )

    subparsers = main_parser.add_subparsers(dest="subcommand")

    sphere_parser = _sphere_parser()
    sphere_parser = subparsers.add_parser(
        "sphere",
        help="Create a hollow, spherical geometry from a sketch in the X-Y plane",
        description = "Create a hollow, spherical geometry from a sketch in the X-Y plane with upper (+X+Y), lower " \
                      "(+X-Y), or both quadrants.",
        parents=[sphere_parser]
    )

    partition_parser = _partition_parser()
    partition_parser = subparsers.add_parser(
        "partition",
        help="Partition a spherical shape into a turtle shell",
        description="Partition a spherical shape into a turtle shell given a small number of locating parameters",
        parents=[partition_parser]
    )

    mesh_parser = _mesh_parser()
    mesh_parser = subparsers.add_parser(
        "mesh",
        help="Mesh an Abaqus part from a global seed",
        description="Mesh an Abaqus part from a global seed",
        parents=[mesh_parser]
    )

    export_parser = _export_parser()
    export_parser = subparsers.add_parser(
        "export",
        help="Export an Abaqus part mesh as an orphan mesh",
        description="Export an Abaqus part mesh as an orphan mesh",
        parents=[export_parser]
    )

    image_parser = _image_parser()
    image_parser = subparsers.add_parser(
        "image",
        help="Save an image of an Abaqus model",
        description="Save an assembly view image (colored by material) for a given Abaqus input file",
        parents=[image_parser]
    )

    docs_parser = _docs_parser()
    docs_parser = subparsers.add_parser(
        "docs",
        help=f"Open the {_settings._project_name_short} HTML documentation",
        description=f"Open the packaged {_settings._project_name_short} HTML documentation in the  " \
                     "system default web browser",
        parents=[docs_parser])

    return main_parser


def main():

    parser = get_parser()
    args, unknown = parser.parse_known_args()
    if args.subcommand == "sphere":
        _sphere(args)
    elif args.subcommand == "partition":
        _partition(args)
    elif args.subcommand == "mesh":
        _mesh(args)
    elif args.subcommand == "image":
        _image(args)
    elif args.subcommand == "export":
        _export(args)
    elif args.subcommand == "docs":
        _docs(print_local_path=args.print_local_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
