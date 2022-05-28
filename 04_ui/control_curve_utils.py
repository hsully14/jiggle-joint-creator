# Control curve creation utilities - shapes dictionary and helper functions
import maya.cmds as mc


# ************************************************************************************
# VARIABLES
# ************************************************************************************
RGB = ("R", "G", "B")


# ************************************************************************************
# HELPER FUNCTIONS
# ************************************************************************************
def set_side_color(control_name, side_color):
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
    for channel, color in zip(RGB, side_color):
        # mc.setAttr(control_shape + '.overrideColor%s' % channel, color)
        mc.setAttr('{}.overrideColor{}'.format(control_shape, channel), color)


def lock_and_hide(object, lock=True, hide=True, attrs=[]):
    '''Locks and hides given attrs on given object. Change value of lock, hide as needed'''
    for attr in attrs:
        mc.setAttr('{}.{}'.format(object, attr), lock=lock, keyable=hide)
