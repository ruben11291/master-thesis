 #!/usr/bin/env python

import threading
import pdb
from processingChain import processingChainController
from AyC import catalog

class Iorchestator:
    def setImage(self,img):
        None
    

class orchestator(Iorchestator):

    def __init__(self):
        print "[Orchestrator] Creating orchestrator!"
        controller = processingChainController.get()
        controller.setOrchestrator(self)
        self.catalog = catalog.catalog("http://localhost:8080/geoserver/rest")
        print "[Orchestrator] Initializing geoserver client"
        self.i = 0
        print "[Orchestrator] Initializing processing chaing controller!"

    def processRawData(self,img):
        print "[Orchestrator] Creating processing chain!"
        controller = processingChainController.get()
        controller.createProcessingChain(img)
        
    def processedRawData(self,fileOutput):
        #eviar a espacio compartido y donde tiene el working directory geoserver
        print "[Orchestrator] Processed raw data!"
        self.sendToCatalog(fileOutput)

    def sendToCatalog(self, data):
        self.i = self.i +1
        wksp = None
       # pdb.set_trace()
        while True:
            try:
                wksp = self.catalog.createWkspace("Escen"+str(self.i))
                break
            except Exception:
                self.i = self.i+1
        print data
        self.catalog.addImage(str(self.i),wksp,data)
        

    def sendToStore(self):
        None

    

    
