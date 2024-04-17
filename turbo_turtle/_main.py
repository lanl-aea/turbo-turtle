import sys
import argparse

from turbo_turtle import __version__
from turbo_turtle import _settings
from turbo_turtle import _utilities
from turbo_turtle import _fetch
from turbo_turtle import geometry_xyplot
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import parsers


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
        sys.exit("Could not find package documentation HTML index file")

    if print_local_path:
        print(_settings._installed_docs_index, file=sys.stdout)
    else:
        import webbrowser
        webbrowser.open(str(_settings._installed_docs_index))


def _print_abaqus_path_parser():
    parser = argparse.ArgumentParser(add_help=False)
    # This parser has no arguments. Current implementation acts like a flag
    return parser


def _print_abaqus_path_location():
    """Print the absolute path to the Turbo Turtle Abaqus Python package directory

    Exits with a non-zero exit code if the settings variable ``_abaqus_python_parent_abspath`` does not exist.
    """
    if not _settings._abaqus_python_parent_abspath.exists():
        sys.exit("Could not find a documented path to the Abaqus Python package directory")
    else:
        print(_settings._abaqus_python_parent_abspath)


def add_abaqus_and_cubit(parsers):
    """Add the Abaqus and Cubit command arguments to each parser in the parsers list

    :param list parsers: List of parser to run ``add_argument`` for the abaqus command
    """
    for parser in parsers:
        parser.add_argument("--abaqus-command", nargs="+", default=_settings._default_abaqus_options,
                            help="Abaqus executable options (default: %(default)s)")
        parser.add_argument("--cubit-command", nargs="+", default=_settings._default_cubit_options,
                            help="Cubit executable options (default: %(default)s)")
        # TODO: remove deprecated cubit flag
        # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/130
        backend = parser.add_mutually_exclusive_group(required=False)
        backend.add_argument("--cubit", action="store_true",
                             help="DEPRECATED. Use ``--backend cubit``. " \
                                  "Flag to use Cubit instead of Abaqus (default: %(default)s)")
        backend.add_argument("--backend", choices=_settings._backend_choices, default=_settings._default_backend,
                             help="Back end software (default: %(default)s)")


def append_cubit_help(text, append="with Abaqus or Cubit"):
    """Append common short help with optional Cubit text

    :param str text: original text
    :param str append: new text

    :returns: appended text
    :rtype: str
    """
    return f"{text} {append}"


def append_cubit_description(text,
                             append="Defaults to Abaqus, but can optionally run Cubit. Cubit implementation "
                                    "replaces hyphens with underscores in part name(s) and ignores model/assembly name "
                                    "arguments."):
    """Append common long description with optional Cubit text

    :param str text: original text
    :param str append: new text

    :returns: appended text
    :rtype: str
    """
    return f"{text} {append}"


def get_parser():
    """Get parser object for command line options

    :return: parser
    :rtype: ArgumentParser
    """
    main_description = \
        "A collection of solid body modeling tools for 2D sketched, 2D axisymmetric, and 3D revolved models. " \
        "Implemented for Abaqus and Cubit as backend modeling and meshing software. " \
        "Most of the interface options and descriptions use Abaqus modeling concepts and language. " \
        "Turbo-Turtle makes a best effort to maintain common behaviors and features across each third-party " \
        "software's modeling concepts."
    main_parser = argparse.ArgumentParser(
        description=main_description,
        prog=_settings._project_name_short
    )
    main_parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"{_settings._project_name_short} {__version__}"
    )

    subparsers = main_parser.add_subparsers(
        title="subcommands",
        metavar="{subcommand}",
        dest="subcommand"
    )

    subparsers.add_parser(
        "docs",
        help=f"Open the {_settings._project_name_short} HTML documentation",
        description=f"Open the packaged {_settings._project_name_short} HTML documentation in the  " \
                     "system default web browser",
        parents=[_docs_parser()])

    subparsers.add_parser(
        "fetch",
        help=f"Fetch and copy {_settings._project_name} modsim template files and directories",
        description=f"Fetch and copy {_settings._project_name} modsim template files and directories. If no ``FILE`` " \
            "is specified, all available files will be created. Directories are recursively copied. ``pathlib.Path`` " \
            "recursive pattern matching is possible. The source path is truncated to use the shortest common file " \
            "prefix, e.g. requesting two files ``common/source/file.1`` and ``common/source/file.2`` will create " \
            "``/destination/file.1`` and ``/destination/file.2``, respectively.",
        parents=[_fetch.get_parser()]
    )

    subparsers.add_parser(
        "print-abaqus-path",
        help="Print the absolute path to Turbo-Turtle's Abaqus Python compatible package.",
        description="***NOTE: this is an alpha feature for early adopters and developer testing of possible GUI " \
                    "support*** Print the absolute path to Turbo-Turtle's Abaqus Python compatible package. " \
                    "If this directory is on your PYTHONPATH, you can directly import Turbo Turtle Abaqus Python " \
                    "packages in your own scrips (i.e. import turbo_turtle_abaqus.partition)",
        parents=[_print_abaqus_path_parser()])

    geometry_parser = parsers.geometry_parser(add_help=False, cubit=True)
    cylinder_parser = parsers.cylinder_parser(add_help=False, cubit=True)
    sphere_parser = parsers.sphere_parser(add_help=False, cubit=True)
    partition_parser = parsers.partition_parser(add_help=False, cubit=True)
    mesh_parser = parsers.mesh_parser(add_help=False, cubit=True)
    image_parser = parsers.image_parser(add_help=False, cubit=True)
    merge_parser = parsers.merge_parser(add_help=False, cubit=True)
    export_parser = parsers.export_parser(add_help=False, cubit=True)

    add_abaqus_and_cubit([
        geometry_parser,
        cylinder_parser,
        sphere_parser,
        partition_parser,
        mesh_parser,
        image_parser,
        merge_parser,
        export_parser,
    ])

    subparsers.add_parser(
        "geometry",
        help=append_cubit_help(parsers.geometry_cli_help),
        description=append_cubit_description(parsers.geometry_cli_description),
        parents=[geometry_parser]
    )

    subparsers.add_parser(
        "geometry-xyplot",
        help="Plot the lines-and-splines as parsed by the geometry subcommand.",
        description="Plot the lines-and-splines as parsed by the geometry subcommand. " \
                    "Lines are shown as solid lines with circle markers at the vertices. " \
                    "Splines are show as dashed lines with plus sign markers at the vertices. " \
                    "If there is more than one part, each part is shown in a unique color.",
        parents=[geometry_parser, geometry_xyplot._get_parser()]
    )

    subparsers.add_parser(
        "cylinder",
        help=append_cubit_help(parsers.cylinder_cli_help),
        description=append_cubit_description(parsers.cylinder_cli_description),
        parents=[cylinder_parser]
    )

    subparsers.add_parser(
        "sphere",
        help=append_cubit_help(parsers.sphere_cli_help),
        description=append_cubit_description(parsers.sphere_cli_description),
        parents=[sphere_parser]
    )

    subparsers.add_parser(
        "partition",
        help=append_cubit_help(parsers.partition_cli_help),
        description=append_cubit_description(parsers.partition_cli_description),
        parents=[partition_parser]
    )

    subparsers.add_parser(
        "mesh",
        help=append_cubit_help(parsers.mesh_cli_help),
        description=append_cubit_description(parsers.mesh_cli_description),
        parents=[mesh_parser]
    )

    merge_parser = subparsers.add_parser(
        "merge",
        help=append_cubit_help(parsers.merge_cli_help),
        description=append_cubit_description(parsers.merge_cli_description),
        parents=[merge_parser]
    )

    subparsers.add_parser(
        "export",
        help=append_cubit_help(parsers.export_cli_help),
        description=append_cubit_description(parsers.export_cli_description),
        parents=[export_parser]
    )

    subparsers.add_parser(
        "image",
        help=append_cubit_help(parsers.image_cli_help),
        description=append_cubit_description(parsers.image_cli_description),
        parents=[image_parser]
    )

    return main_parser


def main():
    parser = get_parser()
    subcommand_list = parser._subparsers._group_actions[0].choices.keys()
    args = parser.parse_args()

    if args.subcommand not in subcommand_list:
        parser.print_help()
    elif args.subcommand == "docs":
        _docs(print_local_path=args.print_local_path)
    elif args.subcommand == "fetch":
        root_directory = _settings._tutorials_directory.parent
        relative_paths = _settings._fetch_subdirectories
        _fetch.main(
            args.subcommand, root_directory, relative_paths, args.destination,
            requested_paths=args.FILE, overwrite=args.overwrite,
            dry_run=args.dry_run, print_available=args.print_available
        )
    elif args.subcommand == "print-abaqus-path":
        _print_abaqus_path_location()
    elif args.subcommand == "geometry-xyplot":
        geometry_xyplot._main(
            args.input_file, args.output_file,
            part_name=args.part_name,
            unit_conversion=args.unit_conversion,
            euclidean_distance=args.euclidean_distance,
            delimiter=args.delimiter,
            header_lines=args.header_lines,
            y_offset=args.y_offset,
            rtol=args.rtol,
            atol=args.atol,
            no_markers=args.no_markers,
            annotate=args.annotate,
            scale=args.scale
        )
    else:
        _wrappers, command = _utilities.set_wrappers_and_command(args)
        wrapper_command = getattr(_wrappers, args.subcommand)
        wrapper_command(args, command)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
