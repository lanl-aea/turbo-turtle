import os
import sys
import inspect

filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import parsers  # noqa: E402
from turbo_turtle_abaqus import _mixed_utilities  # noqa: E402


def main(
    input_file,
    output_file,
    merged_model_name=parsers.merge_defaults["merged_model_name"],
    model_name=parsers.merge_defaults["model_name"],
    part_name=parsers.merge_defaults["part_name"],
):
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

    part_name = _mixed_utilities.remove_duplicate_items(part_name)
    requested_part_count = len(part_name)

    input_file = [os.path.splitext(input_file_name)[0] + ".cae" for input_file_name in input_file]
    output_file = os.path.splitext(output_file)[0] + ".cae"

    # This loop creates temporary models and then cleans them at the end, because you cannot have multiple abaqus.mdb
    # objects active under the same ``abaqus cae -noGui`` kernel
    merged_model = abaqus.mdb.Model(name=merged_model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
    for cae_file in input_file:
        abaqus.mdb.openAuxMdb(pathName=cae_file)
        available_models = abaqus.mdb.getAuxMdbModelNames()
        current_models = _mixed_utilities.intersection_of_lists(model_name, available_models)
        # Loop through current model_name
        for this_model in current_models:
            tmp_model = "temporary_model_" + this_model
            abaqus.mdb.copyAuxMdbModel(fromName=this_model, toName=tmp_model)
            available_parts = abaqus.mdb.models[tmp_model].parts.keys()
            current_parts = _mixed_utilities.intersection_of_lists(part_name, available_parts)
            # Loop through part_name and send a warning when a part name is not found in the current model
            for this_part in current_parts:
                try:
                    merged_model.Part(this_part, abaqus.mdb.models[tmp_model].parts[this_part])
                    success_message = (
                        "SUCCESS: merged part '{}' from model '{}' from '{}' into merged model '{}'\n".format(
                            this_part, this_model, cae_file, merged_model_name
                        )
                    )
                    sys.stdout.write(success_message)
                except abaqus.AbaqusException as err:
                    message = "ERROR: could not merge part '{}' in model '{}' in database '{}'\n{}".format(
                        this_part, this_model, cae_file, err
                    )
                    _mixed_utilities.sys_exit(message)
            # If the current model was found in the current cae_file, clean it before ending the loop
            if tmp_model is not None:
                del abaqus.mdb.models[tmp_model]
        abaqus.mdb.closeAuxMdb()
    abaqus.mdb.saveAs(pathName=output_file)

    merged_part_count = len(merged_model.parts.keys())
    if merged_part_count == 0:
        message = "No parts were merged. Check the input file, model and part name lists."
        _mixed_utilities.sys_exit(message)
    elif part_name[0] is not None and merged_part_count != requested_part_count:
        message = "Merged part count '{}' doesn't match unique part name count '{}'.".format(
            merged_part_count, requested_part_count
        )
        _mixed_utilities.sys_exit(message)


if __name__ == "__main__":
    parser = parsers.merge_parser(basename=basename)
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit as err:
        sys.exit(err.code)

    sys.exit(
        main(
            input_file=args.input_file,
            output_file=args.output_file,
            merged_model_name=args.merged_model_name,
            model_name=args.model_name,
            part_name=args.part_name,
        )
    )
