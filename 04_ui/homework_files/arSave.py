# ************************************************************************************
# arSave example
# ************************************************************************************

import os
import sys
import webbrowser

from Qt import QtWidgets, QtGui, QtCore, QtCompat


# ************************************************************************************
# VARIABLES
# ************************************************************************************
TITLE = os.path.splitext(os.path.basename(__file__))[0]
CURRENT_PATH = os.path.dirname(__file__)
IMG_PATH = CURRENT_PATH + '/img/{}.png'


# ************************************************************************************
# CLASS
# ************************************************************************************
class ArSave:

    def __init__(self):
        path_ui = CURRENT_PATH + '/' + TITLE + '.ui'
        self.wgSave = QtCompat.loadUi(path_ui)

        # connect icons
        self.wgSave.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("btn_save"))))

        self.wgSave.btnPreview.setIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("default"))))
        self.wgSave.btnScreenshot.setIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("btn_camera"))))
        self.wgSave.btnViewport.setIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("btn_viewport"))))

        self.wgSave.lblPen.setPixmap(QtGui.QPixmap(IMG_PATH.format("btn_write")))

        self.wgSave.btnFolder.setIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("btn_folder"))))
        self.wgSave.btnProject.setIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("btn_project"))))
        self.wgSave.btnUser.setIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("btn_user"))))
        self.wgSave.btnReport.setIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("btn_report"))))
        self.wgSave.btnHelp.setIcon(QtGui.QIcon(QtGui.QPixmap(IMG_PATH.format("btn_help"))))
        
        # signals
        self.wgSave.btnSave.clicked.connect(self.press_btnSave)
        self.wgSave.btnPublish.clicked.connect(self.press_btnPublish)
        self.wgSave.btnVersionUp.clicked.connect(self.press_btnVersionUp)
        self.wgSave.btnVersionDown.clicked.connect(self.press_btnVersionDown)

        self.wgSave.btnPreview.clicked.connect(self.press_btnPreview)
        self.wgSave.btnScreenshot.clicked.connect(self.press_btnScreenshot)
        self.wgSave.btnViewport.clicked.connect(self.press_btnViewport)

        self.wgSave.btnFolder.clicked.connect(self.press_btnFolder)
        self.wgSave.btnProject.clicked.connect(self.press_btnProject)
        self.wgSave.btnUser.clicked.connect(self.press_btnUser)
        self.wgSave.btnReport.clicked.connect(self.press_btnReport)
        self.wgSave.btnHelp.clicked.connect(self.press_btnHelp)

        # setup
        self.wgSave.edtFile.setText('mike_RIG_v001')
        self.wgSave.lblComments.setText('')
        self.set_open_folder(CURRENT_PATH)

        self.wgSave.show()


    # ************************************************************************************
    # PRESS
    # ************************************************************************************
    def press_btnSave(self):
        self.wgSave.lblComments.setText("Saving file")

    def press_btnPublish(self):
        self.wgSave.lblComments.setText('Publish')

    def press_btnVersionUp(self):
        self.wgSave.lblComments.setText('Version Up')

    def press_btnVersionDown(self):
        self.wgSave.lblComments.setText('Version Down')

    def press_btnFolder(self):
        webbrowser.open(self.open_path)

    def press_btnUser(self):
        webbrowser.open("https://www.alexanderrichtertd.com")

    def press_btnProject(self):
        webbrowser.open(self.open_path)

    def press_btnReport(self):
        webbrowser.open("https://github.com/alexanderrichtertd/plex/issues")

    def press_btnHelp(self, name=''):
        webbrowser.open("https://github.com/alexanderrichtertd/plex/wiki/arSave")


    # ************************************************************************************
    # menu
    # ************************************************************************************
    def press_btnPreview(self):
        if os.path.exists(self.preview_img_path):
            webbrowser.open(os.path.realpath(self.preview_img_path))

    def press_btnScreenshot(self):
        self.wgSave.lblComments.setText('Create Screenshot')
        screenshot_path = IMG_PATH.format('screenshot')
        QtGui.QPixmap.grabWindow(QtWidgets.QApplication.desktop().winId()).save(screenshot_path, screenshot_path.split(".")[-1])
        self.wgSave.btnPreview.setIcon(QtGui.QPixmap(screenshot_path))

    def press_btnViewport(self):
        self.wgSave.lblComments.setText('Create Render')

    # *********************************************************************
    # functions
    # *********************************************************************
    def set_open_folder(self, path=''):
        """ Sets the current folder path

        Args:
            path (str, optional): folder path
        """
        if len(path.split('.')) > 1:
            path = os.path.dirname(path)

        if os.path.exists(path):
            self.wgSave.btnFolder.setEnabled(True)
            self.open_path = os.path.normpath(path)
            self.wgSave.lblFolder.setText(self.open_path)
        else:
            self.wgSave.lblFolder.setText('')
            self.wgSave.btnFolder.setEnabled(False)


# ************************************************************************************
# START UI
# ************************************************************************************


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ar_save = ArSave()
    app.exec_()
