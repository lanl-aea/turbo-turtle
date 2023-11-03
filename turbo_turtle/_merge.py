import re
import os
import sys
import shutil
import inspect
import argparse
import tempfile

def main(input_file, output_file, model_name, part_name):
    """Merge parts from multiple Abaqus CAE files and models into one Abaqus CAE file and model
    
    :param list input_file: Abaqus CAE file(s) to query for model(s)/part(s)
    :param str output_file: Abaqus CAE file for saving the merged model
    :param list model_name: model name(s) to query
    :param list part_name: part_names(s) to search for
    """
    
    import abaqus
    import abaqusConstants
    
    input_file = [os.path.splitext(input_file_name)[0] + ".cae" for input_file_name in input_file]
    output_file = os.path.splitext(output_file)[0] + ".cae"
    
    for cae_database in input_file:
        with tempfile.NamedTemporaryFile(suffix=".cae", dir=".") as copy_file:
            shutil.copyfile(cae_database, copy_file.name)
            abaqus.openMdb(pathName=copy_file.name)
            for this_model in model_name:
                if this_model in abaqus.mdb.models.keys():
                    for this_part in part_names:
                        if this_part in mdb.models[this_model].parts.keys()


    for new_part, new_element in zip(part_name, element_type):
        tmp_name = "tmp" + new_part
        # Create a temporary model to house a single part
        abaqus.mdb.Model(name=tmp_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
        # Copy current part to tmp model
        abaqus.mdb.models[tmp_name].Part(new_part, abaqus.mdb.models[model_name].parts[new_part])
        mesh_output_file = os.path.join(destination, new_part) + ".inp"
        export(output_file=mesh_output_file, model_name=tmp_name, part_name=new_part)
        if new_element is not None:
            substitute_element_type(mesh_output_file, new_element)


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
    parser.add_argument("--part-name", type=str, nargs='+', default=default_part_name,
                        help="List of Abaqus part names (default: %(default)s)")
    parser.add_argument("--element-type", type=str, nargs='+', default=default_element_type,
                        help="List of element types, one per part name or one global replacement for every part name (default: %(default)s)")
    parser.add_argument("--destination", type=str, default=default_destination,
                        help="Write orphan mesh files to this output directory (default: PWD)")

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
        part_name=args.part_name,
        element_type=args.element_type,
        destination=args.destination
    ))
