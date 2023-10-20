import numpy as np
import ast
import os
import argparse
import inspect


def main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions):
    """Turbo Turtle

    Main work-horse function

    This function partitions an **arbitrary, hollow, body** using the turtle shell method (also know as the soccer ball
    method). The following list of actions is performed using generalized vector equations to allow nearly any body to
    be partitioned. This script can be executed from Abaqus CAE from the command line.

    If the body is modeled with symmetry (e.g. quater or half symmetry), this code will attempt all partitioning and
    face removal actions anyways. If certain aspects of the code fail, the code will move on and give no errors.

    **Note:** This behavior means that it is possible to create strange looking partitions if inputs are not defined
    properly. Always check your partitions visually after using this tool.

    1. Define ``center``
    2. Define ``xpoint``
    3. Define ``main_axis`` through ``center`` and ``xpoint``
    4. Create a plane normal to ``main_axis`` at the ``center`` called ``plane1``
    5. Create ``zpoint`` on ``plane1`` to finish the coordinate system definition
    6. Create a plane called ``plane2`` on ``center``, ``xpoint``, and ``zpoint``
    7. Create a plane perpendicular called ``plane3`` to ``plane1`` and ``plane2`` by rotating ``plane2`` about ``main_axis`` by 90 deg
    8. Create axis at intersection of ``plane2`` and ``plane1`` called ``axis21``
    9. Create axis at intersection of ``plane3`` and ``plane1`` called ``axis31``
    10. Partition all cells by ``plane1``, ``plane2``, and ``plane3``
    11. Create planes called ``plane1p`` and ``plane1n`` by rotating ``plane1`` about ``axis21`` by 45 and -45 deg, respectively
    12. Create planes called ``plane2p`` and ``plane2n`` by rotating ``plane2`` about ``main_axis`` by 45 and -45 deg, respectively
    13. Create planes called ``plane2p`` and ``plane3n`` by rotating ``plane3`` about ``axis31`` by 45 and -45 deg, respectively
    14. Partition all cells by ``plane1p`` and ``plane1n``
    15. Partition all cells by ``plane2p`` and ``plane2n``
    16. Partition all cells by ``plane3p`` and ``plane3n``
    17.	Define unit vectors of ``xpoint`` and ``zpoint``
    18. Finalize the orthonormal coordinate system by creating the ``ypoint`` unit vector via the cross product of the
        ``xpoint`` and ``zpoint`` vectors
    19. Find the vertices that intersect faces to remove along the x-axis
    20. Find faces with a normal at ``plane_angle`` to the local coordinate system
    21. Recursively remove the faces and redundant enties (as a result of removed faces)
    22. same as **19** but for y-axis vertices
    23. Same as **20** but for y-axis vertices
    24. Same as **21** but for y-axis vertices
    25. Same as **19** but for z-axis vertices
    26. Same as **20** but for z-axis vertices
    27. Same as **21** bur for z-axis vertices
    28. Partition an offset principal planes defined by ``partitions``
    29. Validate the resulting geometry and topology

    :param center: center location of the geometry
    :type center: list

    :param xpoint: location on the x-axis local to the geometry
    :type xpoint: list

    :param zpoint: location on the z-axis local to the geometry
    :type zpoint: list

    :param plane_angle: angle at which partition planes will be created
    :type plane_angle: float

    :param partitions: partitions to be created by offsetting the principal planes. This is only available when using
        the Abaqus CAE GUI.
    :type partitions: dict

    :param model_name: model to query in the Abaqus model database (only applies when used with ``abaqus cae -nogui``)
    :type model_name: str

    :param part_name: part to query in the specified Abaqus model (only applies when used with ``abaqus cae -nogui``)
    :type part_name: str

    :param input_file: Abaqus CAE file to open that already contains a model with a part to be partitioned (only applies
        when used with ``abaqus cae -nogui``)
    :type input_file: str

    :param output_file: Abaqus CAE file to save with the newly partitioned part (only applies when used with ``abaqus
        cae -nogui``)
    :type output_file: str

    :param partitions: locations of partitions to be created by offsetting the principal planes
    :type partitions: dict

    :returns: Abaqus CAE database named ``{output_file}.cae`` if executed from the command line
    """
    from abaqus import *
    from abaqusConstants import *
    from caeModules import *

    if center is None:
        print('\nTurboTurtle was canceled\n')
        return

    if input_file is None:
        model_name = session.viewports[session.currentViewportName].displayedObject.modelName
        part_name = session.viewports[session.currentViewportName].displayedObject.name
    else:
        openMdb(pathName=input_file)

    # Step 1 - define center
    p = mdb.models[model_name].parts[part_name]
    p.DatumPointByCoordinate(coords=tuple(center))

    # Step 2 - define xpoint
    p = mdb.models[model_name].parts[part_name]
    p.DatumPointByCoordinate(coords=tuple(xpoint))

    # Step 3 - create main_axis
    p = mdb.models[model_name].parts[part_name]
    main_axis = p.datums[p.DatumAxisByTwoPoint(point1=tuple(center), point2=tuple(xpoint)).id]

    # Step 4 - create plane1
    p = mdb.models[model_name].parts[part_name]
    plane1 = p.datums[p.DatumPlaneByPointNormal(point=tuple(center), normal=main_axis).id]

    # Step 5 - define zpoint
    p = mdb.models[model_name].parts[part_name]
    p.DatumPointByCoordinate(coords=tuple(zpoint))

    # Step 6 - create plane2
    p = mdb.models[model_name].parts[part_name]
    plane2 = p.datums[p.DatumPlaneByThreePoints(point1=tuple(center), point2=tuple(xpoint), point3=tuple(zpoint)).id]

    # Step 7 - create plane3
    p = mdb.models[model_name].parts[part_name]
    plane3 = p.datums[p.DatumPlaneByRotation(plane=plane2, axis=main_axis, angle=90.0).id]

    # Step 8 - create axis21
    p = mdb.models[model_name].parts[part_name]
    axis21 = p.datums[p.DatumAxisByTwoPlane(plane1=plane2, plane2=plane1).id]

    # Step 9 - create axis 31
    p = mdb.models[model_name].parts[part_name]
    axis31 = p.datums[p.DatumAxisByTwoPlane(plane1=plane3, plane2=plane1).id]

    # Step 10 - partition all cells by plane1, plane2, and plane3
    try:
        p = mdb.models[model_name].parts[part_name]
        p.PartitionCellByDatumPlane(datumPlane=plane1, cells=p.cells[:])
    except:
        pass
    try:
        p = mdb.models[model_name].parts[part_name]
        p.PartitionCellByDatumPlane(datumPlane=plane2, cells=p.cells[:])
    except:
        pass
    try:
        p = mdb.models[model_name].parts[part_name]
        p.PartitionCellByDatumPlane(datumPlane=plane3, cells=p.cells[:])
    except:
        pass

    # Step 11 - create plane1p and plane1n
    p = mdb.models[model_name].parts[part_name]
    plane1p = p.datums[p.DatumPlaneByRotation(plane=plane1, axis=axis21, angle=plane_angle).id]
    p = mdb.models[model_name].parts[part_name]
    plane1n = p.datums[p.DatumPlaneByRotation(plane=plane1, axis=axis21, angle=-plane_angle).id]

    # Step 12 - create plane2p and plane2n
    p = mdb.models[model_name].parts[part_name]
    plane2p = p.datums[p.DatumPlaneByRotation(plane=plane2, axis=main_axis, angle=plane_angle).id]
    p = mdb.models[model_name].parts[part_name]
    plane2n = p.datums[p.DatumPlaneByRotation(plane=plane2, axis=main_axis, angle=-plane_angle).id]

    # Step 13 - create plane3p and plane3n
    p = mdb.models[model_name].parts[part_name]
    plane3p = p.datums[p.DatumPlaneByRotation(plane=plane3, axis=axis31, angle=plane_angle).id]
    p = mdb.models[model_name].parts[part_name]
    plane3n = p.datums[p.DatumPlaneByRotation(plane=plane3, axis=axis31, angle=-plane_angle).id]

    # Step 14 - partition all cells by plane1p and plane1n
    try:
        p = mdb.models[model_name].parts[part_name]
        p.PartitionCellByDatumPlane(datumPlane=plane1p, cells=p.cells[:])
    except:
        pass
    try:
        p = mdb.models[model_name].parts[part_name]
        p.PartitionCellByDatumPlane(datumPlane=plane1n, cells=p.cells[:])
    except:
        pass

    # Step 15 - partition all cells by plane2p and plane2n
    try:
        p = mdb.models[model_name].parts[part_name]
        p.PartitionCellByDatumPlane(datumPlane=plane2p, cells=p.cells[:])
    except:
        pass
    try:
        p = mdb.models[model_name].parts[part_name]
        p.PartitionCellByDatumPlane(datumPlane=plane2n, cells=p.cells[:])
    except:
        pass

    # Step 16 - partition all cells by plane3p and plane3n
    try:
        p = mdb.models[model_name].parts[part_name]
        p.PartitionCellByDatumPlane(datumPlane=plane3p, cells=p.cells[:])
    except:
        pass
    try:
        p = mdb.models[model_name].parts[part_name]
        p.PartitionCellByDatumPlane(datumPlane=plane3n, cells=p.cells[:])
    except:
        pass

    p = mdb.models[model_name].parts[part_name]
    center = np.array(center)
    xpoint = np.array(xpoint)
    zpoint = np.array(zpoint)

    # Step 17 - define unit vectors from xpoint and zpoint
    xpoint_vector = xpoint-center
    xpoint_vector = xpoint_vector / np.linalg.norm(xpoint_vector)
    zpoint_vector = zpoint-center
    zpoint_vector = zpoint_vector / np.linalg.norm(zpoint_vector)

    # Step 18 - define a ypoint unit vector
    ypoint_vector = np.cross(zpoint_vector, xpoint_vector)

    # Step 19 - Find the vertices intersecting faces to remove for the x-axis
    found_face = True

    while found_face:
        p = mdb.models[model_name].parts[part_name]
        vertices = p.vertices
        x_vectors = ()
        for v in vertices:
            pointOn = np.asarray(v.pointOn[0])
            this_vector = pointOn - center
            this_vector = this_vector / np.linalg.norm(this_vector)
            if np.abs(np.abs(np.dot(this_vector, xpoint_vector)) - 1.0) < 0.01:
                x_vectors += ((v), )
        x_points = np.asarray([v.pointOn[0][0] for v in x_vectors])
        x_points.sort()
        x_vectors_grabbed = ()
        for xp in x_points:
            for v in x_vectors:
                pointOn = v.pointOn[0]
                if pointOn[0]  == xp:
                    x_vectors_grabbed += ((v), )
        x_vectors_grabbed_idxs = [v.index for v in x_vectors_grabbed]

        # Step 20 - locate faces with a normal at the plane_angle to the local coordinate system
        # Step 21 - recursively remove the faces and redundant enties as a result of removed faces
        p = mdb.models[model_name].parts[part_name]
        for II, face in enumerate(p.faces):
            this_vert_idxs = face.getVertices()
            try:
                if x_vectors_grabbed_idxs[1] in this_vert_idxs or x_vectors_grabbed_idxs[2] in this_vert_idxs:
                    this_normal = np.array(face.getNormal())
                    this_normal = this_normal / np.linalg.norm(this_normal)
                    if np.abs(np.abs(np.dot(this_normal, zpoint_vector))-np.abs(np.cos(plane_angle*np.pi/180.0))) < 0.001:
                        # p.DatumPointByCoordinate(coords=face.getCentroid()[0])
                        p.RemoveFaces(faceList=p.faces[face.index:(face.index+1)], deleteCells=False)
                        p = mdb.models[model_name].parts[part_name]
                        p.RemoveRedundantEntities(vertexList = p.vertices[:], edgeList = p.edges[:])
                        found_face = True
                        break
            except:
                pass
        if II == (len(p.faces)-1):
            found_face = False
        else:
            pass

    #Step 22 - same as 19 but for y
    found_face = True
    while found_face:
        p = mdb.models[model_name].parts[part_name]
        vertices = p.vertices
        y_vectors = ()
        for v in vertices:
            pointOn = np.asarray(v.pointOn[0])
            this_vector = pointOn - center
            this_vector = this_vector / np.linalg.norm(this_vector)
            if np.abs(np.abs(np.dot(this_vector, ypoint_vector)) - 1.0) < 0.01:
                y_vectors += ((v), )
        y_points = np.asarray([v.pointOn[0][1] for v in y_vectors])
        y_points.sort()
        y_vectors_grabbed = ()
        for yp in y_points:
            for v in y_vectors:
                pointOn = v.pointOn[0]
                if pointOn[1] == yp:
                    y_vectors_grabbed += ((v), )
        y_vectors_grabbed_idxs = [v.index for v in y_vectors_grabbed]

        # Step 23 - same as 20 but for y
        # Step 24 - same as 21 but for y
        p = mdb.models[model_name].parts[part_name]
        for II, face in enumerate(p.faces):
            this_vert_idxs = face.getVertices()
            try:
                if y_vectors_grabbed_idxs[1] in this_vert_idxs or y_vectors_grabbed_idxs[2] in this_vert_idxs:
                    this_normal = np.array(face.getNormal())
                    this_normal = this_normal / np.linalg.norm(this_normal)
                    if np.abs(np.abs(np.dot(this_normal, xpoint_vector))-np.cos(plane_angle*np.pi/180.0)) < 0.001:
                        # p.DatumPointByCoordinate(coords=face.getCentroid()[0])
                        p.RemoveFaces(faceList=p.faces[face.index:(face.index+1)], deleteCells=False)
                        p = mdb.models[model_name].parts[part_name]
                        p.RemoveRedundantEntities(vertexList = p.vertices[:], edgeList = p.edges[:])
                        found_face = True
                        break
            except:
                pass
        if II == (len(p.faces)-1):
            found_face = False
        else:
            pass

    # Step 25 - same as 19 but for z
    found_face = True
    while found_face:
        p = mdb.models[model_name].parts[part_name]
        vertices = p.vertices
        z_vectors = ()
        for v in vertices:
            pointOn = np.asarray(v.pointOn[0])
            this_vector = pointOn - center
            this_vector = this_vector / np.linalg.norm(this_vector)
            if np.abs(np.abs(np.dot(this_vector, zpoint_vector)) - 1.0) < 0.01:
                z_vectors += ((v), )
        z_points = np.asarray([v.pointOn[0][2] for v in z_vectors])
        z_points.sort()
        z_vectors_grabbed = ()
        for zp in z_points:
            for v in z_vectors:
                pointOn = v.pointOn[0]
                if pointOn[2] == zp:
                    z_vectors_grabbed += ((v), )
        z_vectors_grabbed_idxs = [v.index for v in z_vectors_grabbed]

        # Step 26 - same as 20 but for z
        # Step 27 - same as 21 but for z
        p = mdb.models[model_name].parts[part_name]
        for II, face in enumerate(p.faces):
            this_vert_idxs = face.getVertices()
            try:
                if z_vectors_grabbed_idxs[1] in this_vert_idxs or z_vectors_grabbed_idxs[2] in this_vert_idxs:
                    this_normal = np.array(face.getNormal())
                    this_normal = this_normal / np.linalg.norm(this_normal)
                    if np.abs(np.abs(np.dot(this_normal, ypoint_vector))-np.cos(plane_angle*np.pi/180.0)) < 0.001:
                        # p.DatumPointByCoordinate(coords=face.getCentroid()[0])
                        p.RemoveFaces(faceList=p.faces[face.index:(face.index+1)], deleteCells=False)
                        p = mdb.models[model_name].parts[part_name]
                        p.RemoveRedundantEntities(vertexList = p.vertices[:], edgeList = p.edges[:])
                        found_face = True
                        break
            except:
                pass
        if II == (len(p.faces)-1):
            found_face = False
        else:
            pass

    # Step 28 - partition the offset planes
    for coord in partitions:
        if coord == 'x':
            selected_plane = plane1
        elif coord == 'y':
            selected_plane = plane2
        elif coord == 'z':
            selected_plane = plane3
        for val in [x for x in partitions[coord] if x != 0.0]:
            p = mdb.models[model_name].parts[part_name]
            this_plane = p.datums[p.DatumPlaneByOffset(plane=selected_plane, offset=val, flip=SIDE2).id]
            try:
                p.PartitionCellByDatumPlane(datumPlane=this_plane, cells=p.cells[:])
            except:
                pass

    # Step 29 - validate geometry
    p = mdb.models[model_name].parts[part_name]
    mdb.models[model_name].parts[part_name].checkGeometry()

    # Finally, save the model or set the viewport to remove nasty datum planes and axes
    if output_file is None:
        session.viewports[session.currentViewportName].partDisplay.geometryOptions.setValues(datumPoints=OFF, datumAxes=OFF, datumPlanes=OFF)
    else:
        mdb.saveAs(pathName=output_file)

    return


def get_inputs():
    """Interactive Inputs

    Prompt the user for inputs with this interactive data entry function. When called, this function opens an Abaqus CAE
    GUI window with text boxes to enter values for the outputs listed below:

    :return: ``center`` - center location of the geometry
    :rtype: list

    :return: ``xpoint`` - location on the x-axis local to the geometry
    :rtype: list

    :return: ``zpoint`` - location on the z-axis local to the geometry
    :rtype: list

    :return: ``plane_angle`` - angle at which partition planes will be created
    :rtype: float

    :return: ``partitions`` - locations to create partitions by offsetting principal planes
    :rtype: dict
    """
    from abaqus import getInputs

    fields = (('Center:','0.0, 0.0, 0.0'),
        ('X-Axis Point:', '1.0, 0.0, 0.0'),
        ('Z-Axis Point:', '0.0, 0.0, 1.0'),
        ('Partition Angle:', '45.0'),
        ('Partitions Along X', '0.0, 0.0'),
        ('Partitions Along Y', '0.0, 0.0'),
        ('Partitions Along Z', '0.0, 0.0'),
        ('Copy and Paste Parameters', 'ctrl+c ctrl+v printed parameters'), )
    center, xpoint, zpoint, plane_angle, partition_x, partition_y, partition_z, cp_parameters = getInputs(fields=fields,
        label='Specify Geometric Parameters:',
        dialogTitle='Turbo Turtle', )
    partitions = {}
    if center is not None:
        if cp_parameters != fields[-1][-1]:
            cp_param = [x.replace('\n', '') for x in cp_parameters.split('\n')]
            center = ast.literal_eval(cp_param[0].replace('Center: ', ''))
            xpoint = ast.literal_eval(cp_param[1].replace('X-Axis Point: ', ''))
            zpoint = ast.literal_eval(cp_param[2].replace('Z-Axis Point: ', ''))
            plane_angle = ast.literal_eval(cp_param[3].replace('Partition Angle: ', ''))
            partition_x = ast.literal_eval(cp_param[4].replace('Partitions Along X: ', ''))
            partition_y = ast.literal_eval(cp_param[5].replace('Partitions Along Y: ', ''))
            partition_z = ast.literal_eval(cp_param[6].replace('Partitions Along Z: ', ''))
        else:
            center = list(ast.literal_eval(center))
            xpoint = list(ast.literal_eval(xpoint))
            zpoint = list(ast.literal_eval(zpoint))
            plane_angle = ast.literal_eval(plane_angle)
            partition_x = [ast.literal_eval(x) for x in partition_x.replace(' ', '').split(',')]
            partition_y = [ast.literal_eval(x) for x in partition_y.replace(' ', '').split(',')]
            partition_z = [ast.literal_eval(x) for x in partition_z.replace(' ', '').split(',')]
        partitions['x'] = partition_x
        partitions['y'] = partition_y
        partitions['z'] = partition_z
        print('\nPartitioning Parameters Entered By User:')
        print('----------------------------------------')
        print('Center: {}'.format(center))
        print('X-Axis Point: {}'.format(xpoint))
        print('Z-Axis Point: {}'.format(zpoint))
        print('Partition Angle: {}'.format(plane_angle))
        print('Partitions Along X: {}'.format(partition_x))
        print('Partitions Along Y: {}'.format(partition_y))
        print('Partitions Along Z: {}'.format(partition_z))
        print('')
    return center, xpoint, zpoint, plane_angle, partitions


def get_parser():
    # The global '__file__' variable doesn't appear to be set when executing from Abaqus CAE
    filename = inspect.getfile(lambda: None)
    basename = os.path.basename(filename)

    # Set Defaults
    default_center = [0.0, 0.0, 0.0]
    default_xpoint = [1.0, 0.0, 0.0]
    default_zpoint = [0.0, 0.0, 1.0]
    default_plane_angle = 45.0
    default_partitions_x = [0.0, 0.0]
    default_partitions_y = [0.0, 0.0]
    default_partitions_z = [0.0, 0.0]

    prog = "abaqus cae -noGui {} --".format(basename)
    cli_description = "Partition a spherical shape into a turtle shell given a small number of locating parameters."
    parser = argparse.ArgumentParser(description=cli_description, prog=prog)
    parser.add_argument('--xpoint', nargs=3, type=float, default=default_xpoint,
                        help="Point on the x-axis (default: %(default)s)")
    parser.add_argument('--center', nargs=3, type=float, default=default_center,
                        help="Center of the sphere (default: %(default)s)")
    parser.add_argument('--zpoint', nargs=3, type=float, default=default_zpoint,
                        help="Point on the z-axis (default: %(default)s)")
    parser.add_argument('--plane-angle', type=float, default=default_plane_angle,
                        help="Angle for non-principal partitions (default: %(default)s)")
    parser.add_argument('--x-partitions', type=float, nargs='+', default=default_partitions_x,
                        help="Create a partition offset from the x-principal-plane (default: %(default)s)")
    parser.add_argument('--y-partitions', type=float, nargs='+', default=default_partitions_y,
                        help="Create a partition offset from the y-principal-plane (default: %(default)s)")
    parser.add_argument('--z-partitions', type=float, nargs='+', default=default_partitions_z,
                        help="Create a partition offset from the z-principal-plane (default: %(default)s)")

    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--model-name', type=str, required=True,
                        help="Abaqus model name")
    requiredNamed.add_argument('--part-name', type=str, required=True,
                        help="Abaqus part name")
    requiredNamed.add_argument('--input-file', type=str, required=True,
                        help="Abaqus model database to open")
    parser.add_argument('--output-file', type=str, default=None,
                        help="Abaqus model database to save to. Defaults to the specified --input-file")
    return parser


if __name__ == "__main__":
    try:
        center, xpoint, zpoint, plane_angle, partitions = get_inputs()
        model_name=None
        part_name=None
        input_file=None
        output_file=None
    except:
        pass
        parser = get_parser()
        args, unknown = parser.parse_known_args()
        if args.output_file is None:
            args.output_file = args.input_file
        center=args.center
        xpoint=args.xpoint
        zpoint=args.zpoint
        plane_angle=args.plane_angle
        model_name=args.model_name
        part_name=args.part_name
        input_file=args.input_file
        output_file=args.output_file
        partitions = {'x': args.x_partitions,
                      'y': args.y_partitions,
                      'z': args.z_partitions}
    main(center, xpoint, zpoint, plane_angle, model_name, part_name, input_file, output_file, partitions)
