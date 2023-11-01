import re
import os
import sys
import shutil
import inspect
import argparse
import tempfile

default_output_file = None
default_model_name = "Model-1"
default_part_names = ["Part-1"]
default_element_types = []

def main(input_file, output_file=default_output_file, model_name=default_model_name,
         part_names=default_part_names, element_types=default_element_types):
    """Wrap orphan mesh export function for input file handling

    :param str input_file: Abaqus CAE file to open that already contains a model with a part to be meshed
    :param str output_file: Abaqus CAE file to save with the newly meshed part
    :param str model_name: model to query in the Abaqus model database
    :param list part_names: list of parts to query in the specified Abaqus model
    :param list element_types: list of element types, one for each part specified in ``part_names``
    """
    import abaqus

    if output_file is None:
        output_file = input_file
    input_file = os.path.splitext(input_file)[0] + ".cae"
    output_file = os.path.splitext(output_file)[0] + ".inp"
    with tempfile.NamedTemporaryFile(suffix=".cae", dir=".") as copy_file:
        shutil.copyfile(input_file, copy_file.name)
        abaqus.openMdb(pathName=copy_file.name)
        export(output_file, model_name=model_name, part_name=part_name)


def export(output_file, model_name=default_model_name, part_name=default_part_name):
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
    parser.add_argument("--output-file", type=str, default=default_output_file,
                        help="Abaqus INP output file (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument("--part-names", type=str, nargs='+', default=default_part_name,
                        help="List of Abaqus part names (default: %(default)s)")
    parser.add_argument("--element-types", type=str, nargs='+', default=default_element_types,
                        help="List of element types, one for each part specified in part_names (default: %(default)s means no element type substitution)"

    return parser


if __name__ == "__main__":
    parser = get_parser()
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit as err:
        sys.exit(err.code)

    sys.exit(main(
        args.input_file,
        output_file=args.output_file,
        model_name=args.model_name,
        part_names=args.part_names,
        element_types=args.element_types
    ))
