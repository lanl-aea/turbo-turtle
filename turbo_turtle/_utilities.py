import sys
import shutil
import pathlib
import inspect
import functools
import subprocess

from turbo_turtle._abaqus_python._utilities import print_exception_message


def search_commands(options):
    """Return the first found command in the list of options. Return None if none are found.

    :param list options: executable path(s) to test

    :returns: command absolute path
    :rtype: str
    """
    command_search = (shutil.which(command) for command in options)
    command_abspath = next((command for command in command_search if command is not None), None)
    return command_abspath


def find_command(options):
    """Return first found command in list of options.

    Raise a FileNotFoundError if none is found.

    :param list options: alternate command options

    :returns: command absolute path
    :rtype: str
    """
    command_abspath = search_commands(options)
    if command_abspath is None:
        raise FileNotFoundError(f"Could not find any executable on PATH in: {', '.join(options)}")
    return command_abspath


@print_exception_message
def find_command_or_exit(*args, **kwargs):
    return find_command(*args, **kwargs)


def find_cubit_bin(options):
    """Provided a few options for the Cubit executable, search for the bin directory.

    Recommend first checking to see if cubit will import.

    If the Cubit command or bin directory is not found, raise a FileNotFoundError.

    :param list options: Cubit command options

    :returns: Cubit bin directory absolute path
    :rtype: pathlib.Path
    """
    message = "Could not find a Cubit bin directory. Please ensure the Cubit executable is on PATH or provide an " \
              "absolute path to the Cubit executable."
    cubit_command = find_command(options)
    cubit_command = os.path.realpath(cubit_command)
    cubit_bin = pathlib.Path(cubit_command)
    if "bin" in cubit_bin.parts:
        while cubit_bin.name != "bin":
            cubit_bin = cubit_bin.parent
    else:
        search = cubit_bin.glob("bin")
        cubit_bin = next((path for path in search if path.name == "bin"), None)
    if cubit_bin is None:
        raise FileNotFoundError(message)
    return cubit_bin


def run_command(command):
    """Split command on whitespace, execute shell command, call sys.exit with any error message

    :param str command: String to run on the shell
    """
    command = command.split()
    try:
        stdout = subprocess.check_output(command)
    except subprocess.CalledProcessError as err:
        sys.exit(err.output.decode())
