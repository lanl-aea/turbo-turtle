import os
import sys
import shutil
import inspect
import argparse
import tempfile


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import _parsers


def main(input_file, element_type,
         output_file=mesh_default_output_file,
         model_name=mesh_default_model_name,
         part_name=mesh_default_part_name,
         global_seed=mesh_default_global_seed):
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


def mesh(element_type,
         model_name=mesh_default_model_name,
         part_name=mesh_default_part_name,
         global_seed=mesh_default_global_seed):
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




if __name__ == "__main__":

    parser = _parsers.mesh_parser(basename=basename)
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit as err:
        sys.exit(err.code)

    sys.exit(main(
        args.input_file,
        args.element_type,
        output_file=args.output_file,
        model_name=args.model_name,
        part_name=args.part_name,
        global_seed=args.global_seed
    ))
