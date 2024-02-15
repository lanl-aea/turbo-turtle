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

from turbo_turtle import _utilities
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
             planar=parsers.geometry_defaults["planar"],
             part_name=parsers.geometry_defaults["part_name"],
             unit_conversion=parsers.geometry_defaults["unit_conversion"],
             euclidean_distance=parsers.geometry_defaults["euclidean_distance"],
             delimiter=parsers.geometry_defaults["delimiter"],
             header_lines=parsers.geometry_defaults["header_lines"],
             revolution_angle=parsers.geometry_defaults["revolution_angle"],
             y_offset=parsers.geometry_defaults["y_offset"]):
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
    :param float y_offset: vertical offset along the global Y-axis. Offset should be provided in units *after* the unit
        conversion.

    :returns: writes ``{output_file}.cae``
    """
    # TODO: Figure out how to log the Cubit operations without printing to console
    # TODO: Figure out how to get a better log of the non-APREPRO actions
    cubit.init(["cubit"])
    part_name = _mixed_utilities.validate_part_name_or_exit(input_file, part_name)
    part_name = _mixed_utilities.cubit_part_names(part_name)
    output_file = pathlib.Path(output_file).with_suffix(".cub")
    surfaces = []
    # TODO: VV Everything between todo markers should be a common function to remove triply repeated logic VV
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/123
    for file_name, new_part in zip(input_file, part_name):
        coordinates = _mixed_utilities.return_genfromtxt(file_name, delimiter, header_lines,
                                                         expected_dimensions=2, expected_columns=2)
        coordinates = coordinates * unit_conversion
        coordinates[:, 1] += y_offset
        lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance)
    # TODO: ^^ Everything between todo markers should be a common function to remove triply repeated logic ^^
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
        curves.append(_create_spline_from_coordinates(spline_3d))
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

    :returns: Cubit curve object defining a spline
    :rtype: cubit.Curve
    """
    points = []
    for point in coordinates:
        points.append(cubit.create_vertex(*tuple(point)))
    vertex_ids = [point.id() for point in points]
    vertex_ids_text = " ".join(map(str, vertex_ids))
    # TODO: Find a suitable Cubit Python function for creating splines that returns the curve object
    cubit_command_or_exit(f"create curve spline vertex {vertex_ids_text} delete")
    curve = points[0].curves()[0]
    return curve


def _create_arc_from_coordinates(center, point1, point2):
    """Create a circular arc cubit.Curve object from center and points on the curve

    :returns: cubit curve object
    :rtype: curbit.Curve
    """
    center_vertex = cubit.create_vertex(*tuple(center))

    # Cubit creates arcs with anticlockwise rotation. Order vertices with most negative Y axis coordinate first.
    if point1[1] < point2[1]:
        vertex1 = cubit.create_vertex(*tuple(point1))
        vertex2 = cubit.create_vertex(*tuple(point2))
    else:
        vertex1 = cubit.create_vertex(*tuple(point2))
        vertex2 = cubit.create_vertex(*tuple(point1))

    # TODO: Find a suitable Cubit Python function for creating arcs that returns the curve object
    cubit_command_or_exit(f"create curve arc center vertex {center_vertex.id()} {vertex1.id()} {vertex2.id()} normal 0 0 1")
    curve = vertex1.curves()[0]
    cubit_command_or_exit(f"delete vertex {center_vertex.id()}")
    return curve


def _create_surface_from_coordinates(coordinates):
    """Create a surface from an [N, 3] array of coordinates

    Each row of the array represents a coordinate in 3D space. Must have at least 3 rows or a RuntimeError is raised.
    Coordinates are connected in pairs to create curves. First and last coordinate connected for final curve. Curves
    must defind a closed perimeter to generate a surface.

    :param numpy.array coordinates: [N, 3] array of 3D coordinates where N > 2.

    :returns: Cubit surface object
    :rtype: cubit.surface
    """
    coordinates = numpy.array(coordinates)
    if coordinates.shape[0] < 3:
        raise RuntimeError("Requires at least 3 coordinates to create a surface")
    curves = []
    last = numpy.array([coordinates[-1]])
    coordinates_shift = numpy.append(last, coordinates[0:-1], axis=0)
    for point1, point2 in zip(coordinates, coordinates_shift):
        curves.append(_create_curve_from_coordinates(point1, point2))
    return cubit.create_surface(curves)


def _surface_numbers(surfaces):
    """Return a list of surface IDs from the provided list of surface objects

    :param list surfaces: list of Cubit surface objects

    :returns: list of surface IDs
    :rtype: list of int
    """
    return [surface.surfaces()[0].id() for surface in surfaces]


def _surface_centroids(surfaces):
    """Return a list of 3D surface centroids from the provided list of surface objects

    :param list surfaces: list of Cubit surface objects

    :returns: list of surface centroids
    :rtype: list of numpy.arrays
    """
    surface_ids = _surface_numbers(surfaces)
    surface_centroids = [numpy.array(cubit.get_surface_centroid(id)) for id in surface_ids]
    return surface_centroids


def _surfaces_for_volumes(volumes):
    """Return a flat list of surface objects for a list of volumes

    :param list volumes: list of Cubit volume objects

    :returns: list of Cubit surface objects
    :rtype: list
    """
    surfaces = []
    for volume in volumes:
        surfaces.extend(volume.surfaces())
    return surfaces


def _surfaces_by_vector(surfaces, principal_vector, center=numpy.zeros(3)):
    """Return a flat list of Cubit surface objects that meet the requirement of a
    positive dot product between a given vector and the vector between two points:
    a user provided center point and a surface object centroid.

    :param list surfaces: list of Cubit surface objects
    :param numpy.array principal_vector: Local principal axis vector defined in global coordinates
    :param numpy.array center: center location of the geometry

    :returns: numpy.array of Cubit surface objects
    :rtype: numpy.array
    """
    surface_centroids = _surface_centroids(surfaces)
    direction_vectors = [numpy.subtract(centroid, center) for centroid in surface_centroids]

    vector_dot = numpy.array(([numpy.dot(direction_vector, principal_vector) for direction_vector in direction_vectors]))
    # Account for numerical errors in significant digits
    vector_dot[numpy.isclose(vector_dot, 0.)] = 0.
    return numpy.array(surfaces)[numpy.where(vector_dot > 0.)]


def _create_volume_from_surfaces(surfaces, keep=True):
    """Create a volume from the provided surfaces. Surfaces must create a closed volume.

    :param list surfaces: List of Cubit surface objects
    :param bool keep: Keep the original surface objects/sheet bodies

    :returns: Cubit volume object
    :rtype: cubit.Volume
    """
    volumes_before = cubit.get_entities("volume")
    surface_numbers = _surface_numbers(surfaces)
    surface_string = " ".join(map(str, surface_numbers))
    command = f"create volume surface {surface_string} heal"
    if keep:
        command = f"{command} keep"
    # TODO: Recover volume object directly when creation is possible with Cubit Python API
    cubit_command_or_exit(command)
    volumes_after = cubit.get_entities("volume")
    volume_id = list(set(volumes_after) - set(volumes_before))
    volume_id = volume_id[0]
    return cubit.volume(volume_id)


def _rename_and_sweep(surface, part_name,
                      center=numpy.array([0., 0., 0.]),
                      planar=parsers.geometry_defaults["planar"],
                      revolution_angle=parsers.geometry_defaults["revolution_angle"]):
    """Recover body or volume from body surface, sweep part if required, and rename body/volume by part name

    Hyphens are replaced by underscores to make the ACIS engine happy.

    :param cubit.Surface surface: Cubit surface object to rename and conditionally sweep
    :param list part_name: name(s) of the part(s) being created
    :param bool planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries. Ignore when planar is True.

    :returns: Cubit volume object
    :rtype: cubit.Volume
    """
    center = numpy.array(center)
    center_string = " ".join(map(str, center))
    revolution_axis = numpy.array([0., 1., 0.])
    revolution_string = " ".join(map(str, revolution_axis))
    body_number = surface.id()
    surface_number = _surface_numbers([surface])[0]
    part_name = part_name.replace("-", "_")
    if planar:
        return_object = surface.volumes()[0]
    elif numpy.isclose(revolution_angle, 0.0):
        return_object = surface.volumes()[0]
    else:
        cubit_command_or_exit(f"sweep surface {surface_number} axis {center_string} {revolution_string} "
                              f"angle {revolution_angle} merge")
        return_object = surface.volumes()[0]
        volume_id = return_object.id()
        cubit_command_or_exit(f"regularize volume {volume_id}")

    return_object.set_entity_name(part_name)
    return return_object


def _get_volumes_from_name(names):
    """Return all volume objects with a prefix from the ``names`` list

    :param list names: Name(s) prefix to search for with ``cubit.get_all_ids_from_name``

    :returns: list of Cubit volumes with name prefix
    :rtype: list of cubit.Volume objects
    """
    if isinstance(names, str):
        names = [names]
    parts = []
    for name in names:
        parts.extend([cubit.volume(number) for number in cubit.get_all_ids_from_name("volume", name)])
    if len(parts) < 1:
        raise RuntimeError(f"Could not find any volumes with prefix '{name}'")
    return parts


@_mixed_utilities.print_exception_message
def _get_volumes_from_name_or_exit(*args, **kwargs):
    """Thin wrapper around :meth:`turbo_turtle._cubit_python._get_volumes_from_name` to call ``sys.exit`` on exceptions

    Wrapper of :meth:`turbo_turtle._cubit_python._get_volumes_from_name` with
    :meth:`turbo_turtle._abaqus_python._mixed_utilities._print_exception_message`.
    """
    return _get_volumes_from_name(*args, **kwargs)


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
    cubit.init(["cubit"])
    part_name = _mixed_utilities.cubit_part_names(part_name)
    output_file = pathlib.Path(output_file).with_suffix(".cub")

    coordinates = vertices.cylinder(inner_radius, outer_radius, height, y_offset=y_offset)
    euclidean_distance = min(inner_radius, height) / 2.
    lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance)
    surface = _draw_surface(lines, splines)
    _rename_and_sweep(surface, part_name, revolution_angle=revolution_angle)

    cubit_command_or_exit(f"save as '{output_file}' overwrite")


def sphere(inner_radius, outer_radius, output_file,
           input_file=parsers.sphere_defaults["input_file"],
           quadrant=parsers.sphere_defaults["quadrant"],
           revolution_angle=parsers.sphere_defaults["revolution_angle"],
           y_offset=parsers.sphere_defaults["y_offset"],
           part_name=parsers.sphere_defaults["part_name"]):
    """
    :param float inner_radius: inner radius (size of hollow)
    :param float outer_radius: outer radius (size of sphere)
    :param str output_file: output file name. Will be stripped of the extension and ``.cub`` will be used.
    :param str input_file: input file name. Will be stripped of the extension and ``.cub`` will be used.
    :param str quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param float revolution_angle: angle of rotation 0.-360.0 degrees. Provide 0 for a 2D axisymmetric model.
    :param float y_offset: vertical offset along the global Y-axis
    :param str part_name: name of the part to be created in the Abaqus model
    """
    cubit.init(["cubit"])

    # Preserve the (X, Y) center implementation, but use the simpler y-offset interface
    center = (0., y_offset)

    part_name = _mixed_utilities.cubit_part_names(part_name)
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
            quadrant=parsers.sphere_defaults["quadrant"],
            revolution_angle=parsers.sphere_defaults["revolution_angle"],
            center=parsers.sphere_defaults["center"],
            part_name=parsers.sphere_defaults["part_name"]):
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

    center_3d = numpy.append(center, [0.])
    curves = []
    if numpy.allclose(inner_point1, center) and numpy.allclose(inner_point2, center):
        inner_point1 = center
        inner_point2 = center
    else:
        curves.append(_create_arc_from_coordinates(center_3d, inner_point1, inner_point2))
    curves.append(_create_arc_from_coordinates(center_3d, outer_point1, outer_point2))
    curves.append(_create_curve_from_coordinates(inner_point1, outer_point1))
    curves.append(_create_curve_from_coordinates(inner_point2, outer_point2))
    surface = cubit.create_surface(curves)

    _rename_and_sweep(surface, part_name, revolution_angle=revolution_angle, center=center_3d)


def imprint_and_merge(names):
    """Imprint and merge all volume objects with a prefix from the ``names`` list

    :param list names: Name(s) prefix to search for with ``cubit.get_all_ids_from_name``
    """
    parts = _get_volumes_from_name(names)
    part_ids = [part.id() for part in parts]
    part_string = " ".join(map(str, part_ids))

    cubit_command_or_exit(f"imprint volume {part_string}")
    cubit_command_or_exit(f"merge volume {part_string}")


def partition(input_file,
              output_file=parsers.partition_defaults["output_file"],
              center=parsers.partition_defaults["center"],
              xvector=parsers.partition_defaults["xvector"],
              zvector=parsers.partition_defaults["zvector"],
              part_name=parsers.partition_defaults["part_name"],
              big_number=parsers.partition_defaults["big_number"]):
    """Partition Cubit files with pyramidal body intersections defined by a cube's center and vertices and with local
    coordinate planes.

    :param str input_file: Cubit ``*.cub`` file to open that already contains parts/volumes to be meshed
    :param str output_file: Cubit ``*.cub`` file to write
    :param list center: center location of the geometry
    :param list xvector: Local x-axis vector defined in global coordinates
    :param list zvector: Local z-axis vector defined in global coordinates
    :param list part_name: part/volume name prefixes
    :param float big_number: Number larger than the outer radius of the part to partition.
    """
    cubit.init(["cubit"])
    part_name = _mixed_utilities.cubit_part_names(part_name)

    if output_file is None:
        output_file = input_file
    input_file = pathlib.Path(input_file).with_suffix(".cub")
    output_file = pathlib.Path(output_file).with_suffix(".cub")
    with tempfile.NamedTemporaryFile(suffix=".cub", dir=".") as copy_file:
        shutil.copyfile(input_file, copy_file.name)
        cubit_command_or_exit(f"open '{copy_file.name}'")
        _partition(center, xvector, zvector, part_name, big_number)
        cubit_command_or_exit(f"save as '{output_file}' overwrite")


def _partition(center=parsers.partition_defaults["center"],
               xvector=parsers.partition_defaults["xvector"],
               zvector=parsers.partition_defaults["zvector"],
               part_name=parsers.partition_defaults["part_name"],
               big_number=parsers.partition_defaults["big_number"]):
    """Partition Cubit files with pyramidal body intersections defined by a cube's center and vertices and with local
    coordinate planes.

    :param list center: center location of the geometry
    :param list xvector: Local x-axis vector defined in global coordinates
    :param list zvector: Local z-axis vector defined in global coordinates
    :param list part_name: part/volume name prefixes
    :param float big_number: Number larger than the outer radius of the part to partition.
    """

    center = numpy.array(center)
    xvector = numpy.array(xvector)
    zvector = numpy.array(zvector)
    yvector = numpy.cross(zvector, xvector)

    # TODO: VV Move pyramid volume creation to a dedicated function VV
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/75
    # Create 6 4-sided pyramidal bodies defining the partitioning intersections
    surface_coordinates = vertices.pyramid_surfaces(center, xvector, zvector, big_number)
    pyramid_surfaces = [_create_surface_from_coordinates(coordinates) for coordinates in surface_coordinates]

    # Identify surfaces for individual pyramid volumes based on location relative to local coordinate system
    pyramid_volume_surfaces = [
        _surfaces_by_vector(pyramid_surfaces,  yvector, center),  # +Y
        _surfaces_by_vector(pyramid_surfaces, -yvector, center),  # -Y
        _surfaces_by_vector(pyramid_surfaces,  xvector, center),  # +X
        _surfaces_by_vector(pyramid_surfaces, -xvector, center),  # -X
        _surfaces_by_vector(pyramid_surfaces,  zvector, center),  # +Z
        _surfaces_by_vector(pyramid_surfaces, -zvector, center),  # -Z
    ]
    pyramid_volumes = [_create_volume_from_surfaces(surface_list) for surface_list in pyramid_volume_surfaces]
    pyramid_volume_numbers = [pyramid.id() for pyramid in pyramid_volumes]
    pyramid_volume_string = " ". join(map(str, pyramid_volume_numbers))

    # Remove pyramidal construction surfaces
    surface_numbers = _surface_numbers(pyramid_surfaces)
    surface_string = " ".join(map(str, surface_numbers))
    cubit_command_or_exit(f"delete surface {surface_string}")
    # TODO: ^^ Move pyramid volume creation to a dedicated function ^^

    # Create local coordinate system primary planes
    yvector = numpy.cross(zvector, xvector)
    surface_coordinates = [
        numpy.array([center, center + xvector, center + yvector]),
        numpy.array([center, center + yvector, center + zvector]),
        numpy.array([center, center + zvector, center + xvector]),
    ]
    primary_surfaces = [_create_surface_from_coordinates(coordinates) for coordinates in surface_coordinates]
    primary_surface_numbers = _surface_numbers(primary_surfaces)
    primary_surface_string = " ".join(map(str, primary_surface_numbers))

    # Create intersections/partitions
    parts = _get_volumes_from_name(part_name)
    for volume in pyramid_volumes:
        volume_id = volume.id()
        for part in parts:
            cubit_command_or_exit(f"intersect volume {volume_id} with volume {part.id()} keep")
    for part in parts:
        cubit_command_or_exit(f"delete volume {part.id()}")

    # Webcut with local coordinate system primary planes
    for number in primary_surface_numbers:
        parts = _get_volumes_from_name(part_name)
        part_ids = [part.id() for part in parts]
        part_string = " ".join(map(str, part_ids))
        cubit_command_or_exit(f"webcut volume {part_string} with plane from surface {number}")

    # Clean up pyramid volumes and primary surfaces
    cubit_command_or_exit(f"delete volume {pyramid_volume_string}")
    cubit_command_or_exit(f"delete surface {primary_surface_string}")

    # Imprint and merge
    for current_part_name in part_name:
        imprint_and_merge([current_part_name])


def mesh(input_file, element_type,
         output_file=parsers.mesh_defaults["output_file"],
         part_name=parsers.mesh_defaults["part_name"],
         global_seed=parsers.mesh_defaults["global_seed"]):
    """Mesh Cubit volumes and sheet bodies by part/volume name

    :param str input_file: Cubit ``*.cub`` file to open that already contains parts/volumes to be meshed
    :param str element_type: Cubit scheme "trimesh" or "tetmesh". Else ignored.
    :param str output_file: Cubit ``*.cub`` file to write
    :param str part_name: part/volume name prefix
    :param float global_seed: The global mesh seed size
    """
    cubit.init(["cubit"])
    part_name = _mixed_utilities.cubit_part_names(part_name)

    if output_file is None:
        output_file = input_file
    input_file = pathlib.Path(input_file).with_suffix(".cub")
    output_file = pathlib.Path(output_file).with_suffix(".cub")
    with tempfile.NamedTemporaryFile(suffix=".cub", dir=".") as copy_file:
        shutil.copyfile(input_file, copy_file.name)
        cubit_command_or_exit(f"open '{copy_file.name}'")
        _mesh(element_type, part_name, global_seed)
        cubit_command_or_exit(f"save as '{output_file}' overwrite")


def _mesh_sheet_body(volume, global_seed, element_type=None):
    """Mesh a volume that is a sheet body

    Assumes ``cubit.is_sheet_body(volume.id())`` is ``True``.

    :param cubit.Volume volume: Cubit volume to mesh as a sheet body
    :param float global_seed: Seed size, e.g. ``cubit.cmd(surface {} size {global_seed}``
    :param str element_type: Cubit meshing scheme. Accepts 'trimesh' or is ignored.
    """
    # TODO: Process multiple sheet bodies with a single Cubit command set
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/80
    surface_objects = volume.surfaces()
    surfaces = [surface.id() for surface in surface_objects]
    surface_string = " ".join(map(str, surfaces))
    if element_type == "trimesh":
        cubit_command_or_exit(f"surface {surface_string} scheme {element_type}")
    cubit_command_or_exit(f"surface {surface_string} size {global_seed}")
    for surface in surface_objects:
        surface.mesh()


def _mesh_volume(volume, global_seed, element_type=None):
    """Mesh a volume

    :param cubit.Volume volume: Cubit volume to mesh
    :param float global_seed: Seed size, e.g. ``cubit.cmd(volume {} size {global_seed}``
    :param str element_type: Cubit meshing scheme. Accepts 'tetmesh' or is ignored.
    """
    # TODO: Process multiple volumes with a single Cubit command set
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/80
    volume_id = volume.id()
    if element_type == "tetmesh":
        cubit_command_or_exit(f"volume {volume_id} scheme {element_type}")
    cubit_command_or_exit(f"volume {volume_id} size {global_seed}")
    volume.mesh()


def _mesh_multiple_volumes(volumes, global_seed, element_type=None):
    """Mesh ``cubit.Volume`` objects as volumes or sheet bodies

    :param list volumes: list of Cubit volume objects to mesh
    """
    # TODO: Process all sheet bodies and all volumes with a single Cubit command set
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/80
    for volume in volumes:
        volume_id = volume.id()
        if cubit.is_sheet_body(volume_id):
            _mesh_sheet_body(volume, global_seed, element_type=element_type)
        else:
            _mesh_volume(volume, global_seed, element_type=element_type)


def _mesh(element_type, part_name, global_seed):
    """Mesh Cubit volumes and sheet bodies by part/volume name

    :param str element_type: Cubit scheme "trimesh" or "tetmesh". Else ignored.
    :param str part_name: part/volume name prefix
    :param float global_seed: The global mesh seed size
    """
    parts = _get_volumes_from_name_or_exit(part_name)
    element_type = element_type.lower()
    _mesh_multiple_volumes(parts, global_seed, element_type=element_type)


def merge(input_file, output_file):
    """Merge Cubit ``*.cub`` files with forced unique block IDs and save to output file

    :param list input_file: List of Cubit ``*.cub`` file(s) to merge
    :param str output_file: Cubit ``*.cub`` file to write
    """
    cubit.init(["cubit"])
    input_file = [pathlib.Path(path).with_suffix(".cub") for path in input_file]
    output_file = pathlib.Path(output_file).with_suffix(".cub")
    for path in input_file:
        cubit_command_or_exit(f"import cubit '{path}' unique_genesis_ids")
    cubit_command_or_exit(f"save as '{output_file}' overwrite")


def export(input_file,
           part_name=parsers.export_defaults["part_name"],
           element_type=parsers.export_defaults["element_type"],
           destination=parsers.export_defaults["destination"],
           output_type=parsers.export_defaults["output_type"]):
    """Open a Cubit ``*.cub`` file and export ``part_name`` prefixed volumes as ``part_name``.inp

    :param str input_file: Cubit ``*.cub`` file to open that already contains meshed parts/volumes
    :param str part_name: list of part/volume name prefix to export
    :param list element_type: list of element types, one per part name or one global replacement for every part name
    :param str destination: write output orphan mesh files to this output directory
    """
    cubit.init(["cubit"])
    part_name = _mixed_utilities.cubit_part_names(part_name)
    element_type = _mixed_utilities.validate_element_type_or_exit(length_part_name=len(part_name), element_type=element_type)
    input_file = pathlib.Path(input_file).with_suffix(".cub")
    destination = pathlib.Path(destination)

    cubit_command_or_exit(f"open '{input_file}'")

    if output_type.lower() == "abaqus":
        _export_abaqus_list(part_name, element_type, destination)
    elif output_type.lower().startswith("genesis"):
        output_file = destination / input_file.with_suffix(".g").name
        _export_genesis(output_file, part_name, element_type, output_type)
    else:
        sys.exit(f"Uknown output type request '{output_type}'")


def _create_new_block(volumes):
    """Create a new block for all volumes in list

    Sheet bodies are added to block as surfaces. Volumes are added as volumes.

    :param list volumes: list of Cubit volume objects

    :returns: new block ID
    :rtype: int
    """
    new_block_id = cubit.get_next_block_id()
    volume_ids = [volume.id() for volume in volumes]
    volume_string = " ".join(map(str, volume_ids))
    if any([cubit.is_sheet_body(volume_id) for volume_id in volume_ids]):
        surfaces = _surface_numbers(_surfaces_for_volumes(volumes))
        surface_string = " ".join(map(str, surfaces))
        cubit_command_or_exit(f"block {new_block_id} add surface {surface_string}")
    else:
        cubit_command_or_exit(f"block {new_block_id} add volume {volume_string}")
    return new_block_id


def _create_volume_name_block(name):
    """Create a new block with all volumes prefixed by name

    :param str name: Name for new block and prefix for volume search

    :returns: New block ID
    :rtype: int
    """
    volumes = _get_volumes_from_name(name)
    new_block_id = _create_new_block(volumes)
    cubit_command_or_exit(f"block {new_block_id} name '{name}'")
    return new_block_id


def _set_genesis_output_type(output_type):
    """Set Cubit exodus/genesis output type

    :param str output_type: String identifying genesis output type: genesis (large format), genesis-normal, genesis-hdf5
    """
    if output_type.lower() == "genesis":
        cubit_command_or_exit(f"set large exodus file on")
    elif output_type.lower() == "genesis-normal":
        cubit_command_or_exit(f"set large exodus file off")
    elif output_type.lower() == "genesis-hdf5":
        cubit_command_or_exit(f"set exodus netcdf4 on")
    else:
        raise RuntimeError("Unknown genesis output type '{output_type}'")


@_mixed_utilities.print_exception_message
def _set_genesis_output_type_or_exit(*args, **kwargs):
    """Thin wrapper around :meth:`turbo_turtle._cubit_python._set_genesis_output_type` to call sys exit on exceptions"""
    return _set_genesis_output_type(*args, **kwargs)


def _export_genesis(output_file, part_name, element_type, output_type="genesis"):
    """Export all volumes with part name prefix to the output file

    Always creates new blocks named after the part/volume prefix.

    :param pathlib.Path output_file: Genesis file to write
    :param list part_name: list of part/volume names to create as blocks from all volumes with a matching prefix
    :param list element_type: list of element type strings
    :param str output_type: String identifying genesis output type: genesis (large format), genesis-normal, genesis-hdf5
    """
    block_ids = []
    for name, element in zip(part_name, element_type):
        block_ids.append(_create_volume_name_block(name))
        if element_type is not None:
            cubit_command_or_exit(f"block {block_ids[-1]} element type {element}")
    _set_genesis_output_type_or_exit(output_type)
    block_string = " ".join(map(str, block_ids))
    cubit_command_or_exit(f"export mesh '{output_file}' block {block_string} overwrite")


def _export_abaqus_list(part_name, element_type, destination):
    """Export one Abaqus orphan mesh per part in the destination directory

    :param list part_name: list of part/volume names to create as blocks from all volumes with a matching prefix
    :param list element_type: List of element type strings
    :param pathlib.Path destination: Parent directory for orphan mesh files
    """
    for name, element in zip(part_name, element_type):
        output_file = destination / name
        output_file = output_file.with_suffix(".inp")
        _export_abaqus(output_file, name)
        if element is not None:
            _mixed_utilities.substitute_element_type(output_file, element)


def _export_abaqus(output_file, part_name):
    """Create a block named after the part, add all volumes/surfaace with name prefix, export an Abaqus orphan mesh file

    :param pathlib.Path output_file: Abaqus file to write
    :param str part_name: part/volume name to create as blocks from all volumes with a matching prefix
    """
    new_block_id = _create_volume_name_block(part_name)
    cubit_command_or_exit(f"export abaqus '{output_file}' block {new_block_id} partial overwrite")


def image(input_file, output_file, cubit_command,
          x_angle=parsers.image_defaults["x_angle"],
          y_angle=parsers.image_defaults["y_angle"],
          z_angle=parsers.image_defaults["z_angle"],
          image_size=parsers.image_defaults["image_size"]):
    """Open a Cubit ``*.cub`` file and save an image

    Uses the Cubit APREPRO `hardcopy`_ command, which accepts jpg, gif, bmp, pnm, tiff, and eps file extensions. This
    command only works in batch mode from Cubit APREPRO journal files, so an ``input_file``.jou is created for
    execution.

    :param str input_file: Cubit ``*.cub`` file to open that already contains parts/volumes to be meshed
    :param str output_file: Screenshot file to write
    :param float x_angle: Rotation about 'world' X-axis in degrees
    :param float y_angle: Rotation about 'world' Y-axis in degrees
    :param float z_angle: Rotation about 'world' Z-axis in degrees
    """
    input_file = pathlib.Path(input_file).with_suffix(".cub")
    output_file = pathlib.Path(output_file)
    output_type = output_file.suffix.strip('.')

    journal_path = output_file.with_suffix(".jou")
    with open(journal_path, "w") as journal_file:
        journal_file.write(f"open '{input_file}'\n")
        journal_file.write(f"graphics windowsize {image_size[0]} {image_size[1]}\n")
        journal_file.write(f"rotate {x_angle} about world x\n")
        journal_file.write(f"rotate {y_angle} about world y\n")
        journal_file.write(f"rotate {z_angle} about world z\n")
        journal_file.write(f"hardcopy '{output_file}' {output_type}\n")

    command = f"{cubit_command} -batch {journal_path}"
    _utilities.run_command(command)
