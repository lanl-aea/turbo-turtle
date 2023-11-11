import sys

from turbo_turtle import _settings
from turbo_turtle import _utilities


def geometry(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    try:
        import cubit
    except ModuleNotFoundError:
        sys.path.append(_utilities.find_cubit_bin(command))
        import cubit
    sys.exit("Not yet implemented")


def cylinder(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    try:
        import cubit
    except ModuleNotFoundError:
        sys.path.append(_utilities.find_cubit_bin(command))
        import cubit
    sys.exit("Not yet implemented")


def sphere(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    try:
        import cubit
    except ModuleNotFoundError:
        sys.path.append(_utilities.find_cubit_bin(command))
        import cubit
    sys.exit("Not yet implemented")


def partition(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    try:
        import cubit
    except ModuleNotFoundError:
        sys.path.append(_utilities.find_cubit_bin(command))
        import cubit
    sys.exit("Not yet implemented")


def mesh(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    try:
        import cubit
    except ModuleNotFoundError:
        sys.path.append(_utilities.find_cubit_bin(command))
        import cubit
    sys.exit("Not yet implemented")


def merge(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    try:
        import cubit
    except ModuleNotFoundError:
        sys.path.append(_utilities.find_cubit_bin(command))
        import cubit
    sys.exit("Not yet implemented")


def export(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    try:
        import cubit
    except ModuleNotFoundError:
        sys.path.append(_utilities.find_cubit_bin(command))
        import cubit
    sys.exit("Not yet implemented")


def image(args, command):
    """Python 3 wrapper around Cubit

    .. warning::

       Not yet implemented. Will return a non-zero exit code.

    :param argparse.Namespace args: namespace of parsed arguments
    :param str command: cubit executable path
    """
    try:
        import cubit
    except ModuleNotFoundError:
        sys.path.append(_utilities.find_cubit_bin(command))
        import cubit
    sys.exit("Not yet implemented")
