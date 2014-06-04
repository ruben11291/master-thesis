
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *
import cpuplotter
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName(_fromUtf8("TabWidget"))
        TabWidget.resize(600, 600)
        self.tab_pp = QtGui.QWidget()
        self.tab_orch = QtGui.QWidget()

        self.plot_pp=Qwt.QwtPlot()
        self.plot_orch=Qwt.QwtPlot()
        self.plotter_pp = cpuplotter.CpuPlot(self.plot_pp)
        self.plotter_orch = cpuplotter.CpuPlot(self.plot_orch)

        self.tab_orch.setObjectName(_fromUtf8("tab_orch"))
        self.tab_pp.setObjectName(_fromUtf8("tab_pp"))
        self.scrollArea = QtGui.QScrollArea(self.tab_orch)
        self.scrollArea2 = QtGui.QScrollArea(self.tab_pp)

        self.scrollArea.setGeometry(QtCore.QRect(10, 19, 501, 501))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollArea2.setGeometry(QtCore.QRect(10, 19, 521, 501))
        self.scrollArea2.setWidgetResizable(True)
        self.scrollArea2.setObjectName(_fromUtf8("scrollArea"))

   
        self.scrollArea.setWidget(self.plotter_pp)
        
        self.scrollArea2.setWidget(self.plotter_orch)

        TabWidget.addTab(self.tab_pp, _fromUtf8("Procesor Out"))
        TabWidget.addTab(self.tab_orch, _fromUtf8("Orchestrator Out"))

        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

   


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TabWidget = QtGui.QTabWidget()
    ui = Ui_TabWidget()
    ui.setupUi(TabWidget)
    TabWidget.show()
    sys.exit(app.exec_())

