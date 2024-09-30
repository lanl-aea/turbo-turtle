"""Python 3 module that imports python-gmsh"""
import pathlib

import gmsh
import numpy

from turbo_turtle._abaqus_python.turbo_turtle_abaqus import _mixed_utilities
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import vertices
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import parsers


def geometry(*args, **kwargs):
    raise RuntimeError("geometry subcommand is not yet implemented")


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

    # Model setup
    part_name = _mixed_utilities.cubit_part_names(part_name)
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
