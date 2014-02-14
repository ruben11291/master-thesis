 #!/usr/bin/env python

import threading
import pdb
from processingChain import processingChainController

class Iorchestator:
    def setImage(self,img):
        pass
    

class orchestator(Iorchestator):

    def __init__(self):
        print " asdf"

    def processRawData(self,img):
        controller = processingChainController.get()
        controller.createProcessingChain(img)
        
    def processedRawData(fileOutput):
        #eviar a base de datos si se quiere
        pass

    def sendToCatalog(self):
        pass

    def sendToStore(self):
        pass

    

    
