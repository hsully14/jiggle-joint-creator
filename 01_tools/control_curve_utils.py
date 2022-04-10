import maya.cmds as mc

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


def make_control_shape(shape, control_name='control', axis='y', size=1):
   
    """Creates NURBS curve shape for animateable control

    Arguments:
        shape (string): type of shape to create, from ORIENTS
        control_name (string): name of controller
        axis (string): primary aim axis
        size (integer): transform size
    Returns:
        control_curve: NURBS curve transform
    """

    # verify axis input and get orient values from aimAxis
    if axis not in ORIENTS:
        #TODO: change this to a logged error message
        raise ValueError('axis must be \'x\', \'y\', or \'z\'.')
        
    orient = ORIENTS.get(axis)

    if shape == 'circle':
        control_curve = mc.circle(name=control_name, normal=orient, constructionHistory=False, radius=(size * .5))[0]
    else:
        control_curve = mc.curve(name=control_name, degree=1, point=SHAPES[shape])
        # rename curve shape to match parent
        control_curve_shape = mc.listRelatives(control_curve, shapes=True)
        mc.rename(control_curve_shape, "{}Shape".format(control_name))

        mc.setAttr('{}.sx'.format(control_curve), size)
        mc.setAttr('{}.sy'.format(control_curve), size)
        mc.setAttr('{}.sz'.format(control_curve), size)

        if orient[0]:
            mc.setAttr('{}.rz'.format(control_curve), 90)
        elif orient[2]:
            mc.setAttr('{}.rx'.format(control_curve), 90)

        mc.makeIdentity(control_curve, apply=True)

    return control_curve


def set_side_color(control_name, side):
    """Set control color based on given side of rig

    Arguments:
        control_name (string): name of controller transform
        side (string): side of body where controller is placed: L, R, C, or None

    Returns:
    """

    # get shape node and set color overrides
    control_shape = mc.listRelatives(control_name, shapes=True)[0]
    mc.setAttr(control_shape + '.overrideEnabled', 1)
    mc.setAttr(control_shape + '.overrideRGBColors', 1)

    # unzip RGB tuple, side color dict
    for channel, color in zip(RGB, SIDE_COLORS[side]):
        mc.setAttr(control_shape + '.overrideColor%s' % channel, color)

