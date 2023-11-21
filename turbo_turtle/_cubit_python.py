"""Python 3 module that imports cubit

Which requires that Cubit's bin directory is found on PYTHONPATH, either directly by the end user or from a successful
:meth:`turbo_turtle._utilities.find_cubit_bin` call and internal ``sys.path`` modification. This module does *not*
perform ``sys.path`` manipulation, so the importing/calling module/script *must* verify that Cubit will import correctly
first.
"""
import pathlib

import numpy
import cubit

from turbo_turtle._abaqus_python import _mixed_utilities
from turbo_turtle._abaqus_python import vertices
from turbo_turtle._abaqus_python import parsers


def cubit_command_or_exception(command):
    """Thin wrapper around ``cubit.cmd`` to raise an exception when returning False

    Cubit returns True/False on ``cubit.cmd("")`` calls, but does not raise an exception. This method will raise a
    RuntimeError when the command returns False.

    :param str command: Cubit APREPRO command to execute
    """
    success = cubit.cmd(command)
    if not success:
        raise RuntimeError(f"Command '{command}' returned an error. Please see the Cubit log for details.")
    return success


@_mixed_utilities.print_exception_message
def cubit_command_or_exit(*args, **kwargs):
    """Thin wrapper around ``cubit.cmd`` to call ``sys.exit`` when returning False

    Wrapper of :meth:`turbo_turtle._cubit_python.cubit_command_or_exception` with
    :meth:`turbo_turtle._abaqus_python._mixed_utilities._print_exception_message`.

    Cubit returns True/False on ``cubit.cmd("")`` calls, but does not raise an exception. This method will raise a
    SystemExit with ``sys.exit`` when the command returns False.

    :param str command: Cubit APREPRO command to execute
    """
    return cubit_command_or_exception(*args, **kwargs)


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
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries. Ignore when planar is True.

    :returns: writes ``{output_file}.cae``
    """
    # TODO: Figure out how to log the Cubit operations without printing to console
    # TODO: Figure out how to get a better log of the non-APREPRO actions
    cubit.init(["cubit"])
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
            cubit_command_or_exit(f"create curve spline vertex {vertex_ids_text} delete")
        curve_ids = cubit.get_list_of_free_ref_entities("curve")
        curves = [cubit.curve(identity) for identity in curve_ids]
        # TODO: ^^^ Replace free curve recovery ``curves.append(cubit.create_spline(points))`` works
        surfaces.append(cubit.create_surface(curves))

    # TODO: Find a better way to recover Body and Volume objects than assuming the enumerated order is correct
    for number, (surface, new_part) in enumerate(zip(surfaces, part_name), 1):
        _rename_and_sweep(number, surface, new_part, planar=planar, revolution_angle=revolution_angle)

    cubit_command_or_exit(f"save as '{output_file}' overwrite")


def _rename_and_sweep(number, surface, part_name,
                      planar=parsers.geometry_default_planar,
                      revolution_angle=parsers.geometry_default_revolution_angle):
    """Recover body or volume by number, sweep part if required, and rename body/volume by part name

    :param int number: The body or volume number
    :param cubit.Surface surface: Cubit surface object to rename and conditionally sweep
    :param list part_name: name(s) of the part(s) being created
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries. Ignore when planar is True.
    """
    # TODO: Find a better way to recover Body and Volume objects than assuming the enumerated order is correct. Replace
    # ``number`` with ``body/volume`` object variable.
    if planar:
        cubit_command_or_exit(f"body {number} rename '{part_name}'")
    elif numpy.isclose(revolution_angle, 0.0):
        cubit_command_or_exit(f"body {number} rename '{part_name}'")
    else:
        cubit_command_or_exit(f"sweep surface {surface.id()} yaxis angle {revolution_angle} merge")
        cubit_command_or_exit(f"volume {number} rename '{part_name}'")
