# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ScrollArea(object):
    def setupUi(self, ScrollArea):
        ScrollArea.setObjectName(_fromUtf8("ScrollArea"))
        ScrollArea.resize(400, 300)
        ScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 398, 298))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        ScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(ScrollArea)
        QtCore.QMetaObject.connectSlotsByName(ScrollArea)

    def retranslateUi(self, ScrollArea):
        ScrollArea.setWindowTitle(QtGui.QApplication.translate("ScrollArea", "ScrollArea", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ScrollArea", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setStyleSheet('color: darkblue')
        self.label.setText("")
    def append_text(self,text):
        self.label.setText(self.label.text()+"\n"+text)
    
    def clean_text(self):
        self.label.clear()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ScrollArea = QtGui.QScrollArea()
    ui = Ui_ScrollArea()
    ui.setupUi(ScrollArea)
    ScrollArea.show()
    sys.exit(app.exec_())

