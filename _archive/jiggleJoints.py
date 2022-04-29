import maya.cmds as mc
import maya.api.OpenMaya as om
import pymel.core as pm
import logging
from ..utilities import transform as trans
from ..utilities import skinWeights as sk
from ..utilities.rigBuild import shapes as sh

logger = logging.getLogger(__name__)

class JiggleJointMaker:
    '''This class handles creation of super cool jiggle joint controls that follow skinned geo and allow for secondary animation'''
    pass

    def __init__(self):
        self.data = 1 
        self.name = ''
        self.sourceLoc = None
        self.side = ''  


    def buildJigglePlane(self, name, sourceLoc=None, side=None):
        """Build jiggle plane, controller, and joint, based on input locator. Choose name and parent module.

        Parameters:
            name (string): jiggle control name, ie "Spine"
            sourceLoc (string): reference locator or object for jiggle plane transforms
            side (string): side of the body the controller is located, L, R, or C
            
        Returns:
            geo
            jntMultNode

        """
    
        # create and place locator, select it in scene
        # create error logging here if nothing is selected
        # if not sourceLoc:
        #     try:
        #         sourceLoc = mc.ls(sl=True)
        #     except:
        #         logger.error('No objects provided for jiggle joint placement.')
        #         return

        if not sourceLoc:
            sourceLoc= mc.ls(sl=True)   

        # object names
        controlName = 'C_{}_{}_Jiggle'.format(side, name)
        geoName = 'H_{}_{}_Jiggle_Proxy'.format(side, name)
        pinName = 'F_{}_{}_UVPin'.format(side, name)
        jointName = 'J_{}_{}_Jiggle'.format(side, name)

        # make plane
        geo = mc.polyPlane(name=geoName,
                        w=20,
                        h=20,
                        sh=6,
                        sw=6,
                        ch=False,
                        ax=[1, 0, 0])[0]
        geoShape = mc.listRelatives(geo)[0]
        orig = mc.deformableShape(geo, cog=True)

        # make joint
        mc.select(clear=True)
        joint = mc.joint(n=jointName)

        # make jiggle controller and add attrs for UV coordinates
        controller = sh.makeShape('sphere', name=controlName, axis='x', size=15)
        mc.addAttr(controller, at='float', dv=.5, k=True, min=0, max=1, ln='coordinateU')
        mc.addAttr(controller, at='float', dv=.5, k=True, min=0, max=1, ln='coordinateV')

        # prep control for color updates and set color according to side
        setSideColor(controller, side)

        # make uvPin node, set temp axes
        pin = mc.createNode('uvPin', name=pinName)
        mc.setAttr('{}.normalAxis'.format(pin), 0)
        mc.setAttr('{}.tangentAxis'.format(pin), 5)

        # make connections from controller to UVpin
        mc.connectAttr('{}.coordinateU'.format(controller), '{}.coordinate[0].coordinateU'.format(pin))
        mc.connectAttr('{}.coordinateV'.format(controller), '{}.coordinate[0].coordinateV'.format(pin))
        mc.connectAttr(orig[0], '{}.originalGeometry'.format(pin))
        mc.connectAttr('{}.worldMesh[0]'.format(geoShape), '{}.deformedGeometry'.format(pin))
        mc.connectAttr('{}.outputMatrix[0]'.format(pin), '{}.offsetParentMatrix'.format(controller))

        #make matrix nodes for controller to joint, named for joint
        jntDecompNode = mc.createNode('decomposeMatrix', n='{}_decomp'.format(jointName))
        jntMultNode = mc.createNode('multMatrix', n='{}_mult'.format(jointName))

        # make connections from controller to joint via matrices
        mc.connectAttr('{}.worldMatrix[0]'.format(controller), '{}.matrixIn[0]'.format(jntMultNode))
        mc.connectAttr('{}.matrixSum'.format(jntMultNode), '{}.inputMatrix'.format(jntDecompNode))
        mc.connectAttr('{}.outputTranslate'.format(jntDecompNode), '{}.translate'.format(joint))
        mc.connectAttr('{}.outputRotate'.format(jntDecompNode), '{}.rotate'.format(joint))   
        mc.connectAttr('{}.outputScale'.format(jntDecompNode), '{}.scale'.format(joint))

        # snap plane to source locator and freeze transforms
        mc.matchTransform(geo, sourceLoc)
        mc.makeIdentity(geo, apply=True)

        return [geo, jntMultNode]


###############################################


def buildJigglePlane(name, sourceLoc=None, side=None):
    """Build jiggle plane, controller, and joint, based on input locator. Choose name and parent module.

    Parameters:
        name (string): jiggle control name, ie "Spine"
        sourceLoc (string): reference locator or object for jiggle plane transforms
        side (string): side of the body the controller is located, L, R, or C
        
    Returns:
        geo
        jntMultNode

    """
    
    # create and place locator, select it in scene
    # create error logging here if nothing is selected
    # if not sourceLoc:
    #     try:
    #         sourceLoc = mc.ls(sl=True)
    #     except:
    #         logger.error('No objects provided for jiggle joint placement.')
    #         return

    if not sourceLoc:
        sourceLoc= mc.ls(sl=True)   

    # object names
    controlName = 'C_{}_{}_Jiggle'.format(side, name)
    geoName = 'H_{}_{}_Jiggle_Proxy'.format(side, name)
    pinName = 'F_{}_{}_UVPin'.format(side, name)
    jointName = 'J_{}_{}_Jiggle'.format(side, name)

    # make plane
    geo = mc.polyPlane(name=geoName,
                       w=20,
                       h=20,
                       sh=6,
                       sw=6,
                       ch=False,
                       ax=[1, 0, 0])[0]
    geoShape = mc.listRelatives(geo)[0]
    orig = mc.deformableShape(geo, cog=True)

    # make joint
    mc.select(clear=True)
    joint = mc.joint(n=jointName)

    # make jiggle controller and add attrs for UV coordinates
    controller = sh.makeShape('sphere', name=controlName, axis='x', size=15)
    mc.addAttr(controller, at='float', dv=.5, k=True, min=0, max=1, ln='coordinateU')
    mc.addAttr(controller, at='float', dv=.5, k=True, min=0, max=1, ln='coordinateV')

    # prep control for color updates and set color according to side
    setSideColor(controller, side)

    # make uvPin node, set temp axes
    pin = mc.createNode('uvPin', name=pinName)
    mc.setAttr('{}.normalAxis'.format(pin), 0)
    mc.setAttr('{}.tangentAxis'.format(pin), 5)

    # make connections from controller to UVpin
    mc.connectAttr('{}.coordinateU'.format(controller), '{}.coordinate[0].coordinateU'.format(pin))
    mc.connectAttr('{}.coordinateV'.format(controller), '{}.coordinate[0].coordinateV'.format(pin))
    mc.connectAttr(orig[0], '{}.originalGeometry'.format(pin))
    mc.connectAttr('{}.worldMesh[0]'.format(geoShape), '{}.deformedGeometry'.format(pin))
    mc.connectAttr('{}.outputMatrix[0]'.format(pin), '{}.offsetParentMatrix'.format(controller))

    #make matrix nodes for controller to joint, named for joint
    jntDecompNode = mc.createNode('decomposeMatrix', n='{}_decomp'.format(jointName))
    jntMultNode = mc.createNode('multMatrix', n='{}_mult'.format(jointName))

    # make connections from controller to joint via matrices
    mc.connectAttr('{}.worldMatrix[0]'.format(controller), '{}.matrixIn[0]'.format(jntMultNode))
    mc.connectAttr('{}.matrixSum'.format(jntMultNode), '{}.inputMatrix'.format(jntDecompNode))
    mc.connectAttr('{}.outputTranslate'.format(jntDecompNode), '{}.translate'.format(joint))
    mc.connectAttr('{}.outputRotate'.format(jntDecompNode), '{}.rotate'.format(joint))   
    mc.connectAttr('{}.outputScale'.format(jntDecompNode), '{}.scale'.format(joint))

    # snap plane to source locator and freeze transforms
    mc.matchTransform(geo, sourceLoc)
    mc.makeIdentity(geo, apply=True)

    return [geo, jntMultNode]

def shrinkWrapGeo(targetGeo, sourceGeo):
    """Wrap jiggle plane to character main mesh 
    
    Parameters:
        targetGeo (string): geo to be deformed, such as jiggle proxy plane
        sourceGeo (string): geo to wrap to, such as skinned character mesh 
        
    Returns:
        
    """
    shrinkWrapName = 'temp_{}_shrinkwrap'.format(targetGeo)

    #create shrink wrap deformer to wrap jiggle plane to character mesh
    shrinkWrapNode = pm.deformer(targetGeo, type='shrinkWrap', name=shrinkWrapName)[0]
    pm.PyNode(sourceGeo).worldMesh[0] >> shrinkWrapNode.targetGeom
    shrinkWrapNode.closestIfNoIntersection.set(True)
    shrinkWrapNode.projection.set(4)

    return [shrinkWrapName, targetGeo]

def disconnectDeformer(deformerName, deformedGeo):
    """Break connections between mesh and deformer. Designed for use with shrink wrap, can't promise it works for more deformer types
    
    Parameters:
        deformerName (string): name of deformer to disconnect
        deformedGeo (string): geo to disconnect deformer from 
        
    Returns:
        
    """
    mc.disconnectAttr('{}.outputGeometry[0]'.format(deformerName), '{}.inMesh'.format(deformedGeo))


def addJntsToSkin(skinCluster='', joints=[]):
    """Add given joints into given skinCluster with locked, zeroed weights
    
    Parameters:
        joint (string): name of joint to add
        skin (string): target skin cluster 
        
    Returns:
        
    """
    # if no skin or joint given, use selected objects with skin selected first
    # need to grab skin cluster from skin object!
   
    # if not source and not dest:
    #     objects = mc.ls(sl=True)
    #     if len(objects) < 2:
    #         return False
    #     else:
    #         source = objects[0]
    #         dest = objects[1:]

    # sourceHistory = mc.listHistory(source)
    # sc = mc.ls(sourceHistory, typ='skinCluster')
    # if not sc:
    #     mc.error('No skinCluster found in source history.')
    # elif len(sc) > 1:
    #     mc.warning('More then one skinCluster found in source history.')
    # else:
    #     maintainMaxInfluences = mc.getAttr('{}.maintainMaxInfluences'.format(
    #         sc[0]))
    #     maxInfluences = mc.getAttr('{}.maxInfluences'.format(sc[0]))

    for joint in joints:
        mc.skinCluster(skinCluster, edit=True, dr=4, ps=0, ns=10, lw=True, wt=0, ai=joint)


def setSideColor(control, side):
    """Set control color based on placement
    
    Parameters:
        control (string): name of controller
        side (string): side of body where controller is placed, R, L, or C
        
    Returns:
        
    """
    #get shape node and set color overrides
    controlShape = mc.listRelatives(control, shapes=True)[0]
    mc.setAttr(controlShape + '.overrideEnabled', 1)
    mc.setAttr(controlShape + '.overrideRGBColors', 1)

    # creating zippable tuple 
    rgb = ("R", "G", "B")

    #setting color template
    colorRight = [1, 0, 0]
    colorLeft = [0, 1, 1]
    colorCenter = [1, 1, 0]

    #evaluate side value and set colors
    if side == 'L':
        for channel, color in zip(rgb, colorLeft):
            mc.setAttr(controlShape + '.overrideColor%s' % channel, color)
    if side == 'R':
        for channel, color in zip(rgb, colorRight):
            mc.setAttr(controlShape + '.overrideColor%s' % channel, color)
    if side == 'C':
        for channel, color in zip(rgb, colorCenter):
            mc.setAttr(controlShape + '.overrideColor%s' % channel, color)
        

def connectToHierarchy(jiggleJoint, parentJoint, jntMultNode, jiggleController, parentModule, proxyGeo):
    """Connect jiggle joint setup into rig module and skeletal hierarchy using matrices
    
    Parameters:
        jiggleJoint (string): the individual jiggle joint
        parentJoint (string): the skeletal joint to use as jiggle joint parent
        jntMultNode (string): the jiggle joint's multmatrix node 
        jiggleController (string): the jiggle controller
        parentModule (string): the parent module to hold the jiggle controller and proxy geo
        proxyGeo (string): skinned jiggle geo mesh 

    Returns:
        
    """
    
    # parent JJ to parent joint and cancel transforms out with matrix connection
    mc.parent(jiggleJoint, parentJoint)
    mc.connectAttr('{}.worldInverseMatrix[0]'.format(parentJoint), '{}.matrixIn[1]'.format(jntMultNode))

    # find existing rig jiggle control group or create one, then parent jiggle control into group
    jiggleGrp = ''
    jiggleGrpName = ''
    jiggleGrpParent = ''

    if mc.objExists('|MOD_{0}|CTRL_{0}|C_{0}_Shared|G_{0}_Jiggle'.format(parentModule)):
        jiggleGrp = '|MOD_{0}|CTRL_{0}|C_{0}_Shared|G_{0}_Jiggle'.format(parentModule)
    elif mc.objExists('|MOD_{0}|CTRL_{0}|C_{0}_Shared|G_{0}_JIggle'.format(parentModule)):
        jiggleGrp = '|MOD_{0}|CTRL_{0}|C_{0}_Shared|G_{0}_JIggle'.format(parentModule)
    else:
        jiggleGrpName = 'G_{}_Jiggle'.format(parentModule)
        jiggleGrpParent = '|MOD_{0}|CTRL_{0}|C_{0}_Shared'.format(parentModule)
        jiggleGrp = mc.group(n=jiggleGrpName, p=jiggleGrpParent, em=True)

    mc.parent(jiggleController, jiggleGrp)

    # parent proxy jiggle geo into RIG_module, G_Module_Proxy group and hide visibility
    proxyGrp = ''
    proxyGrpName = ''
    proxyGrpParent = ''

    if mc.objExists('|MOD_{0}|RIG_{0}|G_{0}_Proxy'.format(parentModule)):
        proxyGrp = '|MOD_{0}|RIG_{0}|G_{0}_Proxy'.format(parentModule)
    else:
        proxyGrpName = 'G_{}_Proxy'.format(parentModule)
        proxyGrpParent = '|MOD_{0}|RIG_{0}|G_{0}_Proxy'.format(parentModule)
        proxyGrp = mc.group(n=proxyGrpName, p=proxyGrpParent, em=True)
    
    mc.parent(proxyGeo, proxyGrp)
    mc.hide(proxyGeo)

     

    






#collect source input locator and snap to position DONE
#collect input locator rotations, match axes on uvpin NOT NEEDED
#wrap to surface source, delete deformer DONE 
#transfer skinning from source surface to my plane DONE
#add jiggle joint into skin cluster of source surface DONE
#create input for parenting and selecting parent module, updating matrix inputs DONE

#create input for mirroring function
#create input for multiple locators for multiple controls; need to find center of all locs and create function for connections
#save out source locator positions?
#error logging for not naming, selecting locs
#create input for selecting face on geo and creating plane matched there - could also use this to grab character source geo
