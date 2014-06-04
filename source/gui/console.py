import  sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class embterminal(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.process = QProcess(self)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self.process.start(
                'xterm',['-into',str(self.terminal.winId())])
	    # Works also with urxvt:
        #self.process.start(
                #'urxvt',['-embed', str(self.terminal.winId())])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = embterminal()
    main.show()
    sys.exit(app.exec_())
