import sys

import cubit

from turbo_turtle._abaqus_python import _mixed_utilties

def geometry(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    cubit.init(["cubit", "-nojournal"])
    part_name = _mixed_utilities.validate_part_name_or_exit(input_file, part_name)
    output_file = pathlib.Path(output_file).with_suffix(".cub")
    for file_name, new_part in zip(input_file, part_name):
        coordinates = _mixed_utilities.return_genfromtxt(file_name, args.delimiter, args.header_lines,
                                                         expected_dimensions=2, expected_columns=2)
        coordinates = coordinates * args.unit_conversion
        lines, splines = vertices.lines_and_splines(coordinates, euclidean_distance)
        for point1, point2 in lines:
            point1_text = " ".join(map(str, point1)) + " 0"
            point2_text = " ".join(map(str, point1)) + " 0"
            cubit.command("create curve location {point1_text} location {point2_text}")
    cubit.command("save as '{output_file}' overwrite")


def cylinder(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


def sphere(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    sys.exit("Not yet implemented")


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
