#!/usr/bin/env python

from jobOrder import jobOrder
import threading
from orchestator import *

class processingChainController:
    _controller = None

    # def __new__(cls,*args,**kwargs):
    #     if not cls._instance:
    #         cls._instance = super(Singleton,cls).__new__(cls,*args,**kwargs)
    #     return cls._instance

    @classmethod
    def get(cls):
        if ( cls._controller == None ):
            cls._controller = processingChainController()
        return cls._controller

    def __init__(self):
        self.actives = {}
        self.petitions = {}
        self.maxPetitions = 100
        if self._controller is not None:
            raise ValueError("[ProcessingChainController] An instantiation already exists")

    def setOrchestrator(self,orchestrator):
        self.orchestrator = orchestrator

    def createProcessingChain(self,pathRawData):
        pc = processingChain(pathRawData)
        print "[ProcessingChainController] Creating processing chain!"
        pc.start()
        self.actives.update({pc.getIdent():pc})
    
    def deleteProcessingChain(self,idThread):
        print "[ProcessingChainController] Deleting processing chain!"
        #self.actives.remove(idThread);
        del self.actives[idThread]

    def processed(self, idThread, fileOutput):
        print "[ProcessingChainController] Sending to orchestrator file data!"
        self.orchestrator.processedRawData(fileOutput)
        self.deleteProcessingChain(idThread)

class processingChain(threading.Thread):
    
    def __init__(self,pathRawData):
        threading.Thread.__init__(self)
        self.path = pathRawData
        self.defaultJobOrder = jobOrder(pathRawData)
        
    def getIdent(self):
        print self.ident
        return self.ident
       

    def run(self):
        print "[Processing Chain] Starting processing chain!!"
        l0JobOrder = self.defaultJobOrder.setL0()
        #ejecutar PL0 y comprobar resultado
        l1AJobOrder = self.defaultJobOrder.setL1A()
        #ejecutar PL1A y comprobar resultado
        l1BJobOrder = self.defaultJobOrder.setL1B()
        #ejecutar PL1B y comprobar resultado
        l1CJobOrdre = self.defaultJobOrder.setL1C()
        #ejecutar PL1C y comprobar resultado
        #capturar excepciones 
        contr = processingChainController.get()
        #contr.processed(thread.get_ident(),l1CJobOrder.getOutput())#return thread identity 
        contr.processed(self.getIdent(),"/home/ruben/dataoutput")
    
