 #!/usr/bin/env python
from orchestator import *
from ftplib import FTP, error_reply,error_temp,error_proto,all_errors
import threading
import pdb
from datetime import *
from time import *
import MySQLdb as mdb


lock = threading.Lock()
tmp_path="/tmp/"

# TODO: 
# Hacer metodo para enviar a memoria compartida para la nube
# Modificar tiempo sleep para 1minuto




class listener:
    """This class is alwais pooling the ftp conections opened. When a connection have a new raw data, listener gets and 
send it to orchestrator"""

    ftpconex =[]
    gstations=[]
    downloading = []
    lastdata = {}
    

    def connect(self):
        self.counter = 0
        """Simply it connects listener to all ftp connections of ground stations"""
        for i in range(len(self.gstations)):
        #    pdb.set_trace()
           #ftpconex[i] = FTP(i[0],i[1])
            try:
                ftp = FTP(self.gstations[i][0])
                ftp.login(self.ftp_user,self.ftp_passwd)
                ftp.cwd(tmp_path)
                print ftp.pwd()
                self.ftpconex.append(ftp)
            except error_reply:
                print "[Listener] error_reply",e
            except error_temp:
                print "[Listener] error_temp",e
            except error_proto:
                print "[Listener] error_proto",e
            except all_errors:
                print "[Listener] all_errors",e

    def pooling(self):
        
        while True:
            try:
                for i in self.ftpconex:
                    if(self.ifdata(i)):
                        # #print "DATA"
                        # self.orchestator.processRawData("")
                        lock.acquire()
                        self.downloading.append(i)
                        self.ftpconex.remove(i)
                        lock.release()
                       # print len(self.ftpconex),len(self.downloading)
                        t = downloadThread(self.data[0],i,self.orchestator,self.ftpconex,self.downloading);
                        t.start()
            except error_reply:
                print "[Listener] error_reply"
            except error_temp:
                print "[Listener] error_temp"
            except error_proto:
                print "[Listener] error_proto"
            except all_errors:
                print "[Listener] all_errors"
                
  
        
    def ifdata(self,ftp):
        """Make a test for know if some ground station  have raw dat available"""
        self.data = []

        def needDownload(name,host):
            """
            needDownload
            Obtain if is necessary download raw data
            """
            sp = name.split('_')
            logic = False

            if len(sp) == 7:
                readwrite = sp[0]
                idGs = sp[1]
                sat = sp[2]
                scenario=sp[3]
                use = sp[4]
                hour = sp[5]
                date = sp[6]
                
                if readwrite == "W":
                    if host in self.lastdata:
                        if moreRecently(host,hour,date):
                            self.lastdata.update({host:[hour,date]})
                            logic = True
                
                    else:
                        self.lastdata.update({host:[hour,date]})
                        logic = True
            
            return logic
           


        def moreRecently(host, hour, date):
            try:
                """Compare two dates for get if the new date is more newer"""
                olddate = self.lastdata[host][1].split('-')
                oldhour = self.lastdata[host][0].split(':')
                olddatetime = datetime(int(olddate[2]),int(olddate[1]),int(olddate[0]),int(oldhour[0]),int(oldhour[1]),int(oldhour[2]))
                
                date = date.split('-')
                hour = hour.split(':')

                newdatetime = datetime(int(date[2]),int(date[1]),int(date[0]),int(hour[0]),int(hour[1]),int(hour[2]))
                return newdatetime > olddatetime
            except Exception as e:
                print "[Listener] Unexpected Exception" ,e 
                return False

        def proccesingLines(lines,host):
            
            """For each line of ftp.nlst looks if the file needs to download"""
            for line in lines:
                #name = line.split(' ')[-1]
                if(needDownload(line[len(tmp_path):],host)):
                       self.data.append(line)
        try:
           # ftp.dir(proccesingLine)
            names = None
            try:
                sleep(1)
       #         print ftp
                #pdb.set_trace()
                names = ftp.nlst(tmp_path)
      #          print names
                self.counter = self.counter + 1
            except Exception as e:
                print e
                print self.counter
                self.counter = 0
            #pdb.set_trace()
            if names != None:
                proccesingLines(names,ftp.host)
                if(len(self.data) == 0):
                    return False
                return True
            else:
                return False
        except Exception as e:
            print "[Listener] Unexpected Error ",e 
                

  

    def __init__(self, orchesta, ftp_user, ftp_passwd, ground_stations_address):
        self.ftp_user = ftp_user
        self.ftp_passwd = ftp_passwd
        
        pdb.set_trace()
        self.orchestator = orchesta;     

        for i in range(12):
            #self.gstations.append(["localhost",2000+i])
            self.gstations.append(ground_stations_address[i])

        self.connect()
        print "[Listener] Listener ready!"



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
        print "[Listener] Creating download thread!"
        self.downloadFile()
       
    # def downloadFile(self):
    #     try:
    #        # print len(self.ftpconex), len(self.downloading)
    #         print "[Listener] Downloading raw data!"
    #         self.ftp.voidcmd('TYPE I')
    #         sock = self.ftp.transfercmd('RETR ' + self.filename)
    #         f = open("/home/deimos/test", 'wb')
    #         while True:
    #             block = sock.recv(1024*1024)
    #             if not block:
    #                 break
    #             self.ftp.voidcmd('NOOP')
    #             f.write(block)
    #         sock.close()
    #         lock.acquire(True)
    #         self.ftpconex.append(self.ftp)
    #         self.downloading.remove(self.ftp)
    #         lock.release()
    #         print len(self.ftpconex), len(self.downloading)
    #         print "[Listener] Sending raw data to orchestrator!"
    #         self.orchestrator.processRawData("/home/deimos/test")
    #     except Exception as e :
    #         print "[Listener] Unexpected error asd" ,e

    def downloadFile(self):
        try:
            f = open(tmp_path+self.filename,"wb")
            self.ftp.retrbinary('RETR '+self.filename, f.write)
            lock.acquire(True)
            self.ftpconex.append(self.ftp)
            self.downloading.remove(self.ftp)
            lock.release()
            self.orchestrator.processRawData(tmp_path+self.filename)
        except Exception as e:

            print "[Listener] Unexpected exception ",e
        

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
            
