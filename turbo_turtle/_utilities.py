import sys
import shutil
import functools


def _search_commands(options):
    """Return the first found command in the list of options. Return None if none are found.

    :param list options: executable path(s) to test

    :returns: command absolute path
    :rtype: str
    """
    command_search = (shutil.which(command) for command in options)
    command_abspath = next((command for command in command_search if command is not None), None)
    return command_abspath


def _find_command(options):
    """Return first found command in list of options.

    Raise a FileNotFoundError if none is found.

    :param str requested: requested command
    :param list options: alternate command options

    :returns: command absolute path
    :rtype: str
    """
    command_abspath = _search_commands(options)
    if command_abspath is None:
        raise FileNotFoundError(f"Could not find any executable on PATH in: {', '.join(options)}")
    return command_abspath


def _print_exception_message(function):
    """Decorate a function to catch any exception, print the message and call sys.exit

    :param function: function to decorate
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            output = function(*args, **kwargs)
        except Exception as err:
            print(str(err))
            sys.exit(2)
        return output
    return wrapper


@_print_exception_message
def _find_command_or_exit(*args, **kwargs):
    return _find_command(*args, **kwargs)
