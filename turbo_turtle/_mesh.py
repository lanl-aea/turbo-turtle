import os
import sys
import shutil
import inspect
import argparse
import tempfile


default_output_file = None
default_model_name = "Model-1"
default_part_name = "Part-1"
default_global_seed = 1.0


def main(input_file, element_type, output_file=default_output_file, model_name=default_model_name,
         part_name=default_part_name, global_seed=default_global_seed):
    """Wrap mesh function for input file handling

    :param str input_file: Abaqus CAE file to open that already contains a model with a part to be meshed
    :param str element_type: Abaqus element type
    :param str output_file: Abaqus CAE file to save with the newly meshed part
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model
    :param float global_seed: The global mesh seed size
    """
    import abaqus

    if output_file is None:
        output_file = input_file
    input_file = os.path.splitext(input_file)[0] + ".cae"
    output_file = os.path.splitext(output_file)[0] + ".cae"
    with tempfile.NamedTemporaryFile(suffix=".cae", dir=".") as copy_file:
        shutil.copyfile(input_file, copy_file.name)
        abaqus.openMdb(pathName=copy_file.name)
        mesh(element_type, model_name=model_name, part_name=part_name, global_seed=global_seed)
        abaqus.mdb.saveAs(pathName=output_file)


def mesh(element_type, model_name=default_model_name, part_name=default_part_name, global_seed=default_global_seed):
    """Apply a global seed and mesh the specified part

    :param str element_type: Abaqus element type
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model
    :param float global_seed: The global mesh seed size
    """
    import mesh
    import abaqus
    import abaqusConstants

    model = abaqus.mdb.models[model_name]
    part = model.parts[part_name]

    # TODO: make the deviation and size factor options
    part.seedPart(size=global_seed, deviationFactor=0.1, minSizeFactor=0.1)

    # TODO: figure out how to use element type for both 2D/3D meshes
    element_type_object = return_abaqus_constant(element_type)
    if element_type_object is None:
        sys.stderr.write("Element type '{}' not found in abaqusConstants".format(element_type))
        sys.exit(1)
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


def return_abaqus_constant(search_string):
    """If search_string is found in the abaqusConstants module, return the abaqusConstants object. Else None

    :param str search_string: string to search in the abaqusConstants module attributes

    :return value: abaqusConstants attribute, if it exists. Else None
    :rtype: abaqusConstants attribute type, if it exists. Else None
    """
    import abaqusConstants

    search_string = search_string.upper()
    attribute = None
    if hasattr(abaqusConstants, search_string):
        attribute = getattr(abaqusConstants, search_string)
    return attribute


def get_parser():
    file_name = inspect.getfile(lambda: None)
    base_name = os.path.basename(file_name)

    prog = "abaqus cae -noGui {} --".format(base_name)
    cli_description = "Mesh an Abaqus part from a global seed"

    parser = argparse.ArgumentParser(description=cli_description, prog=prog)

    parser.add_argument("--input-file", type=str, required=True,
                        help="Abaqus CAE input file")
    parser.add_argument("--element-type", type=str, required=True,
                        help="Abaqus element type")
    parser.add_argument("--output-file", type=str, default=default_output_file,
                        help="Abaqus CAE output file (default: %(default)s)")
    parser.add_argument("--model-name", type=str, default=default_model_name,
                        help="Abaqus model name (default: %(default)s)")
    parser.add_argument("--part-name", type=str, default=default_part_name,
                        help="Abaqus part name (default: %(default)s)")
    parser.add_argument("--global-seed", type=float, default=default_global_seed,
                        help="The global mesh seed size. Positive float.")

    return parser


if __name__ == "__main__":
    parser = get_parser()
    args, unknown = parser.parse_known_args()

    sys.exit(main(
        args.input_file,
        args.element_type,
        output_file=args.output_file,
        model_name=args.model_name,
        part_name=args.part_name,
        global_seed=args.global_seed
    ))
