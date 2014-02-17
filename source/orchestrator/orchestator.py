 #!/usr/bin/env python

import threading
import pdb
from processingChain import processingChainController

class Iorchestator:
    def setImage(self,img):
        None
    

class orchestator(Iorchestator):

    def __init__(self):
        print "[Orchestrator] Creating orchestrator!"
        controller = processingChainController.get()
        controller.setOrchestrator(self)
        print "[Orchestrator] Initializing processing chaing controller!"

    def processRawData(self,img):
        print "[Orchestrator] Creating processing chain!"
        controller = processingChainController.get()
        controller.createProcessingChain(img)
        
    def processedRawData(self,fileOutput):
        #eviar a base de datos si se quiere
        print "[Orchestrator] Processed raw data!"
      

    def sendToCatalog(self):
        None

    def sendToStore(self):
        None

    

    
