"""Python 3 module that imports python-gmsh."""

import pathlib
import typing

import numpy

from turbo_turtle import _utilities
from turbo_turtle._abaqus_python.turbo_turtle_abaqus import _mixed_utilities, parsers, vertices

gmsh = _utilities.import_gmsh()


def geometry(
    input_file: typing.Sequence[str | pathlib.Path],
    output_file: str | pathlib.Path,
    planar: bool = parsers.geometry_defaults["planar"],  # type: ignore[assignment]
    model_name: str = parsers.geometry_defaults["model_name"],  # type: ignore[assignment]
    part_name: str = parsers.geometry_defaults["part_name"],  # type: ignore[assignment]
    unit_conversion: float = parsers.geometry_defaults["unit_conversion"],  # type: ignore[assignment]
    euclidean_distance: float = parsers.geometry_defaults["euclidean_distance"],  # type: ignore[assignment]
    delimiter: str = parsers.geometry_defaults["delimiter"],  # type: ignore[assignment]
    header_lines: int = parsers.geometry_defaults["header_lines"],  # type: ignore[assignment]
    revolution_angle: float = parsers.geometry_defaults["revolution_angle"],  # type: ignore[assignment]
    y_offset: float = parsers.geometry_defaults["y_offset"],  # type: ignore[assignment]
    rtol: float = parsers.geometry_defaults["rtol"],  # type: ignore[assignment]
    atol: float = parsers.geometry_defaults["atol"],  # type: ignore[assignment]
) -> None:
    """Create 2D planar, 2D axisymmetric, or 3D revolved geometry from an array of XY coordinates.

    Note that 2D axisymmetric sketches and sketches for 3D bodies of revolution about the global Y-axis must lie
    entirely on the positive-X side of the global Y-axis.

    This function can create multiple surfaces or volumes in the same Gmsh ``*.step`` file. If no part (body/volume)
    names are provided, the body/volume will be named after the input file base name.

    :param input_file: input text file(s) with coordinates to draw
    :param output_file: Gmsh ``*.step`` database to save the part(s)
    :param planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param model_name: name of the Gmsh model in which to create the part
    :param part_name: name(s) of the part(s) being created
    :param unit_conversion: multiplication factor applies to all coordinates
    :param euclidean_distance: if the distance between two coordinates is greater than this, draw a straight line.
        Distance should be provided in units *after* the unit conversion
    :param delimiter: character to use as a delimiter when reading the input file
    :param header_lines: number of lines in the header to skip when reading the input file
    :param revolution_angle: angle of solid revolution for ``3D`` geometries. Ignore when planar is True.
    :param y_offset: vertical offset along the global Y-axis. Offset should be provided in units *after* the unit
        conversion.
    :param rtol: relative tolerance for vertical/horizontal line checks
    :param atol: absolute tolerance for vertical/horizontal line checks

    :returns: writes ``{output_file}.step``
    """
    # Universally required setup
    gmsh.initialize()
    gmsh.logger.start()

    # Input/Output setup
    # TODO: allow other output formats supported by Gmsh
    output_file = pathlib.Path(output_file).with_suffix(".step")

    # Model setup
    gmsh.model.add(model_name)
    part_name = _mixed_utilities.validate_part_name(input_file, part_name)
    part_name = _mixed_utilities.cubit_part_names(part_name)

    # Create part(s)
    surfaces = []
    for file_name, _new_part in zip(input_file, part_name, strict=True):
        coordinates = _mixed_utilities.return_genfromtxt(
            file_name, delimiter, header_lines, expected_dimensions=2, expected_columns=2
        )
        coordinates = vertices.scale_and_offset_coordinates(coordinates, unit_conversion, y_offset)
        lines_and_splines = vertices.ordered_lines_and_splines(coordinates, euclidean_distance, rtol=rtol, atol=atol)
        surfaces.append(_draw_surface(lines_and_splines))

    # Conditionally create the 3D revolved shape
    for surface, new_part in zip(surfaces, part_name, strict=True):
        _rename_and_sweep(surface, new_part, planar=planar, revolution_angle=revolution_angle)

    # Output and cleanup
    # FIXME: Write physical groups to geometry output files
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/221
    gmsh.write(str(output_file))
    gmsh.logger.stop()
    gmsh.finalize()


def _draw_surface(lines_and_splines: list[numpy.ndarray]) -> int:
    """Given ordered lists of line/spline coordinates, create a Gmsh 2D surface object.

    :param lines_and_splines: list of [N, 2] shaped arrays of (x, y) coordinates defining a line (N=2) or spline
        (N>2)

    :returns: Gmsh 2D entity tag
    """
    curves = []
    for coordinates in lines_and_splines:
        if len(coordinates) == 2:
            point1 = (*tuple(coordinates[0]), 0.0)
            point2 = (*tuple(coordinates[1]), 0.0)
            curves.append(_create_line_from_coordinates(point1, point2))
        else:
            zero_column = numpy.zeros([len(coordinates), 1])
            spline_3d = numpy.append(coordinates, zero_column, axis=1)
            curves.append(_create_spline_from_coordinates(spline_3d))

    curve_loop = gmsh.model.occ.addCurveLoop(curves)
    return gmsh.model.occ.addPlaneSurface([curve_loop])


def _create_line_from_coordinates(point1: tuple[float, float, float], point2: tuple[float, float, float]) -> int:
    """Create a curve from 2 three-dimensional coordinates.

    :param point1: First set of coordinates (x1, y1, z1)
    :param point2: Second set of coordinates (x2, y2, z2)

    :returns: Gmsh 1D entity tag
    """
    point1_tag = gmsh.model.occ.addPoint(*point1)
    point2_tag = gmsh.model.occ.addPoint(*point2)
    return gmsh.model.occ.addLine(point1_tag, point2_tag)


def _create_spline_from_coordinates(coordinates: typing.Sequence[tuple[float, float, float]] | numpy.ndarray) -> int:
    """Create a spline from a sequence of coordinates.

    :param coordinates: [N, 3] array of coordinates (x, y, z)

    :returns: Gmsh 1D entity tag
    """
    coordinates = numpy.array(coordinates)
    minimum = 2
    if coordinates.shape[0] < minimum:
        raise RuntimeError(f"Requires at least {minimum} coordinates to create a spline")

    points = [gmsh.model.occ.addPoint(*tuple(point)) for point in coordinates]

    return gmsh.model.occ.addBSpline(points)


def _rename_and_sweep(
    surface: int,
    part_name: str,
    center: tuple[float, float, float] | numpy.ndarray = (0.0, 0.0, 0.0),
    planar: bool = parsers.geometry_defaults["planar"],  # type: ignore[assignment]
    revolution_angle: float = parsers.geometry_defaults["revolution_angle"],  # type: ignore[assignment]
) -> typing.Tuple[int, int]:
    """Recover surface, sweep part if required, and rename surface/volume by part name.

    Hyphens are replaced by underscores to make the ACIS engine happy.

    :param surface: Gmsh surface tag to rename and conditionally sweep
    :param part_name: name(s) of the part(s) being created
    :param center: coordinate location for the center of axisymmetric sweep
    :param planar: switch to indicate that 2D model dimensionality is planar, not axisymmetric
    :param revolution_angle: angle of solid revolution for ``3D`` geometries. Ignore when planar is True.

    :returns: Gmsh dimTag (dimension, tag)
    """
    center = numpy.array(center)
    revolution_axis = numpy.array([0.0, 1.0, 0.0])
    if planar:
        dim_tag = (2, surface)
    elif numpy.isclose(revolution_angle, 0.0):
        dim_tag = (2, surface)
    else:
        # Using naming convention of the external library, Gmsh
        dimTags = gmsh.model.occ.revolve(  # noqa: N806
            [(2, surface)],
            *center,
            *revolution_axis,
            numpy.radians(revolution_angle),
        )
        dim_tag = dimTags[0]

    part_dimension = dim_tag[0]
    part_tag = dim_tag[0]
    part_name = _mixed_utilities.cubit_part_names(part_name)
    gmsh.model.occ.synchronize()
    part_tag = gmsh.model.addPhysicalGroup(part_dimension, [part_tag], name=part_name)

    return dim_tag


def cylinder(
    inner_radius: float,
    outer_radius: float,
    height: float,
    output_file: str | pathlib.Path,
    model_name: str = parsers.geometry_defaults["model_name"],  # type: ignore[assignment]
    part_name: str = parsers.cylinder_defaults["part_name"],  # type: ignore[assignment]
    revolution_angle: float = parsers.geometry_defaults["revolution_angle"],  # type: ignore[assignment]
    y_offset: float = parsers.cylinder_defaults["y_offset"],  # type: ignore[assignment]
) -> None:
    """Accept dimensions of a right circular cylinder and generate an axisymmetric revolved geometry.

    Centroid of cylinder is located on the global coordinate origin by default.

    :param inner_radius: Radius of the hollow center
    :param outer_radius: Outer radius of the cylinder
    :param height: Height of the cylinder
    :param output_file: Gmsh ``*.step`` file to save the part(s)
    :param model_name: name of the Gmsh model in which to create the part
    :param part_name: name(s) of the part(s) being created
    :param revolution_angle: angle of solid revolution for ``3D`` geometries
    :param y_offset: vertical offset along the global Y-axis
    """
    # Universally required setup
    gmsh.initialize()
    gmsh.logger.start()

    # Input/Output setup
    # TODO: allow other output formats supported by Gmsh
    output_file = pathlib.Path(output_file).with_suffix(".step")
    gmsh.model.add(model_name)

    # Create the 2D axisymmetric shape
    lines = vertices.cylinder_lines(inner_radius, outer_radius, height, y_offset=y_offset)
    surface_tag = _draw_surface(lines)

    # Conditionally create the 3D revolved shape
    _rename_and_sweep(surface_tag, part_name, revolution_angle=revolution_angle)

    # Output and cleanup
    # FIXME: Write physical groups to geometry output files
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/221
    gmsh.write(str(output_file))
    gmsh.logger.stop()
    gmsh.finalize()


def sphere(
    inner_radius: float,
    outer_radius: float,
    output_file: str | pathlib.Path,
    input_file: str | pathlib.Path | None = parsers.sphere_defaults["input_file"],  # type: ignore[assignment]
    quadrant: typing.Literal["upper", "lower", "both"] = parsers.sphere_defaults["quadrant"],  # type: ignore[assignment]
    revolution_angle: float = parsers.sphere_defaults["revolution_angle"],  # type: ignore[assignment]
    y_offset: float = parsers.sphere_defaults["y_offset"],  # type: ignore[assignment]
    model_name: str = parsers.sphere_defaults["model_name"],  # type: ignore[assignment]
    part_name: str = parsers.sphere_defaults["part_name"],  # type: ignore[assignment]
) -> None:
    """Create a sphere geometry with file I/O handling.

    :param inner_radius: inner radius (size of hollow)
    :param outer_radius: outer radius (size of sphere)
    :param output_file: output file name. Will be stripped of the extension and ``.step`` will be used.
    :param input_file: input file name. Will be stripped of the extension and ``.step`` will be used.
    :param quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param revolution_angle: angle of rotation 0.-360.0 degrees. Provide 0 for a 2D axisymmetric model.
    :param y_offset: vertical offset along the global Y-axis
    :param model_name: name of the Gmsh model in which to create the part
    :param part_name: name of the part to be created in the Abaqus model
    """
    # Universally required setup
    gmsh.initialize()
    gmsh.logger.start()

    # Input/Output setup
    # TODO: allow other output formats supported by Gmsh
    output_file = pathlib.Path(output_file).with_suffix(".step")

    # Preserve the (X, Y) center implementation, but use the simpler y-offset interface
    center = (0.0, y_offset)

    if input_file is not None:
        # TODO: allow other input formats supported by Gmsh
        input_file = pathlib.Path(input_file).with_suffix(".step")
        # Avoid modifying the contents or timestamp on the input file.
        # Required to get conditional re-builds with a build system such as GNU Make, CMake, or SCons
        with _utilities.NamedTemporaryFileCopy(input_file, suffix=".step", dir=".") as copy_file:
            gmsh.open(copy_file.name)
            _sphere(
                inner_radius,
                outer_radius,
                quadrant=quadrant,
                revolution_angle=revolution_angle,
                center=center,
                part_name=part_name,
            )
            # FIXME: Write physical groups to geometry output files
            # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/221
            gmsh.write(str(output_file))
    else:
        gmsh.model.add(model_name)
        _sphere(
            inner_radius,
            outer_radius,
            quadrant=quadrant,
            revolution_angle=revolution_angle,
            center=center,
            part_name=part_name,
        )
        # FIXME: Write physical groups to geometry output files
        # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/221
        gmsh.write(str(output_file))

    # Output and cleanup
    gmsh.logger.stop()
    gmsh.finalize()


def _sphere(
    inner_radius: float,
    outer_radius: float,
    quadrant: str = parsers.sphere_defaults["quadrant"],  # type: ignore[assignment]
    revolution_angle: float = parsers.sphere_defaults["revolution_angle"],  # type: ignore[assignment]
    center: tuple[float, float] = parsers.sphere_defaults["center"],  # type: ignore[assignment]
    part_name: str = parsers.sphere_defaults["part_name"],  # type: ignore[assignment]
) -> None:
    """Create a sphere geometry without file I/O handling.

    :param inner_radius: inner radius (size of hollow)
    :param outer_radius: outer radius (size of sphere)
    :param quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param revolution_angle: angle of rotation 0.-360.0 degrees. Provide 0 for a 2D axisymmetric model.
    :param center: tuple of floats (X, Y) location for the center of the sphere
    :param part_name: name of the part to be created in the Abaqus model
    """
    # TODO: consolidate pure Python 3 logic in a common module for both Gmsh and Cubit
    # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/boards
    arc_points = vertices.sphere(center, inner_radius, outer_radius, quadrant)

    center_3d = numpy.append(center, [0.0])
    zero_column = numpy.zeros([len(arc_points), 1])
    arc_points_3d = numpy.append(arc_points, zero_column, axis=1)
    inner_point1 = arc_points_3d[0]
    inner_point2 = arc_points_3d[1]
    outer_point1 = arc_points_3d[2]
    outer_point2 = arc_points_3d[3]

    curves = []
    if numpy.allclose(inner_point1, center_3d) and numpy.allclose(inner_point2, center_3d):
        inner_point1 = center_3d
        inner_point2 = center_3d
    else:
        curves.append(_create_arc_from_coordinates(center_3d, inner_point1, inner_point2))
    curves.append(_create_line_from_coordinates(inner_point2, outer_point2))
    curves.append(_create_arc_from_coordinates(center_3d, outer_point2, outer_point1))
    curves.append(_create_line_from_coordinates(outer_point1, inner_point1))
    curve_loop = gmsh.model.occ.addCurveLoop(curves)
    surface = gmsh.model.occ.addPlaneSurface([curve_loop])

    _rename_and_sweep(surface, part_name, revolution_angle=revolution_angle, center=center_3d)


def _create_arc_from_coordinates(
    center: tuple[float, float, float] | numpy.ndarray,
    point1: tuple[float, float, float] | numpy.ndarray,
    point2: tuple[float, float, float] | numpy.ndarray,
) -> int:
    """Create a circle arc Gmsh object from center and points on the curve.

    :param center: tuple of floats (X, Y, Z) location for the center of the circle arc
    :param point1: tuple of floats (X, Y, Z) location for the first point on the arc
    :param point2: tuple of floats (X, Y, Z) location for the second point on the arc

    :returns: Gmsh curve tag
    """
    center_tag = gmsh.model.occ.addPoint(*center)
    point1_tag = gmsh.model.occ.addPoint(*point1)
    point2_tag = gmsh.model.occ.addPoint(*point2)

    return gmsh.model.occ.addCircleArc(point1_tag, center_tag, point2_tag, center=True)


# TODO: Remove ``noqa: ARG001`` when this function is implemented.
# https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/212
def partition(*args, **kwargs) -> typing.NoReturn:  # noqa: ARG001
    raise RuntimeError("partition subcommand is not yet implemented")


# TODO: Remove ``noqa: ARG001`` when this function is implemented.
def sets(*args, **kwargs) -> typing.NoReturn:  # noqa: ARG001
    raise RuntimeError("sets subcommand is not yet implemented")


# Argument(s) retained for compatibility with ``_cubit_python.mesh`` API
def mesh(
    input_file: str | pathlib.Path,
    element_type: str,  # noqa: ARG001
    output_file: str | pathlib.Path | None = parsers.mesh_defaults["output_file"],  # type: ignore[assignment]
    model_name: str | None = parsers.mesh_defaults["model_name"],  # type: ignore[assignment] # noqa: ARG001
    part_name: str | None = parsers.mesh_defaults["part_name"],  # type: ignore[assignment] # noqa: ARG001
    global_seed: float = parsers.mesh_defaults["global_seed"],  # type: ignore[assignment]
    edge_seeds: typing.Sequence[tuple[str, str | int | float]] | None = parsers.mesh_defaults["edge_seeds"],  # type: ignore[assignment] # noqa: ARG001
) -> None:
    """Mesh Gmsh physical entities by part name.

    :param input_file: Gmsh ``*.step`` file to open that already contains physical entities to be meshed
    :param element_type: Gmsh scheme.
    :param output_file: Gmsh mesh file to write
    :param model_name: name of the Gmsh model in which to create the part
    :param part_name: physical entity name prefix
    :param global_seed: The global mesh seed size
    :param edge_seeds: Edge seed tuples (name, number)
    """
    # Universally required setup
    gmsh.initialize()
    gmsh.logger.start()

    # Input/Output setup
    # TODO: allow other output formats supported by Gmsh
    input_file = pathlib.Path(input_file).with_suffix(".step")
    if output_file is None:
        output_file = input_file.with_suffix(".msh")
    output_file = pathlib.Path(output_file)

    with _utilities.NamedTemporaryFileCopy(input_file, suffix=input_file.suffix, dir=".") as copy_file:
        gmsh.open(copy_file.name)
        # TODO: Move to dedicated meshing function
        # TODO: Do physical group names apply to all dimensional entities associated with original name? Can we jump
        # straight to points with matching physical/entity names?
        # FIXME: The physical groups are not getting saved. Stop global application of seed without regard to
        # part/entity name.
        # https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/222
        points = gmsh.model.getEntities(dim=0)
        gmsh.model.mesh.setSize(points, global_seed)
        gmsh.model.mesh.generate(3)
        gmsh.write(str(output_file))

    gmsh.option.setNumber("Mesh.SaveGroupsOfElements", 1)
    gmsh.option.setNumber("Mesh.SaveGroupsOfNodes", 1)

    # Output and cleanup
    gmsh.logger.stop()
    gmsh.finalize()


# TODO: Remove ``noqa: ARG001`` when this function is implemented.
# https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/216
def merge(*args, **kwargs) -> typing.NoReturn:  # noqa: ARG001
    raise RuntimeError("merge subcommand is not yet implemented")


# TODO: Remove ``noqa: ARG001`` when this function is implemented.
def export(*args, **kwargs) -> typing.NoReturn:  # noqa: ARG001
    raise RuntimeError("export subcommand is not yet implemented")


def image(
    input_file: str | pathlib.Path,
    output_file: str | pathlib.Path,
    x_angle: float = parsers.image_defaults["x_angle"],  # type: ignore[assignment]
    y_angle: float = parsers.image_defaults["y_angle"],  # type: ignore[assignment]
    z_angle: float = parsers.image_defaults["z_angle"],  # type: ignore[assignment]
    # ARG001: Argument retained for compatibility with ``_cubit_python.image`` API
    image_size: tuple[int, int] = parsers.image_defaults["image_size"],  # type: ignore[assignment] # noqa: ARG001
) -> None:
    """Open a Gmsh geometry or mesh file and save an image.

    Uses the Gmsh ``write`` command, which accepts gif, jpg, tex, pdf, png, pgf, ps, ppm, svg, tikz, and yuv file
    extensions.

    :param str input_file: Gmsh input file to open
    :param str output_file: Screenshot file to write
    :param float x_angle: Rotation about 'world' X-axis in degrees
    :param float y_angle: Rotation about 'world' Y-axis in degrees
    :param float z_angle: Rotation about 'world' Z-axis in degrees
    :param tuple image_size: Image size in pixels (width, height)
    """
    # Universally required setup
    gmsh.initialize()
    gmsh.logger.start()

    # Input/Output setup
    input_file = pathlib.Path(input_file)
    output_file = pathlib.Path(output_file)

    gmsh.open(str(input_file))

    gmsh.fltk.initialize()
    gmsh.option.setNumber("General.Trackball", 0)
    gmsh.option.setNumber("General.RotationX", x_angle)
    gmsh.option.setNumber("General.RotationY", y_angle)
    gmsh.option.setNumber("General.RotationZ", z_angle)

    # Output and cleanup
    gmsh.write(str(output_file))
    gmsh.logger.stop()
    gmsh.finalize()
