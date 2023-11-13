"""Python 2/3 compatible utilities for use in both Abaqus Python scripts and Turbo-Turtle Python 3 modules"""
import os
import sys
import functools

import numpy


def sys_exit(err):
    """Thin wrapper on ``sys.exit`` to force print to STDERR from Abaqus Python

    Preserves Python 3 compatibility by performing a Python major version check prior to the Python 2 syntax call to
    ``print``.

    :param Exception err: The exception object to print and pass to ``sys.exit``
    """
    if sys.version_info.major == 2:
        print >> sys.__stderr__, "{}".format(err)  # pragma: no cover
    sys.exit(str(err))


def print_exception_message(function):
    """Decorate a function to catch bare exception and instead call sys.exit with the message

    :param function: function to decorate
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            output = function(*args, **kwargs)
        except Exception as err:
            sys_exit(err)
        return output
    return wrapper


def validate_part_name(input_file, part_name):
    """Validate the structure of the ``part_name`` list to the following rules:

    * If ``part_name`` is ``[None]``, assign the base names of ``input_file`` to ``part_name``
    * Else if the length of ``part_name`` is not equal to the length of ``input_file``, raise an exception

    :param list input_file: input text file(s) with coordinates to draw
    :param list part_name: name(s) of part(s) being created

    :return: part name(s)
    :rtype: list
    """
    if part_name[0] is None:
        part_name = [os.path.splitext(os.path.basename(part_file))[0] for part_file in input_file]
    elif len(input_file) != len(part_name):
        message = "Error: The part name length '{}' must match the input file length '{}'\n".format(
                  len(part_name), len(input_file))
        raise RuntimeError(message)
    return part_name


@print_exception_message
def validate_part_name_or_exit(*args, **kwargs):
    return validate_part_name(*args, **kwargs)


def validate_element_type(length_part_name, element_type):
    """Validate the structure of the ``element_type`` list to the following rules:

    * If the length of ``element_type`` is 1, propagate to match ``length_part_name``
    * Raise a RuntimeError if ``element_type`` is greater than 1, but not equal to the length of ``part_name``

    :param int length_part_name: length of the ``part_name`` list
    :param list element_type: list of element types

    :return: element types
    :rtype: list
    """
    length_element_type = len(element_type)
    if length_element_type == 1:
        element_type = element_type * length_part_name
    elif length_element_type != length_part_name:
        message = "The element type length '{}' must match the part name length '{}'\n".format(
                  length_element_type, length_part_name)
        raise RuntimeError(message)
    return element_type


@print_exception_message
def validate_element_type_or_exit(*args, **kwargs):
    return validate_element_type(*args, **kwargs)


def return_genfromtxt(file_name,
                      delimiter=',',
                      header_lines=0,
                      expected_dimensions=None,
                      expected_columns=None):
    """Parse a text file of XY coordinates into a numpy array

    If the resulting numpy array doesn't have the specified dimensions or column count, return an error exit code

    :param str file_name: input text file with coordinates to draw
    :param str delimiter: character to use as a delimiter when reading the input file
    :param int header_lines: number of lines in the header to skip when reading the input file

    :return: 2D array of XY coordinates with shape [N, 2]
    :rtype: numpy.array
    """
    with open(file_name, 'r') as points_file:
        coordinates = numpy.genfromtxt(points_file, delimiter=delimiter, skip_header=header_lines)
    shape = coordinates.shape
    dimensions = len(shape)
    if expected_dimensions is not None and dimensions != expected_dimensions:
        message = "Expected coordinates with '{}' dimensions. Found '{}' dimensions\n".format(
                  expected_dimensions, dimensions)
        raise RuntimeError(message)
    columns = shape[1]
    if expected_columns is not None and columns != expected_columns:
        message = "Expected coordinates with '{}' columns. Found '{}' columns\n".format(
                  expected_columns, columns)
        raise RuntimeError(message)
    return coordinates


@print_exception_message
def return_genfromtxt_or_exit(*args, **kwargs):
    return return_genfromtxt(*args, **kwargs)
