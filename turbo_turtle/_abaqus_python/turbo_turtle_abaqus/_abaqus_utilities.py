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


def gui_wrapper(inputs_function, subcommand_function, post_action_function=None):
    """Wrapper for a function calling ``abaqus.getInputs``, then the wrapper calls a ``turbo_turtle`` subcommand module

    ``inputs_function`` cannot have any function arguments. ``inputs_function`` must return
    a dictionary of key-value pairs that match the ``subcommand_function`` arguments. ``post_action_function`` must have
    identical arguments to ``subcommand_function`` or the ability to ignore provided arguments. Any return values from
    ``post_action_function`` will have no affect.

    This wrapper expects the dictionary output from ``inputs_function`` to be empty when the GUI interface is exited
    early (escape or cancel). Otherwise, the dictionary will be unpacked as ``**kwargs`` into ``subcommand_function``
    and ``post_action_function``.

    :param func inputs_function: function to get user inputs through the Abaqus CAE GUI
    :param func subcommand_function: function with arguments matching the return values from ``inputs_function``
    :param func post_action_function: function to call for script actions after calling ``subcommand_function``
    """
    import abaqus

    user_inputs = inputs_function()  # Dictionary user inputs, if the user Cancels, user_inputs will be {}
    if user_inputs:
        subcommand_function(**user_inputs)  # Assumes inputs_function returns same arguments expected by subcommand_function
        if post_action_function is not None:
            post_action_function(**user_inputs)
    else:
        print('\nTurboTurtle was canceled\n')  # Do not sys.exit, that will kill Abaqus CAE
