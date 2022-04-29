# STYLE ***************************************************************************
# content = assignment (Python Advanced)
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
# **********************************************************************************
import maya.cmds as mc

# COMMENT --------------------------------------------------
# Not optimal


def set_color(ctrl_list=None, ctrl_color=None):

    colors = {1 : 4,
              2 : 13,
              3 : 25,
              4 : 17,
              5 : 17,
              6 : 15,
              7 : 6,
              8 : 16}

    for ctrl in ctrl_list:
        try:
            mc.setAttr(ctrl + 'Shape.overrideEnabled', 1)
            mc.setAttr(ctrl + 'Shape.overrideColor', colors[ctrl_color])
        except Exception as err:
            print("Cannot set color override on {} shape. Exception: {}".format(ctrl, str(err)))

# EXAMPLE
# set_color(['circle','circle1'], 8)
