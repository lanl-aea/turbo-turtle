import abaqus
import abaqusConstants


def main(model_name, output_file):
    """Wrapper for test geometry creation

    :param str model_name: name of the Abaqus model
    :param str output_file: name of the output Abaqus CAE database

    :returns: ``{output_file}.cae`` Abaqus database
    """
    seveneigths_sphere(model_name)
    swiss_cheese(model_name)


def seveneigths_sphere(model_name, part_name="seveneigths-sphere"):
    """Create a hollow, seveneigths-sphere geometry

    :param str model_name: name of the Abaqus model
    :param str part_name: name of the part to be created in the Abaqus model
    """
    if model_name not in abaqus.mdb.models.keys():
        abaqus.mdb.Model(name=model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
    s = abaqus.mdb.models[model_name].ConstrainedSketch(name="__profile__", sheetSize=200.0)
    g, v, c = s.geometry, s.vertices, s.constraints
    s.setPrimaryObject(option=abaqusConstants.STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 1.0), point2=(0.0, -1.0), direction=abaqusConstants.CLOCKWISE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 2.0), point2=(0.0, -2.0), direction=abaqusConstants.CLOCKWISE)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 1.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.Line(point1=(0.0, -2.0), point2=(0.0, -1.0))
    s.VerticalConstraint(entity=g[6], addUndoState=False)
    p = abaqus.mdb.models[model_name].Part(
        name=part_name, dimensionality=abaqusConstants.THREE_D, type=abaqusConstants.DEFORMABLE_BODY
    )
    p = abaqus.mdb.models[model_name].parts[part_name]
    p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=abaqusConstants.OFF)
    s.unsetPrimaryObject()
    p = abaqus.mdb.models[model_name].parts[part_name]
    del abaqus.mdb.models[model_name].sketches["__profile__"]
    p = abaqus.mdb.models[model_name].parts[part_name]
    p.DatumPlaneByPrincipalPlane(principalPlane=abaqusConstants.XYPLANE, offset=0.0)
    p = abaqus.mdb.models[model_name].parts[part_name]
    c = p.cells
    pickedCells = c.getSequenceFromMask(
        mask=("[#1 ]",),
    )
    d1 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d1[2], cells=pickedCells)
    p = abaqus.mdb.models[model_name].parts[part_name]
    f, e = p.faces, p.edges
    t = p.MakeSketchTransform(
        sketchPlane=f[0],
        sketchUpEdge=e[1],
        sketchPlaneSide=abaqusConstants.SIDE1,
        sketchOrientation=abaqusConstants.RIGHT,
        origin=(0.0, 0.0, 0.0),
    )
    s = abaqus.mdb.models[model_name].ConstrainedSketch(
        name="__profile__", sheetSize=11.31, gridSpacing=0.28, transform=t
    )
    g, v, c = s.geometry, s.vertices, s.constraints
    s.setPrimaryObject(option=abaqusConstants.SUPERIMPOSE)
    p = abaqus.mdb.models[model_name].parts[part_name]
    p.projectReferencesOntoSketch(sketch=s, filter=abaqusConstants.COPLANAR_EDGES)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 0.0))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[9], addUndoState=False)
    s.Line(point1=(0.0, 0.0), point2=(2.0, 0.0))
    s.HorizontalConstraint(entity=g[10], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[9], entity2=g[10], addUndoState=False)
    s.CoincidentConstraint(entity1=v[5], entity2=g[7], addUndoState=False)
    s.EqualDistanceConstraint(entity1=v[0], entity2=v[1], midpoint=v[5], addUndoState=False)
    s.Line(point1=(2.0, 0.0), point2=(2.0, 2.0))
    s.VerticalConstraint(entity=g[11], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[10], entity2=g[11], addUndoState=False)
    s.Line(point1=(2.0, 2.0), point2=(0.0, 2.0))
    s.HorizontalConstraint(entity=g[12], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[11], entity2=g[12], addUndoState=False)
    p = abaqus.mdb.models[model_name].parts[part_name]
    f1, e1 = p.faces, p.edges
    p.CutRevolve(
        sketchPlane=f1[0],
        sketchUpEdge=e1[1],
        sketchPlaneSide=abaqusConstants.SIDE1,
        sketchOrientation=abaqusConstants.RIGHT,
        sketch=s,
        angle=90.0,
        flipRevolveDirection=abaqusConstants.OFF,
    )
    s.unsetPrimaryObject()
    del abaqus.mdb.models[model_name].sketches["__profile__"]

    abaqus.mdb.saveAs(pathName=output_file)


def swiss_cheese(model_name, part_name="swiss-cheese"):
    """Create a hollow, spherical geometry with a few holes sparsely placed through the thickness

    :param str model_name: name of the Abaqus model
    :param str part_name: name of the part to be created in the Abaqus model
    """
    if model_name not in abaqus.mdb.models.keys():
        abaqus.mdb.Model(name=model_name, modelType=abaqusConstants.STANDARD_EXPLICIT)
    s = abaqus.mdb.models[model_name].ConstrainedSketch(name="__profile__", sheetSize=200.0)
    g = s.geometry
    s.setPrimaryObject(option=abaqusConstants.STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 1.0), point2=(0.0, -1.0), direction=abaqusConstants.CLOCKWISE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 2.0), point2=(0.0, -2.0), direction=abaqusConstants.CLOCKWISE)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 1.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.Line(point1=(0.0, -2.0), point2=(0.0, -1.0))
    s.VerticalConstraint(entity=g[6], addUndoState=False)
    p = abaqus.mdb.models[model_name].Part(
        name=part_name, dimensionality=abaqusConstants.THREE_D, type=abaqusConstants.DEFORMABLE_BODY
    )
    p = abaqus.mdb.models[model_name].parts[part_name]
    p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=abaqusConstants.OFF)
    s.unsetPrimaryObject()
    p = abaqus.mdb.models[model_name].parts[part_name]
    del abaqus.mdb.models[model_name].sketches["__profile__"]
    p = abaqus.mdb.models[model_name].parts[part_name]
    p.DatumPlaneByPrincipalPlane(principalPlane=abaqusConstants.XYPLANE, offset=0.0)
    p = abaqus.mdb.models[model_name].parts[part_name]
    p.DatumPlaneByPrincipalPlane(principalPlane=abaqusConstants.YZPLANE, offset=0.0)
    p = abaqus.mdb.models[model_name].parts[part_name]
    p.DatumPlaneByPrincipalPlane(principalPlane=abaqusConstants.XZPLANE, offset=0.0)
    p = abaqus.mdb.models[model_name].parts[part_name]
    e, d2 = p.edges, p.datums
    t = p.MakeSketchTransform(
        sketchPlane=d2[2],
        sketchUpEdge=e[0],
        sketchPlaneSide=abaqusConstants.SIDE1,
        sketchOrientation=abaqusConstants.RIGHT,
        origin=(0.0, 0.0, 0.0),
    )
    s1 = abaqus.mdb.models[model_name].ConstrainedSketch(
        name="__profile__", sheetSize=15.71, gridSpacing=0.39, transform=t
    )
    g = s1.geometry
    s1.setPrimaryObject(option=abaqusConstants.SUPERIMPOSE)
    p = abaqus.mdb.models[model_name].parts[part_name]
    p.projectReferencesOntoSketch(sketch=s1, filter=abaqusConstants.COPLANAR_EDGES)
    s1.CircleByCenterPerimeter(center=(0.5, 0.2), point1=(0.55, 0.25))
    s1.CircleByCenterPerimeter(center=(-0.5, -0.2), point1=(-0.55, -0.25))
    p = abaqus.mdb.models[model_name].parts[part_name]
    e1, d1 = p.edges, p.datums
    p.CutExtrude(
        sketchPlane=d1[2],
        sketchUpEdge=e1[0],
        sketchPlaneSide=abaqusConstants.SIDE1,
        sketchOrientation=abaqusConstants.RIGHT,
        sketch=s1,
        flipExtrudeDirection=abaqusConstants.OFF,
    )
    s1.unsetPrimaryObject()
    del abaqus.mdb.models[model_name].sketches["__profile__"]
    p = abaqus.mdb.models[model_name].parts[part_name]
    e, d2 = p.edges, p.datums
    t = p.MakeSketchTransform(
        sketchPlane=d2[4],
        sketchUpEdge=e[5],
        sketchPlaneSide=abaqusConstants.SIDE1,
        sketchOrientation=abaqusConstants.RIGHT,
        origin=(0.0, 0.0, 0.0),
    )
    s = abaqus.mdb.models[model_name].ConstrainedSketch(
        name="__profile__", sheetSize=15.71, gridSpacing=0.39, transform=t
    )
    g = s.geometry
    s.setPrimaryObject(option=abaqusConstants.SUPERIMPOSE)
    p = abaqus.mdb.models[model_name].parts[part_name]
    p.projectReferencesOntoSketch(sketch=s, filter=abaqusConstants.COPLANAR_EDGES)
    s.CircleByCenterPerimeter(center=(0.5, 0.2), point1=(0.55, 0.25))
    s.CircleByCenterPerimeter(center=(-0.5, -0.2), point1=(-0.55, -0.25))
    p = abaqus.mdb.models[model_name].parts[part_name]
    e1, d1 = p.edges, p.datums
    p.CutExtrude(
        sketchPlane=d1[4],
        sketchUpEdge=e1[5],
        sketchPlaneSide=abaqusConstants.SIDE1,
        sketchOrientation=abaqusConstants.RIGHT,
        sketch=s,
        flipExtrudeDirection=abaqusConstants.OFF,
    )
    s.unsetPrimaryObject()
    del abaqus.mdb.models[model_name].sketches["__profile__"]
    p = abaqus.mdb.models[model_name].parts[part_name]
    e, d2 = p.edges, p.datums
    t = p.MakeSketchTransform(
        sketchPlane=d2[3],
        sketchUpEdge=e[9],
        sketchPlaneSide=abaqusConstants.SIDE1,
        sketchOrientation=abaqusConstants.RIGHT,
        origin=(0.0, 0.0, 0.0),
    )
    s1 = abaqus.mdb.models[model_name].ConstrainedSketch(
        name="__profile__", sheetSize=15.71, gridSpacing=0.39, transform=t
    )
    g = s1.geometry
    s1.setPrimaryObject(option=abaqusConstants.SUPERIMPOSE)
    p = abaqus.mdb.models[model_name].parts[part_name]
    p.projectReferencesOntoSketch(sketch=s1, filter=abaqusConstants.COPLANAR_EDGES)
    s1.CircleByCenterPerimeter(center=(0.5, 0.2), point1=(0.55, 0.25))
    s1.CircleByCenterPerimeter(center=(-0.5, -0.2), point1=(-0.55, -0.25))
    p = abaqus.mdb.models[model_name].parts[part_name]
    e1, d1 = p.edges, p.datums
    p.CutExtrude(
        sketchPlane=d1[3],
        sketchUpEdge=e1[9],
        sketchPlaneSide=abaqusConstants.SIDE1,
        sketchOrientation=abaqusConstants.RIGHT,
        sketch=s1,
        flipExtrudeDirection=abaqusConstants.OFF,
    )
    s1.unsetPrimaryObject()
    del abaqus.mdb.models[model_name].sketches["__profile__"]

    abaqus.mdb.saveAs(pathName=output_file)


if __name__ == "__main__":
    model_name = "Turbo-Turtle-Tests"
    output_file = "Turbo-Turtle-Tests"
    main(model_name, output_file)
