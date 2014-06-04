from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon

class Window(QtGui.QWidget):
    def __init__(self,width,height):

        QtGui.QWidget.__init__(self)
        self.media = Phonon.MediaObject(self)
        self.media.stateChanged.connect(self.handleStateChanged)

        self.video = Phonon.VideoWidget(self)
        self.video2 = Phonon.VideoWidget(self)
        self.video.setMinimumSize(width/3, height/3)
        self.video2.setMinimumSize(width/3, height/3)
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)
        Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.video)
        self.button = QtGui.QPushButton('Choose File', self)
        self.button.clicked.connect(self.handleButton)
        self.list = QtGui.QListWidget(self)
        self.list.addItems(Phonon.BackendCapabilities.availableMimeTypes())
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.video, 1,0)
        layout.addWidget(self.video2,2,0)
        layout.addWidget(self.button,1,1)
        layout.addWidget(self.list,2,1)

    def handleButton(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
        else:
            path = QtGui.QFileDialog.getOpenFileName(self, self.button.text())
            if path:
                self.media.setCurrentSource(Phonon.MediaSource(path))
                self.media.play()

    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.button.setText('Stop')
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.button.setText('Choose File')
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().fileName()
                print ('ERROR: could not play:', source.toLocal8Bit().data())
                print ('  %s' % self.media.errorString().toLocal8Bit().data())

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Phonon Player')
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    window = Window(width,height)
    window.show()
    sys.exit(app.exec_())
