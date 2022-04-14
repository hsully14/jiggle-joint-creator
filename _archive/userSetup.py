import sys
import maya.cmds as cmds

USERSETUP_DIR = cmds.internalVar(userScriptDir=True)

def start():

    #sys.path.append(r"E:\Documents\Python for Maya Masterclass\maya_resources\week_07\lecture_notes")
    #sys.path.append(r"E:\Documents\Python for Maya Masterclass\maya_resources\week_07\assignment")
    sys.path.append(r"E:\Documents\Python for Maya Masterclass\homework_files\week_08")
    
    import jiggle_joint_creator
    import jiggle_joint_creator_shelf

    jiggle_joint_creator_shelf.custom_menu()
    #jiggle_joint_creator_shelf.custom_shelf()

    print(USERSETUP_DIR)

cmds.evalDeferred(start, lp=True)

