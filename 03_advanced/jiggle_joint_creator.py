import os

import maya.cmds as mc
import pymel.core as pm

import mesh_utils as mu
import control_curve_utils as ccu

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

    if mc.window(ui_title, exists=True):
        print('CLOSE duplicate window')
        mc.deleteUI(ui_title)


    #**************************************************************************
    # CREATE NEW UI
    # It is important to give the window a name besides the title
    # the name will be used above for the deleteUI
    window = mc.window(ui_title, 
                        title='Jiggle Joint Creator', 
                        width=500)

    mc.columnLayout(adjustableColumn=True)

    #add image
    mc.image(image=IMG_PATH + 'jiggle_joint_creator.png')

    mc.separator(height=10)

    #input MESH
    mc.rowLayout(numberOfColumns=2)
    mc.text(label='Skinned Mesh:', 
                annotation="Input name of skinned mesh to add jiggle joint", 
                width=250,
                height=30, 
                align='right')
    mc.textField('skinned_mesh', 
                    width=250, 
                    height=30, 
                    text='')

    mc.setParent('..')    # this "closes" the current layout

    #input LOCATOR
    mc.rowLayout(numberOfColumns=2)
    mc.text(label='Placement Locator:', 
                annotation="Input name of locator to use as reference object", 
                width=250, 
                height=30, 
                align='right')
    mc.textField('locator', 
                    width=250,
                    height=30, 
                    text='')

    mc.setParent('..')    # this "closes" the current layout

    #input CONTROL NAME
    mc.rowLayout(numberOfColumns=2)
    mc.text(label='Control Name:', 
                annotation="Input name of controller", 
                width=250, 
                height=30, 
                align='right')
    mc.textField('control_name', 
                    width=250, 
                    height=30, 
                    text='')

    mc.setParent('..')    # this "closes" the current layout

    #input SIDE
    mc.rowLayout(numberOfColumns=2)
    mc.text(label='Side of Body:', 
                annotation="Input L, R, or C to assign color and name accordingly", 
                width=250, 
                height=30, 
                align='right')
    mc.textField('body_side', 
                    width=250, 
                    height=30, 
                    text='')

    mc.setParent('..')    # this "closes" the current layout

    #input JOINT PARENT
    mc.rowLayout(numberOfColumns=2)
    mc.text(label='Parent Joint:', 
                annotation="Input joint to use as joint parent", 
                width=250, 
                height=30, 
                align='right')
    mc.textField('jnt_parent', 
                    width=250, 
                    height=30, 
                    text='')

    mc.setParent('..')    # this "closes" the current layout

    #input CONTROLLER PARENT GRP
    mc.rowLayout(numberOfColumns=2)
    mc.text(label='Controller Parent Group:', 
                annotation="Input hierarchy object to use as controller parent", 
                width=250, 
                height=30, 
                align='right')
    mc.textField('parent_grp', 
                    width=250, 
                    height=30, 
                    text='')

    mc.setParent('..')    # this "closes" the current layout

    mc.separator(height=10)

    # CHECKBOXES
    mc.rowLayout(numberOfColumns=1)
    mc.checkBox('cbx_add_to_skc', 
                    label='Add to Skin Cluster?', 
                    annotation="Choose whether to add jiggle joint to skinned mesh cluster automatically", 
                    width=500, 
                    height=30, 
                    onCommand="print('Adding new joint to skin cluster')", 
                    offCommand="print('Will not add new joint to skin cluster')", 
                    align='center')

    mc.setParent('..')    # this "closes" the current layout

    #CREATE!
    mc.separator(height=10)
    mc.button(label="Create Jiggle Joint",
                annotation="Create jiggle joint and control setup",
                width=500, 
                height=50, 
                command="jiggle_joint_creator.confirm_creation_popup()", 
                backgroundColor=[0,.5,0])
    mc.separator(height=10)

    mc.setParent('..')    # this "closes" the current layout

    #TODO: confirm this setup
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="report problem", 
                annotation="Report issues online", 
                width=250,
                command="import webbrowser; webbrowser.open('https://www.artstation.com/hsully')")
    mc.button(label="get help", 
                annotation="Reach out to author", 
                width=250,
                command="import webbrowser; webbrowser.open('https://www.artstation.com/hsully')")

    mc.setParent('..')    # this "closes" the current layout

    mc.showWindow(window)

#jiggle_joint_ui()

def confirm_creation_popup():

    popup_message = 'Are you ready?'

    result = mc.confirmDialog(title='Confirm Creation',
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

    result = mc.confirmDialog(title='Missing Info',
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
    skin_mesh = mc.textField('skinned_mesh', query=True, text=True)
    sourceLoc = mc.textField('locator', query=True, text=True)
    ctrl_name = mc.textField('control_name', query=True, text=True)
    side = mc.textField('body_side', query=True, text=True)
    jnt_parent = mc.textField('jnt_parent', query=True, text=True)
    grp_parent = mc.textField('parent_grp', query=True, text=True)
    
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
    mc.delete(JIGGLE_COMPONENTS['proxy_geo'], ch=True)

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
    add_to_skc = mc.checkBox('cbx_add_to_skc', query=True, value=True)

    if add_to_skc:
        addJntsToSkin(JIGGLE_COMPONENTS['skin_mesh'], joints=[JIGGLE_COMPONENTS['jiggle_jnt']])

    #hide locator 
    mc.hide(sourceLoc)

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
    geo = mc.polyPlane(name=geoName,
                       w=3,
                       h=3,
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
    controller = makeShape('sphere', name=controlName, axis='x', size=2)
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
    mc.parent(jiggleJoint, parentJoint)
    mc.connectAttr('{}.worldInverseMatrix[0]'.format(parentJoint), '{}.matrixIn[1]'.format(jntMultNode))

    mc.parent(jiggleController, parentModule)

    # parent proxy jiggle geo into G_Proxy group and hide visibility
    proxyGrp = mc.group(n='G_Jiggle_Proxy', em=True)
    mc.parent(proxyGeo, proxyGrp)
    mc.hide(proxyGeo)


def test():
    print('Hello World')


# ************************************************************************************
# CLEANING UP THIS MODULE - NEW STUFF STARTS BELOW
# ************************************************************************************

# TODO: 4/26, implement mirroring. start work on UI to grab inputs. 

def init_jiggle_joint(name, base_geometry, source_verts=[], side='None'):
    """Build jiggle plane, controller, and joint, based on input locators. Input name and parent module.

    Parameters:
        name (string): jiggle control name, ie "Spine"
        base_geometry (string): duplicated geo used as driver mesh
        source_loc (list): reference locators for joint positioning
        side (string): side of the body the controller is located, L, R, or C
        
    Returns:
        
    """

    # TODO: confirm this naming convention, naming is unclear with 'C' center naming - J_C_, C_C_ 
    # maybe create single variable to control naming, allow for easier updating?

    # TODO: convert UVpin creation to function?
    pin_name = 'F_{}_{}_UVPin'.format(side, name)
    # make uvPin node, set temp axes
    uv_pin = mc.createNode('uvPin', name=pin_name)
    mc.setAttr('{}.normalAxis'.format(uv_pin), 0)
    mc.setAttr('{}.tangentAxis'.format(uv_pin), 5)
    
    # get info from base_geometry
    base_geometry_shape = mc.listRelatives(base_geometry)[0]
    shape_orig = mc.deformableShape(base_geometry, createOriginalGeometry=True)

    # connect pin to base_geometry 
    # TODO: convert this to function? get base geo info 
    mc.connectAttr(shape_orig[0], '{}.originalGeometry'.format(uv_pin))
    mc.connectAttr('{}.worldMesh[0]'.format(base_geometry_shape), '{}.deformedGeometry'.format(uv_pin))

    ### get UV coordinate of points first, then input point UV to coordinate
    ### assign UV coord data to UV info on controllers, then connect to UV pin attr
    ### then connect offset parent matrix data to controller, with existing UV info

    for index, vert in enumerate(source_verts):
        print(index, vert)

        # format index to 2 digit number and add 1 for nicer object naming
        naming_index = '{0:0=2d}'.format(index+1)
        control_name = 'C_{}_{}_Jiggle_{}'.format(side, name, naming_index)
        joint_name   = 'J_{}_{}_Jiggle_{}'.format(side, name, naming_index)

        # create jiggle controller based on selected shape 
        # TODO: expose shape, axis, size, to UI
        controller = ccu.make_control_shape('sphere', control_name=control_name, axis='x', size=2)
        ccu.set_side_color(controller, side)

        vertex_uvs = mu.get_vertex_uvs(vert)
        vertex_u = vertex_uvs[0]
        vertex_v = vertex_uvs[1]

        # create attrs to store UV coord data
        mc.addAttr(controller, attributeType='float', defaultValue=vertex_u, keyable=True, minValue=0, maxValue=1, longName='coordinateU')
        mc.addAttr(controller, attributeType='float', defaultValue=vertex_v, keyable=True, minValue=0, maxValue=1, longName='coordinateV')

        # make connections from controller attrs to UVpin based on index count of controller
        mc.connectAttr('{}.coordinateU'.format(controller), '{}.coordinate[{}].coordinateU'.format(uv_pin, index))
        mc.connectAttr('{}.coordinateV'.format(controller), '{}.coordinate[{}].coordinateV'.format(uv_pin, index))

        # connect UVpin to controller offset parent for follow
        # TODO: figure out where things should be placed for this connection to happen
        mc.connectAttr('{}.outputMatrix[{}]'.format(uv_pin, index), '{}.offsetParentMatrix'.format(controller))
        
        # create joint
        mu.clear_selection()
        joint = mc.joint(name=joint_name)

        # TODO: create function to handle this matrix parenting?
        # create matrix nodes for controller to joint driving
        joint_decomp_node = mc.createNode('decomposeMatrix', n='{}_decomp'.format(joint_name))
        joint_mult_node = mc.createNode('multMatrix', n='{}_mult'.format(joint_name))

        # make connections from controller to joint via matrices
        mc.connectAttr('{}.worldMatrix[0]'.format(controller), '{}.matrixIn[0]'.format(joint_mult_node))
        mc.connectAttr('{}.matrixSum'.format(joint_mult_node), '{}.inputMatrix'.format(joint_decomp_node))
        mc.connectAttr('{}.outputTranslate'.format(joint_decomp_node), '{}.translate'.format(joint))
        mc.connectAttr('{}.outputRotate'.format(joint_decomp_node), '{}.rotate'.format(joint))   
        mc.connectAttr('{}.outputScale'.format(joint_decomp_node), '{}.scale'.format(joint))

    geo_name = 'H_{}_{}_Jiggle_Proxy'.format(side, name)
    mc.rename(base_geometry, geo_name)

        # #store data
        # JIGGLE_COMPONENTS['proxy_geo'] = geo
        # JIGGLE_COMPONENTS['jiggle_jnt'] = joint
        # JIGGLE_COMPONENTS['jiggle_ctrl'] = controller
        # JIGGLE_COMPONENTS['jnt_mult_node'] = joint_mult_node

        # return [geo, joint_mult_node]
































