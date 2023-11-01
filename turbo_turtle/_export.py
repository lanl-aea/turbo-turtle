import re
import os
import sys
import shutil
import inspect
import argparse
import tempfile

default_model_name = "Model-1"
default_part_names = ["Part-1"]
default_element_types = []

def main(input_file, model_name=default_model_name, part_names=default_part_names,
    element_types=default_element_types):
    """Wrap orphan mesh export function for input file handling

    :param str input_file: Abaqus CAE file to open that already contains a model with a part to be meshed
    :param str model_name: model to query in the Abaqus model database
    :param list part_names: list of parts to query in the specified Abaqus model
    :param list element_types: list of element types, one for each part specified in ``part_names`` or empty
    """
    import abaqus

    input_file = os.path.splitext(input_file)[0] + ".cae"
    element_types = _validate_element_types_length(part_names, element_types)
    with tempfile.NamedTemporaryFile(suffix=".cae", dir=".") as copy_file:
        shutil.copyfile(input_file, copy_file.name)
        abaqus.openMdb(pathName=copy_file.name)
        export_multiple_parts(model_name=model_name, part_names=part_names, element_types=element_types)


def export_multiple_parts(model_name, part_names, element_types):
    """Export orphan mesh files for multiple parts, and allow element type changes
    
    Specify a model name and one or multiple part names for exporting orphan mesh files. This function will write one 
    orphan mesh file per part name specified, and the orphan mesh file name will be the part name.
    
    :param str model_name: model to query in the Abaqus model database
    :param list part_names: list of parts to query in the specified Abaqus model
    :param list element_types: list of element types, one for each part specified in ``part_names`` or empty
    
    :returns: uses :meth:`turbo_turtle._export.export` to write an orphan mesh file and optionally modifies element 
              types
    """
    import abaqusConstants

    for part_name, element_type in zip(part_names, element_types):
        mdb.Model(name=tmp_name, modelType=abaqusConstants.STANDARD_EXPLICIT)  # Create a temporary model to house a single part
        mdb.models[tmp_name].Part(part_name, mdb.models[model_name].parts[part_name])  # Copy current part to tmp model
        mesh_output_file = part_name + ".inp"
        export(output_file=mesh_output_file, model_name=tmp_name, part_name=part_name)
        del mdb.models[tmp_name]  # Delete temprary model
        
        if element_type is not None:
            with open(mesh_output_file, 'r') as output:
                orphan_mesh_lines = output.readlines()
            # TODO: Simplify this by using regex
            for II, l in enumerate(orphan_mesh_lines):
                if l.upper().find("*ELEMENT") == 0:
                    orphan_mesh_lines[II] = "*Element, type={}\n".format(element_type)
            with open(mesh_output_file, 'w') as output:
                output.writelines(orphan_mesh_lines)


def _validate_element_types_length(part_names, element_types):
    """Validate the number of element types provided
    
    Element types must either be an empty list to indicate that no element type change should be performed or a list of 
    the same length as part_names.
    
    :param list part_names: list of parts for exporting orphan meshes
    :param list element_types: list of element types, one for each part in ``part_names`` or empty
    
    :return: element types
    :rtype: list
    """
    if element_types and len(part_names) != len(element_types):
        sys.exit("Number of element types must match the number of part names\n")
    elif not element_types:  # Empty list of element types indicates to skip element type change operations
        element_types = [None] * len(part_names)  # None values will be skipped in the exporter function
    return element_types


def export(output_file, model_name=default_model_name, part_name=default_part_names[0]):
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
    block_string = '\n'.join(block)
    orphan_mesh = re.findall(".*?\*Part, name=({})$\n(.*?)\*End Part".format(part_name),
                             block_string, re.DOTALL | re.I | re.M)
    part_definition = orphan_mesh[0]
    with open(output_file, 'w') as output:
        output.write(part_definition[1].strip())


def get_parser():
    file_name = inspect.getfile(lambda: None)
    base_name = os.path.basename(file_name)

    prog = "abaqus cae -noGui {} --".format(base_name)
    cli_description = "Export an Abaqus part mesh as an orphan mesh"

    parser = argparse.ArgumentParser(description=cli_description, prog=prog)

    parser.add_argument("--input-file", type=str, required=True,
                        help="Abaqus CAE input file")
    parser.add_argument("--model-name", type=str, default=default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument("--part-names", type=str, nargs='+', default=default_part_names,
                        help="List of Abaqus part names (default: %(default)s)")
    parser.add_argument("--element-types", type=str, nargs='+', default=default_element_types,
                        help="List of element types, one for each part specified in part_names (default: %(default)s means no element type substitution)")

    return parser


if __name__ == "__main__":
    parser = get_parser()
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit as err:
        sys.exit(err.code)

    sys.exit(main(
        args.input_file,
        model_name=args.model_name,
        part_names=args.part_names,
        element_types=args.element_types
    ))
