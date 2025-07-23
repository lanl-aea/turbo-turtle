import os
import sys
import inspect


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import parsers  # noqa: E402
from turbo_turtle_abaqus import _abaqus_utilities  # noqa: E402
from turbo_turtle_abaqus import _mixed_utilities  # noqa: E402
from turbo_turtle_abaqus import _mixed_settings  # noqa: E402


def main(
    input_file,
    element_type,
    output_file=parsers.mesh_defaults["output_file"],
    model_name=parsers.mesh_defaults["model_name"],
    part_name=parsers.mesh_defaults["part_name"],
    global_seed=parsers.mesh_defaults["global_seed"],
    edge_seeds=parsers.mesh_defaults["edge_seeds"],
):
    """Wrap mesh function for input file handling

    :param str input_file: Abaqus CAE file to open that already contains a model with a part to be meshed
    :param str element_type: Abaqus element type
    :param str output_file: Abaqus CAE file to save with the newly meshed part
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model
    :param float global_seed: The global mesh seed size
    :param list[tuple[str, number]] edge_seeds: List of edge seed (name, number) pairs
    """
    import abaqus

    try:
        if output_file is None:
            output_file = input_file
        input_file = os.path.splitext(input_file)[0] + ".cae"
        output_file = os.path.splitext(output_file)[0] + ".cae"
        with _abaqus_utilities.AbaqusNamedTemporaryFile(input_file, suffix=".cae", dir="."):
            mesh(
                element_type,
                model_name=model_name,
                part_name=part_name,
                global_seed=global_seed,
                edge_seeds=edge_seeds,
            )
            abaqus.mdb.saveAs(pathName=output_file)
    except RuntimeError as err:
        _mixed_utilities.sys_exit(str(err))


def mesh(
    element_type,
    model_name=parsers.mesh_defaults["model_name"],
    part_name=parsers.mesh_defaults["part_name"],
    global_seed=parsers.mesh_defaults["global_seed"],
    edge_seeds=parsers.mesh_defaults["edge_seeds"],
):
    """Apply a global seed, optional edge seed(s), and mesh the specified part

    Always creates sets

    * ``ELEMENTS``: All elements
    * ``NODES``: All nodes

    :param str element_type: Abaqus element type
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model
    :param float global_seed: The global mesh seed size
    :param list[tuple[str, number]] edge_seeds: List of edge seed (name, number) pairs
    """
    import mesh
    import abaqus
    import abaqusConstants

    model = abaqus.mdb.models[model_name]
    part = model.parts[part_name]

    if edge_seeds is not None:
        _abaqus_utilities.edge_seeds(part, edge_seeds)
    # TODO: make the deviation and size factor options
    part.seedPart(size=global_seed, deviationFactor=0.1, minSizeFactor=0.1)

    element_type_object = _abaqus_utilities.return_abaqus_constant_or_exit(element_type)

    # TODO: enable STANDARD/EXPLICIT switch?
    mesh_element_type = mesh.ElemType(elemCode=element_type_object, elemLibrary=abaqusConstants.STANDARD)

    # TODO: make the set names optional arguments
    cells = part.cells[:]
    if len(cells) > 0:
        part.Set(cells=cells, name="ELEMENTS")
        part.Set(cells=cells, name="NODES")
        part.setElementType(regions=(cells,), elemTypes=(mesh_element_type,))
    else:
        faces = part.faces
        part.Set(faces=faces, name="ELEMENTS")
        part.Set(faces=faces, name="NODES")
        part.setElementType(regions=(faces,), elemTypes=(mesh_element_type,))

    part.generateMesh()


def _gui_get_default_elem_type(model_name, part_name):
    """Set default element types for the _gui_get_inputs_function

    Use a one-time dump of the Abaqus default element types for known part dimensionality

    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model

    :return: element type from a hard-coded mapping of Abaqus default element types
    :rtype: str
    """
    import abaqus

    known_dimensions = {  # Abaqus 2023.HF5 default element types for Abaqus Standard/Explicit dimensions
        "Axisymmetric": "CAX4R",
        "3D": "C3D8R",
        "2D Planar": "CPS4R",
    }

    part = abaqus.mdb.models[model_name].parts[part_name]
    geometry_properties = part.queryGeometry(printResults=False)
    dimensionality = geometry_properties["space"]

    elem_type = known_dimensions.get(dimensionality)  # Returns None if dimensionality is not a key in known_dimensions
    if elem_type is None:
        elem_type = ""  # Will also show up as a blank string in the Abaqus/CAE GUI inputs dialog box

    return elem_type


def _gui_get_inputs():
    """Mesh Interactive Inputs

    Prompt the user for inputs with this interactive data entry function. When called, this function opens an Abaqus CAE
    GUI window with text boxes to enter the values given below. Note to developers - if you update this 'GUI-INPUTS'
    below, also update ``_mixed_settings._mesh_gui_help_string`` that gets used as the GUI ``label``.

    GUI-INPUTS
    ==========
    * Part Name - part name to mesh
    * Element Type - a valid Abaqus element type for meshing the part
    * Global Seed - global seed value in the model's units

    **IMPORTANT** - this function must return key-value pairs that will successfully unpack as ``**kwargs`` in
    ``mesh``

    :return: ``user_inputs`` - a dictionary of the following key-value pair types:

    * ``element_type``: ``str`` type, valid Abaqus element type
    * ``model_name``: ``str`` type, name of the model in the current viewport
    * ``part_name``: ``list`` type, name of the part to mesh
    * ``global_seed``: ``float`` type, global element seed

    :raises RuntimeError: if a element type or global mesh seed are not specified.
    """
    import abaqus

    model_name = abaqus.session.viewports[abaqus.session.currentViewportName].displayedObject.modelName

    try:
        default_part_name = abaqus.session.viewports[abaqus.session.currentViewportName].displayedObject.name
    except AttributeError:
        print(
            "Warning: could not determine a default part name using the current viewport. "
            "Using default '{}'".format(parsers.mesh_defaults["part_name"][0])
        )
        default_part_name = parsers.mesh_defaults["part_name"][0]  # part_name defaults to list of length 1

    fields = (
        ("Part Name:", default_part_name),
        ("Element Type:", _gui_get_default_elem_type(model_name, default_part_name)),
        ("Global Seed:", str(parsers.mesh_defaults["global_seed"])),
    )

    part_name, element_type, global_seed = abaqus.getInputs(
        dialogTitle="Turbo Turtle Mesh",
        label=_mixed_settings._mesh_gui_help_string,
        fields=fields,
    )

    if part_name is not None:  # Will be None if the user hits the "cancel/esc" button
        if not global_seed:
            error_message = "Error: You must specify a global seed for meshing"
            raise RuntimeError(error_message)

        if not element_type:
            error_message = "Error: You must specify an element type for meshing"
            raise RuntimeError(error_message)

        user_inputs = {
            "element_type": element_type,
            "model_name": model_name,
            "part_name": part_name,
            "global_seed": float(global_seed),
        }
    else:
        user_inputs = {}
    return user_inputs


def _gui():
    """Function with no inputs that drives the plug-in"""
    _abaqus_utilities.gui_wrapper(
        inputs_function=_gui_get_inputs, subcommand_function=mesh, post_action_function=_abaqus_utilities._view_part
    )


if __name__ == "__main__":
    if "caeModules" in sys.modules:  # All Abaqus CAE sessions immediately load caeModules
        _gui()
    else:
        parser = parsers.mesh_parser(basename=basename)
        try:
            args, unknown = parser.parse_known_args()
        except SystemExit as err:
            sys.exit(err.code)

        sys.exit(
            main(
                args.input_file,
                args.element_type,
                output_file=args.output_file,
                model_name=args.model_name,
                part_name=args.part_name,
                global_seed=args.global_seed,
                edge_seeds=args.edge_seeds,
            )
        )
