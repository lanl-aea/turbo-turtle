import re
import os
import sys
import shutil
import inspect

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import parsers


def main(input_file, output_file,
         merged_model_name=parsers.merge_default_merged_model_name,
         model_name=parsers.merge_default_model_name,
         part_name=parsers.merge_default_part_name):
    """Merge parts from multiple Abaqus CAE files and models into one Abaqus CAE file and model

    This script loops through all input file(s) specified and merges the intersection of provided model/part name(s) and
    available model/part combinations. Duplicate part names are removed from the part name list. If a part name exists
    in more than one model, return an error.

    :param list input_file: Abaqus CAE file(s) to query for model(s)/part(s)
    :param str output_file: Abaqus CAE file for saving the merged model
    :param str merged_model_name: Abaqus model to merge into
    :param list model_name: model name(s) to query
    :param list part_name: part_names(s) to search for

    :returns: writes ``{output_file}.cae`` with the merged model
    """
    import abaqus
    import abaqusConstants

    part_name = _check_for_duplicate_part_names(part_name)

    input_file = [os.path.splitext(input_file_name)[0] + ".cae" for input_file_name in input_file]
    output_file = os.path.splitext(output_file)[0] + ".cae"

    # This loop creates temporary models and then cleans them at the end, because you cannot have multiple abaqus.mdb
    # objects active under the same ``abaqus cae -noGui`` kernel
    merged_model = abaqus.mdb.Model(name=merged_model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
    for cae_file in input_file:
        abaqus.mdb.openAuxMdb(pathName=cae_file)
        available_models = abaqus.mdb.getAuxMdbModelNames()
        current_models = _intersection_of_lists(model_name, available_models)
        # Loop through current model_name
        for this_model in current_models:
            tmp_model = 'temporary_model_' + this_model
            abaqus.mdb.copyAuxMdbModel(fromName=this_model, toName=tmp_model)
            available_parts = abaqus.mdb.models[tmp_model].parts.keys()
            current_parts = _intersection_of_lists(part_name, available_parts)
            # Loop through part_name and send a warning when a part name is not found in the current model
            for this_part in current_parts:
                try:
                    merged_model.Part(this_part, abaqus.mdb.models[tmp_model].parts[this_part])
                    success_message = "SUCCESS: merged part '{}' from model '{}' from '{}' into merged model '{}'\n".format(
                        this_part, this_model, cae_file, merged_model_name)
                    sys.stdout.write(success_message)
                except:
                    warning_message = "ERROR: could not merge part '{}' in model '{}' in database '{}'\n".format(
                        this_part, this_model, cae_file)
                    sys.stderr.write(warning_message)
                    sys.exit(2)
            # If the current model was found in the current cae_file, clean it before ending the loop
            if tmp_model is not None:
                del abaqus.mdb.models[tmp_model]
        abaqus.mdb.closeAuxMdb()
    abaqus.mdb.saveAs(pathName=output_file)


def _intersection_of_lists(requested, available):
    """Return intersection of available and requested items or all available items if none requested

    :param list requested: requested items
    :param list available: available items

    :returns: intersection of requested and available items. All available items if None requested.
    :ttype: list
    """
    if requested[0] is not None and len(requested) > 0:
        intersection = list(set(requested) & set(available))
    else:
        intersection = available
    return intersection


def _check_for_duplicate_part_names(part_name):
    """Function for checking the ``part_name`` list for duplicates

    Merge behavior in this script assumes unique part names in the final merged model. STDERR warning when duplicates
    are found and removed.

    :param list part_name: part_names(s) to search for

    :returns: unique part names
    :rtype: list
    """
    unique_part_names = []
    duplicate_part_names = []
    [unique_part_names.append(x) if x not in unique_part_names else duplicate_part_names.append(x) for x in part_name]
    if duplicate_part_names:
        error_message = "WARNING: removing '{}' duplicate part names: '{}'".format(
            len(duplicate_part_names), ', '.join(map(str, duplicate_part_names)))
        sys.stderr.write(error_message)
    return unique_part_names


if __name__ == "__main__":
    parser = parsers.merge_parser(basename=basename)
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
