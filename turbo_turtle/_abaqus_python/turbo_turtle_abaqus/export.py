import re
import os
import sys
import inspect
import fnmatch


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import parsers  # noqa: E402
from turbo_turtle_abaqus import _mixed_utilities  # noqa: E402
from turbo_turtle_abaqus import _abaqus_utilities  # noqa: E402
from turbo_turtle_abaqus import _mixed_settings  # noqa: E402


def main(
    input_file,
    model_name=parsers.export_defaults["model_name"],
    part_name=parsers.export_defaults["part_name"],
    element_type=parsers.export_defaults["element_type"],
    destination=parsers.export_defaults["destination"],
    assembly=parsers.export_defaults["assembly"],
):
    """Wrap orphan mesh export function for input file handling

    :param str input_file: Abaqus CAE file to open that already contains a model with a part to be meshed
    :param str model_name: model to query in the Abaqus model database
    :param list part_name: list of parts to query in the specified Abaqus model
    :param list element_type: list of element types, one per part name or one global replacement for every part name
    :param str destination: write output orphan mesh files to this output directory
    :param str assembly: Assembly file for exporting the assembly keyword block. If provided and no instances are
        found, instance all part names before export.
    """
    input_file = os.path.splitext(input_file)[0] + ".cae"
    with _abaqus_utilities.AbaqusNamedTemporaryFile(input_file, suffix=".cae", dir="."):
        export(
            model_name=model_name,
            part_name=part_name,
            element_type=element_type,
            destination=destination,
            assembly=assembly,
        )


def export(model_name, part_name, element_type, destination, assembly):
    """Driver function for exporting part and assembly files

    :param str model_name: model to query in the Abaqus model database
    :param list part_name: list of parts to query in the specified Abaqus model
    :param list element_type: list of element types, one per part name or one global replacement for every part name
    :param str destination: write output orphan mesh files to this output directory
    :param str assembly: Assembly file for exporting the assembly keyword block. If provided and no instances are
        found, instance all part names before export.
    """
    element_type = _mixed_utilities.validate_element_type_or_exit(
        length_part_name=len(part_name), element_type=element_type
    )

    export_multiple_parts(
        model_name=model_name, part_name=part_name, element_type=element_type, destination=destination
    )
    if assembly is not None:
        assembly = os.path.splitext(assembly)[0] + ".inp"
        _export_assembly(assembly, model_name, part_name)


def _export_assembly(assembly_file, model_name, part_name):
    import abaqus
    import abaqusConstants

    model = abaqus.mdb.models[model_name]
    assembly = model.rootAssembly
    if len(part_name) == 0:
        part_name = model.parts.keys()
    if len(assembly.instances.keys()) == 0:
        for new_instance in part_name:
            part = abaqus.mdb.models[model_name].parts[new_instance]
            assembly.Instance(name=new_instance, part=part, dependent=abaqusConstants.ON)
    model.keywordBlock.synchVersions()
    block = model.keywordBlock.sieBlocks
    block_string = "\n".join(block)
    regex = r"\*assembly.*?\*end assembly"
    assembly_text = re.findall(regex, block_string, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    assembly_text = assembly_text[0]
    assembly_text_list = assembly_text.split("\n")
    assembly_text_list.pop(0)
    assembly_text_list.pop(-1)
    assembly_text = "\n".join(assembly_text_list)
    with open(assembly_file, "w") as output:
        output.write(assembly_text)
        output.write("\n")


def export_multiple_parts(model_name, part_name, element_type, destination):
    """Export orphan mesh files for multiple parts, and allow element type changes

    Specify a model name and one or multiple part names for exporting orphan mesh files. This function will write one
    orphan mesh file per part name specified, and the orphan mesh file name will be the part name.

    :param str model_name: model to query in the Abaqus model database
    :param list part_name: list of parts to query in the specified Abaqus model
    :param list element_type: list of element types, one per part name or one global replacement for every part name
    :param str destination: write output orphan mesh files to this output directory

    :returns: uses :meth:`turbo_turtle._export.export` to write an orphan mesh file and optionally modifies element
              types with :turbo_turtle._export.substitute_element_type`
    """
    import abaqus
    import abaqusConstants

    for new_part, new_element in zip(part_name, element_type):
        tmp_name = "tmp" + new_part
        # Create a temporary model to house a single part
        abaqus.mdb.Model(name=tmp_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
        # Copy current part to tmp model
        abaqus.mdb.models[tmp_name].Part(new_part, abaqus.mdb.models[model_name].parts[new_part])
        mesh_output_file = os.path.join(destination, new_part) + ".inp"
        export_mesh_file(output_file=mesh_output_file, model_name=tmp_name, part_name=new_part)
        if new_element is not None:
            _mixed_utilities.substitute_element_type(mesh_output_file, new_element)


def export_mesh_file(
    output_file, model_name=parsers.export_defaults["model_name"], part_name=parsers.export_defaults["part_name"][0]
):
    """Export an orphan mesh from a single part

    :param str output_file: Abaqus CAE file to save with the newly meshed part
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model

    :returns: writes ``output_file``
    """
    import abaqus
    import abaqusConstants

    model = abaqus.mdb.models[model_name]
    assembly = model.rootAssembly
    if len(assembly.instances.keys()) == 0:
        part = abaqus.mdb.models[model_name].parts[part_name]
        assembly.Instance(name=part_name, part=part, dependent=abaqusConstants.ON)

    model.keywordBlock.synchVersions()
    block = model.keywordBlock.sieBlocks
    block_string = "\n".join(block)
    orphan_mesh = re.findall(
        r".*?\*Part, name=({})$\n(.*?)\*End Part".format(part_name), block_string, re.DOTALL | re.I | re.M
    )
    part_definition = orphan_mesh[0]
    with open(output_file, "w") as output:
        output.write(part_definition[1].strip())


def _gui_get_inputs():
    """Interactive Inputs

    Prompt the user for inputs with this interactive data entry function. When called, this function opens an Abaqus CAE
    GUI window with text boxes to enter the values given below. Note to developers - if you update this 'GUI-INPUTS'
    below, also update ``_mixed_settings._export_gui_help_string`` that gets used as the GUI ``label``.

    GUI-INPUTS
    ==========
    * Model Name - model to query
    * Part Name - list of part names to query. Comma separated, no spaces (part-1 or part-1,part-2).
    * Element Type - list of element types, one per part, or one global replacement for every part. If blank, element
      type in the part will not be changed. Comma separated, no spaces (c3d8r or c3d8r,c3d8).
    * Destination - destination directory for orphan mesh files
    * Assembly File - file with assembly block keywords. If provided, and no instances are found, all part names are
      instanced before exporting the file.

    **IMPORTANT** - this function must return key-value pairs that will successfully unpack as ``**kwargs`` in
    ``export``

    :return: ``user_inputs`` - a dictionary of the following key-value pair types:

    * ``model_name``: ``str`` type, model to query
    * ``part_name``: ``list`` type, part names to query
    * ``element_type``: ``list`` type, element types one for each part or  one global replacement
    * ``destination``: ``str`` type, destination directory for orphan mesh files
    * ``assembly``: ``str`` type, assembly keword block file. If provided and no instances are found, all part names are
      instanced before exporting the file.
    """
    import abaqus

    model_name = abaqus.session.viewports[abaqus.session.currentViewportName].displayedObject.modelName

    try:
        default_part_name = abaqus.session.viewports[abaqus.session.currentViewportName].displayedObject.name
    except AttributeError:
        print("Warning: could not determine a default part name using the current viewport")
        default_part_name = parsers.export_defaults["part_name"][0]  # part_name defaults to list of length 1

    fields = (
        ("Model Name:", model_name),
        ("Part Name:", default_part_name),
        ("Element Type:", ""),
        ("Destination:", parsers.export_defaults["destination"]),
        ("Assembly File:", ""),
    )

    model_name, part_name_strings, element_type_strings, destination, assembly = abaqus.getInputs(
        dialogTitle="Turbo Turtle Export",
        label=_mixed_settings._export_gui_help_string,
        fields=fields,
    )

    if model_name is not None:  # Model name will be None if the user hits the "cancel/esc" button
        if part_name_strings == "rootAssembly":
            part_name = []
        elif not part_name_strings:
            part_name = []
        else:
            part_name = []
            for this_part_name_string in part_name_strings.split(","):
                part_name += fnmatch.filter(abaqus.mdb.models[model_name].parts.keys(), this_part_name_string)

        element_type = element_type_strings.split(",")
        if len(element_type) == 1 and not element_type[0]:
            element_type = [None]

        user_inputs = {
            "model_name": model_name,
            "part_name": part_name,
            "element_type": element_type,
            "destination": destination,
            "assembly": assembly,
        }
    else:
        user_inputs = {}
    return user_inputs


def _gui():
    """Function with no inputs that drives the plug-in"""
    _abaqus_utilities.gui_wrapper(
        inputs_function=_gui_get_inputs, subcommand_function=export, post_action_function=None
    )


if __name__ == "__main__":
    if "caeModules" in sys.modules:  # All Abaqus CAE sessions immediately load caeModules
        _gui()
    else:
        parser = parsers.export_parser()
        try:
            args, unknown = parser.parse_known_args()
        except SystemExit as err:
            sys.exit(err.code)

        sys.exit(
            main(
                args.input_file,
                model_name=args.model_name,
                part_name=args.part_name,
                element_type=args.element_type,
                destination=args.destination,
                assembly=args.assembly,
            )
        )
