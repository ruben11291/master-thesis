# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'column2.ui'
#
# Created: Tue Jun 17 11:09:43 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_column(object):
    def setupUi(self, column,width,height):
        column.setObjectName(_fromUtf8("column"))
        column.resize(668, 406)
        self.widget = QtGui.QWidget(column)
        self.widget.setGeometry(QtCore.QRect(10, 10, 593, 461))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.ComboBox = QtGui.QComboBox(self.widget)
        self.ComboBox.setGeometry(QtCore.QRect(10, 60, 182, 27))
        self.ComboBox.setObjectName(_fromUtf8("fontComboBox"))
        self.pushButton_2 = QtGui.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 170, 199, 51))
        self.pushButton_2.setText(_fromUtf8(""))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 230, 201, 51))
        self.pushButton_3.setText(_fromUtf8(""))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(20, 20, 108, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(10, 110, 201, 51))
        self.pushButton.setText(_fromUtf8(""))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_4 = QtGui.QPushButton(self.widget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 290, 201, 51))
        self.pushButton_4.setText(_fromUtf8(""))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(220, 110, 361, 331))
        self.label_2.setMinimumSize(QtCore.QSize(361, 331))
        self.label_2.setMaximumSize(QtCore.QSize(361, 331))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("resources/Logo.png")))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(396, 30, 187, 92))
        self.label_3.setMinimumSize(QtCore.QSize(187, 92))
        self.label_3.setMaximumSize(QtCore.QSize(187, 92))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8("resources/logo-deimos.png")))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(column)
        QtCore.QMetaObject.connectSlotsByName(column)

    def retranslateUi(self, column):
        column.setWindowTitle(QtGui.QApplication.translate("column", "WizardPage", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("column", "Stop Scenario", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("column", "Clean logs and hits", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("column", "Select Scenario:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("column", "Start Scenario", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("column", "About GeoCloud", None, QtGui.QApplication.UnicodeUTF8))
        ##Adding scenarios
        #self.ComboBox.insertItem(0,"")
        self.ComboBox.insertItem(0,"Scenario1 \'Emergencies Lorca Earthquake\'")
        self.ComboBox.insertItem(1,"Scenario2 \'Infrastructure monitoring\'")
        self.ComboBox.insertItem(2,"Scenario3 \'South West England\'")
        self.ComboBox.insertItem(3,"Scenario4 \'Precision Agriculture Argentina\'")
        self.ComboBox.insertItem(4,"Scenario5 \'Basemap Worlwide\'")

    def set_handler_about(self,handler):
        self.pushButton_4.clicked.connect(handler)

    def set_handler_start(self,handler):
        self.pushButton.clicked.connect(handler)

    def set_handler_stop(self,handler):
        self.pushButton_2.clicked.connect(handler)
    
    def set_handler_clean(self,handler):
        self.pushButton_3.clicked.connect(handler)
    
    def getScenario(self):
        return  self.ComboBox.currentIndex()

if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    column = QtGui.QWizardPage()
    ui = Ui_column()
    ui.setupUi(column)
    column.show()
    sys.exit(app.exec_())
