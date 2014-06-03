#!/usr/bin/env python

from jobOrder import jobOrder
import threading
import os
from orchestator import *
import paramiko

class processingChainController:
    """ProcessingChainController Class.
    This class is a singleton whose function is to create new processing chains objects
    in order to process the raw images sended by the Orchestrator.
    The methods are:
    *setOrchestrator(orchestrator) : assign the passed Orchestrator to ProcessingChainController in order to stablish communication with.
    *createProcessingChain(pathRawData): creates a new processing chain object whose raw data is the param pathRawData
    *deleteProcessingChain(idThread): delete the processing chain that has finished.
    *processed(idThread,fileOutput): says to the Orchestrator that the file has been created (processed image) and removes the thread from system.
    """

    _controller = None

   

    @classmethod
    def get(cls):
        if ( cls._controller == None ):
            cls._controller = processingChainController()
        return cls._controller

    def __init__(self):
        self.actives = {}
        self.petitions = {}
        self.files = {}
        self.queue = []
        self.maxPetitions = 100
        if self._controller is not None:
            raise ValueError("[ProcessingChainController] An instantiation already exists")

    def setOrchestrator(self,orchestrator):
        self.orchestrator = orchestrator

    def createProcessingChain(self,pathRawData):
        pc = processingChain(pathRawData,self.orchestrator.getPP())
        print "[ProcessingChainController] Creating processing chain!"
        pc.start()
        self.actives.update({pc.getIdent():pc})
        self.petitions.update({pc.getIdent():pathRawData})
    
    def deleteProcessingChain(self,idThread):
        print "[ProcessingChainController] Deleting processing chain!"
        #self.actives.remove(idThread);
        del self.petitions[idThread]
        del self.actives[idThread]

    def processed(self, idThread, fileOutput):
        print "[ProcessingChainController] Sending to orchestrator file data!"
        self.orchestrator.processedRawData(self.petitions[idThread])
        self.deleteProcessingChain(idThread)

class processingChain(threading.Thread):
    
    def __init__(self,pathRawData,PP_ip):
        threading.Thread.__init__(self)
        self.path = pathRawData
        self.defaultJobOrder = jobOrder(pathRawData)
        self.PP_IP = PP_ip
        
    def getIdent(self):
        print self.ident
        return self.ident
       

    def run(self):
        # print "[Processing Chain] Starting processing chain!!"
        # l0JobOrder = self.defaultJobOrder.setL0()
        # #ejecutar PL0 y comprobar resultado
        # l1AJobOrder = self.defaultJobOrder.setL1A()
        # #ejecutar PL1A y comprobar resultado
        # l1BJobOrder = self.defaultJobOrder.setL1B()
        # #ejecutar PL1B y comprobar resultado
        # l1CJobOrdre = self.defaultJobOrder.setL1C()
        # #ejecutar PL1C y comprobar resultado
        # #capturar excepciones 
        os.system("ssh -o \"StrictHostKeyChecking no\" d2pp@%s \"bash /mnt/disco/PPscript.sh %s\""%(self.PP_IP, self.path))
        #contr.processed(thread.get_ident(),l1CJobOrder.getOutput())#return thread identity 
        self.orchestrator.processed(self.getIdent(),"/home/ruben/dataoutput")
    
