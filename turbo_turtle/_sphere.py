import os
import sys
import numpy
import shutil

def sphere(inner_radius, outer_radius, output_file, input_file=None, quadrant="both", angle=360., center=(0., 0.),
           model_name="Model-1", part_name='sphere'):
    """Create a hollow, spherical geometry in the X-Y plane with upper (+Y), lower (-Y), or both quadrants.

    .. warning::

       The lower quadrant creation is currently broken

    :param float inner_radius: inner radius (size of hollow)
    :param float outer_radius: outer radius (size of sphere)
    :param str output_file: output file name. Will be stripped of the extension and ``.cae`` will be used.
    :param str input_file: input file name. Will be stripped of the extension and ``.cae`` will be used.
    :param str quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param float angle: angle of rotation 0.-360.0 degrees.
    :param tuple center: tuple of floats (X, Y) location for the center of the sphere
    :param str model_name: name of the Abaqus model
    :param str part_name: name of the part to be created in the Abaqus model
    """
    import abaqus
    import abaqusConstants

    quadrant_options = ("both", "upper", "lower")
    if not quadrant in quadrant_options:
        sys.stderr.write("Quadrant option must be one of: {}".format(quadrant_options))
        sys.exit(1)

    # Avoid modifying the contents or timestamp on the input file.
    # Required to get conditional re-builds with a build system such as GNU Make, CMake, or SCons
    output_file = os.path.splitext(output_file)[0]
    if input_file is None:
        input_file = output_file
    input_file = os.path.splitext(input_file)[0]
    input_with_extension = '{}.cae'.format(input_file)
    output_with_extension = '{}.cae'.format(output_file)
    if input_file != output_file:
        shutil.copyfile(input_with_extension, output_with_extension)

    if not model_name in abaqus.mdb.models.keys():
        abaqus.mdb.Model(name=model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)

    inner_radius = abs(inner_radius)
    outer_radius = abs(outer_radius)

    inner_point1 = tuple(numpy.array(center) + numpy.array((0.,  inner_radius)))
    outer_point1 = tuple(numpy.array(center) + numpy.array((0.,  outer_radius)))

    if quadrant == "both":
        inner_point1 = tuple(numpy.array(center) + numpy.array((0.,  inner_radius)))
        outer_point1 = tuple(numpy.array(center) + numpy.array((0.,  outer_radius)))

        inner_point2 = tuple(numpy.array(center) + numpy.array((0., -inner_radius)))
        outer_point2 = tuple(numpy.array(center) + numpy.array((0., -outer_radius)))

    elif quadrant == "upper":
        inner_point1 = tuple(numpy.array(center) + numpy.array((0.,  inner_radius)))
        outer_point1 = tuple(numpy.array(center) + numpy.array((0.,  outer_radius)))

        inner_point2 = tuple(numpy.array(center) + numpy.array((inner_radius, 0.)))
        outer_point2 = tuple(numpy.array(center) + numpy.array((outer_radius, 0.)))

    elif quadrant == "lower":
        inner_point2 = tuple(numpy.array(center) + numpy.array((0.,  -inner_radius)))
        outer_point2 = tuple(numpy.array(center) + numpy.array((0.,  -outer_radius)))

        inner_point1 = tuple(numpy.array(center) + numpy.array((inner_radius, 0.)))
        outer_point1 = tuple(numpy.array(center) + numpy.array((outer_radius, 0.)))

    s = abaqus.mdb.models[model_name].ConstrainedSketch(name='__profile__',
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=abaqusConstants.STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=center, point1=inner_point1, point2=inner_point2,
        direction=abaqusConstants.CLOCKWISE)
    s.ArcByCenterEnds(center=center, point1=outer_point1, point2=outer_point2,
        direction=abaqusConstants.CLOCKWISE)
    s.Line(point1=outer_point1, point2=inner_point1)
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.Line(point1=outer_point2, point2=inner_point2)
    if quadrant in ("upper", "lower"):
        s.HorizontalConstraint(entity=g[6], addUndoState=False)
    else:
        s.VerticalConstraint(entity=g[6], addUndoState=False)
    s.ConstructionLine(point1=center, angle=90.0)
    s.VerticalConstraint(entity=g[7], addUndoState=False)
    s.sketchOptions.setValues(constructionGeometry=abaqusConstants.ON)
    s.assignCenterline(line=g[7])
    p = abaqus.mdb.models[model_name].Part(name=part_name, dimensionality=abaqusConstants.THREE_D,
        type=abaqusConstants.DEFORMABLE_BODY)
    p.BaseSolidRevolve(sketch=s, angle=angle, flipRevolveDirection=abaqusConstants.OFF)
    del abaqus.mdb.models[model_name].sketches['__profile__']

    abaqus.mdb.saveAs(pathName=output_file)
