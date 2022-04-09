import maya.cmds as mc


def lockAndHide(obj, lock=False, hide=False, attrs=[]):
    for a in attrs:
        if a == 't':
            a = 'translate'
        if a == 'r':
            a = 'rotate'
        if a == 's':
            a = 'scale'
        mc.setAttr('{}.{}'.format(obj, a), l=lock, k=hide)