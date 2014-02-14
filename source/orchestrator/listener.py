 #!/usr/bin/env python
import orchestator
from orchestator import *
from ftplib import FTP, error_reply,error_temp,error_proto,all_errors
import threading
import pdb
# ftp = FTP('localhost')
# ftp.login('deimos','deimos')

lock = threading.Lock()


# TODO: 
# Hacer metodo para enviar a memoria compartida para la nube
# Avisar al controlador


class listener:
    
    ftpconex =[]
    gstations=[]
    downloading = []
    

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
        pdb.set_trace()
        while True:
            try:
                for i in self.ftpconex:
                    if(self.ifdata(i)):
                        #print "DATA"
                        lock.acquire()
                        self.downloading.append(i)
                        self.ftpconex.remove(i)
                        lock.release()
                       # print len(self.ftpconex),len(self.downloading)
                        t = downloadThread(self.data[0],i,self.orchestator,self.ftpconex,self.downloading);
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

        def proccesingLines(lines):
            for line in lines:
                name = line.split(' ')[-1]
                if(name[0] == 'W'):
                    self.data.append(name)
        try:
           # ftp.dir(proccesingLine)
            names = ftp.nlst()
            proccesingLines(names)
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
    def __init__(self, filename, ftp,orchestra,ftpconex,downloading):
        threading.Thread.__init__(self)
        self.filename = filename
        self.ftp = ftp
        self.orchestrator = orchestra
        self.ftpconex = ftpconex
        self.downloading = downloading

    def run(self):
        self.downloadFile()
        print "run hilo download"
       
    def downloadFile(self):
        try:
            print len(self.ftpconex), len(self.downloading)
            self.ftp.voidcmd('TYPE I')
            sock = self.ftp.transfercmd('RETR ' + self.filename)
            f = open("/home/deimos/test", 'wb')
            while True:
                block = sock.recv(1024*1024)
                if not block:
                    break
                self.ftp.voidcmd('NOOP')
                f.write(block)
            sock.close()
            lock.acquire(True)
            self.ftpconex.append(self.ftp)
            self.downloading.remove(self.ftp)
            lock.release()
            print len(self.ftpconex), len(self.downloading)
            #self.orchestrator.processRawData("/home/deimos/test")
            o = self.orchestrator
            o.processRawData("/home/deimos/test")
        except Exception as e :
            print "Unexpected error" ,e


    # def downloadFile(self):
    #     try:
    #         f = open("/home/deimos/des","wb")
    #         self.ftp.retrbinary('RETR %s' % self.file,f.write)
    #         f.close()
    #         self.lock.adquire()
    #         self.ftpconex.append(self.ftp)
    #         self.downloading.remove(self.ftp)
    #         self.lock.release()
    #     except:
    #         print "Unexpedted error"
            
