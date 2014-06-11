
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

        self.init_timers(self.logs_sem, self.loads_sem)

        #self.semaphore = threading.Semaphore(-len(self.satellites))


    def init_timers(self,logs_sem,loads_sem):
         self.timer_pp_log= QtCore.QTimer(self,logs_sem)
         self.timer_pp_log.setInterval(3000)
         self.timer_pp_log.timeout.connect(self.update_log)
         
         self.timer_orch_log =QtCore.QTimer(self,logs_sem)
         self.timer_orch_log.setInterval(3000)
         self.timer_orch_log.timeout.connect(self.update_log)
         
         self.timer_pp_load= QtCore.QTimer(self,loads_sem)
         self.timer_pp_load.setInterval(3000)
         self.timer_pp_load.timeout.connect(self.update_load)
         
         self.timer_orch_load =QtCore.QTimer(self,loads_sem)
         self.timer_orch_load.setInterval(3000)
         self.timer_orch_load.timeout.connect(self.update_load)

         
    def logs_sem(self):
        
    def start_satellites(self):
        self.sat_threads=[]
        num = 1
        for sat in self.satellites:
            order = "'python satellite.py %s %s `cat ipdb`'"%(num, self.getScenario())
            t=SSH_order_thread(sat,self,"Satellite",num,order,self.threadLog)
            self.sat_threads.append(t)
            num+=1
        for sat in self.sat_threads:
            sat.start()
            self.log("Satellite %d started!"%(sat.getId()))
       
        self.log("Satellites started!")
            
    def start_ground(self):
        self.gs_threads=[]
        num = 0
        pdb.set_trace()
        for gs in self.groundstations:
            order = "'python groundstation.py %s %s `cat ipdb` &'"%(num,self.getScenario())
            t=SSH_order_thread(gs,self,"Ground Station",num,order,self.threadLog)
            self.gs_threads.append(t)
            num+=1
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
            os.system("ssh -A -i /home/deimos/.ssh/id_rsa jbecedas@%s"%(sat) + " -oPort=22 -oProxyCommand='ssh -e none -i /home/deimos/Descargas/emulabcert.pem -oPort=22 jbecedas@bastion.test.iminds.be nc -w 5 %h %p' 'killall python'")
        self.log("Cleaned Satellites")
        for gs in self.groundstations:
            os.system("ssh -A -i /home/deimos/.ssh/id_rsa jbecedas@%s"%(gs) + " -oPort=22 -oProxyCommand='ssh -e none -i /home/deimos/Descargas/emulabcert.pem -oPort=22 jbecedas@bastion.test.iminds.be nc -w 5 %h %p' 'killall python'")
        self.log("Cleaned Ground Stations")
            
    def setScenario(self,scenario):
        self.scenario = scenario

    def getScenario(self):
        if self.scenario:
            return self.scenario
        else:
            return None

    def log(self,msg):
        if self.widget:
            self.widget.log(msg)

    def error(self,thread):
        if thread.isAlive():
            thread._Thread__stop()
        if self.widget:
            raise DeployingException()

    def run(self,scenario):
        self.setScenario(scenario)
        self.start_ground(scenario)
        time.sleep(5.0)
        self.start_satellites(scenario)
        if self.widget:
            self.widget.scenarioInitiated()
  
       

if __name__ == "__main__":
    e = ExperimentController()
    e.setScenario(1)
    e.start_ground()
    print "STOPP"
    e.start_satellite()
    e.clean()
