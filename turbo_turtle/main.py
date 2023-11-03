import os
import sys
import pathlib
import argparse
import subprocess

from turbo_turtle import __version__
from turbo_turtle import _settings
from turbo_turtle import _wrappers
from turbo_turtle._abaqus_python import parsers


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
    parser.add_argument("--output-file", type=str, default=default_output_file,
                        help="Abaqus CAE output file (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument("--part-name", type=str, default=default_part_name,
                        help="Abaqus part name (default: %(default)s)")
    parser.add_argument("--global-seed", type=float, default=default_global_seed,
                        help="The global mesh seed size. Positive float.")

    parser.add_argument('--abaqus-command', type=str, default=_settings._default_abaqus_command,
                        help='Abaqus executable absolute or relative path (default: %(default)s)')

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


def _merge_parser():

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("--input-file", type=str, nargs="+", required=True,
                        help="Abaqus CAE input file(s)")
    parser.add_argument("--output-file", type=str, required=True,
                        help="Abaqus CAE file to save the merged model")
    parser.add_argument("--merged-model-name", type=str, required=True,
                        help="Model to create and merge parts into")
    # TODO: find a way to make default behavior to take all parts from all models from all cae files and merge them
    #       this would make model_name and part_name no longer required
    #       https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/43
    parser.add_argument("--model-name", type=str, nargs="+", required=True,
                        help="Abaqus model name(s) to attempt to query in the input CAE file(s)")
    parser.add_argument("--part-name", type=str, nargs="+", required=True,
                        help="Part name(s) to search for within model(s)")

    parser.add_argument('--abaqus-command', type=str, default=_settings._default_abaqus_command,
                        help='Abaqus executable absolute or relative path (default: %(default)s)')

    return parser


def _merge(args):
    """Python 3 wrapper around the Abaqus Python merge CLI

    :param argparse.Namespace args: namespace of parsed arguments
    """
    script = _settings._project_root_abspath / "_merge.py"

    command = f"{args.abaqus_command} cae -noGui {script} -- "
    command += f"--input-file {' '.join(map(str, args.input_file))} "
    command += f"--output-file {args.output_file} "
    command += f"--merged-model-name {args.merged_model_name} "
    command += f"--model-name {' '.join(map(str, args.model_name))} "
    command += f"--part-name {' '.join(map(str, args.part_name))}"
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


def add_abaqus_argument(parsers):
    """Add the abaqus command argument to each parser in the parsers list

    :param list parsers: List of parser to run ``add_argument`` for the abaqus command
    """
    for parser in parsers:
        parser.add_argument('--abaqus-command', type=str, default=_settings._default_abaqus_command,
                            help='Abaqus executable absolute or relative path (default: %(default)s)')


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

    geometry_parser = parsers.geometry_parser(add_help=False)
    cylinder_parser = parsers.cylinder_parser(add_help=False)
    sphere_parser = parsers.sphere_parser(add_help=False)
    partition_parser = parsers.partition_parser(add_help=False)
    mesh_parser = parsers.mesh_parser(add_help=False)
    export_parser = parsers.export_parser(add_help=False)
    image_parser = parsers.image_parser(add_help=False)
    add_abaqus_argument([geometry_parser, cylinder_parser, sphere_parser, partition_parser, mesh_parser, export_parser, image_parser])

    subparsers.add_parser(
        "geometry",
        help=parsers.geometry_cli_help,
        description=parsers.geometry_cli_description,
        parents=[geometry_parser]
    )

    subparsers.add_parser(
        "cylinder",
        help=parsers.cylinder_cli_help,
        description=parsers.cylinder_cli_description,
        parents=[cylinder_parser]
    )

    subparsers.add_parser(
        "sphere",
        help=parsers.sphere_cli_help,
        description=parsers.sphere_cli_description,
        parents=[sphere_parser]
    )

    subparsers.add_parser(
        "partition",
        help=parsers.partition_cli_help,
        description=parsers.partition_cli_description,
        parents=[partition_parser]
    )

    subparsers.add_parser(
        "mesh",
        help=parsers.mesh_cli_help,
        description=parsers.mesh_cli_description,
        parents=[mesh_parser]
    )

    merge_parser = _merge_parser()
    merge_parser = subparsers.add_parser(
        "merge",
        help="Merge parts from multiple Abaqus models into a new model",
        description="Supply multiple Abaqus CAE files along with model and part names and attempt " \
                    "to merge the parts into a new model",
        parents=[merge_parser]
    )

    subparsers.add_parser(
        "export",
        help=parsers.export_cli_help,
        description=parsers.export_cli_description,
        parents=[export_parser]
    )

    subparsers.add_parser(
        "image",
        help=parsers.image_cli_help,
        description=parsers.image_cli_description,
        parents=[image_parser]
    )

    docs_parser = _docs_parser()
    subparsers.add_parser(
        "docs",
        help=f"Open the {_settings._project_name_short} HTML documentation",
        description=f"Open the packaged {_settings._project_name_short} HTML documentation in the  " \
                     "system default web browser",
        parents=[docs_parser])

    return main_parser


def main():
    parser = get_parser()
    args, unknown = parser.parse_known_args()
    if args.subcommand == "geometry":
        _wrappers.geometry(args)
    elif args.subcommand == "cylinder":
        _wrappers.cylinder(args)
    elif args.subcommand == "sphere":
        _wrappers.sphere(args)
    elif args.subcommand == "partition":
        _wrappers.partition(args)
    elif args.subcommand == "mesh":
        _wrappers.mesh(args)
    elif args.subcommand == "image":
        _wrappers.image(args)
    elif args.subcommand == "merge":
        _merge(args)
    elif args.subcommand == "export":
        _wrappers.export(args)
    elif args.subcommand == "docs":
        _docs(print_local_path=args.print_local_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
