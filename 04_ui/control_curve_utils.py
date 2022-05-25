# Control curve creation utilities - shapes dictionary and helper functions
import os


import maya.cmds as mc


# ************************************************************************************
# VARIABLES
# ************************************************************************************
ORIENTS = {'x': [1, 0, 0], 'y': [0, 1, 0], 'z': [0, 0, 1]}
RGB = ("R", "G", "B")


# ************************************************************************************
# HELPER FUNCTIONS
# ************************************************************************************
def make_control_shape(shape, control_name='control', axis='y', size=1):
    """Creates NURBS curve shape for animateable control

    Arguments:
        shape (str): type of shape to create, from control curve config
        control_name (str): name of controller
        axis (str): primary aim axis
        size (str): transform size

    Returns:
        control_curve (str): NURBS curve transform
    """
    # TODO: expose axis, name, and size to UI later on
    # verify axis input and get orient values from aimAxis
    curve_shape = get_curve_config()['Control Shapes'][shape]

    if axis not in ORIENTS:
        # TODO: change this to a logged error message
        raise ValueError('Axis must be \'x\', \'y\', or \'z\'.')

    orient = ORIENTS.get(axis)



    if shape == 'circle':
        control_curve = mc.circle(name=control_name,
                                  normal=orient,
                                  constructionHistory=False,
                                  radius=(size * .5))[0]
    else:
        control_curve = mc.curve(name=control_name, degree=1, point=curve_shape)

        mc.setAttr('{}.sx'.format(control_curve), size)
        mc.setAttr('{}.sy'.format(control_curve), size)
        mc.setAttr('{}.sz'.format(control_curve), size)

        if orient[0]:
            mc.setAttr('{}.rz'.format(control_curve), 90)
        elif orient[2]:
            mc.setAttr('{}.rx'.format(control_curve), 90)

    # rename curve shape to match transform
    control_curve_shape = mc.listRelatives(control_curve, shapes=True)
    mc.rename(control_curve_shape, "{}Shape".format(control_name))

    mc.makeIdentity(control_curve, apply=True)

    return control_curve


def set_side_color(control_name, side):
    """Set control color based on given side of rig. References constants in file header.

    Arguments:
        control_name (str): name of controller to act on
        side (str): side of body where controller is placed: L, R, C, or None
    """
    # get control shape node and activate color overrides
    control_shape = mc.listRelatives(control_name, shapes=True)[0]
    mc.setAttr('{}.overrideEnabled'.format(control_shape), 1)
    mc.setAttr('{}.overrideRGBColors'.format(control_shape), 1)

    side_color = get_curve_config()['Side Colors'][side]

    # unzip RGB tuple, side color dict, and apply color
    for channel, color in zip(RGB, side_color):
        # mc.setAttr(control_shape + '.overrideColor%s' % channel, color)
        mc.setAttr('{}.overrideColor{}'.format(control_shape, channel), color)


def lock_and_hide(object, lock=True, hide=True, attrs=[]):
    '''Locks and hides given attrs on given object. Change value of lock, hide as needed'''
    for attr in attrs:
        mc.setAttr('{}.{}'.format(object, attr), lock=lock, keyable=hide)
