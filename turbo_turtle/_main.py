import sys
import typing
import argparse

from turbo_turtle import __version__
from turbo_turtle import _settings
from turbo_turtle import _docs
from turbo_turtle import _utilities
from turbo_turtle import _fetch
from turbo_turtle import geometry_xyplot
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import parsers


def _print_abaqus_path_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    # This parser has no arguments. Current implementation acts like a flag
    return parser


def _print_abaqus_path_location() -> None:
    """Print the absolute path to the Turbo Turtle Abaqus Python package directory

    Exits with a non-zero exit code if the settings variable ``_abaqus_python_parent_abspath`` does not exist.
    """
    if not _settings._abaqus_python_parent_abspath.exists():
        sys.exit("Could not find a documented path to the Abaqus Python package directory")
    else:
        print(_settings._abaqus_python_parent_abspath)


def add_abaqus_and_cubit(parsers: typing.List[argparse.ArgumentParser]) -> None:
    """Add the Abaqus and Cubit command arguments to each parser in the parsers list

    :param list parsers: List of parsers to run ``add_argument`` for the command options
    """
    for parser in parsers:
        parser.add_argument(
            "--abaqus-command",
            nargs="+",
            default=_settings._default_abaqus_options,
            help="Abaqus executable options (default: %(default)s)",
        )
        parser.add_argument(
            "--cubit-command",
            nargs="+",
            default=_settings._default_cubit_options,
            help="Cubit executable options (default: %(default)s)",
        )
        parser.add_argument(
            "--backend",
            choices=_settings._backend_choices,
            default=_settings._default_backend,
            help="Back end software (default: %(default)s)",
        )


def append_cubit_help(text: str, append: str = "with Abaqus, Cubit, or Gmsh (work-in-progress)") -> str:
    """Append common short help with optional Cubit text

    :param str text: original text
    :param str append: new text

    :returns: appended text
    :rtype: str
    """
    return f"{text} {append}"


def append_cubit_description(
    text: str,
    append: str = (
        "Defaults to Abaqus, but can optionally run Cubit (Gmsh implementation is a work-in-progress). "
        "Cubit and Gmsh backends replace hyphens with underscores in part name(s) for ACIS "
        "compatibility. Cubit backend ignores model/assembly name arguments."
    ),
) -> str:
    """Append common long description with optional Cubit text

    :param str text: original text
    :param str append: new text

    :returns: appended text
    :rtype: str
    """
    return f"{text} {append}"


def get_parser() -> argparse.ArgumentParser:
    """Get parser object for command line options

    :return: parser
    :rtype: ArgumentParser
    """
    main_description = (
        "A collection of solid body modeling tools for 2D sketched, 2D axisymmetric, and 3D revolved models. "
        "Implemented for Abaqus, Cubit, and Gmsh (work-in-progress) as backend modeling and meshing software. "
        "Most of the interface options and descriptions use Abaqus modeling concepts and language. "
        "Turbo-Turtle makes a best effort to maintain common behaviors and features across each third-party "
        "software's modeling concepts."
    )
    main_parser = argparse.ArgumentParser(
        description=main_description,
        prog=_settings._project_name_short,
    )
    main_parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"{_settings._project_name_short} {__version__}",
    )

    subparsers = main_parser.add_subparsers(
        title="subcommands",
        metavar="{subcommand}",
        dest="subcommand",
    )

    subparsers.add_parser(
        "docs",
        help=f"Open the {_settings._project_name_short} HTML documentation",
        description=(
            f"Open the packaged {_settings._project_name_short} HTML documentation in the system default web browser"
        ),
        parents=[_docs.get_parser()],
    )

    subparsers.add_parser(
        "fetch",
        help=f"Fetch and copy {_settings._project_name} modsim template files and directories",
        description=(
            f"Fetch and copy {_settings._project_name} modsim template files and directories. If no ``FILE`` "
            "is specified, all available files will be created. Directories are recursively copied. "
            "``pathlib.Path`` recursive pattern matching is possible. The source path is truncated to use the "
            "shortest common file prefix, e.g. requesting two files ``common/source/file.1`` and "
            "``common/source/file.2`` will create ``/destination/file.1`` and ``/destination/file.2``, respectively."
        ),
        parents=[_fetch.get_parser()],
    )

    subparsers.add_parser(
        "print-abaqus-path",
        help="Print the absolute path to Turbo-Turtle's Abaqus Python compatible package.",
        description=(
            "***NOTE: this is an alpha feature for early adopters and developer testing of possible GUI "
            "support*** Print the absolute path to Turbo-Turtle's Abaqus Python compatible package. "
            "If this directory is on your PYTHONPATH, you can directly import Turbo Turtle Abaqus Python "
            "packages in your own scrips (i.e. import turbo_turtle_abaqus.partition)"
        ),
        parents=[_print_abaqus_path_parser()],
    )

    geometry_parser = parsers.geometry_parser(add_help=False, cubit=True)
    cylinder_parser = parsers.cylinder_parser(add_help=False, cubit=True)
    sphere_parser = parsers.sphere_parser(add_help=False, cubit=True)
    partition_parser = parsers.partition_parser(add_help=False, cubit=True)
    sets_parser = parsers.sets_parser(add_help=False, cubit=True)
    mesh_parser = parsers.mesh_parser(add_help=False, cubit=True)
    image_parser = parsers.image_parser(add_help=False, cubit=True)
    merge_parser = parsers.merge_parser(add_help=False, cubit=True)
    export_parser = parsers.export_parser(add_help=False, cubit=True)

    add_abaqus_and_cubit(
        [
            geometry_parser,
            cylinder_parser,
            sphere_parser,
            partition_parser,
            sets_parser,
            mesh_parser,
            image_parser,
            merge_parser,
            export_parser,
        ]
    )

    subparsers.add_parser(
        "geometry",
        help=append_cubit_help(parsers.geometry_cli_help),
        description=append_cubit_description(parsers.geometry_cli_description),
        parents=[geometry_parser],
    )

    subparsers.add_parser(
        "geometry-xyplot",
        help="Plot the lines-and-splines as parsed by the geometry subcommand.",
        description=(
            "Plot the lines-and-splines as parsed by the geometry subcommand. "
            "Lines are shown as solid lines with circle markers at the vertices. "
            "Splines are show as dashed lines with plus sign markers at the vertices. "
            "If there is more than one part, each part is shown in a unique color."
        ),
        parents=[geometry_parser, geometry_xyplot._get_parser()],
    )

    subparsers.add_parser(
        "cylinder",
        help=append_cubit_help(parsers.cylinder_cli_help),
        description=append_cubit_description(parsers.cylinder_cli_description),
        parents=[cylinder_parser],
    )

    subparsers.add_parser(
        "sphere",
        help=append_cubit_help(parsers.sphere_cli_help),
        description=append_cubit_description(parsers.sphere_cli_description),
        parents=[sphere_parser],
    )

    subparsers.add_parser(
        "partition",
        help=append_cubit_help(parsers.partition_cli_help),
        description=append_cubit_description(parsers.partition_cli_description),
        parents=[partition_parser],
    )

    subparsers.add_parser(
        "sets",
        help=append_cubit_help(parsers.sets_cli_help),
        description=append_cubit_description(parsers.sets_cli_description),
        parents=[sets_parser],
    )

    subparsers.add_parser(
        "mesh",
        help=append_cubit_help(parsers.mesh_cli_help),
        description=append_cubit_description(parsers.mesh_cli_description),
        parents=[mesh_parser],
    )

    merge_parser = subparsers.add_parser(
        "merge",
        help=append_cubit_help(parsers.merge_cli_help),
        description=append_cubit_description(parsers.merge_cli_description),
        parents=[merge_parser],
    )

    subparsers.add_parser(
        "export",
        help=append_cubit_help(parsers.export_cli_help),
        description=append_cubit_description(parsers.export_cli_description),
        parents=[export_parser],
    )

    subparsers.add_parser(
        "image",
        help=append_cubit_help(parsers.image_cli_help),
        description=append_cubit_description(parsers.image_cli_description),
        parents=[image_parser],
    )

    return main_parser


def main() -> None:
    parser = get_parser()
    subcommand_list = parser._subparsers._group_actions[0].choices.keys()
    args = parser.parse_args()

    try:
        if args.subcommand not in subcommand_list:
            parser.print_help()
        elif args.subcommand == "docs":
            _docs.main(_settings._installed_docs_index, print_local_path=args.print_local_path)
        elif args.subcommand == "fetch":
            root_directory = _settings._tutorials_directory.parent
            relative_paths = _settings._fetch_subdirectories
            _fetch.main(
                args.subcommand,
                root_directory,
                relative_paths,
                args.destination,
                requested_paths=args.FILE,
                overwrite=args.overwrite,
                dry_run=args.dry_run,
                print_available=args.print_available,
            )
        elif args.subcommand == "print-abaqus-path":
            _print_abaqus_path_location()
        elif args.subcommand == "geometry-xyplot":
            geometry_xyplot._main(
                args.input_file,
                args.output_file,
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
                scale=args.scale,
            )
        else:
            _wrappers, command = _utilities.set_wrappers_and_command(args)
            wrapper_command = getattr(_wrappers, args.subcommand)
            wrapper_command(args, command)
    except RuntimeError as err:
        sys.exit(str(err))


if __name__ == "__main__":
    main()  # pragma: no cover
