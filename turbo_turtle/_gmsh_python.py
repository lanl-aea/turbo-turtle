"""Python 3 module that imports python-gmsh"""
import pathlib

import numpy

from turbo_turtle import _utilities
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import _mixed_utilities
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import vertices
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import parsers


gmsh = _utilities.import_gmsh()


def geometry(
    input_file, output_file,
    planar=parsers.geometry_defaults["planar"],
    model_name=parsers.geometry_defaults["model_name"],
    part_name=parsers.geometry_defaults["part_name"],
    unit_conversion=parsers.geometry_defaults["unit_conversion"],
    euclidean_distance=parsers.geometry_defaults["euclidean_distance"],
    delimiter=parsers.geometry_defaults["delimiter"],
    header_lines=parsers.geometry_defaults["header_lines"],
    revolution_angle=parsers.geometry_defaults["revolution_angle"],
    y_offset=parsers.geometry_defaults["y_offset"],
    rtol=parsers.geometry_defaults["rtol"],
    atol=parsers.geometry_defaults["atol"]
) -> None:
    """Create 2D planar, 2D axisymmetric, or 3D revolved geometry from an array of XY coordinates.

    Note that 2D axisymmetric sketches and sketches for 3D bodies of revolution about the global Y-axis must lie
    entirely on the positive-X side of the global Y-axis.

    This function can create multiple sheet bodies or volumes in the same Cubit ``*.cub`` file. If no part (body/volume)
    names are provided, the body/volume will be named after the input file base name.

    :param str input_file: input text file(s) with coordinates to draw
    :param str output_file: Cubit ``*.cub`` database to save the part(s)
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param str model_name: name of the Gmsh model in which to create the part
    :param list part_name: name(s) of the part(s) being created
    :param float unit_conversion: multiplication factor applies to all coordinates
    :param float euclidean_distance: if the distance between two coordinates is greater than this, draw a straight line.
        Distance should be provided in units *after* the unit conversion
    :param str delimiter: character to use as a delimiter when reading the input file
    :param int header_lines: number of lines in the header to skip when reading the input file
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries. Ignore when planar is True.
    :param float y_offset: vertical offset along the global Y-axis. Offset should be provided in units *after* the unit
        conversion.
    :param float rtol: relative tolerance for vertical/horizontal line checks
    :param float atol: absolute tolerance for vertical/horizontal line checks

    :returns: writes ``{output_file}.step``
    """
    # Universally required setup
    gmsh.initialize()
    gmsh.logger.start()

    # Input/Output setup
    # TODO: allow other output formats support by Gmsh
    output_file = pathlib.Path(output_file).with_suffix(".step")

    # Model setup
    gmsh.model.add(model_name)
    part_name = _mixed_utilities.validate_part_name(input_file, part_name)
    part_name = _mixed_utilities.cubit_part_names(part_name)

    # Create part(s)
    surfaces = []
    for file_name, new_part in zip(input_file, part_name):
        coordinates = _mixed_utilities.return_genfromtxt(file_name, delimiter, header_lines,
                                                         expected_dimensions=2, expected_columns=2)
        coordinates = vertices.scale_and_offset_coordinates(coordinates, unit_conversion, y_offset)
        lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance, rtol=rtol, atol=atol)
        surfaces.append(_draw_surface(lines, splines))

    # Conditionally create the 3D revolved shape
    # Part name handling

    # Output and cleanup
    gmsh.write(str(output_file))
    gmsh.logger.stop()
    gmsh.finalize()


def _draw_surface(lines, splines):
    """Given ordered lists of line/spline coordinates, create a Gmsh 2D surface object

    :param list lines: list of [2, 2] shaped arrays of (x, y) coordinates defining a line segment
    :param list splines: list of [N, 2] shaped arrays of (x, y) coordinates defining a spline

    :returns: Gmsh 2D entity tag
    :rtype: int
    """
    curves = []
    for first, second in lines:
        point1 = tuple(first) + (0.,)
        point2 = tuple(second) + (0.,)
        curves.append(_create_line_from_coordinates(point1, point2))
    for spline in splines:
        zero_column = numpy.zeros([len(spline), 1])
        spline_3d = numpy.append(spline, zero_column, axis=1)
        curves.append(_create_spline_from_coordinates(spline_3d))
    return gmsh.model.geo.addPlaneSurface(curves)


def _create_line_from_coordinates(point1, point2):
    """Create a curve from 2 three-dimensional coordinates

    :param tuple point1: First set of coordinates (x1, y1, z1)
    :param tuple point2: Second set of coordinates (x2, y2, z2)

    :returns: Gmsh 1D entity tag
    :rtype: int
    """
    point1_tag = gmsh.model.geo.addPoint(*point1)
    point2_tag = gmsh.model.geo.addPoint(*point2)
    return gmsh.model.geo.addLine(point1_tag, point2_tag)


def _create_spline_from_coordinates(coordinates):
    """Create a spline from a list of coordinates

    :param numpy.array coordinates: [N, 3] array of coordinates (x, y, z)

    :returns: Gmsh 1D entity tag
    :rtype: int
    """
    coordinates = numpy.array(coordinates)
    minimum = 2
    if coordinates.shape[0] < minimum:
        raise RuntimeError(f"Requires at least {minimum} coordinates to create a spline")

    points = []
    for point in coordinates:
        points.append(gmsh.model.geo.addPoint(*tuple(point)))

    return gmsh.model.geo.addBSpline(points)


def cylinder(
    inner_radius, outer_radius, height, output_file,
    model_name=parsers.geometry_defaults["model_name"],
    part_name=parsers.cylinder_defaults["part_name"],
    revolution_angle=parsers.geometry_defaults["revolution_angle"],
    y_offset=parsers.cylinder_defaults["y_offset"]
) -> None:
    """Accept dimensions of a right circular cylinder and generate an axisymmetric revolved geometry

    Centroid of cylinder is located on the global coordinate origin by default.

    :param float inner_radius: Radius of the hollow center
    :param float outer_radius: Outer radius of the cylinder
    :param float height: Height of the cylinder
    :param str output_file: Gmsh ``*.step`` file to save the part(s)
    :param str model_name: name of the Gmsh model in which to create the part
    :param list part_name: name(s) of the part(s) being created
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries
    :param float y_offset: vertical offset along the global Y-axis
    """
    # Universally required setup
    gmsh.initialize()
    gmsh.logger.start()

    # Input/Output setup
    # TODO: allow other output formats support by Gmsh
    output_file = pathlib.Path(output_file).with_suffix(".step")
    gmsh.model.add(model_name)

    # Create the 2D axisymmetric shape
    lines = vertices.cylinder_lines(inner_radius, outer_radius, height, y_offset=y_offset)
    xcoords = [point[0] for points in lines for point in points]
    ycoords = [point[1] for points in lines for point in points]
    x = min(xcoords)
    dx = max(xcoords) - x
    y = min(ycoords)
    dy = max(ycoords) - y
    z = 0.0
    part_dimension = 2
    part_tag = gmsh.model.occ.addRectangle(x, y, z, dx, dy)

    # Conditionally create the 3D revolved shape
    if not numpy.isclose(revolution_angle, 0.0):
        dimTags = gmsh.model.occ.revolve(
            [(part_dimension, part_tag)],
            0.,  # Center: x
            0.,  # Center: y
            0.,  # Center: z
            0.,  # Direction: x
            1.,  # Direction: y
            0.,  # Direction: z
            numpy.radians(revolution_angle)
        )
        part_dimension = dimTags[0][0]
        part_tag = dimTags[0][1]

    # Part name handling
    gmsh.model.occ.synchronize()
    part_name = _mixed_utilities.cubit_part_names(part_name)
    part_tag = gmsh.model.addPhysicalGroup(part_dimension, [part_tag], name=part_name)

    # Output and cleanup
    gmsh.write(str(output_file))
    gmsh.logger.stop()
    gmsh.finalize()


def sphere(*args, **kwargs):
    raise RuntimeError("sphere subcommand is not yet implemented")


def partition(*args, **kwargs):
    raise RuntimeError("partition subcommand is not yet implemented")


def sets(*args, **kwargs):
    raise RuntimeError("sets subcommand is not yet implemented")


def mesh(*args, **kwargs):
    raise RuntimeError("mesh subcommand is not yet implemented")


def merge(*args, **kwargs):
    raise RuntimeError("merge subcommand is not yet implemented")


def export(*args, **kwargs):
    raise RuntimeError("export subcommand is not yet implemented")


def image(*args, **kwargs):
    raise RuntimeError("image subcommand is not yet implemented")
