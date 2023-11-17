import ast
import os
import sys
import shutil
import inspect
import argparse
import tempfile

import numpy


filename = inspect.getfile(lambda: None)
basename = os.path.basename(filename)
parent = os.path.dirname(filename)
sys.path.insert(0, parent)
import parsers
import vertices


def main(input_file,
         output_file=parsers.partition_default_output_file,
         center=parsers.partition_default_center,
         xvector=parsers.partition_default_xvector,
         zvector=parsers.partition_default_zvector,
         polar_angle=parsers.partition_default_polar_angle,
         azimuthal_angle=parsers.partition_default_azimuthal_angle,
         model_name=parsers.partition_default_model_name,
         part_name=parsers.partition_default_part_name):
    """Wrap  partition function with file open and file write operations

    :param str input_file: Abaqus CAE model database to open
    :param str output_file: Abaqus CAE model database to write. If none is provided, use the input file.
    :param list center: center location of the geometry
    :param list xvector: Local x-axis vector defined in global coordinates
    :param list zvector: Local z-axis vector defined in global coordinates
    :param float polar_angle: Polar angle measured from the local +y-axis in degrees
    :param float azimuthal_angle: Azimuthal angle measured from the local +x-axis in degrees
    :param str model_name: model to query in the Abaqus model database (only applies when used with ``abaqus cae -nogui``)
    :param str part_name: part to query in the specified Abaqus model (only applies when used with ``abaqus cae -nogui``)

    :returns: Abaqus CAE database named ``{output_file}.cae``
    """
    import abaqus

    if output_file is None:
        output_file = input_file
    input_file = os.path.splitext(input_file)[0] + ".cae"
    output_file = os.path.splitext(output_file)[0] + ".cae"
    with tempfile.NamedTemporaryFile(suffix=".cae", dir=".") as copy_file:
        shutil.copyfile(input_file, copy_file.name)
        abaqus.openMdb(pathName=copy_file.name)
        partition(center, xvector, zvector, polar_angle, azimuthal_angle, model_name, part_name)
        abaqus.mdb.saveAs(pathName=output_file)


def partition(center, xvector, zvector, polar_angle, azimuthal_angle, model_name, part_name):
    """Partition the model/part with the turtle shell method, also know as the soccer ball method.

    If the body is modeled with fractional symmetry (e.g. quater or half symmetry), this code will attempt all
    partitioning and face removal actions anyways. If certain aspects of the code fail, the code will move on and give no
    errors.

    **Note:** It is possible to create strange looking partitions if inputs are not defined properly. Always check your
    partitions visually after using this tool.

    :param list center: center location of the geometry
    :param list xvector: Local x-axis vector defined in global coordinates
    :param list zvector: Local z-axis vector defined in global coordinates
    :param float polar_angle: Polar angle measured from the local +y-axis in degrees
    :param float azimuthal_angle: Azimuthal angle measured from the local +x-axis in degrees
    :param str model_name: model to query in the Abaqus model database (only applies when used with ``abaqus cae -nogui``)
    :param str part_name: part to query in the specified Abaqus model (only applies when used with ``abaqus cae -nogui``)
    """
    import abaqus
    import caeModules


    if center is None:
        print('\nTurboTurtle was canceled\n')
        return

    part = abaqus.mdb.models[model_name].parts[part_name]

    center = numpy.array(center)
    plane_normals = vertices.datum_planes(xvector, zvector, polar_angle, azimuthal_angle)
    for normal in plane_normals:
        point = center + normal
        axis = part.datums[part.DatumAxisByTwoPoint(point1=tuple(center), point2=tuple(point)).id]
        plane = part.datums[part.DatumPlaneByPointNormal(point=tuple(center), normal=axis).id]
        try:
            part.PartitionCellByDatumPlane(datumPlane=plane, cells=part.cells[:])
        except:
            pass

    # Step 19 - Find the vertices intersecting faces to remove for the x-axis
    # TODO: Clean this up. Maybe march along local primary axes? Maybe remove all the surface guessing and save surfaces
    # from partition command?
    plane_angle = 45.
    found_face = True

    while found_face:
        vertices = part.vertices
        x_vectors = ()
        for v in vertices:
            pointOn = numpy.asarray(v.pointOn[0])
            this_vector = pointOn - center
            this_vector = this_vector / numpy.linalg.norm(this_vector)
            if numpy.abs(numpy.abs(numpy.dot(this_vector, xpoint_vector)) - 1.0) < 0.01:
                x_vectors += ((v), )
        x_points = numpy.asarray([v.pointOn[0][0] for v in x_vectors])
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
        for II, face in enumerate(part.faces):
            this_vert_idxs = face.getVertices()
            try:
                if x_vectors_grabbed_idxs[1] in this_vert_idxs or x_vectors_grabbed_idxs[2] in this_vert_idxs:
                    this_normal = numpy.array(face.getNormal())
                    this_normal = this_normal / numpy.linalg.norm(this_normal)
                    if numpy.abs(numpy.abs(numpy.dot(this_normal, zpoint_vector))-numpy.abs(numpy.cos(plane_angle*numpy.pi/180.0))) < 0.001:
                        # part.DatumPointByCoordinate(coords=face.getCentroid()[0])
                        part.RemoveFaces(faceList=part.faces[face.index:(face.index+1)], deleteCells=False)
                        part.RemoveRedundantEntities(vertexList = part.vertices[:], edgeList = part.edges[:])
                        found_face = True
                        break
            except:
                pass
        if II == (len(part.faces)-1):
            found_face = False
        else:
            pass

    #Step 22 - same as 19 but for y
    found_face = True
    while found_face:
        vertices = part.vertices
        y_vectors = ()
        for v in vertices:
            pointOn = numpy.asarray(v.pointOn[0])
            this_vector = pointOn - center
            this_vector = this_vector / numpy.linalg.norm(this_vector)
            if numpy.abs(numpy.abs(numpy.dot(this_vector, ypoint_vector)) - 1.0) < 0.01:
                y_vectors += ((v), )
        y_points = numpy.asarray([v.pointOn[0][1] for v in y_vectors])
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
        for II, face in enumerate(part.faces):
            this_vert_idxs = face.getVertices()
            try:
                if y_vectors_grabbed_idxs[1] in this_vert_idxs or y_vectors_grabbed_idxs[2] in this_vert_idxs:
                    this_normal = numpy.array(face.getNormal())
                    this_normal = this_normal / numpy.linalg.norm(this_normal)
                    if numpy.abs(numpy.abs(numpy.dot(this_normal, xpoint_vector))-numpy.cos(plane_angle*numpy.pi/180.0)) < 0.001:
                        # part.DatumPointByCoordinate(coords=face.getCentroid()[0])
                        part.RemoveFaces(faceList=part.faces[face.index:(face.index+1)], deleteCells=False)
                        part.RemoveRedundantEntities(vertexList = part.vertices[:], edgeList = part.edges[:])
                        found_face = True
                        break
            except:
                pass
        if II == (len(part.faces)-1):
            found_face = False
        else:
            pass

    # Step 25 - same as 19 but for z
    found_face = True
    while found_face:
        vertices = part.vertices
        z_vectors = ()
        for v in vertices:
            pointOn = numpy.asarray(v.pointOn[0])
            this_vector = pointOn - center
            this_vector = this_vector / numpy.linalg.norm(this_vector)
            if numpy.abs(numpy.abs(numpy.dot(this_vector, zpoint_vector)) - 1.0) < 0.01:
                z_vectors += ((v), )
        z_points = numpy.asarray([v.pointOn[0][2] for v in z_vectors])
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
        for II, face in enumerate(part.faces):
            this_vert_idxs = face.getVertices()
            try:
                if z_vectors_grabbed_idxs[1] in this_vert_idxs or z_vectors_grabbed_idxs[2] in this_vert_idxs:
                    this_normal = numpy.array(face.getNormal())
                    this_normal = this_normal / numpy.linalg.norm(this_normal)
                    if numpy.abs(numpy.abs(numpy.dot(this_normal, ypoint_vector))-numpy.cos(plane_angle*numpy.pi/180.0)) < 0.001:
                        # part.DatumPointByCoordinate(coords=face.getCentroid()[0])
                        part.RemoveFaces(faceList=part.faces[face.index:(face.index+1)], deleteCells=False)
                        part.RemoveRedundantEntities(vertexList = part.vertices[:], edgeList = part.edges[:])
                        found_face = True
                        break
            except:
                pass
        if II == (len(part.faces)-1):
            found_face = False
        else:
            pass

    # Step 29 - validate geometry
    abaqus.mdb.models[model_name].parts[part_name].checkGeometry()


def get_inputs():
    """Interactive Inputs

    Prompt the user for inputs with this interactive data entry function. When called, this function opens an Abaqus CAE
    GUI window with text boxes to enter values for the outputs listed below:

    :return: ``center`` - center location of the geometry
    :rtype: list

    :return: ``xvector`` - location on the x-axis local to the geometry
    :rtype: list

    :return: ``zvector`` - location on the z-axis local to the geometry
    :rtype: list

    :return: ``polar_angle`` - angle at which partition planes will be created
    :rtype: float

    :return: ``azimuthal_angle`` - angle at which partition planes will be created
    :rtype: float
    """
    from abaqus import getInputs


    fields = (('Center:','0.0, 0.0, 0.0'),
              ('X-Vector:', '1.0, 0.0, 0.0'),
              ('Z-Vector:', '0.0, 0.0, 1.0'),
              ('Polar Angle:', '45.0'),
              ('Azimuthal Angle:', '45.0'),
              ('Copy and Paste Parameters', 'ctrl+c ctrl+v printed parameters'), )
    center, xvector, zvector, polar_angle, azimuthal_angle, cp_parameters = getInputs(fields=fields,
        label='Specify Geometric Parameters:',
        dialogTitle='Turbo Turtle', )
    if center is not None:
        if cp_parameters != fields[-1][-1]:
            cp_param = [x.replace('\n', '') for x in cp_parameters.split('\n')]
            center = ast.literal_eval(cp_param[0].replace('Center: ', ''))
            xpoint = ast.literal_eval(cp_param[1].replace('X-Vector: ', ''))
            zpoint = ast.literal_eval(cp_param[2].replace('Z-Vector: ', ''))
            polar_angle = ast.literal_eval(cp_param[3].replace('Polar Angle: ', ''))
            azimuthal_angle = ast.literal_eval(cp_param[3].replace('Azimuthal Angle: ', ''))
        else:
            center = list(ast.literal_eval(center))
            xvector = list(ast.literal_eval(xvector))
            zvector = list(ast.literal_eval(zvector))
            polar_angle = ast.literal_eval(polar_angle)
            azimuthal_angle = ast.literal_eval(azimuthal_angle)
        print('\nPartitioning Parameters Entered By User:')
        print('----------------------------------------')
        print('Center: {}'.format(center))
        print('X-Vector: {}'.format(xvector))
        print('Z-Vector: {}'.format(zvector))
        print('Polar Angle: {}'.format(polar_angle))
        print('Azimuthal Angle: {}'.format(azimuthal_angle))
        print('')
    return center, xpoint, zpoint, polar_angle, azimuthal_angle


if __name__ == "__main__":
    try:
        center, xvector, zvector, polar_angle, azimuthal_angle = get_inputs()
        model_name=None
        part_name=None
        partition(center, xvector, zvector, polar_angle, azimuthal_angle, model_name, part_name)

    except:
        parser = parsers.partition_parser(basename=basename)
        try:
            args, unknown = parser.parse_known_args()
        except SystemExit as err:
            sys.exit(err.code)

        sys.exit(main(
            input_file=args.input_file,
            output_file=args.output_file,
            center=args.center,
            xvector=args.xvector,
            zvector=args.zvector,
            polar_angle=args.polar_angle,
            azimuthal_angle=args.azimuthal_angle,
            model_name=args.model_name,
            part_name=args.part_name
        ))
