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
print("# 01 : INFORMATION, WARNING AND ERROR")
print("**********************************************************************")
# CREATE multiple simple popup functions that you can also reuse for your application:

#   A. Inform about a current status.
#      Button: OKAY

import maya.cmds as cmds
import webbrowser

#popup_message = 'You have encountered a problem!'
#popup_message = 'Your current status is: BLANK'
#popup_message = 'You have encountered an error. Get help?'

def current_status(popup_message):
    result = cmds.confirmDialog(title='Current Status',
                                message=popup_message,
                                button=['OKAY'],
                                defaultButton='OKAY',
                                cancelButton='DONE')

    print(result)

    # EXECUTE button
    if result == 'OKAY':
        print('Status Updated!')
        
#   B. Warn about an issue and ask to stop or continue the process.
#      BUTTONS: CONTINUE or STOP

def raise_issue_warning(popup_message):

    result = cmds.confirmDialog(title='Warning!',
                                message=popup_message,
                                button=['CONTINUE', 'STOP'],
                                defaultButton='STOP',
                                cancelButton='STOP')

    print(result)

    # EXECUTE button
    if result == 'CONTINUE':
        print('Continuing process')

    if result == 'STOP':
        print('Halting process')

#   C. Highlight an error in your process and give the options
#      of closing the popup window or opening a helping website.
#      BUTTONS: OKAY and HELP (opens your website)

def error_assistance(popup_message):

    result = cmds.confirmDialog(title='Error!',
                                message=popup_message,
                                button=['GET HELP', 'CLOSE'],
                                defaultButton='GET HELP',
                                cancelButton='CLOSE')

    print(result)

    # EXECUTE button
    if result == 'GET HELP':
        print('Getting help')
        webbrowser.open("https://www.artstation.com/hsully")

    if result == 'CLOSE':
        print('Closing popup')


# All this functions await the argument:
# message (which is the message of the info/warning/error)
# This allows you to reuse them for different occasions.

# TIP: Print out the button presses
