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
        self.wgSave = QtCompat.loadUI(path_ui)

        self.wgSave.show()


# ************************************************************************************
# START UI
# ************************************************************************************
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ar_save = ArSave()
    app.exec_()
