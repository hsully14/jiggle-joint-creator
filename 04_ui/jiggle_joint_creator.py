# primary jiggle joint creator file
import os
import sys
import json
import webbrowser

import maya.cmds as mc

from collections import namedtuple
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
# HELPER FUNCTIONS
# ************************************************************************************
def get_curve_config():
    """Read .json file as Python object"""
    config_file = CURRENT_PATH + '/control_curve_config.json'

    with open(config_file, 'r') as f:
        config_data = json.loads(f.read())
    return config_data


# ************************************************************************************
# UI CLASS
# ************************************************************************************
class JiggleJointUI():
    '''UI class to handle jiggle joint data intake and jiggle setup generation'''
    def __init__(self):
        # build local ui path and load ui
        path_ui = CURRENT_PATH + '/' + TITLE + '.ui'
        self.wgCreator = QtCompat.loadUi(path_ui)

        # init data
        self.config_data = get_curve_config()
        self.create_connections()
        self.wgCreator.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.wgCreator.show()

    def create_connections(self):
        '''Build connections from UI elements to functions'''
        # connect icons
        self.wgCreator.btnHelp.setIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("btn_help"))))

        # controller dropdown setup
        side_options = []
        for color in self.config_data["Side Colors"]:
            side_options.append(color)

        shape_options = []
        for shape in self.config_data["Control Shapes"]:
            shape_options.append(shape)

        self.wgCreator.cbxSide.addItems(side_options)
        self.wgCreator.cbxSide.currentIndexChanged.connect(self.on_side_type_change)
        self.wgCreator.edtName.textChanged.connect(self.get_base_control_name)
        self.wgCreator.edtName.setPlaceholderText('control name')
        self.wgCreator.cbxShape.addItems(shape_options)
        self.wgCreator.cbxShape.currentIndexChanged.connect(self.on_shape_type_change)
        self.wgCreator.sbxScale.valueChanged.connect(self.on_size_change)

        self.side = self.wgCreator.cbxSide.currentText()
        self.base_name = self.wgCreator.edtName.text()
        self.shape = self.wgCreator.cbxShape.currentText()
        self.size = self.wgCreator.sbxScale.value()

        # scene setup group
        self.wgCreator.btnDrivers.clicked.connect(self.press_drivers)
        self.wgCreator.btnVerts.clicked.connect(self.press_verts)
        self.wgCreator.btnParentJnt.clicked.connect(self.press_parent_jnt)
        self.wgCreator.btnParentGrp.clicked.connect(self.press_parent_grp)

        # builder group
        self.wgCreator.btnBuild.clicked.connect(self.press_build)
        self.wgCreator.btnAddToSkc.clicked.connect(self.press_add_to_skc)

        # footer
        self.wgCreator.btnHelp.clicked.connect(self.press_help)

    # ************************************************************************************
    # button press
    # ************************************************************************************
    def on_side_type_change(self):
        self.side = self.wgCreator.cbxSide.currentText()

    def get_base_control_name(self):
        self.base_name = self.wgCreator.edtName.text()

    def on_shape_type_change(self):
        self.shape = self.wgCreator.cbxShape.currentText()

    def on_size_change(self):
        self.size = self.wgCreator.sbxScale.value()

    def press_drivers(self):
        '''get selected driver faces after checking validity'''
        selected = mc.ls(sl=True)

        if not selected:
            print('please select driver faces!')
            return

        # check selection type
        selected = self.get_selected_components()

        if selected.faces and not selected.verts and not selected.edges:
            geos = mu.duplicate_selected_faces()
            self.skinned_geometry = geos[0]
            self.base_geometry = geos[1]
            print('selecting faces on {}'.format(self.skinned_geometry))
        else:
            print('please select faces only!')

    def press_verts(self):
        '''get selected verts after checking validity'''
        selected = mc.ls(sl=True)

        if not selected:
            print('please select location verts!')
            return

        # check selection type
        selected = self.get_selected_components()

        if selected.verts and not selected.faces and not selected.edges:
            self.source_verts = mu.get_selected_verts()
            print('selecting verts {} on {}'.format(self.source_verts, self.skinned_geometry))
        else:
            print('please select verts only!')

        mc.selectMode(object=True)
        mu.clear_selection()

    def press_parent_jnt(self):
        selected = mc.ls(sl=True, type='joint')

        if len(selected) > 1 or not selected:
            print('please select one parent joint!')
            return

        self.parent_jnt = selected[0]
        print('selecting parent joint {}'.format(self.parent_jnt))

    def press_parent_grp(self):
        selected = mc.ls(sl=True, type='transform')

        if len(selected) > 1 or not selected:
            print('please select one parent group!')
            return

        self.parent_grp = selected[0]
        print('selecting controller parent group {}'.format(self.parent_grp))

    def press_build(self):
        if not self.base_name:
            print('please input a control name!')
            return
        if not self.base_geometry:
            print('please select driver faces!')
            return
        if not self.source_verts:
            print('please select source verts!')
            return
        if not self.parent_jnt:
            print('please select a parent joint!')
            return
        if not self.parent_jnt:
            print('please select a parent group!')
            return

        print('Building jiggle joint setups')
        self.jiggle_setups = self.build_jiggle_setups()
        self.connect_to_hierarchy(self.jiggle_setups)
        mu.copy_skincluster(self.skinned_geometry, self.base_geometry)

    def press_add_to_skc(self):
        for jiggle_setup in self.jiggle_setups:
            mu.add_joints_to_skincluster(self.skinned_geometry, jiggle_setup.joint_name)
            print('Adding joint {} to skincluster'.format(jiggle_setup.joint_name))

    def press_help(self):
        webbrowser.open("https://github.com/hsully14/jiggle-joint-creator")

    # ************************************************************************************
    # BUILDER FUNCTIONS
    # ************************************************************************************
    def build_jiggle_setups(self):
        '''feed info to jigglejoint class object and loop through selected verts'''        
        jiggle_setups = []

        uv_pin = mu.create_uv_pin(self.base_name, self.side, self.base_geometry)

        for index, source_vert in enumerate(self.source_verts):
            # format index to 2 digit number and add 1 for nicer object naming
            naming_index = '{0:0=2d}'.format(index+1)
            self.control_name = 'C_{}_{}_Jiggle_{}'.format(self.side, self.base_name, naming_index)
            self.joint_name   = 'J_{}_{}_Jiggle_{}'.format(self.side, self.base_name, naming_index)

            jiggle_joint = JiggleJoint(self.joint_name, self.control_name, source_vert, uv_pin, self.side, naming_index, self.base_geometry, self.shape, self.size)
            jiggle_setups.append(jiggle_joint)

        geo_name = 'H_{}_{}_Jiggle_Proxy'.format(self.side, self.base_name)
        self.base_geometry = mc.rename(self.base_geometry, geo_name)

        mc.showHidden(self.skinned_geometry)

        return jiggle_setups

    def connect_to_hierarchy(self, jiggle_setups):
        '''attach created jigglejoint objects to hierarchy'''
        # controller, joint
        for jiggle_joint in jiggle_setups:
            mc.parent(jiggle_joint.joint, self.parent_jnt)
            mc.connectAttr('{}.worldInverseMatrix[0]'.format(self.parent_jnt), '{}.matrixIn[1]'.format(jiggle_joint.joint_mult_node))
            mc.parent(jiggle_joint.control_name, self.parent_grp)

        # driver geo
        if not mc.objExists('G_Jiggle_Proxy'):
            proxy_geo_group = mc.group(name='G_Jiggle_Proxy', empty=True)
        else:
            proxy_geo_group = 'G_Jiggle_Proxy'

        mc.parent(self.base_geometry, proxy_geo_group)
        mc.hide(self.base_geometry)

    def get_selected_components(self):
        selectiontype = namedtuple('selectiontype', 'faces verts edges')
        
        sel = mc.ls(sl=True, type='float3') # this is obscure maya way to get only components
        faces = mc.polyListComponentConversion(sel, ff=True, tf =True)
        verts = mc.polyListComponentConversion(sel, fv=True, tv =True)
        edges = mc.polyListComponentConversion(sel, fe=True, te =True)
        return selectiontype (faces, verts, edges)

    def create(self):
        app = QtWidgets.QApplication(sys.argv)
        main_widget = JiggleJointUI()
        sys.exit(app.exec_())

    def start(self):
        global main_widget
        main_widget = JiggleJointUI()


# ************************************************************************************
# JIGGLE JOINT OBJECT CLASS
# ************************************************************************************
class JiggleJoint():
    '''A class improves this module by making a standard base for the jiggle joint setup. It 
    also allows for easier transference of data within the object, and easier data access on created
    jiggle joint objects.'''

    def __init__(self, joint_name, control_name, source_vert, uv_pin, side, index, base_geometry, shape, size):
        # Question - is there a better way to init these variables? Will want to grab these from UI
        self.joint_name = joint_name
        self.control_name = control_name
        self.source_vert = source_vert
        self.uv_pin = uv_pin
        self.side = side
        self.index = index
        self.base_geometry = base_geometry
        self.size = size
        self.shape = shape

        self.color_config_data = get_curve_config()

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
        controller = self.make_control_shape()
        side_color = get_curve_config()['Side Colors'][self.side]
        ccu.set_side_color(controller, side_color)

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

        # create matrix nodes for controller to joint driving
        self.joint_decomp_node = mc.createNode('decomposeMatrix', n='{}_decomp'.format(self.joint_name))
        self.joint_mult_node = mc.createNode('multMatrix', n='{}_mult'.format(self.joint_name))

        # make connections from controller to joint via matrices
        mc.connectAttr('{}.worldMatrix[0]'.format(controller), '{}.matrixIn[0]'.format(self.joint_mult_node))
        mc.connectAttr('{}.matrixSum'.format(self.joint_mult_node), '{}.inputMatrix'.format(self.joint_decomp_node))
        mc.connectAttr('{}.outputTranslate'.format(self.joint_decomp_node), '{}.translate'.format(self.joint))
        mc.connectAttr('{}.outputRotate'.format(self.joint_decomp_node), '{}.rotate'.format(self.joint))   
        mc.connectAttr('{}.outputScale'.format(self.joint_decomp_node), '{}.scale'.format(self.joint))

    def make_control_shape(self):
        """Creates NURBS curve shape for animateable control

        Arguments:
            shape (str): type of shape to create, from control curve config
            control_name (str): name of controller
            axis (str): primary aim axis
            size (str): transform size

        Returns:
            control_curve (str): NURBS curve transform
        """

        orients = {'x': [1, 0, 0], 'y': [0, 1, 0], 'z': [0, 0, 1]}
        axis='x'

        if axis not in orients:
            raise ValueError('Axis must be \'x\', \'y\', or \'z\'.')
        
        orient = orients.get(axis)

        # verify axis input and get orient values from aimAxis
        curve_shape = get_curve_config()['Control Shapes'][self.shape]

        if self.shape == 'circle':
            self.control_curve = mc.circle(name=self.control_name,
                                    normal=orient,
                                    constructionHistory=False,
                                    radius=(self.size * .5))[0]
        else:
            self.control_curve = mc.curve(name=self.control_name, degree=1, point=curve_shape)

            mc.setAttr('{}.sx'.format(self.control_curve), self.size)
            mc.setAttr('{}.sy'.format(self.control_curve), self.size)
            mc.setAttr('{}.sz'.format(self.control_curve), self.size)

            if orient[0]:
                mc.setAttr('{}.rz'.format(self.control_curve), 90)
            elif orient[2]:
                mc.setAttr('{}.rx'.format(self.control_curve), 90)

        # rename curve shape to match transform
        control_curve_shape = mc.listRelatives(self.control_curve, shapes=True)
        mc.rename(control_curve_shape, "{}Shape".format(self.control_name))

        mc.makeIdentity(self.control_curve, apply=True)

        return self.control_curve


# ************************************************************************************
# START
# ************************************************************************************
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    classVar = JiggleJointUI()
    app.exec_()


def create():
    app = QtWidgets.QApplication(sys.argv)
    main_widget = JiggleJointUI()
    sys.exit(app.exec_())


def start():
    global main_widget
    main_widget = JiggleJointUI()
