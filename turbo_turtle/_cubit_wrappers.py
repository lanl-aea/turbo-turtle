import sys
import pathlib

import numpy
import cubit

from turbo_turtle._abaqus_python import _mixed_utilities
from turbo_turtle._abaqus_python import vertices
from turbo_turtle._abaqus_python import parsers


def geometry(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    _geometry(args.input_file, args.output_file,
              planar=args.planar,
              model_name=args.model_name,
              part_name=args.part_name,
              unit_conversion=args.unit_conversion,
              euclidean_distance=args.euclidean_distance,
              delimiter=args.delimiter,
              header_lines=args.header_lines,
              revolution_angle=args.revolution_angle)


def _geometry(input_file, output_file,
              planar=parsers.geometry_default_planar,
              model_name=parsers.geometry_default_model_name,
              part_name=parsers.geometry_default_part_name,
              unit_conversion=parsers.geometry_default_unit_conversion,
              euclidean_distance=parsers.geometry_default_euclidean_distance,
              delimiter=parsers.geometry_default_delimiter,
              header_lines=parsers.geometry_default_header_lines,
              revolution_angle=parsers.geometry_default_revolution_angle):
    """Create geometry from an array of XY coordiantes

    :param str input_file: input text file(s) with coordinates to draw
    :param str output_file: Abaqus CAE database to save the part(s)
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param str model_name: name of the Abaqus model in which to create the part
    :param list part_name: name(s) of the part(s) being created
    :param float unit_conversion: multiplication factor applies to all coordinates
    :param float euclidean_distance: if the distance between two coordinates is greater than this, draw a straight line.
        Distance should be provided in units *after* the unit conversion
    :param str delimiter: character to use as a delimiter when reading the input file
    :param int header_lines: number of lines in the header to skip when reading the input file
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries

    :returns: writes ``{output_file}.cae``
    """
    cubit.init(["cubit", "-nojournal"])
    part_name = _mixed_utilities.validate_part_name_or_exit(input_file, part_name)
    output_file = pathlib.Path(output_file).with_suffix(".cub")
    surfaces = []
    for file_name, new_part in zip(input_file, part_name):
        coordinates = _mixed_utilities.return_genfromtxt(file_name, delimiter, header_lines,
                                                         expected_dimensions=2, expected_columns=2)
        coordinates = coordinates * unit_conversion
        lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance)
        curves = []
        for point1, point2 in lines:
            vertex1 = cubit.create_vertex(*tuple(point1), 0.)
            vertex2 = cubit.create_vertex(*tuple(point2), 0.)
            curves.append(cubit.create_curve(vertex1, vertex2))
        for spline in splines:
            points = []
            for point in spline:
                points.append(cubit.create_vertex(*tuple(point), 0.))
        # TODO: VVV Replace free curve recovery ``curves.append(cubit.create_spline(points))`` works
            vertex_ids = sorted(cubit.get_list_of_free_ref_entities("vertex"))
            vertex_ids_text = " ".join(map(str, vertex_ids))
            cubit.cmd(f"create curve spline vertex {vertex_ids_text} delete")
        curve_ids = cubit.get_list_of_free_ref_entities("curve")
        curves = [cubit.curve(identity) for identity in curve_ids]
        # TODO: ^^^ Replace free curve recovery ``curves.append(cubit.create_spline(points))`` works
        surfaces.append(cubit.create_surface(curves))

    # TODO: Find a better way to recover Body and Volume objects
    for number, (surface, new_part) in enumerate(zip(surfaces, part_name), 1):
        if planar:
            cubit.cmd(f"body {number} rename '{new_part}'")
        elif numpy.isclose(revolution_angle, 0.0):
            cubit.cmd(f"body {number} rename '{new_part}'")
        else:
            cubit.cmd(f"sweep surface {surface.id()} yaxis angle {revolution_angle} merge")
            cubit.cmd(f"volume {number} rename '{new_part}'")

        # TODO: Replace surface recovery with a ``surfaces = cubit.create_surface()`` command with spline creation
    cubit.cmd(f"save as '{output_file}' overwrite")


def cylinder(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def sphere(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def partition(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def mesh(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def merge(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def export(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def image(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")
