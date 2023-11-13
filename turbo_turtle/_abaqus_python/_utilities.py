import os
import sys

import numpy


def _validate_part_name(input_file, part_name):
    """Validate the structure of the ``part_name`` list to the following rules:

    * If ``part_name`` is ``[None]``, assign the base names of ``input_file`` to ``part_name``
    * Else if the length of ``part_name`` is not equal to the length of ``input_file``, exit with an error

    :param list input_file: input text file(s) with coordinates to draw
    :param list part_name: name(s) of part(s) being created

    :return: part name(s)
    :rtype: list
    """
    if part_name[0] is None:
        part_name = [os.path.splitext(os.path.basename(part_file))[0] for part_file in input_file]
    elif len(input_file) != len(part_name):
        error_message = "Error: The part name length '{}' must match the input file length '{}'\n".format(
            len(part_name), len(input_file))
        sys.stderr.write(error_message)
        sys.exit(1)
    return part_name


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
        sys.stderr.write("Expected coordinates with '{}' dimensions. Found '{}' dimensions\n".format(
                         expected_dimensions, dimensions))
        sys.exit(1)
    columns = shape[1]
    if expected_columns is not None and columns != expected_columns:
        sys.stderr.write("Expected coordinates with '{}' columns. Found '{}' columns\n".format(
                         expected_columns, columns))
        sys.exit(2)
    return coordinates
