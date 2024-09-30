"""Thin unpacking of the command line argparse namespace into full function interfaces"""
from turbo_turtle import _gmsh_python


def cylinder(args, command):
    """Python 3 wrapper around Gmsh calling :meth:`turbo_turtle._gmsh_python.cylinder`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: gmsh executable path, unused. Kept for API compatibility with
        :meth:`turbo_turtle._abaqus_wrappers`
    """
    _gmsh_python.cylinder(
        args.inner_radius,
        args.outer_radius,
        args.height,
        args.output_file,
        part_name=args.part_name,
        revolution_angle=args.revolution_angle,
        y_offset=args.y_offset
    )
