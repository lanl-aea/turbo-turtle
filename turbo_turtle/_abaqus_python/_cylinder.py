import os
import sys
import inspect

import numpy

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import _parsers
import _geometry


def main(inner_radius, outer_radius, height, output_file,
         model_name=_parsers.geometry_default_model_name,
         part_name=_parsers.cylinder_default_part_name,
         revolution_angle=_parsers.geometry_default_revolution_angle):
    """Accept dimensions of a right circular cylinder and generate an axisymmetric revolved geometry

    :param float inner_radius: Radius of the hollow center
    :param float outer_radius: Outer radius of the cylinder
    :param float height: Height of the cylinder
    :param str output_file: Abaqus CAE database to save the part(s)
    :param str model_name: name of the Abaqus model in which to create the part
    :param list part_name: name(s) of the part(s) being created
    :param float revolution_angle: angle of solid revolution for ``3D`` geometries
    """
    import abaqus
    import abaqusConstants

    abaqus.mdb.Model(name=model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
    output_file = os.path.splitext(output_file)[0] + ".cae"

    all_splines = cylinder_vertices(inner_radius, outer_radius, height)
    _geometry.draw_part_from_splines(all_splines, planar=False, model_name=model_name, part_name=part_name,
                                     revolution_angle=revolution_angle)

    abaqus.mdb.saveAs(pathName=output_file)


def cylinder_vertices(inner_radius, outer_radius, height):
    """Return a :meth:`turbo_turtle._abaqus_python._geometry.draw_part_from_splines` compatible vertex list

    :param float inner_radius: Radius of the hollow center
    :param float outer_radius: Outer radius of the cylinder
    :param float height: Height of the cylinder
    """
    all_splines = [
        numpy.array([[inner_radius, height]]),
        numpy.array([[outer_radius, height]]),
        numpy.array([[outer_radius, 0.]]),
        numpy.array([[inner_radius, 0.]])
    ]
    return all_splines


if __name__ == "__main__":

    parser = _parsers.cylinder_parser(basename=basename)
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit as err:
        sys.exit(err.code)

    sys.exit(main(
        inner_radius=args.inner_radius,
        outer_radius=args.outer_radius,
        height=args.height,
        output_file=args.output_file,
        model_name=args.model_name,
        part_name=args.part_name,
        revolution_angle=args.revolution_angle
    ))