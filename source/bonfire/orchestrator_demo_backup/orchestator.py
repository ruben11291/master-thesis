 #!/usr/bin/env python


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



import threading
import pdb
from processingChain import processingChainController
#from AyC import catalog
import MySQLdb as mdb
import threading
from collections import deque

class Iorchestator:
    def setImage(self,img):
        None
    

class orchestator(Iorchestator):

    def __init__(self, service_ip):
       
        self._service_pp = service_ip
        print "[Orchestrator] Creating orchestrator!"
        controller = processingChainController.get()
        controller.setOrchestrator(self)
        self.ocupated = False
        self.sem = threading.Lock()
        self.images_to_process=deque()
        #self.catalog = catalog.catalog(self._geoserver_path)
        print "[Orchestrator] Initializing geoserver client"
        self.i = 0
        print "[Orchestrator] Initializing processing chaing controller!"

    def getPP(self):
        if self._service_pp is not None:
            return self._service_pp
        else:
            print "Error with reference"

    def processRawData(self,img):
        self.sem.acquire()
        if not self.ocupated:
            self.ocupated=True
            self.images_to_process.append(img)
            print "[Orchestrator] Creating processing chain!"
            controller = processingChainController.get()
            controller.createProcessingChain(self.images_to_process[0])
        else:
            self.images_to_process.append(img)
        self.sem.release()
        
    def processedRawData(self,fileOutput):
        #eviar a espacio compartido y donde tiene el working directory geoserver
        print "[Orchestrator] Processed raw data! ",fileOutput
        self.sem.acquire()
        self.images_to_process.popleft()
        if len(self.images_to_process) == 0:
            self.ocupated =False
        else:
            print "[Orchestrator] Creating processing chain!"
            controller = processingChainController.get()
            controller.createProcessingChain(self.images_to_process[0])
        self.sem.release()
        
        #self.sendToCatalog(fileOutput)

    # def sendToCatalog(self, data):
    #     self.i = self.i +1
    #     wksp = None
    #    # pdb.set_trace()
    #     while True:
    #         try:
    #             wksp = self.catalog.createWkspace("Escen"+str(self.i))
    #             break
    #         except Exception:
    #             self.i = self.i+1
    #     print data
    #     self.catalog.addImage(str(self.i),wksp,data)
        

    def sendToStore(self):
        None
        
        

    
