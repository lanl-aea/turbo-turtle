from abaqus import *
from abaqusConstants import *
from caeModules import *
import numpy as np

from abaqus import getInputs
import ast

def get_inputs():
    """Interactive Inputs
    
    Prompt the user for inputs with this interactive data entry function. When called, this function opens an Abaqus CAE GUI window with text boxes to 
    enter values for the outputs listed below:
    
    :return: ``center`` - center location of the geometry
    :rtype: list
    
    :return: ``xpoint`` - location on the x-axis local to the geometry
    :rtype: list
    
    :return: ``zpoint`` - location on the z-axis local to the geometry
    :rtype: list
    
    :return: ``plane_angle`` - angle at which partition planes will be created
    :rtype: float
    """
    
    fields = (('Center:','0.0, 0.0, 0.0'), ('X-Axis Point:', '1.0, 0.0, 0.0'), ('Z-Axis Point:', '0.0, 0.0, 1.0'), ('Partition Angle:', '45.0'), )
    center, xpoint, zpoint, plane_angle = getInputs(fields=fields, label='Specify Geometric Parameters:',dialogTitle='Create Block', )
    center = list(ast.literal_eval(center))
    xpoint = list(ast.literal_eval(xpoint))
    zpoint = list(ast.literal_eval(zpoint))
    plane_angle = ast.literal_eval(plane_angle)
    
    print('\nPartitioning Parameters Entered By User:')
    print('----------------------------------------')
    print('Center: {}'.format(center))
    print('X-Axis Point: {}'.format(xpoint))
    print('Z-Axis Point: {}'.format(zpoint))
    print('Partition Angle: {}'.format(plane_angle))
    print('')
    return center, xpoint, zpoint, plane_angle
    
def main(center, xpoint, zpoint, plane_angle):
    """Turbo Turtle
       Main work-horse function
    
    This function partitions an **arbitrary, hollow, enclosed body** using the turtle shell method (also know as the soccer ball method).
    The following list of actions is performed using generalized vector equations to allow nearly any body to be partitioned.

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
    18. Finalize the orthonormal coordinate system by creating the ``ypoint`` unit vector via the cross product of the ``xpoint`` and ``zpoint`` vectors
    19. Find the vertices that intersect faces to remove along the x-axis
    20. Find faces with a normal at ``plane_angle`` to the local coordinate system
    21. Recursively remove the faces and redundant enties (as a result of removed faces)
    22. same as **19** but for y-axis vertices
    23. Same as **20** but for y-axis vertices
    24. Same as **21** but for y-axis vertices
    25. Same as **19** but for z-axis vertices
    26. Same as **20** but for z-axis vertices
    27. Same as **21** bur for z-axis vertices
    28. Validate the resulting geometry and topology
    
    :param center: center location of the geometry
    :type center: list
    
    :param xpoint: location on the x-axis local to the geometry
    :type xpoint: list
    
    :param zpoint: location on the z-axis local to the geometry
    :type zpoint: list
    
    :param plane_angle: angle at which partition planes will be created
    :type plane_angle: float
   
    """

    model_name = session.viewports[session.currentViewportName].displayedObject.modelName
    part_name = session.viewports[session.currentViewportName].displayedObject.name
    
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
    
    # Step 28 - validate geometry
    p = mdb.models[model_name].parts[part_name]
    mdb.models[model_name].parts[part_name].checkGeometry()
    
    return

if __name__ == "__main__":
    
    center = None
    xpoint = None
    zpoint = None
    plane_angle = None
    
    if center is None or xpoint is None or zpoint is None or plane_angle is None:
        center, xpoint, zpoint, plane_angle = get_inputs()
    else:
        pass
    
    main(center, xpoint, zpoint, plane_angle)
