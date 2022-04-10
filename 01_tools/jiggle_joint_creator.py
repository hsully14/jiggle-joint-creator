import maya.cmds as cmds
import pymel.core as pm
import os

#--------------------------------------------------------------------------------#
#            
#             jiggle_joint_creator.py 
#             March 2022 Haley Sullivan
#             Email: hsully14@gmail.com
#             Website: www.artstation.com/hsully
#
#--------------------------------------------------------------------------------#
#            
#             this UI allows the user to create a UVPin-based jiggle/tweaker joint
#             setup for secondary animation, and connects it into an existing hierarchy
#             and skinned mesh based on user inputs. the script can be added 
#             to a maya session via userSetup or by running the script in the 
#             script editor
#
#--------------------------------------------------------------------------------#
#            
#             things that can be improved:
#             -passing of data between functions is clunky
#             -buttons to select objects vs. typing content in, and dropdowns to select side from existing list 
#             -ability to create multiple joints at once, and mirror setup
#             -ability to use selected verts instead of reference locator 
#             -more user control on control shape choice and sizing
#             -shelf usage is broken, but menu works
#
#--------------------------------------------------------------------------------#

#adding header image
IMG_PATH = os.path.dirname(__file__) + "/img/"
JIGGLE_COMPONENTS = {}


def jiggle_joint_ui():
    #**************************************************************************
    # CLOSE if exists (avoid duplicates)
    ui_title = 'jiggle_joint_creator'

    if cmds.window(ui_title, exists=True):
        print('CLOSE duplicate window')
        cmds.deleteUI(ui_title)


    #**************************************************************************
    # CREATE NEW UI
    # It is important to give the window a name besides the title
    # the name will be used above for the deleteUI
    window = cmds.window(ui_title, 
                        title='Jiggle Joint Creator', 
                        width=500)

    cmds.columnLayout(adjustableColumn=True)

    #add image
    cmds.image(image=IMG_PATH + 'jiggle_joint_creator.png')

    cmds.separator(height=10)

    #input MESH
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label='Skinned Mesh:', 
                annotation="Input name of skinned mesh to add jiggle joint", 
                width=250,
                height=30, 
                align='right')
    cmds.textField('skinned_mesh', 
                    width=250, 
                    height=30, 
                    text='')

    cmds.setParent('..')    # this "closes" the current layout

    #input LOCATOR
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label='Placement Locator:', 
                annotation="Input name of locator to use as reference object", 
                width=250, 
                height=30, 
                align='right')
    cmds.textField('locator', 
                    width=250,
                    height=30, 
                    text='')

    cmds.setParent('..')    # this "closes" the current layout

    #input CONTROL NAME
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label='Control Name:', 
                annotation="Input name of controller", 
                width=250, 
                height=30, 
                align='right')
    cmds.textField('control_name', 
                    width=250, 
                    height=30, 
                    text='')

    cmds.setParent('..')    # this "closes" the current layout

    #input SIDE
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label='Side of Body:', 
                annotation="Input L, R, or C to assign color and name accordingly", 
                width=250, 
                height=30, 
                align='right')
    cmds.textField('body_side', 
                    width=250, 
                    height=30, 
                    text='')

    cmds.setParent('..')    # this "closes" the current layout

    #input JOINT PARENT
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label='Parent Joint:', 
                annotation="Input joint to use as joint parent", 
                width=250, 
                height=30, 
                align='right')
    cmds.textField('jnt_parent', 
                    width=250, 
                    height=30, 
                    text='')

    cmds.setParent('..')    # this "closes" the current layout

    #input CONTROLLER PARENT GRP
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label='Controller Parent Group:', 
                annotation="Input hierarchy object to use as controller parent", 
                width=250, 
                height=30, 
                align='right')
    cmds.textField('parent_grp', 
                    width=250, 
                    height=30, 
                    text='')

    cmds.setParent('..')    # this "closes" the current layout

    cmds.separator(height=10)

    # CHECKBOXES
    cmds.rowLayout(numberOfColumns=1)
    cmds.checkBox('cbx_add_to_skc', 
                    label='Add to Skin Cluster?', 
                    annotation="Choose whether to add jiggle joint to skinned mesh cluster automatically", 
                    width=500, 
                    height=30, 
                    onCommand="print('Adding new joint to skin cluster')", 
                    offCommand="print('Will not add new joint to skin cluster')", 
                    align='center')

    cmds.setParent('..')    # this "closes" the current layout

    #CREATE!
    cmds.separator(height=10)
    cmds.button(label="Create Jiggle Joint",
                annotation="Create jiggle joint and control setup",
                width=500, 
                height=50, 
                command="jiggle_joint_creator.confirm_creation_popup()", 
                backgroundColor=[0,.5,0])
    cmds.separator(height=10)

    cmds.setParent('..')    # this "closes" the current layout

    #TODO: confirm this setup
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="report problem", 
                annotation="Report issues online", 
                width=250,
                command="import webbrowser; webbrowser.open('https://www.artstation.com/hsully')")
    cmds.button(label="get help", 
                annotation="Reach out to author", 
                width=250,
                command="import webbrowser; webbrowser.open('https://www.artstation.com/hsully')")

    cmds.setParent('..')    # this "closes" the current layout

    cmds.showWindow(window)

#jiggle_joint_ui()

def confirm_creation_popup():

    popup_message = 'Are you ready?'

    result = cmds.confirmDialog(title='Confirm Creation',
                                message=popup_message,
                                messageAlign='center',
                                button=['YES!', 'WAIT!'],
                                defaultButton='YES!',
                                cancelButton='WAIT!')

    print(result)

    # EXECUTE button
    if result == 'YES!':
        print('Creating jiggle joint!')
        create_jiggle_setup()

    if result == 'WAIT!':
        print('Double checking...')

def missing_info_popup():

    popup_message = 'Missing info! Double check input fields'

    result = cmds.confirmDialog(title='Missing Info',
                                message=popup_message,
                                messageAlign='center',
                                button=['CLOSE'],
                                defaultButton='CLOSE',
                                cancelButton='CLOSE')

    print(result)

def check_empty_inputs(inputs=[]):
    
    missing_inputs = []

    for text in inputs:
        if not text:
            missing_inputs.append(text)

    return missing_inputs

def create_jiggle_setup():
    """Helper function to call and run components of jiggle joint creator system 
        
    """
    
    #get values from UI textfields
    skin_mesh = cmds.textField('skinned_mesh', query=True, text=True)
    sourceLoc = cmds.textField('locator', query=True, text=True)
    ctrl_name = cmds.textField('control_name', query=True, text=True)
    side = cmds.textField('body_side', query=True, text=True)
    jnt_parent = cmds.textField('jnt_parent', query=True, text=True)
    grp_parent = cmds.textField('parent_grp', query=True, text=True)
    
    #validate input values, cancel if empty strings exist
    inputs = [skin_mesh, sourceLoc, ctrl_name, side, jnt_parent, grp_parent]
    if check_empty_inputs(inputs):
        missing_info_popup()
        return

    #store information in dictionary for easier access; FIXME: make this better 
    JIGGLE_COMPONENTS['skin_mesh'] = skin_mesh
    JIGGLE_COMPONENTS['locator'] = sourceLoc
    JIGGLE_COMPONENTS['control_name'] = ctrl_name
    JIGGLE_COMPONENTS['body_side'] = side
    JIGGLE_COMPONENTS['jnt_parent'] = jnt_parent
    JIGGLE_COMPONENTS['parent_grp'] = grp_parent

    #start building jiggle setup
    build_jiggle_plane(ctrl_name, sourceLoc, side)
    
    #shrinkwrap geo to skinned geo
    shrink_wrap_geo(JIGGLE_COMPONENTS['proxy_geo'], JIGGLE_COMPONENTS['skin_mesh'])

    #remove shrinkwrap node and history
    cmds.delete(JIGGLE_COMPONENTS['proxy_geo'], ch=True)

    #copy skinning from skin_mesh to proxy_geo
    copySkinCluster(source=JIGGLE_COMPONENTS['skin_mesh'], dest=[JIGGLE_COMPONENTS['proxy_geo']], rename=True)

    #collect all created items and connect them to the hierarchy using matrices
    connectToHierarchy(JIGGLE_COMPONENTS['jiggle_jnt'], 
                        JIGGLE_COMPONENTS['jnt_parent'], 
                        JIGGLE_COMPONENTS['jnt_mult_node'], 
                        JIGGLE_COMPONENTS['jiggle_ctrl'], 
                        JIGGLE_COMPONENTS['parent_grp'], 
                        JIGGLE_COMPONENTS['proxy_geo'])

    #get values from UI checkbox
    add_to_skc = cmds.checkBox('cbx_add_to_skc', query=True, value=True)

    if add_to_skc:
        addJntsToSkin(JIGGLE_COMPONENTS['skin_mesh'], joints=[JIGGLE_COMPONENTS['jiggle_jnt']])

    #hide locator 
    cmds.hide(sourceLoc)

    print('Created jiggle setup')

def build_jiggle_plane(ctrl_name, sourceLoc, side):
    """Build jiggle plane, controller, and joint, based on input locator. Choose name and parent module.

    Parameters:
        name (string): jiggle control name, ie "Spine"
        sourceLoc (string): reference locator or object for jiggle plane transforms
        side (string): side of the body the controller is located, L, R, or C
        
    Returns:
        geo
        jntMultNode

    """

    # object names
    controlName = 'C_{}_{}_Jiggle'.format(side, ctrl_name)
    geoName = 'H_{}_{}_Jiggle_Proxy'.format(side, ctrl_name)
    pinName = 'F_{}_{}_UVPin'.format(side, ctrl_name)
    jointName = 'J_{}_{}_Jiggle'.format(side, ctrl_name)

    # make plane
    geo = cmds.polyPlane(name=geoName,
                       w=3,
                       h=3,
                       sh=6,
                       sw=6,
                       ch=False,
                       ax=[1, 0, 0])[0]
    geoShape = cmds.listRelatives(geo)[0]
    orig = cmds.deformableShape(geo, cog=True)

    # make joint
    cmds.select(clear=True)
    joint = cmds.joint(n=jointName)

    # make jiggle controller and add attrs for UV coordinates
    controller = makeShape('sphere', name=controlName, axis='x', size=2)
    cmds.addAttr(controller, at='float', dv=.5, k=True, min=0, max=1, ln='coordinateU')
    cmds.addAttr(controller, at='float', dv=.5, k=True, min=0, max=1, ln='coordinateV')

    # prep control for color updates and set color according to side
    setSideColor(controller, side)

    # make uvPin node, set temp axes
    pin = cmds.createNode('uvPin', name=pinName)
    cmds.setAttr('{}.normalAxis'.format(pin), 0)
    cmds.setAttr('{}.tangentAxis'.format(pin), 5)

    # make connections from controller to UVpin
    cmds.connectAttr('{}.coordinateU'.format(controller), '{}.coordinate[0].coordinateU'.format(pin))
    cmds.connectAttr('{}.coordinateV'.format(controller), '{}.coordinate[0].coordinateV'.format(pin))
    cmds.connectAttr(orig[0], '{}.originalGeometry'.format(pin))
    cmds.connectAttr('{}.worldMesh[0]'.format(geoShape), '{}.deformedGeometry'.format(pin))
    cmds.connectAttr('{}.outputMatrix[0]'.format(pin), '{}.offsetParentMatrix'.format(controller))

    #make matrix nodes for controller to joint, named for joint
    jntDecompNode = cmds.createNode('decomposeMatrix', n='{}_decomp'.format(jointName))
    jntMultNode = cmds.createNode('multMatrix', n='{}_mult'.format(jointName))

    # make connections from controller to joint via matrices
    cmds.connectAttr('{}.worldMatrix[0]'.format(controller), '{}.matrixIn[0]'.format(jntMultNode))
    cmds.connectAttr('{}.matrixSum'.format(jntMultNode), '{}.inputMatrix'.format(jntDecompNode))
    cmds.connectAttr('{}.outputTranslate'.format(jntDecompNode), '{}.translate'.format(joint))
    cmds.connectAttr('{}.outputRotate'.format(jntDecompNode), '{}.rotate'.format(joint))   
    cmds.connectAttr('{}.outputScale'.format(jntDecompNode), '{}.scale'.format(joint))

    # snap plane to source locator and freeze transforms
    cmds.matchTransform(geo, sourceLoc)
    cmds.makeIdentity(geo, apply=True)

    #store data
    JIGGLE_COMPONENTS['proxy_geo'] = geo
    JIGGLE_COMPONENTS['jiggle_jnt'] = joint
    JIGGLE_COMPONENTS['jiggle_ctrl'] = controller
    JIGGLE_COMPONENTS['jnt_mult_node'] = jntMultNode

    return [geo, jntMultNode]

def shrink_wrap_geo(targetGeo, sourceGeo):
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
    cmds.parent(jiggleJoint, parentJoint)
    cmds.connectAttr('{}.worldInverseMatrix[0]'.format(parentJoint), '{}.matrixIn[1]'.format(jntMultNode))

    cmds.parent(jiggleController, parentModule)

    # parent proxy jiggle geo into G_Proxy group and hide visibility
    proxyGrp = cmds.group(n='G_Jiggle_Proxy', em=True)
    cmds.parent(proxyGeo, proxyGrp)
    cmds.hide(proxyGeo)

def renameDeformers(objects=[]):
    if not objects:
        objects = cmds.ls(sl=True)
    if objects:
        for o in objects:
            inputs = cmds.listHistory(o, il=1)
            sc = cmds.ls(inputs, typ='skinCluster')
            if sc:
                newSC = cmds.rename(sc[0], 'skinCluster_{}'.format(o))
                return newSC 

def copySkinCluster(source='', dest=[], rename=False):
    maxInfluences = 0
    maintainMaxInfluences = False
    if not source and not dest:
        objects = cmds.ls(sl=True)
        if len(objects) < 2:
            return False
        else:
            source = objects[0]
            dest = objects[1:]
    sourceHistory = cmds.listHistory(source, lv=1)
    sc = cmds.ls(sourceHistory, typ='skinCluster')
    if sc:
        maintainMaxInfluences = cmds.getAttr('{}.maintainMaxInfluences'.format(
            sc[0]))
        maxInfluences = cmds.getAttr('{}.maxInfluences'.format(sc[0]))
    newSCNames = []
    for d in dest:
        destHistory = cmds.listHistory(d, lv=1)
        oldSC = cmds.ls(destHistory, typ='skinCluster')
        if oldSC:
            cmds.delete(oldSC)
        jnts = cmds.skinCluster(sc[0], weightedInfluence=True, q=True)
        newSC = cmds.skinCluster(jnts, d, tsb=True)[0]
        cmds.setAttr('{}.maintainMaxInfluences'.format(newSC),
                   maintainMaxInfluences)
        cmds.setAttr('{}.maxInfluences'.format(newSC), maxInfluences)
        cmds.copySkinWeights(ss=sc[0],
                           ds=newSC,
                           nm=True,
                           surfaceAssociation='closestPoint')
        if rename:
            pass
            newSCName = renameDeformers(objects=[d])
        else:
            newSCName = newSC
        newSCNames.append(newSCName)
    #cmds.select(objects)
    return (newSCNames) 


def addJntsToSkin(skin_mesh, joints=[]):
    """Add given joints into given skinCluster with locked, zeroed weights
    
    Parameters:
        joint (string): name of joint to add
        skin (string): target skin cluster 
        
    Returns:
        
    """
    skin_cluster = cmds.ls(cmds.listHistory(skin_mesh), type='skinCluster')

    for joint in joints:
        cmds.skinCluster(skin_cluster, edit=True, dr=4, ps=0, ns=10, lw=True, wt=0, ai=joint)

def setSideColor(control, side):
    """Set control color based on placement
    
    Parameters:
        control (string): name of controller
        side (string): side of body where controller is placed, R, L, or C
        
    Returns:
        
    """
    #get shape node and set color overrides
    controlShape = cmds.listRelatives(control, shapes=True)[0]
    cmds.setAttr(controlShape + '.overrideEnabled', 1)
    cmds.setAttr(controlShape + '.overrideRGBColors', 1)

    # creating zippable tuple 
    rgb = ("R", "G", "B")

    #setting color template
    colorRight = [1, 0, 0]
    colorLeft = [0, 1, 1]
    colorCenter = [1, 1, 0]

    #evaluate side value and set colors
    if side == 'L':
        for channel, color in zip(rgb, colorLeft):
            cmds.setAttr(controlShape + '.overrideColor%s' % channel, color)
    if side == 'R':
        for channel, color in zip(rgb, colorRight):
            cmds.setAttr(controlShape + '.overrideColor%s' % channel, color)
    if side == 'C':
        for channel, color in zip(rgb, colorCenter):
            cmds.setAttr(controlShape + '.overrideColor%s' % channel, color)
        
def makeShape(shape, name='control', axis='y', size=.2):
    """Make nurbs curve shapes.

    """

    # get orient values from aimAxis
    if not axis in orients:
        raise ValueError('axis must be \'x\', \'y\', or \'z\'.')
    orient = orients.get(axis)
    if shape == 'circle':
        c = cmds.circle(name=name, nr=orient, ch=False, r=(size * .5))[0]
    else:
        c = cmds.curve(name=name, d=1, p=shapes[shape])
        cmds.setAttr('{}.sx'.format(c), size)
        cmds.setAttr('{}.sy'.format(c), size)
        cmds.setAttr('{}.sz'.format(c), size)
        if orient[0]:
            cmds.setAttr('{}.rz'.format(c), 90)
        elif orient[2]:
            cmds.setAttr('{}.rx'.format(c), 90)
        cmds.makeIdentity(c, apply=True)
    return c

orients = {'x': [1, 0, 0], 'y': [0, 1, 0], 'z': [0, 0, 1]}

shapes = {
    'sphere': [[0.0, 0.5, 0.0], [-0.19, 0.46, 0.0], [-0.35, 0.35, 0.0],
               [-0.46, 0.19, 0.0], [-0.5, 0.0, 0.0], [-0.46, -0.19, 0.0],
               [-0.35, -0.35, 0.0], [-0.19, -0.46, 0.0], [0.0, -0.5, 0.0],
               [0.19, -0.46, 0.0], [0.35, -0.35, 0.0], [0.46, -0.19, 0.0],
               [0.5, 0.0, 0.0], [0.46, 0.19, 0.0], [0.35, 0.35, 0.0],
               [0.19, 0.46, 0.0], [0.0, 0.5, 0.0], [0.0, 0.46, 0.19],
               [0.0, 0.35, 0.35], [0.0, 0.19, 0.46], [0.0, 0.0, 0.5],
               [0.19, 0.0, 0.46], [0.35, 0.0, 0.35], [0.46, 0.0, 0.19],
               [0.5, 0.0, 0.0], [0.46, 0.0, -0.19], [0.35, 0.0, -0.35],
               [0.19, 0.0, -0.46], [0.0, 0.0, -0.5], [-0.19, 0.0, -0.46],
               [-0.35, 0.0, -0.35], [-0.46, 0.0, -0.19], [-0.5, 0.0, 0.0],
               [-0.46, 0.0, 0.19], [-0.35, 0.0, 0.35], [-0.19, 0.0, 0.46],
               [0.0, 0.0, 0.5], [0.0, -0.19, 0.46], [0.0, -0.35, 0.35],
               [0.0, -0.46, 0.19], [0.0, -0.5, 0.0], [0.0, -0.46, -0.19],
               [0.0, -0.35, -0.35], [0.0, -0.19, -0.46], [0.0, 0.0, -0.5],
               [0.0, 0.19, -0.46], [0.0, 0.35, -0.35], [0.0, 0.46, -0.19],
               [0.0, 0.5, 0.0]]
}