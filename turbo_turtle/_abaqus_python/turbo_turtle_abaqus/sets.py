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
from turbo_turtle_abaqus import _abaqus_utilities
from turbo_turtle_abaqus import _mixed_utilities


def main(
    input_file,
    face_sets=parsers.sets_defaults["face_sets"],
    edge_sets=parsers.sets_defaults["edge_sets"],
    vertex_sets=parsers.sets_defaults["vertex_sets"],
    output_file=parsers.sets_defaults["output_file"],
    model_name=parsers.sets_defaults["model_name"],
    part_name=parsers.sets_defaults["part_name"]
):
    """Wrap sets function for input file handling

    :param str input_file: Abaqus CAE file to open that already contains a model with a part to be meshed
    :param list[tuple[str, str]] face_sets: Face set tuples (name, mask)
    :param list[tuple[str, str]] edge_sets: Edge set tuples (name, mask)
    :param list[tuple[str, str]] vertex_sets: Vertex set tuples (name, mask)
    :param str output_file: Abaqus CAE file to save with the newly meshed part
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model
    """
    import abaqus

    if not any([face_sets, edge_sets, vertex_sets]):
        _mixed_utilities.sys_exit("Must specify at least one of: face_sets, edge_sets, vertex_sets")

    try:
        if output_file is None:
            output_file = input_file
        input_file = os.path.splitext(input_file)[0] + ".cae"
        output_file = os.path.splitext(output_file)[0] + ".cae"
        with tempfile.NamedTemporaryFile(suffix=".cae", dir=".") as copy_file:
            shutil.copyfile(input_file, copy_file.name)
            abaqus.openMdb(pathName=copy_file.name)
            sets(
                face_sets=face_sets,
                edge_sets=edge_sets,
                vertex_sets=vertex_sets,
                model_name=model_name,
                part_name=part_name
            )
    except RuntimeError as err:
        _mixed_utilities.sys_exit(err.message)
    abaqus.mdb.saveAs(pathName=output_file)


def sets(
    face_sets=parsers.sets_defaults["face_sets"],
    edge_sets=parsers.sets_defaults["edge_sets"],
    vertex_sets=parsers.sets_defaults["vertex_sets"],
    model_name=parsers.sets_defaults["model_name"],
    part_name=parsers.sets_defaults["part_name"]
):
    """Create sets from masks

    :param list[tuple[str, str]] face_sets: Face set tuples (name, mask)
    :param list[tuple[str, str]] edge_sets: Edge set tuples (name, mask)
    :param list[tuple[str, str]] vertex_sets: Vertex set tuples (name, mask)
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model
    """
    import abaqus

    model = abaqus.mdb.models[model_name]
    part = model.parts[part_name]

    if face_sets is not None:
        _abaqus_utilities.set_from_mask(part, "faces", face_sets)
        _abaqus_utilities.surface_from_mask(part, "faces", face_sets)

    if edge_sets is not None:
        _abaqus_utilities.set_from_mask(part, "edges", edge_sets)
        if _abaqus_utilities.part_dimensionality(part) == 2:
            _abaqus_utilities.surface_from_mask(part, "edges", edge_sets)

    if vertex_sets is not None:
        _abaqus_utilities.set_from_mask(part, "vertices", vertex_sets)


if __name__ == "__main__":
    if 'caeModules' in sys.modules:  # All Abaqus CAE sessions immediately load caeModules
        pass
    else:
        parser = parsers.sets_parser(basename=basename)
        try:
            args, unknown = parser.parse_known_args()
        except SystemExit as err:
            sys.exit(err.code)

        sys.exit(main(
            args.input_file,
            face_sets=args.face_sets,
            edge_sets=args.edge_sets,
            vertex_sets=args.vertex_sets,
            output_file=args.output_file,
            model_name=args.model_name,
            part_name=args.part_name,
        ))
