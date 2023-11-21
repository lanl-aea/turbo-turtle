"""Python 3 module that imports cubit

Which requires that Cubit's bin directory is found on PYTHONPATH, either directly by the end user or from a successful
:meth:`turbo_turtle._utilities.find_cubit_bin` call and internal ``sys.path`` modification. This module does *not*
perform ``sys.path`` manipulation, so the importing/calling module/script *must* verify that Cubit will import correctly
first.
"""
import shutil
import pathlib
import tempfile

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
    :param str output_file: Cubit ``*.cub`` database to save the part(s)
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
        surfaces.append(_draw_surface(lines, splines))

    for surface, new_part in zip(surfaces, part_name):
        _rename_and_sweep(surface, new_part, planar=planar, revolution_angle=revolution_angle)

    cubit_command_or_exit(f"save as '{output_file}' overwrite")


def _draw_surface(lines, splines):
    """Given ordered lists of line/spline coordinates, create a Cubit surface object

    :param list lines: list of [2, 2] shaped arrays of (x, y) coordinates defining a line segment
    :param list splines: list of [N, 2] shaped arrays of (x, y) coordinates defining a spline

    :returns: Cubit surface defined by the lines and splines input
    :rtype: cubit.Surface
    """
    curves = []
    for first, second in lines:
        point1 = tuple(first) + (0.,)
        point2 = tuple(second) + (0.,)
        curves.append(_create_curve_from_coordinates(point1, point2))
    for spline in splines:
        zero_column = numpy.zeros([len(spline), 1])
        spline_3d = numpy.append(spline, zero_column, axis=1)
        _create_spline_from_coordinates(spline_3d)
    # TODO: VVV Replace free curve recovery ``curves.append(cubit.create_spline(points))`` works
    curve_ids = cubit.get_list_of_free_ref_entities("curve")
    curves = [cubit.curve(identity) for identity in curve_ids]
    # TODO: ^^^ Replace free curve recovery ``curves.append(cubit.create_spline(points))`` works
    return cubit.create_surface(curves)


def _create_curve_from_coordinates(point1, point2):
    """Create a curve from 2 three-dimensional coordinates

    :param tuple point1: First set of coordinates (x1, y1, z1)
    :param tuple point2: Second set of coordinates (x2, y2, z2)

    :returns: Cubit curve object defining a line segment
    :rtype: cubit.Curve
    """
    vertex1 = cubit.create_vertex(*tuple(point1))
    vertex2 = cubit.create_vertex(*tuple(point2))
    return cubit.create_curve(vertex1, vertex2)


def _create_spline_from_coordinates(coordinates):
    """Create a spline from a list of coordinates

    :param numpy.array coordinates: [N, 3] array of coordinates (x, y, z)
    """
    points = []
    for point in coordinates:
        points.append(cubit.create_vertex(*tuple(point)))
    vertex_ids = [point.id() for point in points]
    vertex_ids_text = " ".join(map(str, vertex_ids))
    cubit_command_or_exit(f"create curve spline vertex {vertex_ids_text} delete")
    # TODO: Return a curve object when ``curves.append(cubit.create_spline(points))`` works
    return None


def _create_arc_from_coordinates(center, point1, point2):
    center_vertex = cubit.create_vertex(*tuple(center))

    # Cubit creates arcs with anticlockwise rotation. Order vertices with most negative Y axis coordinate first.
    if point1[1] < point2[1]:
        vertex1 = cubit.create_vertex(*tuple(point1))
        vertex2 = cubit.create_vertex(*tuple(point2))
    else:
        vertex1 = cubit.create_vertex(*tuple(point2))
        vertex2 = cubit.create_vertex(*tuple(point1))

    cubit_command_or_exit(f"create curve arc center vertex {center_vertex.id()} {vertex1.id()} {vertex2.id()} normal 0 0 1")
    cubit_command_or_exit(f"delete vertex {center_vertex.id()}")
    # TODO: Return the curve object when a Cubit Python API method exists to create an arc from center and vertices
    return None


def _rename_and_sweep(surface, part_name,
                      center=numpy.array([0., 0., 0.]),
                      planar=parsers.geometry_default_planar,
                      revolution_angle=parsers.geometry_default_revolution_angle):
    """Recover body or volume from body surface, sweep part if required, and rename body/volume by part name

    Hyphens are replaced by underscores to make the ACIS engine happy.

    :param cubit.Surface surface: Cubit surface object to rename and conditionally sweep
    :param list part_name: name(s) of the part(s) being created
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries. Ignore when planar is True.
    """
    center = numpy.array(center)
    center_string = " ".join(map(str, center))
    vertical_axis = center + numpy.array([0., 1., 0.])
    vertical_string = " ".join(map(str, vertical_axis))
    body_number = surface.id()
    surface_number = surface.surfaces()[0].id()
    part_name = part_name.replace("-", "_")
    if planar:
        cubit_command_or_exit(f"body {body_number} rename '{part_name}'")
    elif numpy.isclose(revolution_angle, 0.0):
        cubit_command_or_exit(f"body {body_number} rename '{part_name}'")
    else:
        cubit_command_or_exit(f"sweep surface {surface_number} axis {center_string} {vertical_string} "
                              f"angle {revolution_angle} merge")
        cubit_command_or_exit(f"volume {body_number} rename '{part_name}'")


def cylinder(inner_radius, outer_radius, height, output_file,
             part_name=parsers.cylinder_default_part_name,
             revolution_angle=parsers.geometry_default_revolution_angle):
    """
    :param float inner_radius: Radius of the hollow center
    :param float outer_radius: Outer radius of the cylinder
    :param float height: Height of the cylinder
    :param str output_file: Cubit ``*.cub`` database to save the part(s)
    :param list part_name: name(s) of the part(s) being created
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries
    """
    cubit.init(["cubit"])
    output_file = pathlib.Path(output_file).with_suffix(".cub")

    coordinates = vertices.cylinder(inner_radius, outer_radius, height)
    euclidean_distance = min(inner_radius, height) / 2.
    lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance)
    surface = _draw_surface(lines, splines)
    _rename_and_sweep(surface, part_name, revolution_angle=revolution_angle)

    cubit_command_or_exit(f"save as '{output_file}' overwrite")


def sphere(inner_radius, outer_radius, output_file,
           input_file=parsers.sphere_default_input_file,
           quadrant=parsers.sphere_default_quadrant,
           revolution_angle=parsers.sphere_default_angle,
           center=parsers.sphere_default_center,
           part_name=parsers.sphere_default_part_name):
    """
    :param float inner_radius: inner radius (size of hollow)
    :param float outer_radius: outer radius (size of sphere)
    :param str output_file: output file name. Will be stripped of the extension and ``.cae`` will be used.
    :param str input_file: input file name. Will be stripped of the extension and ``.cae`` will be used.
    :param str quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param float revolution_angle: angle of rotation 0.-360.0 degrees. Provide 0 for a 2D axisymmetric model.
    :param tuple center: tuple of floats (X, Y) location for the center of the sphere
    :param str part_name: name of the part to be created in the Abaqus model
    """
    cubit.init(["cubit"])
    output_file = pathlib.Path(output_file).with_suffix(".cub")
    if input_file is not None:
        input_file = pathlib.Path(input_file).with_suffix(".cub")
        # Avoid modifying the contents or timestamp on the input file.
        # Required to get conditional re-builds with a build system such as GNU Make, CMake, or SCons
        with tempfile.NamedTemporaryFile(suffix=".cub", dir=".") as copy_file:
            shutil.copyfile(input_file, copy_file.name)
            # TODO: look for a Cubit Python interface proper open/close/save command(s)
            cubit_command_or_exit(f"open '{copy_file.name}'")
            _sphere(inner_radius, outer_radius, quadrant=quadrant, revolution_angle=revolution_angle, center=center,
                    part_name=part_name)
            cubit_command_or_exit(f"save as '{output_file}' overwrite")

    else:
        _sphere(inner_radius, outer_radius, quadrant=quadrant, revolution_angle=revolution_angle, center=center,
                part_name=part_name)
        cubit_command_or_exit(f"save as '{output_file}' overwrite")


def _sphere(inner_radius, outer_radius,
            quadrant=parsers.sphere_default_quadrant,
            revolution_angle=parsers.sphere_default_angle,
            center=parsers.sphere_default_center,
            part_name=parsers.sphere_default_part_name):
    """
    :param float inner_radius: inner radius (size of hollow)
    :param float outer_radius: outer radius (size of sphere)
    :param str quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param float revolution_angle: angle of rotation 0.-360.0 degrees. Provide 0 for a 2D axisymmetric model.
    :param tuple center: tuple of floats (X, Y) location for the center of the sphere
    :param str part_name: name of the part to be created in the Abaqus model
    """
    arc_points = vertices.sphere(center, inner_radius, outer_radius, quadrant)
    zero_column = numpy.zeros([len(arc_points), 1])
    arc_points_3d = numpy.append(arc_points, zero_column, axis=1)
    inner_point1 = arc_points[0]
    inner_point2 = arc_points[1]
    outer_point1 = arc_points[2]
    outer_point2 = arc_points[3]

    center_3d = center + (0.,)
    _create_arc_from_coordinates(center_3d, inner_point1, inner_point2)
    _create_arc_from_coordinates(center_3d, outer_point1, outer_point2)
    _create_curve_from_coordinates(inner_point1, outer_point1)
    _create_curve_from_coordinates(inner_point2, outer_point2)
    # TODO: VVV Replace free curve recovery when an arc by center and two points is available in Cubit Python API
    curve_ids = cubit.get_list_of_free_ref_entities("curve")
    curves = [cubit.curve(identity) for identity in curve_ids]
    # TODO: ^^^ Replace free curve recovery when an arc by center and two points is available in Cubit Python API
    surface = cubit.create_surface(curves)

    _rename_and_sweep(surface, part_name, revolution_angle=revolution_angle, center=center_3d)
