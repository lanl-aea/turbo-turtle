import os
import sys
import shutil
import inspect
import tempfile

import numpy


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import parsers
import vertices
import _mixed_utilities


def main(inner_radius, outer_radius, output_file,
         input_file=parsers.sphere_default_input_file,
         quadrant=parsers.sphere_default_quadrant,
         revolution_angle=parsers.sphere_default_angle,
         y_offset=parsers.sphere_default_y_offset,
         model_name=parsers.sphere_default_model_name,
         part_name=parsers.sphere_default_part_name):
    """Wrap sphere function with file open and file write operations

    :param float inner_radius: inner radius (size of hollow)
    :param float outer_radius: outer radius (size of sphere)
    :param str output_file: output file name. Will be stripped of the extension and ``.cae`` will be used.
    :param str input_file: input file name. Will be stripped of the extension and ``.cae`` will be used.
    :param str quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param float revolution_angle: angle of rotation 0.-360.0 degrees. Provide 0 for a 2D axisymmetric model.
    :param float y_offset: vertical offset along the global Y-axis
    :param str model_name: name of the Abaqus model
    :param str part_name: name of the part to be created in the Abaqus model
    """
    import abaqus

    # Preserve the (X, Y) center implementation, but use the simpler y-offset interface
    center = (0., y_offset)

    output_file = os.path.splitext(output_file)[0] + ".cae"
    if input_file is not None:
        input_file = os.path.splitext(input_file)[0] + ".cae"
        # Avoid modifying the contents or timestamp on the input file.
        # Required to get conditional re-builds with a build system such as GNU Make, CMake, or SCons
        with tempfile.NamedTemporaryFile(suffix=".cae", dir=".") as copy_file:
            shutil.copyfile(input_file, copy_file.name)
            abaqus.openMdb(pathName=copy_file.name)
            sphere(inner_radius, outer_radius, quadrant=quadrant, revolution_angle=revolution_angle, center=center,
                   model_name=model_name, part_name=part_name)
            abaqus.mdb.saveAs(pathName=output_file)

    else:
        sphere(inner_radius, outer_radius, quadrant=quadrant, revolution_angle=revolution_angle, center=center,
               model_name=model_name, part_name=part_name)
        abaqus.mdb.saveAs(pathName=output_file)


def sphere(inner_radius, outer_radius,
           quadrant=parsers.sphere_default_quadrant,
           revolution_angle=parsers.sphere_default_angle,
           y_offset=parsers.sphere_default_y_offset,
           model_name=parsers.sphere_default_model_name,
           part_name=parsers.sphere_default_part_name):
    """Create a hollow, spherical geometry from a sketch in the X-Y plane with upper (+X+Y), lower (+X-Y), or both quadrants.

    .. warning::

       The lower quadrant creation is currently broken

    :param float inner_radius: inner radius (size of hollow)
    :param float outer_radius: outer radius (size of sphere)
    :param str quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param float revolution_angle: angle of rotation 0.-360.0 degrees. Provide 0 for a 2D axisymmetric model.
    :param float y_offset: vertical offset along the global Y-axis
    :param str model_name: name of the Abaqus model
    :param str part_name: name of the part to be created in the Abaqus model
    """
    import abaqus
    import abaqusConstants

    # Preserve the (X, Y) center implementation, but use the simpler y-offset interface
    center = (0., y_offset)

    if not quadrant in parsers.sphere_quadrant_options:
        message = "Quadrant option must be one of: {}".format(quadrant_options)
        _mixed_utilities.sys_exit(message)

    if not model_name in abaqus.mdb.models.keys():
        abaqus.mdb.Model(name=model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
    model = abaqus.mdb.models[model_name]

    arc_points = vertices.sphere(center, inner_radius, outer_radius, quadrant)
    inner_point1, inner_point2, outer_point1, outer_point2 = arc_points

    sketch = model.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    sketch.ArcByCenterEnds(center=center, point1=inner_point1, point2=inner_point2,
        direction=abaqusConstants.CLOCKWISE)
    sketch.ArcByCenterEnds(center=center, point1=outer_point1, point2=outer_point2,
        direction=abaqusConstants.CLOCKWISE)
    sketch.Line(point1=outer_point1, point2=inner_point1)
    sketch.Line(point1=outer_point2, point2=inner_point2)
    centerline = sketch.ConstructionLine(point1=center, angle=90.0)
    sketch.assignCenterline(line=centerline)

    if numpy.isclose(revolution_angle, 0.):
        part = model.Part(name=part_name, dimensionality=abaqusConstants.AXISYMMETRIC,
                          type=abaqusConstants.DEFORMABLE_BODY)
        part.BaseShell(sketch=sketch)
    else:
        part = model.Part(name=part_name, dimensionality=abaqusConstants.THREE_D, type=abaqusConstants.DEFORMABLE_BODY)
        part.BaseSolidRevolve(sketch=sketch, angle=revolution_angle, flipRevolveDirection=abaqusConstants.OFF)
    del sketch


if __name__ == "__main__":

    parser = parsers.sphere_parser(basename=basename)
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit as err:
        sys.exit(err.code)

    sys.exit(main(
        args.inner_radius,
        args.outer_radius,
        args.output_file,
        input_file=args.input_file,
        quadrant=args.quadrant,
        revolution_angle=args.revolution_angle,
        y_offset=args.y_offset,
        model_name=args.model_name,
        part_name=args.part_name
    ))
