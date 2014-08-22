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
import loadData
#from processingChain import processingChainController
#from AyC import catalog
import MySQLdb as mdb
from collections import deque
#Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))

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
        self.count=1

    def getBroker(self):
        broker=None
        try:
            broker=geocloud.BrokerPrx.checkedCast(self.com.stringToProxy("broker"))
        except Ice.NotRegisteredException:
            self.log("Broker unavailable")
        except Exception as e:
            print e
        if broker!=None:
            return broker

    def getArchive(self):
        archive =None
        try:
           archive = geocloud.ArchiveAndCataloguePrx.checkedCast(self.com.stringToProxy('ayc'))
        except Ice.NotRegisteredException:
            self.log("Error obtaining AYC proxy")
        except Exception as e:
            self.log("Unknown exception obtaining the archive and catalogue module!")
        if archive!=None:
            return archive


    def log(self,log):
        if self.broker!=None:
            ami=self.broker.begin_appendLog("<Orchestrator> "+str(log))
            ami.waitForSent()
        else:
            print "<Orchestrator> "+str(log)

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
            self.archive.createScenario(str(scen))

            self.log("Scenario created %d"%(scen))


    def downloadedImage(self,path,current=None):
        hello=None
        try:
            replica_prx = geocloud.ProcessorPrx.checkedCast(current.adapter.getCommunicator().stringToProxy("hello"))
        except Ice.NotRegisteredException:
            replica_prx = geocloud.ProcessorPrx.checkedCast(self.query.findObjectByType("::geocloud::ProcessingChainReplica"))
        except Exception as e:
            self.log("Unknown exception obtaining replica proxy")

        if replica_prx:
            self.sem.acquire()
            self.processing.append(path)
            self.sem.release()
            self.log("Starting processing %s"%(path))
            try:
                ami=replica_prx.begin_processImage(path)
                ami.waitForSent()
            except ProcessingException:
                self.log("Error processing %s"%(path))
                        

    def imageProcessed(self,path,current=None):
        self.log("Image %s processed!"%(path))
        self.sem.acquire()
        print "Processed"
        try:
            self.processing.remove(path)
        except Exception as e:
            print e
        queue= len(self.processing)
        self.sem.release()
        self.log("%d images remaining!"%(queue))
        self.log("Sending %s for cataloguing!"%(path))
        try:
            self.archive.catalogue(path,self.getStore(path),str(self.scenario))
        except geocloud.CataloguingException as e:
            self.log(e)
        except Exception as e:
            self.log(e)

    def getStore(self,path):
        self.count+=1
        return "Storage"+str(self.count)

    def stopScenario(self,current=None):
        self.log("Stopping scenario")
        self.sem.acquire()
        self.archive.deleteScenario(self.scenario)
        self.scenario = -1
        try:
            chains = self.query.findAllReplicas(current.adapter.getCommunicator().stringToProxy("hello"))
            if chains:
                tmp =[]
                for chain in chains:
                    tmp.append(geocloud.ProcessorPrx.uncheckedCast(chain).begin_shutdown()) #unchecked avoids deadlocking
                for ami in tmp:
                    ami.waitForSent()
                self.log("All processing chains were stopped")
            self.processing = []
        except  Ice.NotRegisteredException:
            self.log("Processing chains can not been recovered")
        except Exception as e:
            self.log("Unknown exception recovering proxies")
        finally:
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
