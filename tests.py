from abaqus import *
from abaqusConstants import *

def sphere(model_name, part_name='sphere'):
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 1.0), point2=(0.0, -1.0), 
        direction=CLOCKWISE)
    s.CoincidentConstraint(entity1=v[2], entity2=g[2], addUndoState=False)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 2.0), point2=(0.0, -2.0), 
        direction=CLOCKWISE)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 1.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.Line(point1=(0.0, -2.0), point2=(0.0, -1.0))
    s.VerticalConstraint(entity=g[6], addUndoState=False)
    p = mdb.models[model_name].Part(name=part_name, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[model_name].parts[part_name]
    p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models[model_name].parts[part_name]
    del mdb.models[model_name].sketches['__profile__']
    return


def eigth_sphere(model_name, part_name='eigth-sphere'):
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 1.0), point2=(1.0, 0.0), 
        direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 2.0), point2=(2.0, 0.0), 
        direction=CLOCKWISE)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 1.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.Line(point1=(2.0, 0.0), point2=(1.0, 0.0))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    p = mdb.models[model_name].Part(name=part_name, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[model_name].parts[part_name]
    p.BaseSolidRevolve(sketch=s, angle=90.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models[model_name].parts[part_name]
    del mdb.models[model_name].sketches['__profile__']


def half_sphere(model_name, part_name='half-sphere'):
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 1.0), point2=(1.0, 0.0), 
        direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 2.0), point2=(2.0, 0.0), 
        direction=CLOCKWISE)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 1.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.Line(point1=(2.0, 0.0), point2=(1.0, 0.0))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    p = mdb.models[model_name].Part(name=part_name, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[model_name].parts[part_name]
    p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models[model_name].parts[part_name]
    del mdb.models[model_name].sketches['__profile__']
    return


def quarter_sphere(model_name, part_name='quarter-sphere'):
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 1.0), point2=(0.0, -1.0), 
        direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 2.0), point2=(0.0, -2.0), 
        direction=CLOCKWISE)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 1.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.Line(point1=(0.0, -2.0), point2=(0.0, -1.0))
    s.VerticalConstraint(entity=g[6], addUndoState=False)
    p = mdb.models[model_name].Part(name=part_name, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[model_name].parts[part_name]
    p.BaseSolidRevolve(sketch=s, angle=90.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models[model_name].parts[part_name]
    del mdb.models[model_name].sketches['__profile__']
    return


def seveneigths_sphere(model_name, part_name='seveneigths-sphere'):
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 1.0), point2=(0.0, -1.0), 
        direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 2.0), point2=(0.0, -2.0), 
        direction=CLOCKWISE)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 1.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.Line(point1=(0.0, -2.0), point2=(0.0, -1.0))
    s.VerticalConstraint(entity=g[6], addUndoState=False)
    p = mdb.models[model_name].Part(name=part_name, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[model_name].parts[part_name]
    p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models[model_name].parts[part_name]
    del mdb.models[model_name].sketches['__profile__']
    p = mdb.models[model_name].parts[part_name]
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)
    p = mdb.models[model_name].parts[part_name]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    d1 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d1[2], cells=pickedCells)
    p = mdb.models[model_name].parts[part_name]
    f, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f[0], sketchUpEdge=e[1], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__', 
        sheetSize=11.31, gridSpacing=0.28, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[model_name].parts[part_name]
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 0.0))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[9], addUndoState=False)
    s.Line(point1=(0.0, 0.0), point2=(2.0, 0.0))
    s.HorizontalConstraint(entity=g[10], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[9], entity2=g[10], addUndoState=False)
    s.CoincidentConstraint(entity1=v[5], entity2=g[7], addUndoState=False)
    s.EqualDistanceConstraint(entity1=v[0], entity2=v[1], midpoint=v[5], 
        addUndoState=False)
    s.Line(point1=(2.0, 0.0), point2=(2.0, 2.0))
    s.VerticalConstraint(entity=g[11], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[10], entity2=g[11], addUndoState=False)
    s.Line(point1=(2.0, 2.0), point2=(0.0, 2.0))
    s.HorizontalConstraint(entity=g[12], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[11], entity2=g[12], addUndoState=False)
    p = mdb.models[model_name].parts[part_name]
    f1, e1 = p.faces, p.edges
    p.CutRevolve(sketchPlane=f1[0], sketchUpEdge=e1[1], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s, angle=90.0, 
        flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']
    return


def offset_sphere(model_name, part_name='offset-sphere'):
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(1.0, 1.0), point1=(1.0, 2.0), point2=(1.0, -2.0), 
        direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(1.0, 1.0), point1=(1.0, 3.0), point2=(1.0, -1.0), 
        direction=CLOCKWISE)
    s.Line(point1=(1.0, 3.0), point2=(1.0, 2.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.Line(point1=(1.0, -1.0), point2=(1.0, 0.0))
    s.VerticalConstraint(entity=g[6], addUndoState=False)
    s.ConstructionLine(point1=(1.0, 1.0), angle=90.0)
    s.VerticalConstraint(entity=g[7], addUndoState=False)
    s.sketchOptions.setValues(constructionGeometry=ON)
    s.assignCenterline(line=g[7])
    p = mdb.models[model_name].Part(name=part_name, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[model_name].parts[part_name]
    p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models[model_name].parts[part_name]
    del mdb.models[model_name].sketches['__profile__']
    return


def swiss_cheese():
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__',
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 1.0), point2=(0.0, -1.0),
        direction=CLOCKWISE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 2.0), point2=(0.0, -2.0),
        direction=CLOCKWISE)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 1.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.Line(point1=(0.0, -2.0), point2=(0.0, -1.0))
    s.VerticalConstraint(entity=g[6], addUndoState=False)
    p = mdb.models[model_name].Part(name=part_name, dimensionality=THREE_D,
        type=DEFORMABLE_BODY)
    p = mdb.models[model_name].parts[part_name]
    p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models[model_name].parts[part_name]
    del mdb.models[model_name].sketches['__profile__']
    p = mdb.models[model_name].parts[part_name]
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)
    p = mdb.models[model_name].parts[part_name]
    p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)
    p = mdb.models[model_name].parts[part_name]
    p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.0)
    p = mdb.models[model_name].parts[part_name]
    f, e, d2 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=d2[2], sketchUpEdge=e[0],
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))
    s1 = mdb.models[model_name].ConstrainedSketch(name='__profile__',
        sheetSize=15.71, gridSpacing=0.39, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[model_name].parts[part_name]
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.CircleByCenterPerimeter(center=(0.5, 0.2), point1=(0.55, 0.25))
    s1.CircleByCenterPerimeter(center=(-0.5, -0.2), point1=(-0.55, -0.25))
    p = mdb.models[model_name].parts[part_name]
    f1, e1, d1 = p.faces, p.edges, p.datums
    p.CutExtrude(sketchPlane=d1[2], sketchUpEdge=e1[0], sketchPlaneSide=SIDE1,
        sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=OFF)
    s1.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']
    p = mdb.models[model_name].parts[part_name]
    f, e, d2 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=d2[4], sketchUpEdge=e[5],
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__',
        sheetSize=15.71, gridSpacing=0.39, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[model_name].parts[part_name]
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.CircleByCenterPerimeter(center=(0.5, 0.2), point1=(0.55, 0.25))
    s.CircleByCenterPerimeter(center=(-0.5, -0.2), point1=(-0.55, -0.25))
    p = mdb.models[model_name].parts[part_name]
    f1, e1, d1 = p.faces, p.edges, p.datums
    p.CutExtrude(sketchPlane=d1[4], sketchUpEdge=e1[5], sketchPlaneSide=SIDE1,
        sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=OFF)
    s.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']
    p = mdb.models[model_name].parts[part_name]
    f, e, d2 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=d2[3], sketchUpEdge=e[9],
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))
    s1 = mdb.models[model_name].ConstrainedSketch(name='__profile__',
        sheetSize=15.71, gridSpacing=0.39, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[model_name].parts[part_name]
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.CircleByCenterPerimeter(center=(0.5, 0.2), point1=(0.55, 0.25))
    s1.CircleByCenterPerimeter(center=(-0.5, -0.2), point1=(-0.55, -0.25))
    p = mdb.models[model_name].parts[part_name]
    f1, e1, d1 = p.faces, p.edges, p.datums
    p.CutExtrude(sketchPlane=d1[3], sketchUpEdge=e1[9], sketchPlaneSide=SIDE1,
        sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=OFF)
    s1.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']
    return

