#!/usr/bin/env python

from jobOrder import jobOrder
import threading
import os
from orchestator import *
import paramiko
import signal
from collections import deque
import Queue
import time


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
        self.queue=Queue.Queue()
        self.available_pp = deque()
        self.busy_pp = {}

        signal.signal(signal.SIGUSR1, self.processed)
        
        if self._controller is not None:
            raise ValueError("[ProcessingChainController] An instantiation already exists")

    def setOrchestrator(self,orchestrator):
        self.orchestrator = orchestrator

    def setProcessingChains(self,pp_ips):
        if pp_ips is not None:
            self.sem.acquire()
            self.available_pp = deque(pp_ips)
            self.sem.release()

    def any_available_pp(self):
        self.sem.acquire()
        if len(self.available_pp) > 0:
            ret=True
        else:
            ret = False
        self.sem.release()
        return ret


    def createProcessingChain(self,pathRawData):
        self.sem.acquire()
        selected = self.available_pp.popleft()
        pc = processingChain(pathRawData, selected ,self.sem ,self.queue ,os.getpid())
        pc.start()
        print "[ProcessingChainController] Creating processing chain %s!"%(str(pc.getIdent()))
        print "Processing chain : ",selected
        self.busy_pp.update({pc.getIdent():selected})
        self.actives.update({pc.getIdent():pc})
        self.petitions.update({pc.getIdent():pathRawData})
        self.sem.release()
    
    def deleteProcessingChain(self,idThread):
        print "[ProcessingChainController] Deleting processing chain %s!"%(str(idThread))
        #self.actives.remove(idThread);
        del self.petitions[idThread]
        del self.actives[idThread]

    def processed(self,signal,frame):
        t=self.queue.get()
        self.sem.acquire()

        fileOutput = self.petitions[t.getIdent()]
        print "ask"
#bloquea aqui deadlock
        self.available_pp.append(self.busy_pp[t.getIdent()])

        del self.busy_pp[t.getIdent()]

        self.deleteProcessingChain(t.getIdent())
        self.sem.release()
        self.orchestrator.processedRawData(fileOutput)
        print "[ProcessingChainController] Processed and sending to orchestrator file data: %s!"%(fileOutput)

class processingChain(threading.Thread):
    
    def __init__(self,pathRawData,PP_ip,sem,queue,idMain):
        threading.Thread.__init__(self)
        self.path = pathRawData
        self.defaultJobOrder = jobOrder(pathRawData)
        self.PP_IP = PP_ip
        self.sem = sem
        self.queue = queue
        self.idMain = idMain

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
        #os.system("ssh -o \"StrictHostKeyChecking no\" d2pp@%s \"time bash /mnt/disco/PPscript.sh %s %s\""%(self.PP_IP,reduce,scenario))
        print "Processing %s"%(os.getpid())
        time.sleep(5.0)
        #contr.processed(thread.get_ident(),l1CJobOrder.getOutput())#return thread identity 
        self.sem.acquire()
        controller = processingChainController.get()
        self.queue.put(self)
        os.kill(self.idMain, signal.SIGUSR1)
        self.sem.release()
