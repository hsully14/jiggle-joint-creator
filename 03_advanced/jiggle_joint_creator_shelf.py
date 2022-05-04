import maya.cmds as cmds
import os

# c. Create a custom shelf button inside your userSetup.
#    The shelf tab is called "checker" and the button has an icon and the following code:

MENU_NAME = 'Jiggle Joint'
IMG_PATH = os.path.dirname(__file__) + "/img/"

#******************************************************************************
# MENU
#******************************************************************************
def custom_menu():
    delete_custom_menu()

    menu = cmds.menu(MENU_NAME, parent='MayaWindow',
                     label=MENU_NAME, helpMenu=True, tearOff=True)

    #*************************************************************************
    # SAVE & LOAD
    cmds.menuItem(parent=menu, label='Open Creator', command='import jiggle_joint_creator;jiggle_joint_creator.jiggle_joint_ui()')

    # BREAK ******************************************************************
    cmds.menuItem(parent=menu, divider=True)
    #*************************************************************************

    cmds.menuItem(parent=menu, label='Credit', command='import webbrowser;webbrowser.open("https://www.artstation.com/hsully")')

def delete_custom_menu():
    if cmds.menu(MENU_NAME, query=True, exists=True):
        cmds.deleteUI(MENU_NAME, menu=True)



#*************************************************************************
# SHELF
def custom_shelf():
    delete_custom_shelf()

    cmds.shelfLayout(MENU_NAME, parent="ShelfLayout")

    cmds.shelfButton(parent=MENU_NAME,
                     annotation='Jiggle Joint Creator',
                     image1=IMG_PATH + 'jj_ui.png',
                     command='import jiggle_joint_creator;jiggle_joint_creator.jiggle_joint_ui()')


def delete_custom_shelf():
    if cmds.shelfLayout(MENU_NAME, exists=True):
        cmds.deleteUI(MENU_NAME)




