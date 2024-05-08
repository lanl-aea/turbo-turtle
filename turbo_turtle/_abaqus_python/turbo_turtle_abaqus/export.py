import re
import os
import sys
import shutil
import inspect
import argparse
import tempfile


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import parsers
from turbo_turtle_abaqus import _mixed_utilities
from turbo_turtle_abaqus import _abaqus_utilities
from turbo_turtle_abaqus import _mixed_settings


def main(input_file,
         model_name=parsers.export_defaults["model_name"],
         part_name=parsers.export_defaults["part_name"],
         element_type=parsers.export_defaults["element_type"],
         destination=parsers.export_defaults["destination"],
         assembly=parsers.export_defaults["assembly"]):
    """Wrap orphan mesh export function for input file handling

    :param str input_file: Abaqus CAE file to open that already contains a model with a part to be meshed
    :param str model_name: model to query in the Abaqus model database
    :param list part_name: list of parts to query in the specified Abaqus model
    :param list element_type: list of element types, one per part name or one global replacement for every part name
    :param str destination: write output orphan mesh files to this output directory
    :param bool assembly: Assembly file for exporting the assembly keyword block. If provided and no instances are
        found, instance all part names before export.
    """
    import abaqus
    input_file = os.path.splitext(input_file)[0] + ".cae"
    element_type = \
        _mixed_utilities.validate_element_type_or_exit(length_part_name=len(part_name), element_type=element_type)
    with tempfile.NamedTemporaryFile(suffix=".cae", dir=".") as copy_file:
        shutil.copyfile(input_file, copy_file.name)
        abaqus.openMdb(pathName=copy_file.name)
        export_multiple_parts(model_name=model_name, part_name=part_name, element_type=element_type,
                              destination=destination)
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
    block_string = '\n'.join(block)
    regex = r"\*assembly.*?\*end assembly"
    assembly_text = re.findall(regex, block_string, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    assembly_text = assembly_text[0]
    assembly_text_list = assembly_text.split("\n")
    assembly_text_list.pop(0)
    assembly_text_list.pop(-1)
    assembly_text = "\n".join(assembly_text_list)
    with open(assembly_file, 'w') as output:
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
        export(output_file=mesh_output_file, model_name=tmp_name, part_name=new_part)
        if new_element is not None:
            _mixed_utilities.substitute_element_type(mesh_output_file, new_element)


def export(output_file,
           model_name=parsers.export_defaults["model_name"],
           part_name=parsers.export_defaults["part_name"][0]):
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
    orphan_mesh = re.findall(r".*?\*Part, name=({})$\n(.*?)\*End Part".format(part_name),
                             block_string, re.DOTALL | re.I | re.M)
    part_definition = orphan_mesh[0]
    with open(output_file, 'w') as output:
        output.write(part_definition[1].strip())


if __name__ == "__main__":
    parser = parsers.export_parser()
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit as err:
        sys.exit(err.code)

    sys.exit(main(
        args.input_file,
        model_name=args.model_name,
        part_name=args.part_name,
        element_type=args.element_type,
        destination=args.destination,
        assembly=args.assembly
    ))
