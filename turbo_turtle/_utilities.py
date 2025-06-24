import os
import sys
import shlex
import shutil
import typing
import pathlib
import argparse
import platform
import tempfile
import subprocess

from turbo_turtle._abaqus_python.turbo_turtle_abaqus._mixed_utilities import print_exception_message


class NamedTemporaryFileCopy:
    """Create a temporary file copy

    Thin wrapper around ``tempfile.NamedTemporaryFile(*args, delete=False, **kwargs)`` to provide Windows handling

    Provides Windows compatible temporary file handling. ``delete=False`` is required until Python 3.12
    ``delete_on_close=False`` option can be made a minimum runtime dependence.

    :param str input_file: The input file to copy into a temporary file
    """

    def __init__(self, input_file, *args, **kwargs):
        self.temporary_file = tempfile.NamedTemporaryFile(*args, delete=False, **kwargs)
        shutil.copyfile(input_file, self.temporary_file.name)

    def __enter__(self):
        return self.temporary_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temporary_file.close()
        os.remove(self.temporary_file.name)


def search_commands(options: typing.Iterable[str]) -> typing.Union[str, None]:
    """Return the first found command in the list of options. Return None if none are found.

    :param options: executable path(s) to test

    :returns: command absolute path
    """
    command_search = (shutil.which(command) for command in options)
    command_abspath = next((command for command in command_search if command is not None), None)
    return command_abspath


def find_command(options: typing.Iterable[str]) -> str:
    """Return first found command in list of options.

    :param options: alternate command options

    :returns: command absolute path

    :raises: FileNotFoundError if no command is found
    """
    command_abspath = search_commands(options)
    if command_abspath is None:
        raise FileNotFoundError(f"Could not find any executable on PATH in: {', '.join(options)}")
    return command_abspath


@print_exception_message
def find_command_or_exit(*args, **kwargs):
    return find_command(*args, **kwargs)


def cubit_os_bin() -> str:
    """Return the OS specific Cubit bin directory name

    Making Cubit importable requires putting the Cubit bin directory on PYTHONPATH. On MacOS, the directory is "MacOS".
    On other systems it is "bin".

    :returns: bin directory name, e.g. "bin" or "MacOS"
    """
    system = platform.system().lower()
    if system == "darwin":
        bin_directory = "MacOS"
    # TODO: Find the Windows bin directory name, update the function and the test.
    else:
        bin_directory = "bin"
    return bin_directory


def find_cubit_bin(options: typing.Iterable[str], bin_directory: typing.Optional[str] = None) -> pathlib.Path:
    """Provided a few options for the Cubit executable, search for the bin directory.

    Recommend first checking to see if cubit will import.

    If the Cubit command or bin directory is not found, raise a FileNotFoundError.

    :param options: Cubit command options
    :param bin_directory: Cubit's bin directory name. Override the bin directory returned by
        :meth:`turbo_turtle._utilities.cubit_os_bin`.

    :returns: Cubit bin directory absolute path
    """
    if bin_directory is None:
        bin_directory = cubit_os_bin()

    message = (
        "Could not find a Cubit bin directory. Please ensure the Cubit executable is on PATH or provide an "
        "absolute path to the Cubit executable."
    )

    cubit_command = find_command(options)
    cubit_command = os.path.realpath(cubit_command)
    cubit_bin = pathlib.Path(cubit_command).parent
    if bin_directory in cubit_bin.parts:
        while cubit_bin.name != bin_directory:
            cubit_bin = cubit_bin.parent
    else:
        search = cubit_bin.glob(f"**/{bin_directory}")
        try:
            cubit_bin = next((path for path in search if path.name == bin_directory))
        except StopIteration:
            raise FileNotFoundError(message)
    return cubit_bin


def import_gmsh():
    """Intermediate gmsh import function

    Allows better CLI error reporting and gmsh package mocking during unit tests
    """
    try:
        import gmsh
    except ImportError as err:
        raise RuntimeError(
            "Could not import gmsh package. Please install `python-gmsh` in the Conda environment.\n"
            f"'ImportError: {err}'"
        )
    return gmsh


def import_cubit():
    """Intermediate Cubit import function

    Allows better CLI error reporting and Cubit package mocking during unit tests
    """
    try:
        import cubit
    except ImportError as err:
        raise RuntimeError(
            f"Could not import Cubit package. Provide or check the Cubit executable path.\n'ImportError: {err}'"
        )
    return cubit


def run_command(command: str) -> None:
    """Split command on whitespace, execute shell command, raise RuntimeError with any error message

    :param command: String to run on the shell
    """
    command_list = shlex.split(command)
    try:
        subprocess.check_output(command_list)
    except subprocess.CalledProcessError as err:
        raise RuntimeError(err.output.decode())


def set_wrappers_and_command(args: argparse.Namespace) -> typing.Tuple:
    """Read an argument namespace and set the wrappers and command appropriately

    :param args: namespace of parsed arguments from :meth:`turbo_turtle._main.get_parser`

    :return: _wrappers, command. Wrapper module, executable command string.
    """
    keys = vars(args).keys()
    if "backend" in keys and args.backend == "gmsh":
        command = "unused"
        from turbo_turtle import _gmsh_wrappers as _wrappers
    elif "backend" in keys and args.backend == "cubit":
        command = find_command_or_exit(args.cubit_command)
        cubit_bin = find_cubit_bin([command])
        cubitx = cubit_bin / "cubitx"
        if cubitx.exists():
            command = cubitx
        import importlib.util

        if importlib.util.find_spec("cubit") is None:
            sys.path.append(str(cubit_bin))
        from turbo_turtle import _cubit_wrappers as _wrappers
    elif "abaqus_command" in keys:
        command = find_command_or_exit(args.abaqus_command)
        from turbo_turtle import _abaqus_wrappers as _wrappers

    return _wrappers, command


def construct_append_options(
    option: str,
    array: typing.Iterable[typing.Tuple],
) -> str:
    """Construct a command string to match the argparse append action

    Build the repeated option string for argparse appending options that accept more than one value

    .. code-block::

       python script.py --option 1 2 --option 3 4

    .. code-block::

       >>> option = "--option"
       >>> array = [[1, 2], [3, 4]]
       >>> construct_append_options(option, array)
       "--option 1 2 --option 3 4"

    :param option: Text for the option, e.g. ``--option``
    :param array: 2D iterable of tuple arguments
    """
    command_string = ""
    for row in array:
        if row:
            command_string += f" {option} " + character_delimited_list(row)
    command_string = command_string.strip()
    return command_string


def character_delimited_list(sequence: typing.Iterable, character: str = " ") -> str:
    """Map a list of non-strings to a character delimited string

    :param sequence: Sequence to turn into a character delimited string
    :param character: Character(s) to use when joining sequence elements

    :returns: string delimited by specified character
    """
    return character.join(map(str, sequence))
