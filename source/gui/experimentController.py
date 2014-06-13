
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


import os
import sys
import threading
from jfedProcXml import JFedParser
import pdb
from ssh_order import SSH_order_thread
import paramiko
from connections import VWConnection
import time

class ExperimentController():
    
    def __init__(self,widget=None):
        self.threadLog = threading.Lock()
        self.widget = widget
        parser = JFedParser("resources/jfed.out")
        self.satellites = parser.get_satellites()
        self.groundstations = parser.get_groundStations()
        self.satellites_finish= threading.Lock()
        self.condition_satellite=threading.Lock()
        self.logs_sem = threading.Lock()
        self.loads_sem = threading.Lock()

        
        #self.init_timers(self.logs_sem, self.loads_sem)

        #self.semaphore = threading.Semaphore(-len(self.satellites))
    def connect(self):
        self.ground_stations_connections = []
        self.satellites_connections=[]
        ground_id = 0
        satellite_id=1
        for ground in self.groundstations:
            self.ground_stations_connections.append(VWConnection(ground_id,ground,'jbecedas','/home/deimos/.ssh/id_rsa.pub','bastion.test.iminds.be','jbecedas',22,'/home/deimos/Descargas/emulabcert.pem'))
            ground_id +=1
        for sat in self.satellites:
            self.satellites_connections.append(VWConnection(satellite_id,sat,'jbecedas','/home/deimos/.ssh/id_rsa.pub','bastion.test.iminds.be','jbecedas',22,'/home/deimos/Descargas/emulabcert.pem'))
            satellite_id+=1
                

    def start_satellites(self):
        #self.sat_threads=[]
        for sat in self.satellites_connections:
            order = "python satellite.py %s %s `cat ipdb`"%(sat.getId(), self.getScenario())#TOCHANGE
            sat.execute(order)
            #t=SSH_order_thread(sat,self,"Satellite",num,order,self.threadLog)
            #self.sat_threads.append(t)
        # for sat in self.sat_threads:
        #     sat.start()
            self.log("Satellite %d started!"%(sat.getId()))
       
        self.log("Satellites started!")
            
    def start_ground(self):
       # pdb.set_trace()
        for gs in self.ground_stations_connections:
            order = "python groundstation.py %s %s `cat ipdb` &"%(gs.getId(),self.getScenario())
            gs.execute(order)
            #t=SSH_order_thread(gs,self,"Ground Station",num,order,self.threadLog)
            #self.gs_threads.append(t)
        # for gs in self.gs_threads:
        #     gs.start()
            self.log("Ground Station %d started!"%(gs.getId()))
        self.log("Ground Stations started!")  

    def stop_ground(self):
        for gs in self.ground_stations_connections:
            gs.stop()
            self.log("Ground Station %d stopped!"%(gs.getId()))
            
    def stop_sat(self):
        for sat in self.satellites_connections:
            sat.stop()
            self.log("Satellite %d stopped!"%(sat.getId()))
   
    def clean_sat(self):
        command="killall python"
        for sat in self.satellites_connections:
            sat.execute(command)
        self.log("Cleaned Satellites")

    def clean_ground(self):
        # for sat in self.satellites:
        #     os.system("ssh -A -i /home/deimos/.ssh/id_rsa jbecedas@%s"%(sat) + " -oPort=22 -oProxyCommand='ssh -e none -i /home/deimos/Descargas/emulabcert.pem -oPort=22 jbecedas@bastion.test.iminds.be nc -w 5 %h %p' 'killall python'")
        command="killall python"
        for gs in self.ground_stations_connections:
            gs.execute(command)
        self.log("Cleaned Ground Stations")
            
    def setScenario(self,scenario):
        self.scenario = scenario

    def getScenario(self):
        if self.scenario:
            return self.scenario
        

    def log(self,msg):
        print msg
        if self.widget:
            self.widget.log(msg)

    def error(self,thread):
        if thread.isAlive():
            thread._Thread__stop()
        if self.widget:
            raise DeployingException()

    def startScenario(self,scenario):
        print "Starting scenario %d"%(int(scenario))
        self.setScenario(scenario)
        self.start_ground()
        time.sleep(5.0)
        self.start_satellites()
        if self.widget:
            self.widget.scenarioInitiated()
  
    def stopScenario(self):
        self.clean_ground()
        self.clean_sat()

if __name__ == "__main__":
    e = ExperimentController()
    e.setScenario(1)
    print "Connecting.."
    e.connect()
    print "connected"
    #e.start_ground()
    print "Ground Started"
    time.sleep(5.0)
    e.start_satellites()
    print "Satellites started"
    while(True):
        None
    #e.clean()
    #e.clean_ground()
