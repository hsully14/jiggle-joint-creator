# Control curve creation utilities - shapes dictionary and helper functions

import maya.cmds as mc


# ************************************************************************************
# VARIABLES
# ************************************************************************************
ORIENTS = {'x': [1, 0, 0], 'y': [0, 1, 0], 'z': [0, 0, 1]}
SHAPES = {
    'square': [[-.5, 0, -.5], [-.5, 0, .5], [.5, 0, .5], [.5, 0, -.5],
               [-.5, 0, -.5]],
    'cube': [[-0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, -0.5],
             [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5],
             [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, -0.5, 0.5],
             [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5],
             [0.5, 0.5, -0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5],
             [-0.5, 0.5, -0.5]],
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
               [0.0, 0.5, 0.0]],
    'arrow': [[0.0, 0.67, 0.4], [0.0, 0.0, 0.4], [0.0, 0.0, 0.67],
              [0.0, -0.4, 0.0], [0.0, 0.0, -0.67], [0.0, 0.0, -0.4],
              [0.0, 0.67, -0.4], [0.0, 0.67, 0.4]],
    'plus': [[1.0, 0.0, -1.0], [2.0, 0.0, -1.0], [2.0, 0.0, 1.0],
             [1.0, 0.0, 1.0], [1.0, 0.0, 2.0], [-1.0, 0.0, 2.0],
             [-1.0, 0.0, 1.0], [-2.0, 0.0, 1.0], [-2.0, 0.0, -1.0],
             [-1.0, 0.0, -1.0], [-1.0, 0.0, -2.0], [1.0, 0.0, -2.0],
             [1.0, 0.0, -1.0]],
    'orient': [[0.1, 0.6, -0.1], [0.5, 0.5, -0.1], [0.75, 0.33, -0.1],
               [0.75, 0.33, -0.1], [0.75, 0.33, -0.34], [0.75, 0.33, -0.34],
               [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.75, 0.33, 0.34],
               [0.75, 0.33, 0.34], [0.75, 0.33, 0.1], [0.75, 0.33, 0.1],
               [0.5, 0.5, 0.1], [0.1, 0.6, 0.1], [0.1, 0.6, 0.1],
               [0.1, 0.5, 0.5], [0.1, 0.33, 0.75], [0.1, 0.33, 0.75],
               [0.34, 0.33, 0.75], [0.34, 0.33, 0.75], [0.0, 0.0, 1.0],
               [0.0, 0.0, 1.0], [-0.34, 0.33, 0.75], [-0.34, 0.33, 0.75],
               [-0.1, 0.33, 0.75], [-0.1, 0.33, 0.75], [-0.1, 0.5, 0.5],
               [-0.1, 0.6, 0.1], [-0.1, 0.6, 0.1], [-0.5, 0.5, 0.1],
               [-0.75, 0.33, 0.1], [-0.75, 0.33, 0.1], [-0.75, 0.33, 0.34],
               [-0.75, 0.33, 0.34], [-1.0, 0.0, 0.0], [-1.0, 0.0, 0.0],
               [-0.75, 0.33, -0.34], [-0.75, 0.33, -0.34], [-0.75, 0.33, -0.1],
               [-0.75, 0.33, -0.1], [-0.5, 0.5, -0.1], [-0.1, 0.6, -0.1],
               [-0.1, 0.6, -0.1], [-0.1, 0.5, -0.5], [-0.1, 0.33, -0.75],
               [-0.1, 0.33, -0.75], [-0.34, 0.33, -0.75], [-0.34, 0.33, -0.75],
               [0.0, 0.0, -1.0], [0.0, 0.0, -1.0], [0.34, 0.33, -0.75],
               [0.34, 0.33, -0.75], [0.1, 0.33, -0.75], [0.1, 0.33, -0.75],
               [0.1, 0.5, -0.5], [0.1, 0.6, -0.1]],
    'world': [[-2.0, 0.0, -6.0], [-4.0, 0.0, -6.0], [0.0, 0.0, -10.0],
              [4.0, 0.0, -6.0], [2.0, 0.0, -6.0], [2.0, 0.0, -2.67],
              [2.67, 0.0, -2.0], [6.0, 0.0, -2.0], [6.0, 0.0, -4.0],
              [10.0, 0.0, 0.0], [6.0, 0.0, 4.0], [6.0, 0.0, 2.0],
              [2.67, 0.0, 2.0], [2.0, 0.0, 2.67], [2.0, 0.0, 6.0],
              [4.0, 0.0, 6.0], [0.0, 0.0, 10.0], [-4.0, 0.0, 6.0],
              [-2.0, 0.0, 6.0], [-2.0, 0.0, 2.67], [-2.67, 0.0, 2.0],
              [-6.0, 0.0, 2.0], [-6.0, 0.0, 4.0], [-10.0, 0.0, 0.0],
              [-6.0, 0.0, -4.0], [-6.0, 0.0, -2.0], [-2.67, 0.0, -2.0],
              [-2.0, 0.0, -2.67], [-2.0, 0.0, -6.0]],
    'triangle': [[-.5, 0, 0], [0, 0, .5], [.5, 0, 0], [-.5, 0, 0]]
}
RGB = ("R", "G", "B")
SIDE_COLORS = {
    'L' : [0, 1, 1],
    'R' : [1, 0, 0],
    'C' : [1, 1, 0],
    'None' : [1, .3, 0]
}


# ************************************************************************************
# HELPER FUNCTIONS
# ************************************************************************************
def make_control_shape(shape, control_name='control', axis='y', size=1):
    """Creates NURBS curve shape for animateable control

    Arguments:
        shape (str): type of shape to create, from ORIENTS
        control_name (str): name of controller
        axis (str): primary aim axis
        size (str): transform size

    Returns:
        control_curve ((str)): NURBS curve transform
    """
    # TODO: expose axis, name, and size to UI later on
    # verify axis input and get orient values from aimAxis
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
        control_curve = mc.curve(name=control_name, degree=1, point=SHAPES[shape])

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

    # unzip RGB tuple, side color dict, and apply color
    for channel, color in zip(RGB, SIDE_COLORS[side]):
        # mc.setAttr(control_shape + '.overrideColor%s' % channel, color)
        mc.setAttr('{}.overrideColor{}'.format(control_shape, channel), color)


def lock_and_hide(object, lock=True, hide=True, attrs=[]):
    '''Locks and hides given attrs on given object. Change value of lock, hide as needed'''
    for attr in attrs:
        mc.setAttr('{}.{}'.format(object, attr), lock=lock, keyable=hide)
