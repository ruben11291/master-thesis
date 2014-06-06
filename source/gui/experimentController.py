import os
import sys
import threading
from jfedProcXml import JFedParser

threadLock = threading.Lock()

class ExperimentController():
    
    def __init__(self,widget=None):
        self.threadLog = threading.Lock()
        self.widget = widget
        parser = JFedParser("resources/jfed.out")
        self.satellites = parser.get_satellites()
        self.groundstations = parser.get_groundStations()

    def start_satellites(self):
        self.sat_threads=List()
        num = 1
        for sat in self.satellites:
            t=SSH_order_thread(sat,self,"Satellite",num)
            self.sat_threads.append(t)
        for sat in self.sat_threads:
            sat.start()
            self.log("Satellite %d started!"%(sat.getId()))
        
        self.log("Satellites started!")
            
    def start_ground(self):
        self.gs_threads=List()
        num = 0
        for gs in self.groundstations:
            t=SSH_order_thread(gs,self,"Ground Station",num)
            self.gs_threads.append(t)
        for gs in self.gs_threads:
            gs.start()
            self.log("Ground Station %d started!"%(gs.getId()))
        self.log("Ground Stations started!")  

    def stop_ground(self):
        for gs in self.gs_threads:
            if gs.isAlive():
                gs.stop()
            self.gs_threads.remove(gs)
            self.log("Ground Station %d stopped!"%(gs.getId()))
   
    def clean_ground(self):
        for sat in self.satellites:
            os.system("ssh -A -i /home/deimos/.ssh/id_rsa jbecedas@%s"%(sat) + " -oPort=22 -oProxyCommand='ssh -e none -i /home/deimos/Descargas/emulabcert.pem -oPort=22 jbecedas@bastion.test.iminds.be nc -w 5 %h %p' 'ls -al'")
        self.log("Cleaned Satellites")
        for gs in self.groundstations:
            os.system("ssh -A -i /home/deimos/.ssh/id_rsa jbecedas@%s"%(gs) + " -oPort=22 -oProxyCommand='ssh -e none -i /home/deimos/Descargas/emulabcert.pem -oPort=22 jbecedas@bastion.test.iminds.be nc -w 5 %h %p' 'ls -al'")
        self.log("Cleaned Ground Stations")
            
    def log(self,msg):
        if self.widget:
            self.threadLog.acquire()
            self.widget.log(msg)
            self.threadLog.release()

class SSH_order_thread(threading.Thread):
    def __init__(self,host,experimentController,msg,id):
        self.host = host
        self.experimentController = experimentController;
        self.msg = msg
        self.id = id
    
    def getHost(self):
        return self.host
    def getId(self):
        return self.id

    def run(self):
        os.command("ssh -A -i /home/deimos/.ssh/id_rsa jbecedas@n144-09a.wall1.ilabt.iminds.be -oPort=22 -oProxyCommand='ssh -e none -i /home/deimos/Descargas/emulabcert.pem -oPort=22 jbecedas@bastion.test.iminds.be nc -w 5 %h %p' 'ls -al'")
        threadLock.acquire()
        self.experimentController.log(self.msg +" "+self.id+ " ha acabado su ejecucion")
        threadLock.release()

if __name__ == "__main__":
    e = ExperimentController()
    a = "ssh -A -i /home/deimos/.ssh/id_rsa jbecedas@%s" %("hostmachine")+ " -oPort=22 -oProxyCommand='ssh -e none -i /home/deimos/Descargas/emulabcert.pem -oPort=22 jbecedas@bastion.test.iminds.be nc -w 5 %h %p' 'ls -al'"
    print a
    e.clean_ground()
