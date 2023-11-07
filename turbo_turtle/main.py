import os
import sys
import pathlib
import argparse
import subprocess

from turbo_turtle import __version__
from turbo_turtle import _settings
from turbo_turtle import _wrappers
from turbo_turtle._abaqus_python import _parsers


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

    geometry_parser = _parsers.geometry_parser(add_help=False)
    cylinder_parser = _parsers.cylinder_parser(add_help=False)
    sphere_parser = _parsers.sphere_parser(add_help=False)
    partition_parser = _parsers.partition_parser(add_help=False)
    mesh_parser = _parsers.mesh_parser(add_help=False)
    export_parser = _parsers.export_parser(add_help=False)
    image_parser = _parsers.image_parser(add_help=False)
    add_abaqus_argument([geometry_parser, cylinder_parser, sphere_parser, partition_parser, mesh_parser, export_parser, image_parser])

    subparsers.add_parser(
        "geometry",
        help=_parsers.geometry_cli_help,
        description=_parsers.geometry_cli_description,
        parents=[geometry_parser]
    )

    subparsers.add_parser(
        "cylinder",
        help=_parsers.cylinder_cli_help,
        description=_parsers.cylinder_cli_description,
        parents=[cylinder_parser]
    )

    subparsers.add_parser(
        "sphere",
        help=_parsers.sphere_cli_help,
        description=_parsers.sphere_cli_description,
        parents=[sphere_parser]
    )

    subparsers.add_parser(
        "partition",
        help=_parsers.partition_cli_help,
        description=_parsers.partition_cli_description,
        parents=[partition_parser]
    )

    subparsers.add_parser(
        "mesh",
        help=_parsers.mesh_cli_help,
        description=_parsers.mesh_cli_description,
        parents=[mesh_parser]
    )

    subparsers.add_parser(
        "export",
        help=_parsers.export_cli_help,
        description=_parsers.export_cli_description,
        parents=[export_parser]
    )

    subparsers.add_parser(
        "image",
        help=_parsers.image_cli_help,
        description=_parsers.image_cli_description,
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
    elif args.subcommand == "export":
        _wrappers.export(args)
    elif args.subcommand == "docs":
        _docs(print_local_path=args.print_local_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
