import ast
import os
import sys
import inspect
import fnmatch

import numpy


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
grandparent = os.path.dirname(parent)
sys.path.insert(0, grandparent)
from turbo_turtle_abaqus import parsers  # noqa: E402
from turbo_turtle_abaqus import vertices  # noqa: E402
from turbo_turtle_abaqus import _abaqus_utilities  # noqa: E402
from turbo_turtle_abaqus import _mixed_settings  # noqa: E402


def main(
    input_file,
    output_file=parsers.partition_defaults["output_file"],
    center=parsers.partition_defaults["center"],
    xvector=parsers.partition_defaults["xvector"],
    zvector=parsers.partition_defaults["zvector"],
    model_name=parsers.partition_defaults["model_name"],
    part_name=parsers.partition_defaults["part_name"],
    big_number=parsers.partition_defaults["big_number"],
):
    """Wrap  partition function with file open and file write operations

    :param str input_file: Abaqus CAE model database to open
    :param str output_file: Abaqus CAE model database to write. If none is provided, use the input file.
    :param list center: center location of the geometry
    :param list xvector: Local x-axis vector defined in global coordinates
    :param list zvector: Local z-axis vector defined in global coordinates
    :param str model_name: model to query in the Abaqus model database (only applies when used with ``abaqus cae
        -nogui``)
    :param list part_name: list of parts to query in the specified Abaqus model (only applies when used with ``abaqus
        cae -nogui``)
    :param float big_number: Number larger than the outer radius of the part to partition.

    :returns: Abaqus CAE database named ``{output_file}.cae``
    """
    import abaqus

    if output_file is None:
        output_file = input_file
    input_file = os.path.splitext(input_file)[0] + ".cae"
    output_file = os.path.splitext(output_file)[0] + ".cae"
    with _abaqus_utilities.AbaqusNamedTemporaryFile(input_file, suffix=".cae", dir="."):
        partition(center, xvector, zvector, model_name, part_name, big_number=big_number)
        abaqus.mdb.saveAs(pathName=output_file)


def datum_axis(center, vector, part):
    """Return an Abaqus DataAxis object by center and normal axis

    :param numpy.array center: center location of the axis
    :param numpy.array vector: axis vector
    :param abaqus.mdb.models[].parts[] part: Abaqus part object

    :returns: Abaqus datum axis object
    :rtype: DatumAxis
    """
    point = center + vector
    return part.datums[part.DatumAxisByTwoPoint(point1=tuple(center), point2=tuple(point)).id]


def datum_plane(center, normal, part):
    """Return an Abaqus DataPlane object by center and normal axis

    :param numpy.array center: center location of the plane
    :param numpy.array normal: plane normal vector
    :param abaqus.mdb.models[].parts[] part: Abaqus part object

    :returns: Abaqus Datum Plane object
    :rtype: DatumPlane
    """
    axis = datum_axis(center, normal, part)
    return part.datums[part.DatumPlaneByPointNormal(point=tuple(center), normal=axis).id]


def partition(center, xvector, zvector, model_name, part_name, big_number=parsers.partition_defaults["big_number"]):
    """Partition the model/part with the turtle shell method, also know as the soccer ball method.

    If the body is modeled with fractional symmetry (e.g. quater or half symmetry), this code will attempt all
    partitioning and face removal actions anyways. If certain aspects of the code fail, the code will move on and give
    no errors.

    **Note:** It is possible to create strange looking partitions if inputs are not defined properly. Always check your
    partitions visually after using this tool.

    :param list center: center location of the geometry
    :param list xvector: Local x-axis vector defined in global coordinates
    :param list zvector: Local z-axis vector defined in global coordinates
    :param str model_name: model to query in the Abaqus model database (only applies when used with ``abaqus cae
        -nogui``)
    :param list part_name: list of parts to query in the specified Abaqus model (only applies when used with ``abaqus
        cae -nogui``)
    :param float big_number: Number larger than the outer radius of the part to partition.
    """
    import abaqus

    # Process input and calculate local coordinate system properties
    xvector = vertices.normalize_vector(xvector)
    zvector = vertices.normalize_vector(zvector)
    yvector = numpy.cross(zvector, xvector)
    center = numpy.array(center)

    angle = numpy.pi / 2.0 - numpy.arccos(numpy.sqrt(2.0 / 3.0))
    big_number_coordinates = vertices.rectalinear_coordinates([big_number], [angle])[0]

    sketch_vertex_pairs = (
        (
            (-big_number_coordinates[0], big_number_coordinates[1]),  # fmt: skip # noqa: E201,E241
            ( big_number_coordinates[0], big_number_coordinates[1]),  # fmt: skip # noqa: E201,E241
        ),
        (
            (-big_number_coordinates[0], -big_number_coordinates[1]),  # fmt: skip # noqa: E201,E241
            ( big_number_coordinates[0], -big_number_coordinates[1]),  # fmt: skip # noqa: E201,E241
        ),
    )

    for current_part in part_name:
        part = abaqus.mdb.models[model_name].parts[current_part]
        if _abaqus_utilities.part_dimensionality_key(part) in ("Axisymmetric", "2D Planar"):  # Abaqus 2023.HF5
            partition_2d(model_name, current_part, center, big_number, sketch_vertex_pairs)
        else:
            partition_3d(model_name, current_part, center, xvector, yvector, zvector, sketch_vertex_pairs)
        abaqus.mdb.models[model_name].parts[current_part].checkGeometry()


def partition_3d(model_name, part_name, center, xvector, yvector, zvector, sketch_vertex_pairs):
    """Partition a 3D-revolved part by using the turtle shell method, also known as the soccer ball method.

    :param str model_name: model to query in the Abaqus model database (only applies when used with ``abaqus cae
        -nogui``)
    :param list part_name: list of parts to query in the specified Abaqus model (only applies when used with ``abaqus
        cae -nogui``)
    :param list center: center location of the geometry
    :param list xvector: Local x-axis vector defined in global coordinates
    :param list yvector: Local y-axis vector defined in global coordinates
    :param list zvector: Local z-axis vector defined in global coordinates
    :param tuple sketch_vertex_pairs: Tuple of vertices that make up the 3D partioning scheme's sketch (See
        :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices.rectalinear_coordinates`)
    """
    import abaqus
    import abaqusConstants

    # Process input and calculate local coordinate system properties
    plane_normals = vertices.datum_planes(xvector, zvector)

    # TODO: This depends on the :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices.datum_planes` tuple
    # order. Find a way to programmatically calculate (or return) the paired positive sketch edge instead of hardcoding
    # the matching order.
    positive_sketch_axis = (yvector, yvector, zvector, zvector, xvector, xvector)

    model = abaqus.mdb.models[model_name]
    part = model.parts[part_name]

    # Create local coordinate system primary partition planes
    partition_planes = [datum_plane(center, normal, part) for normal in plane_normals]

    # Partition by three (3) local coordinate system x/y/z planes
    for plane in partition_planes[0:3]:
        try:
            part.PartitionCellByDatumPlane(datumPlane=plane, cells=part.cells[:])
        except abaqus.AbaqusException:
            pass

    # Partition by sketch on the six (6) 45 degree planes
    for edge, plane in zip(positive_sketch_axis, partition_planes[3:]):
        axis = datum_axis(center, edge, part)
        # TODO: Move to a dedicated partition function
        for vertex_1, vertex_2 in sketch_vertex_pairs:
            transform = part.MakeSketchTransform(
                sketchPlane=plane,
                sketchUpEdge=axis,
                sketchPlaneSide=abaqusConstants.SIDE1,
                origin=center,
            )
            sketch = model.ConstrainedSketch(
                name="__profile__",
                sheetSize=91.45,
                gridSpacing=2.28,
                transform=transform,
            )
            sketch.setPrimaryObject(option=abaqusConstants.SUPERIMPOSE)
            part.projectReferencesOntoSketch(sketch=sketch, filter=abaqusConstants.COPLANAR_EDGES)
            sketch.Line(point1=(0.0, 0.0), point2=vertex_1)
            sketch.Line(point1=(0.0, 0.0), point2=vertex_2)
            sketch.Line(point1=vertex_1, point2=vertex_2)
            try:
                part.PartitionCellBySketch(
                    sketchPlane=plane,
                    sketchUpEdge=axis,
                    cells=part.cells[:],
                    sketch=sketch,
                )
            # TODO: Is it possible to distinguish between expected failures (operating on an incomplete sphere,
            # so sketch doesn't intersect) and unexpected failures (bad options, missing geometry, etc)?
            except abaqus.AbaqusException:
                pass


def partition_2d(model_name, part_name, center, big_number, sketch_vertex_pairs):
    """Partition a 2D-axisymmetric part by three lines using the same vertex pairs computed for the 3D case

    :param str model_name: model to query in the Abaqus model database (only applies when used with ``abaqus cae
        -nogui``)
    :param list part_name: list of parts to query in the specified Abaqus model (only applies when used with ``abaqus
        cae -nogui``)
    :param list center: center location of the geometry
    :param float big_number: Number larger than the outer radius of the part to partition.
    :param tuple sketch_vertex_pairs: Tuple of vertices that make up the 3D partioning scheme's sketch (See
        :meth:`turbo_turtle._abaqus_python.turbo_turtle_abaqus.vertices.rectalinear_coordinates`)
    """

    import abaqus
    import abaqusConstants

    model = abaqus.mdb.models[model_name]
    part = model.parts[part_name]
    transform = part.MakeSketchTransform(
        sketchPlane=part.faces[0],
        sketchPlaneSide=abaqusConstants.SIDE1,
        origin=center,
    )
    sketch = model.ConstrainedSketch(
        name="__profile__",
        sheetSize=91.45,
        gridSpacing=2.28,
        transform=transform,
    )
    sketch.setPrimaryObject(option=abaqusConstants.SUPERIMPOSE)
    part.projectReferencesOntoSketch(sketch=sketch, filter=abaqusConstants.COPLANAR_EDGES)

    sketch_vertices = (
        sketch_vertex_pairs[0][1],  # +x +45 degree partition
        sketch_vertex_pairs[1][1],  # +x -45 degree partition
        (big_number, 0.0),  # Must manually construct the +x horizontal partition
        sketch_vertex_pairs[0][0],  # -x +45 degree partition
        sketch_vertex_pairs[1][0],  # -x -45 degree partition
        (-big_number, 0.0),  # Must manually construct the -x horizontal partition
        (0.0, big_number),  # Must manually construct the +y vertical partition
        (0.0, -big_number),  # Must manually construct the -y vertical partition
    )

    for current_vertex in sketch_vertices:
        sketch.Line(point1=(0.0, 0.0), point2=current_vertex)
    try:
        part.PartitionFaceBySketch(faces=part.faces[:], sketch=sketch)
    # TODO: Is is possible to distinguish between expected failures (operating on an incomplete sphere, so
    # sketch doesn't intersect) and unexpected failures (bad options, missing geometry, etc)?
    except abaqus.AbaqusException:
        pass


def _gui_get_inputs():
    """Partition Interactive Inputs

    Prompt the user for inputs with this interactive data entry function. When called, this function opens an Abaqus CAE
    GUI window with text boxes to enter the values given below. Note to developers - if you update this 'GUI-INPUTS'
    below, also update ``_mixed_settings._partition_gui_help_string`` that gets used as the GUI ``label``.

    GUI-INPUTS
    ==========
    * Center - center location of the geometry
    * X-Vector - location on the x-axis local to the geometry
    * Z-Vector - location on the z-axis local to the geometry
    * Part Name(s) - part name(s) to partition as a comma separated list (NO SPACES). This can also be a glob statement
    * Copy and Paste Parameters - copy and paste the parameters printed to the Abaqus Python terminal to make
      re-use of previous partition parameters easier

    **IMPORTANT** - this function must return key-value pairs that will successfully unpack as ``**kwargs`` in
    ``partition``

    :return: ``user_inputs`` - a dictionary of the following key-value pair types:

    * ``center``: ``list`` type,  center location of the geometry
    * ``xvector``: ``list`` type, location on the x-axis local to the geometry
    * ``zvector``: ``list`` type, location on the z-axis local to the geometry
    * ``model_name``: ``str`` type, name of the model in the current viewport
    * ``part_name``: ``list`` type, name of the part in the current viewport, or a list of all part names in the model
    """
    import abaqus

    try:
        default_part_name = abaqus.session.viewports[abaqus.session.currentViewportName].displayedObject.name
    except AttributeError:
        print("Warning: could not determine a default part name using the current viewport")
        default_part_name = parsers.partition_defaults["part_name"][0]  # part_name defaults to list of length 1

    fields = (
        ("Center:", str(parsers.partition_defaults["center"]).replace("[", "").replace("]", "")),
        ("X-Vector:", str(parsers.partition_defaults["xvector"]).replace("[", "").replace("]", "")),
        ("Z-Vector:", str(parsers.partition_defaults["zvector"]).replace("[", "").replace("]", "")),
        ("Part Name(s):", default_part_name),
        ("Copy and Paste Parameters", "ctrl+c ctrl+v printed parameters"),
    )

    center, xvector, zvector, part_name_strings, cp_parameters = abaqus.getInputs(
        dialogTitle="Turbo Turtle Partition",
        label=_mixed_settings._partition_gui_help_string,
        fields=fields,
    )

    if center is not None:  # Center will be None if the user hits the "cancel/esc" button
        if cp_parameters != fields[-1][-1]:
            cp_param = [x.replace("\n", "") for x in cp_parameters.split("\n")]
            center = ast.literal_eval(cp_param[0].replace("Center: ", ""))
            xvector = ast.literal_eval(cp_param[1].replace("X-Vector: ", ""))
            zvector = ast.literal_eval(cp_param[2].replace("Z-Vector: ", ""))
        else:
            center = list(ast.literal_eval(center))
            xvector = list(ast.literal_eval(xvector))
            zvector = list(ast.literal_eval(zvector))
        print("\nPartitioning Parameters Entered By User:")
        print("----------------------------------------")
        print('Only copy the three lines below to use "Copy and Paste Parameters"\n')
        print("Center: {}".format(center))
        print("X-Vector: {}".format(xvector))
        print("Z-Vector: {}".format(zvector))
        print("")

        model_name = abaqus.session.viewports[abaqus.session.currentViewportName].displayedObject.modelName
        part_name = []
        for this_part_name_string in part_name_strings.split(","):
            part_name += fnmatch.filter(abaqus.mdb.models[model_name].parts.keys(), this_part_name_string)

        user_inputs = {
            "center": center,
            "xvector": xvector,
            "zvector": zvector,
            "model_name": model_name,
            "part_name": part_name,
        }
    else:
        user_inputs = {}
    return user_inputs


def _gui():
    """Function with no inputs that drives the plug-in"""
    _abaqus_utilities.gui_wrapper(
        inputs_function=_gui_get_inputs,
        subcommand_function=partition,
        post_action_function=_abaqus_utilities._view_part,
    )


if __name__ == "__main__":
    if "caeModules" in sys.modules:  # All Abaqus CAE sessions immediately load caeModules
        _gui()
    else:
        parser = parsers.partition_parser(basename=basename)
        try:
            args, unknown = parser.parse_known_args()
        except SystemExit as err:
            sys.exit(err.code)

        sys.exit(
            main(
                input_file=args.input_file,
                output_file=args.output_file,
                center=args.center,
                xvector=args.xvector,
                zvector=args.zvector,
                model_name=args.model_name,
                part_name=args.part_name,
                big_number=args.big_number,
            )
        )
