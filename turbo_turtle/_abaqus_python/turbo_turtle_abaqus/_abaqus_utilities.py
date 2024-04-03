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


def _view_part_gui_post_action(model_name, part_name, **kwargs):
    """Place a part in the current viewport as a GUI post-action

    Depending on if ``part_name`` is a list or a string, either place the last part in the list or the string part name 
    in the viewport.

    This function requires the arguments documented below, and any other arguments will be unpacked but ignored. This 
    behavior makes it convenient to use this function generally with the arguments of any of the GUI plug-in actions (so 
    long as those documented below are present).

    :param str model_name: name of the Abaqus model to query in the post-action
    :param str/list part_name: name of the part to place in the viewport. If ``list`` type, use the last part name in 
        the list. If ``str`` type, use that part name directly.
    """
    import abaqus

    if isinstance(part_name, list):
        part_object = abaqus.mdb.models[model_name].parts[part_name[-1]]
    else:
        part_object = abaqus.mdb.models[model_name].parts[part_name]
    abaqus.session.viewports['Viewport: 1'].setValues(displayedObject=part_object)
    abaqus.session.viewports['Viewport: 1'].view.setValues(abaqus.session.views['Iso'])
    abaqus.session.viewports['Viewport: 1'].view.fitView()


def _conditionally_create_model(model_name):
    """Create a new model in an Abaqus database if the specified model name is not already existing

    :param str model_name: Abaqus model name
    """
    import abaqus
    import abaqusConstants

    if model_name not in abaqus.mdb.models.keys():
        abaqus.mdb.Model(name=model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)


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
    try:
        user_inputs = inputs_function()  # dict of user inputs. If the user hits 'Cancel/esc', user_inputs={}
        if user_inputs:
            subcommand_function(**user_inputs)  # Assumes inputs_function returns same arguments expected by subcommand_function
            if post_action_function is not None:
                post_action_function(**user_inputs)
        else:
            print('\nTurboTurtle was canceled\n')  # Do not sys.exit, that will kill Abaqus CAE
    except RuntimeError as err:
        print(err)
