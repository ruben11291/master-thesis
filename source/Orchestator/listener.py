 #!/usr/bin/env python
import orchestator
from orchestator import *
from ftplib import FTP, error_reply,error_temp,error_proto,all_errors
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
        while True:
            try:
                for i in self.ftpconex:
                    if(self.ifdata(i)):
                        print "DATA"
                        this.lock.acquire()
                        self.downloading.append(i)
                        this.lock.release()
                        t = downloadThread(this.data[0],i);
                        t.start()
            except error_reply:
                print "error_reply"
            except error_temp:
                print "error_temp"
            except error_proto:
                print "error_proto"
            except all_errors:
                print "all_errors"
                
  
        
    def ifdata(self,ftp):
        self.data = []

    #this function is executed ever than ftp.dir gets a line
        def proccesingLine(line):
            name = line.split(' ')[-1]
            if(name[0] == 'W'):
                this.data.append(name)
        try:
            ftp.dir(proccesingLine)
            if(len(self.data) == 0):
                return False
            return True
        except Exception as e:
            print "Unexpected Error",e 
                

  

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


