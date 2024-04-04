import argparse

from turbo_turtle._abaqus_python.turbo_turtle_abaqus import parsers


def _get_parser() -> argparse.ArgumentParser:
    """Return a partial parser for the geometry-xyplot subcommand options appended to the geometry subcommand options

    :return: parser
    """

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--no-markers", action="store_true",
        help="Exclude vertex markers and only plot lines (default: %(default)s)"
    )
    parser.add_argument(
        "--annotate", action="store_true",
        help="Annotate the vertex coordinates with their index from the source CSV file (default: %(default)s)"
    )
    parser.add_argument(
        "--scale", action="store_true",
        help="Change the plot aspect ratio to use the same scale for the X and Y axes (default: %(default)s)"
    )

    return parser


def geometry_xyplot(
    input_file, output_file,
    part_name=parsers.geometry_xyplot_defaults["part_name"],
    unit_conversion=parsers.geometry_xyplot_defaults["unit_conversion"],
    euclidean_distance=parsers.geometry_xyplot_defaults["euclidean_distance"],
    delimiter=parsers.geometry_xyplot_defaults["delimiter"],
    header_lines=parsers.geometry_xyplot_defaults["header_lines"],
    y_offset=parsers.geometry_xyplot_defaults["y_offset"],
    rtol=parsers.geometry_defaults["rtol"],
    atol=parsers.geometry_defaults["atol"],
    no_markers: bool = parsers.geometry_xyplot_defaults["no_markers"],
    annotate: bool = parsers.geometry_xyplot_defaults["annotate"],
    scale: bool = parsers.geometry_xyplot_defaults["scale"]
) -> None:
    """Plotter for :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices.lines_and_splines` division of
    coordinates into lines and splines.

    See the :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.parsers.geometry_parser`,
    :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.geometry.main`, or
    :meth:`turbo_turtle._cubit_python.geometry` interfaces for a description of the input arguments.

    :param no_markers: Exclude vertex markers and only plot lines.
    :param annotate: Annotate the vertex coordinates with their index from the source CSV file.
    :param scale: Change the plot aspect ratio to use the same scale for the X and Y axes.
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
        coordinates = vertices.scale_and_offset_coordinates(coordinates, unit_conversion, y_offset)
        lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance, rtol=rtol, atol=atol)
        for line in lines:
            array = numpy.array(line)
            matplotlib.pyplot.plot(array[:, 0], array[:, 1], color=color, markerfacecolor="none", **line_kwargs)
        for spline in splines:
            array = numpy.array(spline)
            matplotlib.pyplot.plot(array[:, 0], array[:, 1], color=color, linestyle="dashed", **spline_kwargs)
        if annotate:
            for index, coordinate in enumerate(coordinates):
                matplotlib.pyplot.annotate(str(index), coordinate, color=color)

    if scale:
        ax = matplotlib.pyplot.gca()
        ax.set_aspect("equal", adjustable="box")

    matplotlib.pyplot.savefig(output_file)
