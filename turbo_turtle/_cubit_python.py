import pathlib

import numpy
import cubit

from turbo_turtle._abaqus_python import _mixed_utilities
from turbo_turtle._abaqus_python import vertices
from turbo_turtle._abaqus_python import parsers


def geometry(input_file, output_file,
             planar=parsers.geometry_default_planar,
             model_name=parsers.geometry_default_model_name,
             part_name=parsers.geometry_default_part_name,
             unit_conversion=parsers.geometry_default_unit_conversion,
             euclidean_distance=parsers.geometry_default_euclidean_distance,
             delimiter=parsers.geometry_default_delimiter,
             header_lines=parsers.geometry_default_header_lines,
             revolution_angle=parsers.geometry_default_revolution_angle):
    """Create 2D planar, 2D axisymmetric, or 3D revolved geometry from an array of XY coordinates.

    Note that 2D axisymmetric sketches and sketches for 3D bodies of revolution about the global Y-axis must lie
    entirely on the positive-X side of the global Y-axis.

    This function can create multiple sheet bodies or volumes in the same Cubit ``*.cub`` file. If no part (body/volume)
    names are provided, the body/volume will be named after the input file base name.

    :param str input_file: input text file(s) with coordinates to draw
    :param str output_file: Abaqus CAE database to save the part(s)
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
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

    # TODO: Find a better way to recover Body and Volume objects than assuming the enumerated order is correct
    for number, (surface, new_part) in enumerate(zip(surfaces, part_name), 1):
        if planar:
            cubit.cmd(f"body {number} rename '{new_part}'")
        elif numpy.isclose(revolution_angle, 0.0):
            cubit.cmd(f"body {number} rename '{new_part}'")
        else:
            cubit.cmd(f"sweep surface {surface.id()} yaxis angle {revolution_angle} merge")
            cubit.cmd(f"volume {number} rename '{new_part}'")

    cubit.cmd(f"save as '{output_file}' overwrite")
