# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Wed Jun  4 13:54:48 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(559, 433)
        Dialog.setMinimumSize(QtCore.QSize(559, 433))
        Dialog.setMaximumSize(QtCore.QSize(559, 433))
        Dialog.setBaseSize(QtCore.QSize(559, 433))
        Dialog.setAutoFillBackground(True)
        self.icon_1 = QtGui.QLabel(Dialog)
        self.icon_1.setGeometry(QtCore.QRect(40, 30, 201, 171))
        self.icon_1.setMaximumSize(QtCore.QSize(16777215, 281))
        self.icon_1.setText(_fromUtf8(""))
        self.icon_1.setPixmap(QtGui.QPixmap(_fromUtf8("resources/fed4fireico.png")))
        self.icon_1.setScaledContents(True)
        self.icon_1.setObjectName(_fromUtf8("icon_1"))
        self.icon_2 = QtGui.QLabel(Dialog)
        self.icon_2.setGeometry(QtCore.QRect(340, 30, 171, 121))
        self.icon_2.setText(_fromUtf8(""))
        self.icon_2.setPixmap(QtGui.QPixmap(_fromUtf8("resources/europeanico.jpg")))
        self.icon_2.setScaledContents(True)
        self.icon_2.setObjectName(_fromUtf8("icon_2"))
        self.info = QtGui.QLabel(Dialog)
        self.info.setGeometry(QtCore.QRect(40, 240, 461, 111))
        self.info.setObjectName(_fromUtf8("info"))
        self.info.setText(_fromUtf8("Developed by Rubén Pérez Pascual \nThis work was carried out with the support\nof the Fed4FIRE-project (\“Federation for FIRE\"),\nan Integrated project receiving funding from the\nEuropean Union’s Seventh Framework Programme for research, technological\n development and demonstration under grant agreement no 318389.\n It does not necessarily reflect the views of the European Commission.\nThe European Commission is not liable for any use that may be made of the information contained herein."))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(430, 380, 85, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(Dialog.close)

        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "About GeoCloud", None, QtGui.QApplication.UnicodeUTF8))
        QtCore.QMetaObject.connectSlotsByName(Dialog)

   

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

