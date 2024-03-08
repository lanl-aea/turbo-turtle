import os
import sys
import inspect

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import _mixed_utilities


def return_abaqus_constant(search):
    """If search is found in the abaqusConstants module, return the abaqusConstants object.

    Raise a ValueError if the search string is not found.

    :param str search: string to search in the abaqusConstants module attributes

    :return value: abaqusConstants attribute
    :rtype: abaqusConstants.<search>
    """
    import abaqusConstants

    search = search.upper()
    attribute = None
    if hasattr(abaqusConstants, search):
        attribute = getattr(abaqusConstants, search)
    else:
        raise ValueError("The abaqusConstants module does not have a matching '{}' object".format(search))
    return attribute


@_mixed_utilities.print_exception_message
def return_abaqus_constant_or_exit(*args, **kwargs):
    return return_abaqus_constant(*args, **kwargs)
