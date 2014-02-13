 #!/usr/bin/env python
import orchestator
from ftplib import FTP

# ftp = FTP('localhost')
# ftp.login('deimos','deimos')


class listener:
    
    ftpconex =[]
    gstations=[]
    
    def connect(self):
        for i in range(len(self.gstations)):
           #ftpconex[i] = FTP(i[0],i[1])
            self.ftpconex.append(FTP(self.gstations[i][0]))

    def pooling(self):
        self.orchestator.setImage("imagen1")

    def __init__(self, orchesta):
        self.orchestator = orchesta;
        for i in range(12):
            self.gstations.append(["localhost",2000+i])
       
        self.connect()
        print "Listener ready"
