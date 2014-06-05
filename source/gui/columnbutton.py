# -*- coding: utf-8 -*-



from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_column(object):
    def setupUi(self, column,width,height):
        column.setObjectName(_fromUtf8("column"))
        #column.resize(668, 406)
        column.resize(width/2,height/2)
        self.widget = QtGui.QWidget(column)
        self.widget.setGeometry(QtCore.QRect(10, 10, 330, 371))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.ComboBox = QtGui.QComboBox(self.widget)
        self.ComboBox.setGeometry(QtCore.QRect(10, 60, 310, 27))
        self.ComboBox.setObjectName(_fromUtf8("ComboBox"))
        self.pushButton_2 = QtGui.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 170, 199, 51))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 230, 201, 51))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(20, 20, 108, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(10, 110, 201, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_4 = QtGui.QPushButton(self.widget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 290, 201, 51))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.label_2 = QtGui.QLabel(column)
        self.label_2.setGeometry(QtCore.QRect(360, 60, 491, 431))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("resources/Logo.png")))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))

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
        self.ComboBox.insertItem(1,"Scenario1 \'Emergencies Lorca Earthquake\'")
        self.ComboBox.insertItem(2,"Scenario2 \'Infrastructure monitoring\'")
        self.ComboBox.insertItem(3,"Scenario3 \'South West England\'")
        self.ComboBox.insertItem(4,"Scenario4 \'Precision Agriculture Argentina\'")
        self.ComboBox.insertItem(5,"Scenario5 \'Basemap Worlwide\'")

    def set_handler_about(self,handler):
        self.pushButton_4.clicked.connect(handler)

    def set_handler_start(self,handler):
        self.pushButton.clicked.connect(handler)

    def set_handler_stop(self,handler):
        self.pushButton_2.clicked.connect(handler)
    
    def set_handler_clean(self,handler):
        self.pushButton_3.clicked.connect(handler)
    
    def get_scenario(self):
        return 

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    column = QtGui.QWizardPage()
    ui = Ui_column()
    ui.setupUi(column)
    column.show()
    sys.exit(app.exec_())

