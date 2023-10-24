import os
import sys
import numpy
import shutil
import inspect
import argparse


def sphere(inner_radius, outer_radius, output_file, input_file=None, quadrant="both", angle=360., center=(0., 0.),
           model_name="Model-1", part_name='sphere'):
    """Create a hollow, spherical geometry from a sketch in the X-Y plane with upper (+X+Y), lower (+X-Y), or both quadrants.

    .. warning::

       The lower quadrant creation is currently broken

    :param float inner_radius: inner radius (size of hollow)
    :param float outer_radius: outer radius (size of sphere)
    :param str output_file: output file name. Will be stripped of the extension and ``.cae`` will be used.
    :param str input_file: input file name. Will be stripped of the extension and ``.cae`` will be used.
    :param str quadrant: quadrant of XY plane for the sketch: upper (I), lower (IV), both
    :param float angle: angle of rotation 0.-360.0 degrees. Provide 0 for a 2D axisymmetric model.
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
    if numpy.isclose(angle, 0.):
        p = abaqus.mdb.models[model_name].Part(name=part_name, dimensionality=abaqusConstants.AXISYMMETRIC,
                                               type=abaqusConstants.DEFORMABLE_BODY)
        p.BaseShell(sketch=s)
    else:
        p = abaqus.mdb.models[model_name].Part(name=part_name, dimensionality=abaqusConstants.THREE_D,
                                               type=abaqusConstants.DEFORMABLE_BODY)
        p.BaseSolidRevolve(sketch=s, angle=angle, flipRevolveDirection=abaqusConstants.OFF)
    del abaqus.mdb.models[model_name].sketches['__profile__']

    abaqus.mdb.saveAs(pathName=output_file)


def get_parser():
    # The global '__file__' variable doesn't appear to be set when executing from Abaqus CAE
    filename = inspect.getfile(lambda: None)
    basename = os.path.basename(filename)

    prog = "abaqus cae -noGui {} --".format(basename)
    cli_description = "Create a hollow, spherical geometry from a sketch in the X-Y plane with upper (+X+Y), lower " \
                      "(+X-Y), or both quadrants."

    parser = argparse.ArgumentParser(description=cli_description, prog=prog)
    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--inner-radius', type=float, required=True,
                               help="Inner radius (hollow size)")
    requiredNamed.add_argument('--outer-radius', type=float, required=True,
                               help="Outer radius (sphere size)")
    requiredNamed.add_argument('--output-file', type=str, required=True,
                               help="Abaqus model database to create")

    parser.add_argument('--input-file', type=str, default=None,
                        help="Abaqus model database to open (default: %(default)s)")
    parser.add_argument("--quadrant", type=str, choices=("both", "upper", "lower"), default="both",
                        help="XY plane quadrant: both, upper (I), lower (IV) (default: %(default)s)")
    parser.add_argument('--angle', type=float, default=360.,
                        help="Angle of revolution about the +Y axis (default: %(default)s)")
    parser.add_argument('--center', nargs=2, type=float, default=(0., 0.),
                        help="Center of the sphere (default: %(default)s)")
    parser.add_argument('--model-name', type=str, default="Model-1",
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument('--part-name', type=str, default="sphere",
                        help="Abaqus part name (default: %(default)s)")

    return parser


if __name__ == "__main__":
    parser = get_parser()
    args, unknown = parser.parse_known_args()

    if args.input_file is None:
        args.input_file = args.output_file

    sys.exit(sphere(
        args.inner_radius,
        args.outer_radius,
        args.output_file,
        input_file=args.input_file,
        quadrant=args.quadrant,
        angle=args.angle,
        center=args.center,
        model_name=args.model_name,
        part_name=args.part_name
    ))
