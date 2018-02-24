# -*- coding: utf-8 -*-
import Sofa

def loaderFor(name):
    if name.endswith(".obj"):
        return "MeshObjLoader"
    elif name.endswith(".stl"):
        return "MeshSTLLoader"
    elif name.endswith(".vtk"):
        return "MeshVTKLoader"
   
def CollisionMesh(attachedTo=None, 
                  surfaceMeshFileName=None,
                  name="collision",
                  rotation=[0.0,0.0,0.0],
                  translation=[0.0,0.0,0.0],
                  collisionGroup=None):

    if attachedTo == None:
        Sofa.msg_error("Cannot create a CollisionMesh that is not attached to node.")
        return None

    collisionmodel = attachedTo.createChild(name)

    if surfaceMeshFileName == None:
        Sofa.msg_error(collisionmodel, "Unable to create a CollisionMesh without a surface mesh")
        return None

    collisionmodel.createObject(loaderFor(surfaceMeshFileName), name="loader", filename=surfaceMeshFileName,
                                rotation=rotation, translation=translation)
    collisionmodel.createObject('Mesh', src="@loader")
    collisionmodel.createObject('MechanicalObject')
    if collisionGroup:
        collisionmodel.createObject('Point', group=collisionGroup)
        collisionmodel.createObject('Line', group=collisionGroup)
        collisionmodel.createObject('Triangle', group=collisionGroup)
    else:    
        collisionmodel.createObject('Point')
        collisionmodel.createObject('Line')
        collisionmodel.createObject('Triangle')
    
    collisionmodel.createObject('BarycentricMapping')

    return collisionmodel
    

def createScene(rootNode):
    from stlib.scene import MainHeader
    from stlib.physics.deformable import ElasticMaterialObject
    from stlib.physics.constraints import FixedBox

    MainHeader(rootNode)
    target = ElasticMaterialObject(volumeMeshFileName="mesh/liver.msh",
                                   totalMass=0.5,
                                   attachedTo=rootNode)

    FixedBox(atPositions=[-4, 0, 0, 5, 5, 4], applyTo=target,
             doVisualization=True)

    CollisionMesh(surfaceMeshFileName="mesh/liver.obj", attachedTo=target)
