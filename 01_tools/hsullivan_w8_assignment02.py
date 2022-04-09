# 08 Week *********************************************************************
# content     = assignment
#
# deliver     = .zip file with only .py files you created or modified
#               no need for .ma files since they can be recreated using your code
#               if stated provide .jpg, .gif or .mp4
#               (Add a link if too big for the upload)
#
# date        = 2022-01-03
# author      = contact@alexanderrichtertd.com
#******************************************************************************




print("**********************************************************************")
print("# 02 : GUI")
print("**********************************************************************")
# CREATE a simple but custom UI module (no popups/proptDialog/...) that

#   A. allows at least one user input
#   B. has at least 2 action buttons
#   C. both buttons are influenced by the input results.

# Content of your choosing: Modeling, Rigging, Lighting ... whatever helps you.
# e.g. renamer, snapping tool, asset creator, ...

import maya.cmds as cmds

def joint_creator_ui():
    
    window = cmds.window(title="Joint Creator", widthHeight=(350, 125))

    cmds.columnLayout(adjustableColumn=True)

    #input joint name and number
    cmds.textField('name', height=30, text='Joint Name')
    cmds.intField('joints', height=30, value=1) 

    cmds.separator(height=10)

    cmds.button(label='Select Parent',
                command=("hsullivan_w8_assignment02.get_parent()"))

    cmds.button(label='Create Joints',
                command=("hsullivan_w8_assignment02.create_joints()"))

    cmds.showWindow(window)

def get_parent():

    parent = cmds.ls(sl=True)

    print("Parent is " + str(parent))

    return parent

def create_joints():

    cmds.select(clear=True)
    cmds.select(get_parent()[0])

    joints = []

    #access data 
    joint_count = cmds.intField("joints", query=True, value=True)
    joint_name  = cmds.textField("name", query=True, text=True)

    #FIXME: will continue adding _ to create _0_1_2 instead of _0, _1, _2
    for number in range(joint_count):
        joint_name = joint_name + '_' + str(number)
        joint = cmds.joint(name=joint_name)
        joints.append(joint)

    print(str(joint_count) + " joints are created!")

    return joints





    # for nr in range(lgt_count):
    #     lgt_name = lgt_name + '_' + str(nr)
    #     cmds.createNode('aiAreaLight', name=lgt_name)

    # print(str(lgt_count) + " lights are created!")

