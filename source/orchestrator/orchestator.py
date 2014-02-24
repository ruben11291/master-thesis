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
        #eviar a base de datos si se quiere
        print "[Orchestrator] Processed raw data!"
        self.sendToCatalog(fileOutput)

    def sendToCatalog(self, data):
        self.i = self.i +1
        wksp = self.catalog.createWkspace("Escen"+str(self.i))
        self.catalog.addImage(str(self.i),data,wksp)
        

    def sendToStore(self):
        None

    

    
