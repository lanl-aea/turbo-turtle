import sys
import argparse

from turbo_turtle import __version__
from turbo_turtle import _settings
from turbo_turtle import _utilities
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


def _geometry_xyplot(
    input_file, output_file,
    part_name=parsers.geometry_xyplot_defaults["part_name"],
    unit_conversion=parsers.geometry_xyplot_defaults["unit_conversion"],
    euclidean_distance=parsers.geometry_xyplot_defaults["euclidean_distance"],
    delimiter=parsers.geometry_xyplot_defaults["delimiter"],
    header_lines=parsers.geometry_xyplot_defaults["header_lines"],
    y_offset=parsers.geometry_xyplot_defaults["y_offset"],
    rtol=parsers.geometry_defaults["rtol"],
    atol=parsers.geometry_defaults["atol"],
    no_markers=parsers.geometry_xyplot_defaults["no_markers"],
    annotate=parsers.geometry_xyplot_defaults["annotate"]
):
    """Plotter for :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices.lines_and_splines` division of coordinates into lines and splines

    See the :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.geometry_parser`,
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.geometry.main`, or :meth:`turbo_turtle._cubit_python.geometry` interfaces for a
    description of the input arguments.

    :param bool no_markers: Exclude vertex markers and only plot lines.
    :param bool annotate: Annotate the vertex coordinates with their index from the source CSV file.
    """
    import numpy
    import matplotlib.pyplot

    from turbo_turtle._abaqus_python.turbo_turtle_abaqus import _mixed_utilities
    from turbo_turtle._abaqus_python.turbo_turtle_abaqus import vertices

    if no_markers:
        line_kwargs = {}
        spline_kwargs = {}
    else:
        line_kwargs = {"marker": "o"}
        spline_kwargs = {"marker": "+"}

    matplotlib.pyplot.figure()
    part_name = _mixed_utilities.validate_part_name_or_exit(input_file, part_name)
    if len(part_name) > 1:
        colors = matplotlib.cm.rainbow(numpy.linspace(0, 1, len(part_name)))  # NOT part of refactor
    else:
        colors = ["black"]
    for file_name, new_part, color in zip(input_file, part_name, colors):
        coordinates = _mixed_utilities.return_genfromtxt_or_exit(file_name, delimiter, header_lines,
                                                                 expected_dimensions=2, expected_columns=2)
        lines, splines = vertices.modified_lines_and_splines(coordinates, euclidean_distance, unit_conversion, y_offset,
                                                             rtol=rtol, atol=atol)
        for line in lines:
            array = numpy.array(line)
            matplotlib.pyplot.plot(array[:, 0], array[:, 1], color=color, markerfacecolor="none", **line_kwargs)
        for spline in splines:
            array = numpy.array(spline)
            matplotlib.pyplot.plot(array[:, 0], array[:, 1], color=color, linestyle="dashed", **spline_kwargs)
        if annotate:
            for index, coordinate in enumerate(coordinates):
                matplotlib.pyplot.annotate(str(index), coordinate, color=color)

    matplotlib.pyplot.savefig(output_file)


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

    docs_parser = _docs_parser()
    subparsers.add_parser(
        "docs",
        help=f"Open the {_settings._project_name_short} HTML documentation",
        description=f"Open the packaged {_settings._project_name_short} HTML documentation in the  " \
                     "system default web browser",
        parents=[docs_parser])

    print_abaqus_path_parser = _print_abaqus_path_parser()
    subparsers.add_parser(
        "print-abaqus-path",
        help="Print the absolute path to Turbo-Turtle's Abaqus Python compatible package.",
        description="***NOTE: this is an alpha feature for early adopters and developer testing of possible GUI " \
                    "support*** Print the absolute path to Turbo-Turtle's Abaqus Python compatible package. " \
                    "If this directory is on your PYTHONPATH, you can directly import Turbo Turtle Abaqus Python " \
                    "packages in your own scrips (i.e. import turbo_turtle_abaqus.partition)",
        parents=[print_abaqus_path_parser])

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

    geometry_xyplot_parser = geometry_parser
    geometry_xyplot_parser.add_argument(
        "--no-markers", action="store_true",
        help="Exclude vertex markers and only plot lines (default: %(default)s)"
    )
    geometry_xyplot_parser.add_argument(
        "--annotate", action="store_true",
        help="Annotate the vertex coordinates with their index from the source CSV file (default: %(default)s)"
    )
    subparsers.add_parser(
        "geometry-xyplot",
        help="Plot the lines-and-splines as parsed by the geometry subcommand.",
        description="Plot the lines-and-splines as parsed by the geometry subcommand. " \
                    "Lines are shown as solid lines with circle markers at the vertices. " \
                    "Splines are show as dashed lines with plus sign markers at the vertices. " \
                    "If there is more than one part, each part is shown in a unique color.",
        parents=[geometry_parser]
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
    elif args.subcommand == "print-abaqus-path":
        _print_abaqus_path_location()
    elif args.subcommand == "geometry-xyplot":
        _geometry_xyplot(
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
            annotate=args.annotate
        )
    else:
        _wrappers, command = _utilities.set_wrappers_and_command(args)
        wrapper_command = getattr(_wrappers, args.subcommand)
        wrapper_command(args, command)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
