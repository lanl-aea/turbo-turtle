import os
import sys
import inspect


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import parsers  # noqa: E402
from turbo_turtle_abaqus import _abaqus_utilities  # noqa: E402
from turbo_turtle_abaqus import _mixed_utilities  # noqa: E402


def main(
    input_file,
    face_sets=parsers.sets_defaults["face_sets"],
    edge_sets=parsers.sets_defaults["edge_sets"],
    vertex_sets=parsers.sets_defaults["vertex_sets"],
    output_file=parsers.sets_defaults["output_file"],
    model_name=parsers.sets_defaults["model_name"],
    part_name=parsers.sets_defaults["part_name"],
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
        with _abaqus_utilities.AbaqusNamedTemporaryFile(input_file, suffix=".cae", dir="."):
            sets(
                face_sets=face_sets,
                edge_sets=edge_sets,
                vertex_sets=vertex_sets,
                model_name=model_name,
                part_name=part_name,
            )
            abaqus.mdb.saveAs(pathName=output_file)
    except RuntimeError as err:
        _mixed_utilities.sys_exit(str(err))


def sets(
    face_sets=parsers.sets_defaults["face_sets"],
    edge_sets=parsers.sets_defaults["edge_sets"],
    vertex_sets=parsers.sets_defaults["vertex_sets"],
    model_name=parsers.sets_defaults["model_name"],
    part_name=parsers.sets_defaults["part_name"],
):
    """Create sets from masks

    :param list[tuple[str, str]] face_sets: Face set tuples (name, mask)
    :param list[tuple[str, str]] edge_sets: Edge set tuples (name, mask)
    :param list[tuple[str, str]] vertex_sets: Vertex set tuples (name, mask)
    :param str model_name: model to query in the Abaqus model database
    :param str part_name: part to query in the specified Abaqus model

    :raises RuntimeError: Collection of all set creation RuntimeError(s)
    """
    import abaqus

    model = abaqus.mdb.models[model_name]
    part = model.parts[part_name]

    error_messages = []
    try:
        if face_sets is not None:
            _abaqus_utilities.set_from_mask(part, "faces", face_sets)
            _abaqus_utilities.surface_from_mask(part, "faces", face_sets)
    except RuntimeError as face_err:
        error_messages.append("{}".format(face_err))

    try:
        if edge_sets is not None:
            _abaqus_utilities.set_from_mask(part, "edges", edge_sets)
            if _abaqus_utilities.part_dimensionality(part) == 2:
                _abaqus_utilities.surface_from_mask(part, "edges", edge_sets)
    except RuntimeError as face_err:
        error_messages.append("{}".format(face_err))

    try:
        if vertex_sets is not None:
            _abaqus_utilities.set_from_mask(part, "vertices", vertex_sets)
    except RuntimeError as face_err:
        error_messages.append("{}".format(face_err))

    if error_messages:
        message = "\n".join(error_messages)
        raise RuntimeError(message)


if __name__ == "__main__":
    if "caeModules" in sys.modules:  # All Abaqus CAE sessions immediately load caeModules
        pass
    else:
        parser = parsers.sets_parser(basename=basename)
        try:
            args, unknown = parser.parse_known_args()
        except SystemExit as err:
            sys.exit(err.code)

        sys.exit(
            main(
                args.input_file,
                face_sets=args.face_sets,
                edge_sets=args.edge_sets,
                vertex_sets=args.vertex_sets,
                output_file=args.output_file,
                model_name=args.model_name,
                part_name=args.part_name,
            )
        )
