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

import sys, os

import maya.cmds as mc
import maya.OpenMayaUI as omui

from PySide2 import QtCore, QtWidgets, QtUiTools, QtGui
from shiboken2 import wrapInstance

import mesh_utils as mu
import control_curve_utils as ccu


# ************************************************************************************
# VARIABLES
# ************************************************************************************
IMG_PATH = os.path.dirname(__file__) + "/img/"


# ************************************************************************************
# UI # 5/10 - planning to move UI elements to separate file?
# ************************************************************************************
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


# ************************************************************************************
# UI HELPERS
# ************************************************************************************
def maya_main_window():
	"""
	Return the Maya main window widget as a Python object
	"""
	main_window_ptr = omui.MQtUtil.mainWindow()
	if sys.version_info.major >= 3:
		return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
	else:
		return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


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

    
# ************************************************************************************
# JIGGLE JOINT CLASS
# ************************************************************************************
# TODO: 4/26, implement mirroring. start work on UI to grab inputs.
class JiggleJoint():
    '''A class improves this module by making a standard base for the jiggle joint setup. It 
    also allows for easier transference of data within the object, and easier data access on created
    jiggle joint objects.'''

    def __init__(self, joint_name, control_name, source_vert, uv_pin, side, index, base_geometry):
        # Question - is there a better way to init these variables? Will want to grab these from UI
        self.joint_name = joint_name
        self.control_name = control_name
        self.source_vert = source_vert
        self.uv_pin = uv_pin
        self.side = side
        self.index = index
        self.base_geometry = base_geometry

        self.create_jiggle_joint()

    def print_infos(self):
        print("Joint name: {}".format(self.joint_name))
        print("Control name: {}".format(self.control_name))
        print("Source vertex: {}".format(self.source_vert))
        print("UV pin driver: {}".format(self.uv_pin))
        print("Side: {}".format(self.side))
        print("Index: {}".format(self.index))
        print("Base geometry: {}".format(self.base_geometry))
        
    def create_jiggle_joint(self):
        '''assemble jiggle joint setup. create controller, joint, and hook into uvpin node'''
        # TODO: expose shape, axis, size, to UI
        controller = ccu.make_control_shape('sphere', control_name=self.control_name, axis='x', size=2)
        ccu.set_side_color(controller, self.side)

        vertex_uvs = mu.get_vertex_uvs(self.source_vert)
        vertex_u = vertex_uvs[0]
        vertex_v = vertex_uvs[1]

        # create attrs to store UV coord data
        mc.addAttr(controller, attributeType='float', defaultValue=vertex_u, keyable=True, minValue=0, maxValue=1, longName='coordinateU')
        mc.addAttr(controller, attributeType='float', defaultValue=vertex_v, keyable=True, minValue=0, maxValue=1, longName='coordinateV')

        # make connections from controller attrs to UVpin based on index count of controller
        mc.connectAttr('{}.coordinateU'.format(controller), '{}.coordinate[{}].coordinateU'.format(self.uv_pin, self.index))
        mc.connectAttr('{}.coordinateV'.format(controller), '{}.coordinate[{}].coordinateV'.format(self.uv_pin, self.index))
        mc.connectAttr('{}.outputMatrix[{}]'.format(self.uv_pin, self.index), '{}.offsetParentMatrix'.format(controller))
        
        mu.clear_selection()
        self.joint = mc.joint(name=self.joint_name)

        # TODO: create function to handle this matrix parenting?
        # create matrix nodes for controller to joint driving
        self.joint_decomp_node = mc.createNode('decomposeMatrix', n='{}_decomp'.format(self.joint_name))
        self.joint_mult_node = mc.createNode('multMatrix', n='{}_mult'.format(self.joint_name))

        # make connections from controller to joint via matrices
        mc.connectAttr('{}.worldMatrix[0]'.format(controller), '{}.matrixIn[0]'.format(self.joint_mult_node))
        mc.connectAttr('{}.matrixSum'.format(self.joint_mult_node), '{}.inputMatrix'.format(self.joint_decomp_node))
        mc.connectAttr('{}.outputTranslate'.format(self.joint_decomp_node), '{}.translate'.format(self.joint))
        mc.connectAttr('{}.outputRotate'.format(self.joint_decomp_node), '{}.rotate'.format(self.joint))   
        mc.connectAttr('{}.outputScale'.format(self.joint_decomp_node), '{}.scale'.format(self.joint))


# ************************************************************************************
# JOINT CREATION HELPERS
# ************************************************************************************
def build_jiggle_setups(name, base_geometry, source_verts, side):
    '''feed info to jigglejoint class object and loop through selected verts'''
    #TODO: figure out when to rename base geometry; need to replace naming if done at front
    #geo_name = 'H_{}_{}_Jiggle_Proxy'.format(side, name)
    #base_geometry = mc.rename(base_geometry, geo_name)
    jiggle_setups = []

    uv_pin = mu.create_uv_pin(name, side, base_geometry)

    for index, source_vert in enumerate(source_verts):
        # format index to 2 digit number and add 1 for nicer object naming
        naming_index = '{0:0=2d}'.format(index+1)
        control_name = 'C_{}_{}_Jiggle_{}'.format(side, name, naming_index)
        joint_name   = 'J_{}_{}_Jiggle_{}'.format(side, name, naming_index)

        jiggle_joint = JiggleJoint(joint_name, control_name, source_vert, uv_pin, side, naming_index, base_geometry)
        jiggle_setups.append(jiggle_joint)
        
    return jiggle_setups


def connect_to_hierarchy(jiggle_setups, parent_group, parent_joint, base_geometry):
    '''attach created jigglejoint objects to hierarchy'''
    # TODO: evaluate this on more complex setup

    # controller, joint
    for jiggle_joint in jiggle_setups:
        mc.parent(jiggle_joint.joint, parent_joint)
        mc.connectAttr('{}.worldInverseMatrix[0]'.format(parent_joint), '{}.matrixIn[1]'.format(jiggle_joint.joint_mult_node))
        mc.parent(jiggle_joint.control_name, parent_group)

    # driver geo
    if not mc.objExists('G_Jiggle_Proxy'):
        proxy_geo_group = mc.group(name='G_Jiggle_Proxy', empty=True)
    mc.parent(base_geometry, proxy_geo_group)
    mc.hide(base_geometry)





# FIXME: old code, refactor in progress. put here for safekeeping
# def create_jiggle_setup():
#     """Helper function to call and run components of jiggle joint creator system 
        
#     """
    
#     #get values from UI textfields
#     skin_mesh = mc.textField('skinned_mesh', query=True, text=True)
#     sourceLoc = mc.textField('locator', query=True, text=True)
#     ctrl_name = mc.textField('control_name', query=True, text=True)
#     side = mc.textField('body_side', query=True, text=True)
#     jnt_parent = mc.textField('jnt_parent', query=True, text=True)
#     grp_parent = mc.textField('parent_grp', query=True, text=True)
    
#     #validate input values, cancel if empty strings exist
#     inputs = [skin_mesh, sourceLoc, ctrl_name, side, jnt_parent, grp_parent]
#     if check_empty_inputs(inputs):
#         missing_info_popup()
#         return

#     #store information in dictionary for easier access; FIXME: make this better 
#     JIGGLE_COMPONENTS['skin_mesh'] = skin_mesh
#     JIGGLE_COMPONENTS['locator'] = sourceLoc
#     JIGGLE_COMPONENTS['control_name'] = ctrl_name
#     JIGGLE_COMPONENTS['body_side'] = side
#     JIGGLE_COMPONENTS['jnt_parent'] = jnt_parent
#     JIGGLE_COMPONENTS['parent_grp'] = grp_parent

#     #start building jiggle setup
#     build_jiggle_plane(ctrl_name, sourceLoc, side)
    
#     #shrinkwrap geo to skinned geo
#     shrink_wrap_geo(JIGGLE_COMPONENTS['proxy_geo'], JIGGLE_COMPONENTS['skin_mesh'])

#     #remove shrinkwrap node and history
#     mc.delete(JIGGLE_COMPONENTS['proxy_geo'], ch=True)

#     #copy skinning from skin_mesh to proxy_geo
#     copySkinCluster(source=JIGGLE_COMPONENTS['skin_mesh'], dest=[JIGGLE_COMPONENTS['proxy_geo']], rename=True)

#     #collect all created items and connect them to the hierarchy using matrices
#     connectToHierarchy(JIGGLE_COMPONENTS['jiggle_jnt'], 
#                         JIGGLE_COMPONENTS['jnt_parent'], 
#                         JIGGLE_COMPONENTS['jnt_mult_node'], 
#                         JIGGLE_COMPONENTS['jiggle_ctrl'], 
#                         JIGGLE_COMPONENTS['parent_grp'], 
#                         JIGGLE_COMPONENTS['proxy_geo'])

#     #get values from UI checkbox
#     add_to_skc = mc.checkBox('cbx_add_to_skc', query=True, value=True)

#     if add_to_skc:
#         addJntsToSkin(JIGGLE_COMPONENTS['skin_mesh'], joints=[JIGGLE_COMPONENTS['jiggle_jnt']])

#     #hide locator 
#     mc.hide(sourceLoc)

#     print('Created jiggle setup')
















