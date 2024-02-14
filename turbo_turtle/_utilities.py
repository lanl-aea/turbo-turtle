import os
import sys
import shutil
import pathlib
import inspect
import platform
import functools
import subprocess

from turbo_turtle._abaqus_python._mixed_utilities import print_exception_message


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


def cubit_os_bin():
    """Return the OS specific Cubit bin directory name

    Making Cubit importable requires putting the Cubit bin directory on PYTHONPATH. On MacOS, the directory is "MacOS".
    On other systems it is "bin".

    :returns: bin directory name, e.g. "bin" or "MacOS"
    :rtype:
    """
    system = platform.system().lower()
    if system == "darwin":
        bin_directory = "MacOS"
    # TODO: Find the Windows bin directory name, update the function and the test.
    else:
        bin_directory = "bin"
    return bin_directory


def find_cubit_bin(options, bin_directory=None):
    """Provided a few options for the Cubit executable, search for the bin directory.

    Recommend first checking to see if cubit will import.

    If the Cubit command or bin directory is not found, raise a FileNotFoundError.

    :param list options: Cubit command options
    :param str bin_directory: Cubit's bin directory name. Override the bin directory returned by
        :meth:`turbo_turtle._utilities.cubit_os_bin`.

    :returns: Cubit bin directory absolute path
    :rtype: pathlib.Path
    """
    if bin_directory is None:
        bin_directory = cubit_os_bin()

    message = "Could not find a Cubit bin directory. Please ensure the Cubit executable is on PATH or provide an " \
              "absolute path to the Cubit executable."

    cubit_command = find_command(options)
    cubit_command = os.path.realpath(cubit_command)
    cubit_bin = pathlib.Path(cubit_command).parent
    if bin_directory in cubit_bin.parts:
        while cubit_bin.name != bin_directory:
            cubit_bin = cubit_bin.parent
    else:
        search = cubit_bin.glob(f"**/{bin_directory}")
        cubit_bin = next((path for path in search if path.name == bin_directory), None)
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


def set_wrappers_and_command(args):
    """Read an argument namespace and set the wrappers and command appropriately

    :param argparse.Namespace args: namespace of parsed arguments from :meth:`turbo_turtle.main.get_parser`

    :return: _wrappers, command. Wrapper module, executable command string.
    :rtype: tuple
    """
    keys = vars(args).keys()
    if "cubit" in keys and args.cubit is True:
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
