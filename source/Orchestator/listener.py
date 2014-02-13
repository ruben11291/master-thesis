 #!/usr/bin/env python
import orchestator
from orchestator import *
from ftplib import FTP
import threading

# ftp = FTP('localhost')
# ftp.login('deimos','deimos')


class listener:
    
    ftpconex =[]
    gstations=[]
    downloading = []
    lock = threading.Lock()

    def connect(self):
        for i in range(len(self.gstations)):
           #ftpconex[i] = FTP(i[0],i[1])
            try:
                ftp = FTP(self.gstations[i][0])
                ftp.login('deimos','deimos')
                self.ftpconex.append(ftp)
            except error_reply:
                print "error_reply"
            except error_temp:
                print "error_temp"
            except error_proto:
                print "error_proto"
            except all_errors:
                print "all_errors"

    def pooling(self):
        while true:
            try:
                for i in self.ftpconex:
                    if(i.size("rawdata")):
                        lock.acquire()
                        self.downloading.append(i)
                        lock.release()
                        t = downloadThread(filename,folder,i);
                        t.start()
            except error_reply:
                print "error_reply"
            except error_temp:
                print "error_temp"
            except error_proto:
                print "error_proto"
            except all_errors:
                print "all_errors"


  

    def __init__(self, orchesta):
        self.orchestator = orchesta;
        for i in range(12):
            self.gstations.append(["localhost",2000+i])
       
        self.connect()
        print "Listener ready"



#Class downloadThread
#Get the data from FTP connection

class downloadThread(threading.Thread):
    def __init__(self, filename,folder, ftp,listener):
        threading.Thread.__init__(self)
        self.filename = filename
        self.folder = folder
        self.ftp = ftp
        self.listener = listener

    def run(self):
        self.downloadFile(filename,folder,ftp)
        print "run hilo download"

    def downloadFile(self,filename, folder, ftp):
        try:
            ftp.voidcmd('TYPE I')
            sock = ftp.transfercmd('RETR ' + filename)
            f = open(folder + filename, 'wb')
            while True:
                block = sock.recv(1024*1024)
                if not block:
                    break
                ftp.voidcmd('NOOP')
                f.write(block)
            sock.close()
        except:
            print "Unexpedted error"
