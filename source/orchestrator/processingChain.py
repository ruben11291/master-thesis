#!/usr/bin/env python

import jobOrder
import threading
from orchestator import *

class processingChainController:

    @staticmethod
    def get():
        if ( self.controller == None ):
            self.controller = processingChainController()
        return self.controller

    def __init__(self):
        self.actives = {}
        self.petitions = {}
        self.maxPetitions = 100
    
    def setOrchestrator(self,orchestrator):
        this.orchestrator = orchestrator

    def createProcessingChain(self,pathRawData):
        pc = processingChain(pathRawData)
        self.actives.update({pc.get_ident():pc})
    
    def deleteProcessingChain(self,idThread):
        self.actives.remove(idThread);

    def processed(self, idThread, fileOutput):
        orchestrator.processedRawData(fileOutput)
        self.deleteProcessingChain(idThread)

class processingChain(threading.Thread):
    
    def __init__(self,pathRawData):
        self.path = pathRawData
        self.defaultJobOrder = JobOrder(pathRawData)
        

    def run(self):
        
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
        contr.processed(thread.get_ident(),l1CJobOrder.getOutput())#return thread identity 
