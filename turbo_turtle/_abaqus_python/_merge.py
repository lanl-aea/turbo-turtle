import re
import os
import sys
import shutil
import inspect
import argparse

def main(input_file, output_file, merged_model_name, model_name, part_name):
    """Merge parts from multiple Abaqus CAE files and models into one Abaqus CAE file and model

    This script loops through all input file(s) specified and attempts to query each of the provided model name(s). 
    Within each model, all part_name(s) are queried. If a part name match is found, the part is copied to new merged 
    model.

    :meth:`turbo_turtle._merge._check_for_duplicate_part_names` is used to ensure that parts with identical names cannot 
    be querried and copied to the merged model.

    :param list input_file: Abaqus CAE file(s) to query for model(s)/part(s)
    :param str output_file: Abaqus CAE file for saving the merged model
    :param str merged_model_name: Abaqus model to merge into
    :param list model_name: model name(s) to query
    :param list part_name: part_names(s) to search for
    
    :returns: writes ``{output_file}.cae`` with the merged model
    """    
    import abaqus
    import abaqusConstants
    
    _check_for_duplicate_part_names(part_name)

    input_file = [os.path.splitext(input_file_name)[0] + ".cae" for input_file_name in input_file]
    output_file = os.path.splitext(output_file)[0] + ".cae"

    # This loop creates temporary models and then cleans them at the end, because you cannot have multiple abaqus.mdb 
    # objects active under the same ``abaqus cae -noGui`` kernel
    abaqus.mdb.Model(name=merged_model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
    for cae_file in input_file:
        abaqus.mdb.openAuxMdb(pathName=cae_file)
        # Loop through model_name and send a warning when a model name is not found in the current cae_file
        for this_model in model_name:
            try:
                tmp_model = 'temporary_model_' + this_model
                abaqus.mdb.copyAuxMdbModel(fromName=this_model, toName=tmp_model)
            except:
                tmp_model = None
                warning_message = "WARNING: could not find model '{}' in database '{}'\n".format(this_model, cae_file)
                sys.stdout.write(warning_message)
            # If the current model name was found in the current cae_file, continue
            if tmp_model is not None:
                # Loop through part_name and send a warning when a part name is not found in the current model
                for this_part in part_name:
                    try:
                        abaqus.mdb.models[merged_model_name].Part(this_part,
                            abaqus.mdb.models[tmp_model].parts[this_part])
                        success_message = "SUCCESS: merged part '{}' from model '{}' from '{}' into merged model '{}'\n".format(
                            this_part, this_model, cae_file, merged_model_name)
                        sys.stdout.write(success_message)
                    except:
                        warning_message = "WARNING: could not find part '{}' in model '{}' in database '{}'\n".format(
                            this_part, this_model, cae_file)
                        sys.stdout.write(warning_message)
            # If the current model was found in the current cae_file, clean it before ending the loop
            if tmp_model is not None:
                del abaqus.mdb.models[tmp_model]
        abaqus.mdb.closeAuxMdb()
    abaqus.mdb.saveAs(pathName=output_file)


def _check_for_duplicate_part_names(part_name):
    """Function for checking the ``part_name`` list for duplicates

    Merge behavior in this script assumes unique part names in the final merged model.
    
    :param list part_name: part_names(s) to search for
    
    :returns: non-zero exit code through ``sys.exit`` if duplicate part names are found
    """
    unique_part_names = []
    duplicate_part_names = []
    [unique_part_names.append(x) if x not in unique_part_names else duplicate_part_names.append(x) for x in part_name]
    if duplicate_part_names:
        error_message = "ERROR: part_name list has {} duplicated part names: {}".format(
            len(duplicate_part_names), ', '.join(map(str, duplicate_part_names)))
        sys.stderr.write(error_message)
        sys.exit(1)


def get_parser():
    file_name = inspect.getfile(lambda: None)
    base_name = os.path.basename(file_name)

    prog = "abaqus cae -noGui {} --".format(base_name)
    cli_description = "Merge parts from multiple Abaqus CAE files into a single model"

    parser = argparse.ArgumentParser(description=cli_description, prog=prog)

    parser.add_argument("--input-file", type=str, nargs="+", required=True,
                        help="Abaqus CAE input file(s)")
    parser.add_argument("--output-file", type=str, required=True,
                        help="Abaqus CAE file to save the merged model")
    parser.add_argument("--merged-model-name", type=str, required=True,
                        help="Model to create and merge parts into")
    # TODO: find a way to make default behavior to take all parts from all models from all cae files and merge them
    #       this would make model_name and part_name no longer required
    #       https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/issues/43
    parser.add_argument("--model-name", type=str, nargs="+", required=True,
                        help="Abaqus model name(s) to attempt to query in the input CAE file(s)")
    parser.add_argument("--part-name", type=str, nargs="+", required=True,
                        help="Part name(s) to search for within model(s)")
    return parser


if __name__ == "__main__":
    parser = get_parser()
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit as err:
        sys.exit(err.code)
    
    sys.exit(main(
        input_file=args.input_file,
        output_file=args.output_file,
        merged_model_name=args.merged_model_name,
        model_name=args.model_name,
        part_name=args.part_name
    ))
