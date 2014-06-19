from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Video(object):
    def setupUi(self,Widget,width,height):
        Widget.setObjectName(_fromUtf8("VideoWidget"))
        Widget.resize(width,height)
        
        self.media = Phonon.MediaObject(Widget)
        #self.media.stateChanged.connect(self.__handleStateChanged)
        
        self.video = Phonon.VideoWidget(Widget)
        self.video.setMaximumSize(width, height)
        self.video.setMinimumSize(width, height)
        self.video.setAspectRatio(Phonon.VideoWidget.AspectRatioWidget)
	self.audio = Phonon.AudioOutput(Phonon.VideoCategory, Widget)
        Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.video)
    
    def start_reproduction(self,filename):
        if filename:
            self.media.setCurrentSource(Phonon.MediaSource(filename))
            self.media.play()

    def stop_reproduction(self):
        if self.media.state() == Phonon.PlaynigState:
            self.media.stop()

    def change_source(self,filename):
        self.stop_reproduction(filename)
        self.start_reproduction(filename)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('GeoCloud GUI')

    video_widget = QtGui.QWidget()
    ph = Ui_Video()
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    ph.setupUi(video_widget,width,height)
    
    video_widget.resize(width,height)

    video_widget.show()
    sys.exit(app.exec_())

