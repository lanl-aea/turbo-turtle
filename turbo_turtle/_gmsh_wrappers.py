"""Thin unpacking of the command line argparse namespace into full function interfaces"""
from turbo_turtle import _gmsh_python


def geometry(args, command):
    raise RuntimeError("geometry subcommand is not yet implemented")


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


def sphere(args, command):
    raise RuntimeError("sphere subcommand is not yet implemented")


def partition(args, command):
    raise RuntimeError("partition subcommand is not yet implemented")


def sets(args, command):
    raise RuntimeError("sets subcommand is not yet implemented")


def mesh(args, command):
    raise RuntimeError("mesh subcommand is not yet implemented")


def merge(args, command):
    raise RuntimeError("merge subcommand is not yet implemented")


def export(args, command):
    raise RuntimeError("export subcommand is not yet implemented")


def image(args, command):
    raise RuntimeError("image subcommand is not yet implemented")
