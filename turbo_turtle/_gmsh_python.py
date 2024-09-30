"""Python 3 module that imports python-gmsh"""
import gmsh

from turbo_turtle._abaqus_python.turbo_turtle_abaqus import _mixed_utilities
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import vertices
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import parsers


def cylinder(inner_radius, outer_radius, height, output_file,
             part_name=parsers.cylinder_defaults["part_name"],
             revolution_angle=parsers.geometry_defaults["revolution_angle"],
             y_offset=parsers.cylinder_defaults["y_offset"]):
    """Accept dimensions of a right circular cylinder and generate an axisymmetric revolved geometry

    Centroid of cylinder is located on the global coordinate origin by default.

    :param float inner_radius: Radius of the hollow center
    :param float outer_radius: Outer radius of the cylinder
    :param float height: Height of the cylinder
    :param str output_file: Cubit ``*.cub`` database to save the part(s)
    :param list part_name: name(s) of the part(s) being created
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries
    :param float y_offset: vertical offset along the global Y-axis
    """
    gmsh.initialize()
    gmsh.logger.start()

    part_name = _mixed_utilities.cubit_part_names(part_name)
    gmsh.model.add(part_name)
    output_file = pathlib.Path(output_file)

    lines = vertices.cylinder_lines(inner_radius, outer_radius, height, y_offset=y_offset)
    # TODO: implement the Gmsh line/surface creation

    # TODO: revolve

    gmsh.model.occ.synchronize()
    # TODO: Figure out how to save geometry files instead of mesh files with Gmsh
    gmsh.write(str(output_file))
    gmsh.logger.stop()
    gmsh.finalize()
