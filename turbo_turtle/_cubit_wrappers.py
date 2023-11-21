"""Thin unpacking of the command line argparse namespace into full function interfaces"""
import sys

from turbo_turtle import _cubit_python


def geometry(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.geometry`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit(_cubit_python.geometry(
        args.input_file, args.output_file,
        planar=args.planar,
        part_name=args.part_name,
        unit_conversion=args.unit_conversion,
        euclidean_distance=args.euclidean_distance,
        delimiter=args.delimiter,
        header_lines=args.header_lines,
        revolution_angle=args.revolution_angle
    ))


def cylinder(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.cylinder`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit(_cubit_python.cylinder(
        args.inner_radius,
        args.outer_radius,
        args.height,
        args.output_file,
        part_name=args.part_name,
        revolution_angle=args.revolution_angle
    ))


def sphere(args, command):
    """Python 3 wrapper around Cubit calling :meth:`turbo_turtle._cubit_python.sphere`

    Unpack the argument namespace into the full function interface

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit(_cubit_python.sphere(
        args.inner_radius,
        args.outer_radius,
        args.output_file,
        input_file=args.input_file,
        quadrant=args.quadrant,
        revolution_angle=args.revolution_angle,
        center=args.center,
        part_name=args.part_name
    ))


def partition(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def mesh(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def merge(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def export(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def image(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")
