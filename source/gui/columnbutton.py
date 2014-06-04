# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'column.ui'
#
# Created: Wed Jun  4 16:38:52 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_column(object):
    def setupUi(self, column):
        column.setObjectName(_fromUtf8("column"))
        column.resize(227, 344)
        self.widget = QtGui.QWidget(column)
        self.widget.setGeometry(QtCore.QRect(10, 10, 211, 311))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.pushButton_2 = QtGui.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 170, 199, 61))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 240, 201, 51))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(20, 20, 108, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(10, 110, 201, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.comboBox = QtGui.QComboBox(self.widget)
        self.comboBox.setGeometry(QtCore.QRect(10, 60, 191, 27))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))

        self.retranslateUi(column)
        QtCore.QMetaObject.connectSlotsByName(column)

    def retranslateUi(self, column):
        column.setWindowTitle(QtGui.QApplication.translate("column", "WizardPage", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("column", "Cancel current experiment", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("column", "Clean logs and hits", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("column", "Select Scenario:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("column", "Start Scenario", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    column = QtGui.QWizardPage()
    ui = Ui_column()
    ui.setupUi(column)
    column.show()
    sys.exit(app.exec_())

