#!/usr/bin/env python

#
#    Copyright (C) 2014 DEIMOS
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Ruben Perez <ruben.perez@deimos-space.com>

from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
from dialog import Ui_Dialog
from tabwidget import Ui_TabWidget
from columnbutton import Ui_column
from video_widget import Ui_Video
from scrollarea import Ui_ScrollArea
from experimentController import ExperimentController
import paramiko
import socket

import pdb
class Window(QtGui.QWidget):
    def __init__(self,width,height,host_orch,host_pp):
       # pdb.set_trace()
        QtGui.QWidget.__init__(self)
        #Dialog component
        self.dialog = QtGui.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.dialog)
        
        #Tab widget
        self.tabWidget=QtGui.QTabWidget()
        self.tab= Ui_TabWidget()
        self.tab.setupUi(self.tabWidget,width/2,height/2,host_orch,host_pp)
        
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
        try:
            self.__clean_logs()
            scenario = self.col.getScenario()
            self.controller.startScenario(scenario+1)
        except Exception as e:
            self.__show_exception(e)

        self.video.start_reproduction("/home/Data/Demo_Scenario1_2D_T_World.wmv")

    def __stop_scenario(self):
        self.controller.stopScenario()
        
    def __clean_logs(self):
        self.scroll.clean_text()
        
    def __show_about_handle(self):
        self.dialog.show()
    
    def __show_exception(self,exception):
        print "EXCEPTION ",exception
        #TODO
    
    def scenarioInitiated(self):
        print "SHOW WINDOW SCENARIO INITIATED"

    def setController(self,controller):
        self.controller = controller
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

    def log(self,msg):
        self.scroll.append_text(msg)

    def stop(self):
        None
        #TODO


if __name__ == '__main__':

    import sys
    host_orch="172.18.240.210"
    host_pp="172.18.240.209"
    
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('GeoCloud GUI')
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    window = Window(width,height,host_orch,host_pp)
    window.resize(width,height)
    controller = ExperimentController(window)
    try:
        print "Connecting..."
        controller.connect()
        print "Connected!"
    except (paramiko.SSHException, socket.error) as se:
        window.__show_exeption(se)
        window.stop()
        exit(-1)
    window.setController(controller)
    window.show()
    sys.exit(app.exec_())
