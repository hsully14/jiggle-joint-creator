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
import os
import sys
import json
import webbrowser

# TODO: clean up imports across files
import maya.cmds as mc
import maya.OpenMayaUI as omui

from shiboken2 import wrapInstance
from Qt import QtWidgets, QtGui, QtCore, QtCompat

import mesh_utils as mu
import control_curve_utils as ccu


# ************************************************************************************
# VARIABLES
# ************************************************************************************
CURRENT_PATH = os.path.dirname(__file__)
IMG_PATH = CURRENT_PATH + '/img/{}.png'
TITLE = os.path.splitext(os.path.basename(__file__))[0]

# ************************************************************************************
# UI CLASS
# ************************************************************************************
class JiggleJointUI():
    # TODO: add docstring

    def __init__(self):
        # build local ui path and load ui
        path_ui = CURRENT_PATH + '/' + TITLE + '.ui'
        self.wgCreator = QtCompat.loadUi(path_ui)

        # init data
        self.config_data = self.get_curve_config()
        self.create_connections()

        self.wgCreator.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.wgCreator.show()

    def create_connections(self):
        # connect icons
        self.wgCreator.btnHelp.setIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("btn_help"))))
        
        # controller setup group
        side_options = []
        for color in self.config_data["Side Colors"]:
            side_options.append(color)

        shape_options = []
        for shape in self.config_data["Control Shapes"]:
            shape_options.append(shape)
        
        self.wgCreator.cbxSide.addItems(side_options)
        self.wgCreator.cbxSide.currentIndexChanged.connect(self.on_side_type_change)
        self.wgCreator.edtName.textChanged.connect(self.get_control_name)
        self.wgCreator.edtName.setPlaceholderText('control name')
        self.wgCreator.cbxShape.addItems(shape_options)
        self.wgCreator.cbxShape.currentIndexChanged.connect(self.on_shape_type_change)
        self.wgCreator.sbxScale.valueChanged.connect(self.on_size_change)

        # scene setup group
        self.wgCreator.btnDrivers.clicked.connect(self.press_drivers)
        self.wgCreator.btnVerts.clicked.connect(self.press_verts)
        self.wgCreator.btnParentJnt.clicked.connect(self.press_parent_jnt)
        self.wgCreator.btnParentGrp.clicked.connect(self.press_parent_grp)

        # builder group
        self.wgCreator.chxAddToSkc.toggled.connect(self.check_add_to_skc)
        self.wgCreator.chxMirror.toggled.connect(self.check_mirror)
        self.wgCreator.btnBuild.clicked.connect(self.press_build)
        self.wgCreator.btnAddToSkc.clicked.connect(self.press_add_to_skc)
        self.wgCreator.btnMirror.clicked.connect(self.press_mirror)

        # footer
        self.wgCreator.btnHelp.clicked.connect(self.press_help)

    # ************************************************************************************
    # button press
    # ************************************************************************************
    def on_side_type_change(self):
        print('Side type changed to {}'.format(self.wgCreator.cbxSide.currentText()))

        if self.wgCreator.cbxSide.currentText() == 'C':
            self.wgCreator.chxMirror.setEnabled(False)
        if self.wgCreator.cbxSide.currentText() == '-':
            self.wgCreator.chxMirror.setEnabled(False)
        if self.wgCreator.cbxSide.currentText() == 'L':
            self.wgCreator.chxMirror.setEnabled(True)
        if self.wgCreator.cbxSide.currentText() == 'R':
            self.wgCreator.chxMirror.setEnabled(True)

    def get_control_name(self):
        print('Name changed to {}'.format(self.wgCreator.edtName.text()))
        self.name = self.wgCreator.edtName.text()

    def on_shape_type_change(self):
        print('Shape type changed to {}'.format(self.wgCreator.cbxShape.currentText()))
        self.shape = self.wgCreator.cbxShape.currentText()

    def on_size_change(self):
        print('Size changed to {}'.format(self.wgCreator.sbxScale.value()))
        self.size = self.wgCreator.sbxScale.value()

    def press_drivers(self):
        # TODO: try/except error logging for not grabbing faces, not skinned mesh
        print('Driver faces grabbed')
        geos = mu.duplicate_selected_faces()

        self.skinned_geometry = geos[0]
        self.base_geometry = geos[1]

        print(self.skinned_geometry)
        print(self.base_geometry)

    def press_verts(self):
        # TODO: try/except error logging for not grabbing verts, not on driver geo
        print('Driver verts grabbed')
        self.source_verts = mu.get_selected_verts()
        print(self.selected_verts)

    def press_parent_jnt(self):
        # TODO: better error handling
        print('Parent joint grabbed')
        self.parent_jnt = mc.ls(sl=True)
        print(self.parent_jnt)

        if len(self.parent_jnt) > 1:
            print('too many joints selected!')

    def press_parent_grp(self):
        # TODO: better error handling
        print('Parent group grabbed')
        self.parent_grp = mc.ls(sl=True)
        print(self.parent_grp)

        if len(self.parent_grp) > 1:
            print('too many groups selected!')

    def check_add_to_skc(self):
        print('Adding to skincluster check')

    def check_mirror(self):
        print('Mirroring setup check')

    def press_build(self):
        print('Building setup')
        ccu.make_control_shape(self.shape, self.name, self.size)

    def press_add_to_skc(self):
        print('Adding to skincluster press')

    def press_mirror(self):
        print('Mirroring setup press') 

    def press_help(self):
        webbrowser.open("https://github.com/hsully14/jiggle-joint-creator")

    # ************************************************************************************
    # functions
    # ************************************************************************************

    def get_curve_config(self):
        """Read .json file as Python object"""
        config_file = CURRENT_PATH + '/control_curve_config.json'

        with open(config_file, 'r') as f:
            config_data = json.loads(f.read())
        return config_data


    def build_jiggle_setups(self, name, base_geometry, source_verts, side):
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


    def connect_to_hierarchy(self, jiggle_setups, parent_group, parent_joint, base_geometry):
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


    # def showEvent(self, e):
    #     super(JiggleJointUI, self).showEvent(e)

    #     if self.geometry:
    #         self.restoreGeometry(self.geometry)

    # def closeEvent(self, e):
    #     if isinstance(self, JiggleJointUI):
    #         super(JiggleJointUI, self).closeEvent(e)
    #         self.geometry = self.saveGeometry()













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
# def maya_main_window():
# 	"""
# 	Return the Maya main window widget as a Python object
# 	"""
# 	main_window_ptr = omui.MQtUtil.mainWindow()
# 	if sys.version_info.major >= 3:
# 		return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
# 	else:
# 		return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


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





#*******************************************************************
# START
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    classVar = JiggleJointUI()
    app.exec_()











