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
    part_name = _mixed_utilities.cubit_part_names(part_name)
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
                      planar=parsers.geometry_default_planar,
                      revolution_angle=parsers.geometry_default_revolution_angle):
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


def _get_volumes_from_name(name):
    """Return all volume objects with the prefix ``name``

    :param str name: Name prefix to search for with ``cubit.get_all_ids_from_name``

    :returns: list of Cubit volumes with name prefix
    :rtype: list of cubit.Volume objects
    """
    parts = [cubit.volume(number) for number in cubit.get_all_ids_from_name("volume", name)]
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
    part_name = _mixed_utilities.cubit_part_names(part_name)
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

    center_3d = numpy.append(center, [0.])
    curves = []
    curves.append(_create_arc_from_coordinates(center_3d, inner_point1, inner_point2))
    curves.append(_create_arc_from_coordinates(center_3d, outer_point1, outer_point2))
    curves.append(_create_curve_from_coordinates(inner_point1, outer_point1))
    curves.append(_create_curve_from_coordinates(inner_point2, outer_point2))
    surface = cubit.create_surface(curves)

    _rename_and_sweep(surface, part_name, revolution_angle=revolution_angle, center=center_3d)


def partition(input_file,
              output_file=parsers.partition_default_output_file,
              center=parsers.partition_default_center,
              xvector=parsers.partition_default_xvector,
              zvector=parsers.partition_default_zvector,
              part_name=parsers.partition_default_part_name,
              big_number=parsers.partition_default_big_number):
    """Partition Cubit files with pyramidal body intersections defined by a cube's center and vertices and with local
    coordinate planes.

    :param str input_file: Cubit ``*.cub`` file to open that already contains parts/volumes to be meshed
    :param str output_file: Cubit ``*.cub`` file to write
    :param list center: center location of the geometry
    :param list xvector: Local x-axis vector defined in global coordinates
    :param list zvector: Local z-axis vector defined in global coordinates
    :param str part_name: part/volume name prefix
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


def _partition(center=parsers.partition_default_center,
               xvector=parsers.partition_default_xvector,
               zvector=parsers.partition_default_zvector,
               part_name=parsers.partition_default_part_name,
               big_number=parsers.partition_default_big_number):
    """Partition Cubit files with pyramidal body intersections defined by a cube's center and vertices and with local
    coordinate planes.

    :param list center: center location of the geometry
    :param list xvector: Local x-axis vector defined in global coordinates
    :param list zvector: Local z-axis vector defined in global coordinates
    :param str part_name: part/volume name prefix
    :param float big_number: Number larger than the outer radius of the part to partition.
    """

    center = numpy.array(center)
    xvector = numpy.array(xvector)
    zvector = numpy.array(zvector)
    parts = _get_volumes_from_name(part_name)

    # Create 6 4-sided pyramidal bodies defining the partitioning intersections
    surface_coordinates = vertices.pyramid_surfaces(center, xvector, zvector, big_number)
    surfaces = [_create_surface_from_coordinates(coordinates) for coordinates in surface_coordinates]

    # TODO: Figure out how to cleanup these coordinate pairs such that they are independent from the
    # fortyfives/pyramid_surfaces indices
    volume_surfaces = [
        surfaces[0:4] + [surfaces[12]],  # +Y
        surfaces[4:8] + [surfaces[13]],  # -Y
        [surfaces[3], surfaces[7], surfaces[8], surfaces[9], surfaces[14]],   # +X
        [surfaces[1], surfaces[5], surfaces[10], surfaces[11], surfaces[15]], # -X
        [surfaces[0], surfaces[4], surfaces[8], surfaces[10], surfaces[16]],  # +Z
        [surfaces[2], surfaces[6], surfaces[9], surfaces[11], surfaces[17]],  # -Z
    ]
    volumes = [_create_volume_from_surfaces(surface_list) for surface_list in volume_surfaces]

    # Remove pyramidal construction surfaces
    surface_numbers = _surface_numbers(surfaces)
    surface_string = " ".join(map(str, surface_numbers))
    cubit_command_or_exit(f"delete surface {surface_string}")

    # Create intersections/partitions
    for number, volume in enumerate(volumes):
        volume_id = volume.id()
        for part in parts:
            cubit_command_or_exit(f"intersect volume {volume_id} with volume {part.id()} keep")
        cubit_command_or_exit(f"delete volume {volume_id}")
    for part in parts:
        cubit_command_or_exit(f"delete volume {part.id()}")

    # Create local coordinate system primary planes and webcut
    yvector = numpy.cross(zvector, xvector)
    surface_coordinates = [
        numpy.array([center, center + xvector, center + yvector]),
        numpy.array([center, center + yvector, center + zvector]),
        numpy.array([center, center + zvector, center + xvector]),
    ]
    surfaces = [_create_surface_from_coordinates(coordinates) for coordinates in surface_coordinates]
    surface_numbers = _surface_numbers(surfaces)
    for number in surface_numbers:
        cubit_command_or_exit(f"webcut volume all with plane from surface {number}")
    surface_string = " ".join(map(str, surface_numbers))
    cubit_command_or_exit(f"delete surface {surface_string}")

    # Imprint and merge
    parts = _get_volumes_from_name(part_name)
    part_ids = [part.id() for part in parts]
    part_string = " ".join(map(str, part_ids))
    cubit_command_or_exit(f"imprint volume {part_string}")
    cubit_command_or_exit(f"merge volume {part_string}")


def mesh(input_file, element_type,
         output_file=parsers.mesh_default_output_file,
         part_name=parsers.mesh_default_part_name,
         global_seed=parsers.mesh_default_global_seed):
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


def export(input_file,
           part_name=parsers.export_default_part_name,
           element_type=parsers.export_default_element_type,
           destination=parsers.export_default_destination):
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
    for name, element in zip(part_name, element_type):
        output_file = destination / name
        output_file = output_file.with_suffix(".inp")
        _export_abaqus(output_file, name, element, destination)
        if element is not None:
            _mixed_utilities.substitute_element_type(output_file, element)


def _export_abaqus(output_file, part_name, element_type, destination):
    # Manage block ID
    blocks_before = cubit.get_block_id_list()
    if len(blocks_before) >= 1:
        max_block_id = max(blocks_before)
    else:
        max_block_id = 0
    new_block_id = max_block_id + 1

    # Get a list of part_name prefixed volumes
    parts = _get_volumes_from_name(part_name)
    part_ids = [part.id() for part in parts]
    part_string = " ".join(map(str, part_ids))

    if any([cubit.is_sheet_body(part_id) for part_id in part_ids]):
        surfaces = []
        for part in parts:
            surfaces.extend(_surface_numbers(part.surfaces()))
        surface_string = " ".join(map(str, surfaces))
        cubit.cmd(f"block {new_block_id} add surface {surface_string}")
    else:
        cubit.cmd(f"block {new_block_id} add volume {part_string}")

    cubit.cmd(f"block {new_block_id} name '{part_name}'")
    cubit.cmd(f"export abaqus '{output_file}' block {new_block_id} partial overwrite")


def image(input_file, output_file, cubit_command,
          x_angle=parsers.image_default_x_angle,
          y_angle=parsers.image_default_y_angle,
          z_angle=parsers.image_default_z_angle,
          image_size=parsers.image_default_image_size):
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
