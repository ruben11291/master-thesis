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


import sys, traceback, Ice,IceGrid
import time,datetime
import threading
import pdb
#from processingChain import processingChainController
#from AyC import catalog
import MySQLdb as mdb
from collections import deque
#Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
Ice.loadSlice('-I'+Ice.getSliceDir()+' Geocloud.ice')
import geocloud

class OrchestratorI(geocloud.Orchestrator):
    proxies_pp=[]
    busy_proxies_pp=dict()
    stages_pp = dict()
    pending = []
    processing = []
    for_cataloguing=[]
    def __init__(self,com):
        if not com:
            raise RuntimeError("Not communicator")
        self.com = com
        q = com.stringToProxy('IceGrid/Query')
        self.query = IceGrid.QueryPrx.checkedCast(q)
        if not self.query:
            raise RuntimeError("Invalid proxy")
        self.sem = Ice.threading.RLock() #Lock for managing the data structures


    def getBroker(self):
        broker=None
        try:
            broker=geocloud.BrokerPrx.checkedCast(self.com.stringToProxy("broker"))
        except Exception as e:
            print e
        if broker!=None:
            return broker
    def getArchive(self):
        archive =None
        try:
           archive = geocloud.ArchiveAndCataloguePrx.checkedCast(self.com.stringToProxy('ayc'))
        except Exception as e:
            print e
            self.log("Error obtaining the archive and catalogue module!")
        if archive!=None:
            return archive


    def log(self,log):
        if self.broker!=None:
            ami=self.broker.begin_appendLog("<Orchestrator> "+log)
            ami.waitForSent()
        else:
            print "<Orchestrator> "+log

    def initScenario(self, scen,current=None):
        self.broker = self.getBroker()
        self.archive = self.getArchive()
        self.sem.acquire()
        self.scenario = scen
        self.processing = [] #clear the processing
        self.sem.release()
        self.log("Init scenario %d"%(scen))

        if self.archive!=None:
            self.log("Init tras %d"%(scen))
            self.archive.setBroker(self.broker)
            self.archive.createScenario(scen)

            self.log("Scenario created %d"%(scen))


    def downloadedImage(self,path,current=None):
        hello=None
        try:
            hello = geocloud.ProcessorPrx.checkedCast(current.adapter.getCommunicator().stringToProxy("hello"))
        except Ice.NotRegisteredException:
            hello = geocloud.ProcessorPrx.checkedCast(self.query.findObjectByType("::geocloud::ProcessingChainReplica"))
        except Exception as e:
            print e
        if hello:
            self.sem.acquire()
            self.processing.append(path)
            self.sem.release()
            self.log("Starting processing %s"%(path))
            hello.begin_processImage(path)


    def imageProcessed(self,path,current=None):
        self.log("Image %s processed!"%(path))
        self.sem.acquire()
        print "Processed"
        try:
            self.processing.remove(path)
        except Exception as e:
            print e
        queue= len(self.processing)
        print "Fuera exception"
        self.for_cataloguing.append(path)
        self.sem.release()#avisar a broker
        self.log("%d images remaining!"%(queue))
        self.log("Sending %s for cataloguing!"%(path))



    def imageCatalogued(self, path, current=None):
        self.sem.acquire()
        try:
            self.for_cataloguing.remove(path)
        except Exception as e:
            self.broker.appendLog("Not for cataloguing %s"%(path))
        self.sem.release()


    def stopScenario(self,current=None):
        self.log("Stopping scenario")
        self.sem.acquire()
        self.scenario = -1
        try:
            print "Antes"
            chains = self.query.findAllReplicas(current.adapter.getCommunicator().stringToProxy("hello"))#puede bloquearse cuando haya un pp running
            print "Despues"
            if chains:
                tmp =[]
                for chain in chains:
                    tmp.append(geocloud.ProcessorPrx.checkedCast(chain).begin_shutdown())
                    print chain
                    self.log("Stopped Proccesing chain")
                for ami in tmp:
                    ami.waitForSent()
            self.processing = []
        except Exception as e:
            print e
        self.sem.release()


class Orchestrator(Ice.Application):
    def run(self,args):
        try:
            com = self.communicator()
            servant = OrchestratorI(com)
            adapter = com.createObjectAdapter('OrchestratorOA')
            prx = adapter.add(servant, com.stringToIdentity('orchestrator'))
            adapter.activate()
            self.shutdownOnInterrupt()
            com.waitForShutdown()
        except RuntimeError as e:
            print "RuntimeException %s"%(e)
        except Exception as e:
            print "Unrecognized exception has occurred!",e



if __name__=="__main__":
    app = Orchestrator()
    sys.exit(app.main(sys.argv))
