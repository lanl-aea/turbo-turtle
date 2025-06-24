import os
import sys
import shutil
import inspect
import tempfile

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import _mixed_utilities  # noqa: E402


class AbaqusNamedTemporaryFile:
    """Open an Abaqus CAE ``input_file`` as a temporary file. Close and delete on exit of context manager.

    Provides Windows compatible temporary file handling. Required until Python 3.12 ``delete_on_close=False`` option is
    available in Abaqus Python.

    :param str input_file: The input file to copy before open
    """

    def __init__(self, input_file, *args, **kwargs):
        import abaqus

        self.temporary_file = tempfile.NamedTemporaryFile(*args, delete=False, **kwargs)
        shutil.copyfile(input_file, self.temporary_file.name)
        abaqus.openMdb(pathName=self.temporary_file.name)

    def __enter__(self):
        return self.temporary_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        import abaqus

        abaqus.mdb.close()
        self.temporary_file.close()
        os.remove(self.temporary_file.name)


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


def part_dimensionality(part):
    """Return part dimensionality as an int

    :param abaqus.models[model].parts[part] part: Abaqus part object

    :returns: integer number of part dimensions
    :rtype: int
    """
    known_geometries = {
        "Axisymmetric": 2,
        "2D Planar": 2,
        "3D": 3,
    }
    geometry_key = part.queryGeometry(printResults=False)["space"]
    return known_geometries[geometry_key]


def part_dimensionality_key(part):
    """Get the Abaqus dimensionality key for the current part

    :param abaqus.models[model].parts[part] part: Abaqus part object

    :return: part dimensionality
    :rtype: str
    """
    dimensionality = part.queryGeometry(printResults=False)["space"]
    return dimensionality


def set_from_mask(part, feature, name_mask):
    """Create named set(s) from the geometric feature and mask(s)

    :param abaqus.models[model].parts[part] part: Abaqus part object
    :param str feature: Abaqus part geometric attribute, e.g. 'faces', 'edges', 'vertices'
    :param list[tuple[str, str]] name_mask: List of set name/mask tuples to create

    :raises RuntimeError: If Abaqus throws an empty sequence abaqus.AbaqusException on one or more masks
    """
    import abaqus

    attribute = getattr(part, feature)
    bad_masks = []
    for name, mask in name_mask:
        try:
            objects = attribute.getSequenceFromMask(mask=(mask,))
        except abaqus.AbaqusException:
            bad_masks.append((name, mask))
        else:
            part.Set(**{feature: objects, "name": name})
    if bad_masks:
        raise RuntimeError("Creaton of one or more sets failed {}".format(bad_masks))


def surface_from_mask(part, feature, name_mask):
    """Create named surface(s) from the geometric feature and mask(s)

    :param abaqus.models[model].parts[part] part: Abaqus part object
    :param str feature: Abaqus part geometric attribute, e.g. 'faces', 'edges'
    :param list[tuple[str, str]] name_mask: List of set name/mask tuples to create

    :raises ValueError: If feature is not one of 'faces' or 'edges'
    :raises RuntimeError: If Abaqus throws an empty sequence abaqus.AbaqusException on one or more masks
    """
    import abaqus

    attribute = getattr(part, feature)
    if feature == "faces":
        surface_keyword = "side1Faces"
    elif feature == "edges":
        surface_keyword = "side1Edges"
    else:
        raise ValueError("Feature must be one of: faces, edges")
    bad_masks = []
    for name, mask in name_mask:
        try:
            objects = attribute.getSequenceFromMask(mask=(mask,))
        except abaqus.AbaqusException:
            bad_masks.append((name, mask))
        else:
            part.Surface(**{"name": name, surface_keyword: objects})
    if bad_masks:
        raise RuntimeError("Creaton of one or more sets failed {}".format(bad_masks))


def edge_seeds(part, name_number):
    """Seed edges by number (if passed integer) or size (if passed float)

    :param abaqus.models[model].parts[part] part: Abaqus part object
    :param str feature: Abaqus part geometric attribute, e.g. 'faces', 'edges'

    :raises ValueError: If any number is negative
    """
    names, numbers = zip(*name_number)
    numbers = [float(number) for number in numbers]
    positive_numbers = [number > 0.0 for number in numbers]
    if not all(positive_numbers):
        raise ValueError("Edge seeds must be positive numbers")
    for name, number in zip(names, numbers):
        edges = part.sets[name].edges
        if number.is_integer():
            part.seedEdgeByNumber(edges=edges, number=int(number))
        else:
            part.seedEdgeBySize(edges=edges, size=number)


def _view_part(model_name, part_name, **kwargs):
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
        part_name = part_name[-1]
    part_object = abaqus.mdb.models[model_name].parts[part_name]
    abaqus.session.viewports["Viewport: 1"].setValues(displayedObject=part_object)
    abaqus.session.viewports["Viewport: 1"].view.setValues(abaqus.session.views["Iso"])
    abaqus.session.viewports["Viewport: 1"].view.fitView()


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
            # Assumes inputs_function returns same arguments expected by subcommand_function
            subcommand_function(**user_inputs)
            if post_action_function is not None:
                post_action_function(**user_inputs)
        else:
            print("\nTurboTurtle was canceled\n")  # Do not sys.exit, that will kill Abaqus CAE
    except RuntimeError as err:
        print(err)


def revolution_direction(revolution_angle):
    """Pick revolution direction constant consistent with +Y revolve direction

    Positive rotation angles should result in +Y revolve direction (abaqusConstants.ON)
    Negative rotation angles should result in -Y revolve direction (abaqusConstants.OFF)

    :param float revolution_angle: angle of solid revolution for ``3D`` geometries
    """
    import abaqusConstants

    if revolution_angle < 0.0:
        revolution_direction = abaqusConstants.OFF
    else:
        revolution_direction = abaqusConstants.ON
    return revolution_direction
