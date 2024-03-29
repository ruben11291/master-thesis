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
    *setOrchestrator(orchestrator) : assigns the passed Orchestrator to ProcessingChainController in order to stablish communication with.
    *createProcessingChain(pathRawData): creates a new processing chain object whose raw data is the param pathRawData
    *deleteProcessingChain(idThread): deletes the processing chain that has finished.
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
        self.maxPetitions = 100
        self.sem = threading.Lock()
        if self._controller is not None:
            raise ValueError("[ProcessingChainController] An instantiation already exists")

    def setOrchestrator(self,orchestrator):
        self.orchestrator = orchestrator

    def createProcessingChain(self,pathRawData):
        pc = processingChain(pathRawData,self.orchestrator.getPP(),self.sem)
        print "[ProcessingChainController] Creating processing chain %s!"%(str(pc.getIdent()))
        pc.start()
        self.sem.acquire()
        self.actives.update({pc.getIdent():pc})
        self.petitions.update({pc.getIdent():pathRawData})
        self.sem.release()
    
    def deleteProcessingChain(self,idThread):
        print "[ProcessingChainController] Deleting processing chain %s!"%(str(idThread))
        #self.actives.remove(idThread);
        del self.petitions[idThread]
        del self.actives[idThread]

    def processed(self, idThread, fileOutput):
        print "[ProcessingChainController] Processed and sending to orchestrator file data: %s!"%(fileOutput)
        self.orchestrator.processedRawData(self.petitions[idThread])
        self.deleteProcessingChain(idThread)

class processingChain(threading.Thread):
    
    def __init__(self,pathRawData,PP_ip,sem):
        threading.Thread.__init__(self)
        self.path = pathRawData
        self.defaultJobOrder = jobOrder(pathRawData)
        self.PP_IP = PP_ip
        self.sem = sem
        
    def getIdent(self):
        return self.ident
       

    def run(self):
        
	reduce=self.path.split('.')[0].split("/tmp/")[1]
	print reduce
	scenario="Scenario"+reduce.split('USE')[0][:-1][::-1].split('_')[0]
	print "[Processing Chain] Starting processing chain %s:%s!!"%(str(self.ident),reduce)
        # l0JobOrder = self.defaultJobOrder.setL0()
        # #ejecutar PL0 y comprobar resultado
        # l1AJobOrder = self.defaultJobOrder.setL1A()
        # #ejecutar PL1A y comprobar resultado
        # l1BJobOrder = self.defaultJobOrder.setL1B()
        # #ejecutar PL1B y comprobar resultado
        # l1CJobOrdre = self.defaultJobOrder.setL1C()
        # #ejecutar PL1C y comprobar resultado
        # #capturar excepciones 
        #var = os.system("ssh -o \"StrictHostKeyChecking no\" d2pp@%s \"bash /mnt/disco/PPscript.sh %s\""%(self.PP_IP, self.path))
        os.system("ssh -o \"StrictHostKeyChecking no\" d2pp@%s \"time bash /mnt/disco/PPscript.sh %s %s\""%(self.PP_IP,reduce,scenario))
        #contr.processed(thread.get_ident(),l1CJobOrder.getOutput())#return thread identity 
        self.sem.acquire()
        controller = processingChainController.get()
        controller.processed(self.getIdent(),self.path)
        self.sem.release()
