from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
from dialog import Ui_Dialog
from tabwidget import Ui_TabWidget



class Window(QtGui.QWidget):
    def __init__(self,width,height):

        QtGui.QWidget.__init__(self)
        #Dialog component
        self.dialog = QtGui.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.dialog)
        
        #Tab widget
        self.tabWidget=QtGui.QTabWidget()
        self.tab= Ui_TabWidget()
        self.tab.setupUi(self.tabWidget)
        
        # self.palette=QtGui.QPalette()
        # self.palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap("/home/deimos/earth.jpg")))
        # #self.palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.red))
        # self.setPalette(self.palette)
        # self.setAutoFillBackground(True)
        self.media = Phonon.MediaObject(self)
        self.media.stateChanged.connect(self.__handleStateChanged)

        self.video = Phonon.VideoWidget(self)
        self.video.setMaximumSize(width/2, height/2)
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)
        Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.video)
        
        
        self.button = QtGui.QPushButton('STOP', self)
        self.button.clicked.connect(self.__handleButton)
       # self.button.hide()

        self.start_button = QtGui.QPushButton("Start scenario",self)
        self.start_button.clicked.connect(self.__start_scenario_handle)
        

        self.list = QtGui.QListWidget(self)
        self.list.setMaximumSize(width/2,height/2)
        #self.list.hide()
      
        self.listView = QtGui.QListView(self)
        self.listView.setObjectName("listView")
        #self.listView.hide()

        

        # self.tabWidget = QtGui.QTabWidget(self)
        # #self.tabWidget.setGeometry(QtCore.QRect(810, 0, 251, 441))
        # self.tabWidget.setObjectName("tabWidget")
        # #self.tabWidget.setName("TABIW")
        # self.tab_orch = QtGui.QWidget()
        # self.tab_pp = QtGui.QWidget()
        # self.addWidget(self.plotter)

        # self.tab_orch.setObjectName("tab_orch")
        
        # self.tabWidget.addTab(self.tab_orch,"Orchestrator")
        # self.tab_pp.setObjectName("tab_pp")
        # self.tabWidget.addTab(self.tab_pp, "Chain Processor")



        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.video, 0,0)
        layout.addWidget(self.button,2,2)
        layout.addWidget(self.list,1,2)
        layout.addWidget(self.listView,0,2)
        layout.addWidget(self.tabWidget,1,0)
        #layout.addWidget(self.start_button,2,2)

    def __handleButton(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
        else:
            path = QtGui.QFileDialog.getOpenFileName(self, self.button.text())
            if path:
                self.media.setCurrentSource(Phonon.MediaSource(path))
                self.media.play()
        self.dialog.show()

    def __start_scenario_handle(self):
        self.dialog.show()

    def __handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.button.setText('Stop')
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.button.setText('Choose File')
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().fileName()
                print ('ERROR: could not play:', source.toLocal8Bit().data())
                print ('  %s' % self.media.errorString().toLocal8Bit().data())

    def add_new_hit(self,hit):
        self.list.addItems(hit)



if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('GeoCloud GUI')
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    window = Window(width,height)
    window.resize(width,height)
    window.show()
    sys.exit(app.exec_())
