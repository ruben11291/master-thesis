from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
from dialog import Ui_Dialog
from tabwidget import Ui_TabWidget
from columnbutton import Ui_column
from video_widget import Ui_Video
from scrollarea import Ui_ScrollArea
import pdb
class Window(QtGui.QWidget):
    def __init__(self,width,height):
       # pdb.set_trace()
        QtGui.QWidget.__init__(self)
        #Dialog component
        self.dialog = QtGui.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.dialog)
        
        #Tab widget
        self.tabWidget=QtGui.QTabWidget()
        self.tab= Ui_TabWidget()
        self.tab.setupUi(self.tabWidget,width/2,height/2)
        
        #Column widget
        self.column = QtGui.QWidget()
        self.col = Ui_column()
        self.col.setupUi(self.column,width,height)
        
        self.video_widget = Phonon.VideoWidget()
        self.video = Ui_Video()
        self.video.setupUi(self.video_widget,width/2,height/2)

        #List Widget
        # self.list = QtGui.QListWidget(self)
        # self.list.setMaximumSize(width/2,height/2)
        # #self.list.hide()
        #Log Widget
        
        self.scrollArea = QtGui.QScrollArea()
        self.scroll=Ui_ScrollArea()
        self.scroll.setupUi(self.scrollArea)
        # self.listView = QtGui.Qlabel(self)
        # self.listView.setObjectName("listView")

        #Connecting Handlers
        self.col.set_handler_about(self.__show_about_handle)
        self.col.set_handler_start(self.__start_scenario)
        self.col.set_handler_stop(self.__stop_scenario)
        self.col.set_handler_clean(self.__clean_logs)


        #Including in the grid
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.video_widget, 0,0)
        layout.addWidget(self.scrollArea,1,2)
        layout.addWidget(self.tabWidget,1,0)
        layout.addWidget(self.column,0,2)

    # def __handleButton(self):
    #     if self.media.state() == Phonon.PlayingState:
    #         self.media.stop()
    #     else:
    #         path = QtGui.QFileDialog.getOpenFileName(self, self.button.text())
    #         if path:
    #             self.media.setCurrentSource(Phonon.MediaSource(path))
    #             self.media.play()
    #     self.dialog.show()
    def __start_scenario(self):
        self.video.start_reproduction("/home/Data/Demo_Scenario1_2D_T_World.wmv")
    def __stop_scenario(self):
        None
    def __clean_logs(self):
        None
    def __show_about_handle(self):
        self.dialog.show()

    # def __handleStateChanged(self, newstate, oldstate):
    #     if newstate == Phonon.PlayingState:
    #         self.button.setText('Stop')
    #     elif (newstate != Phonon.LoadingState and
    #           newstate != Phonon.BufferingState):
    #         self.button.setText('Choose File')
    #         if newstate == Phonon.ErrorState:
    #             source = self.media.currentSource().fileName()
    #             print ('ERROR: could not play:', source.toLocal8Bit().data())
    #             print ('  %s' % self.media.errorString().toLocal8Bit().data())

    # def add_new_hit(self,hit):
    #     self.list.addItems(hit)



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
