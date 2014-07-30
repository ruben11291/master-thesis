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
import time
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
    def __init__(self,com):
        if not com:
            raise RuntimeError("Not communicator")
        q = com.stringToProxy('IceGrid/Query')
        self.query = IceGrid.QueryPrx.checkedCast(q)
        if not self.query:
            raise RuntimeError("Invalid proxy")
        self.proxies_rawPP = self.query.findAllObjectsByType("::GeoCloud::Processor")
        for prx in self.proxies_rawPP:
            self.proxies_pp.append(geocloud.ProcessorPrx.checkedCast(prx))

        if not self.proxies_pp:
            raise RuntimeError("Not able to fecht processor proxies")

        self.sem = Ice.threading.Lock() #Lock for managing the data structures
        

    def downloadedImage(self,path,current=None):
        self.sem.acquire()
	print "Path %s %s"%(path,current)
        included = False
        for proxy in self.proxies_pp:# for all proxies running into cloud
            if proxy  not in self.busy_proxies_pp and not included: #if any proxy is free
                print "Selected proxy : ",proxy
                self.busy_proxies_pp[proxy]=path # add the proxy to busy with its file
                self.stages_pp[proxy] = "L0" # add proxy with its corresponding stage
                self.async_call= self.processImage(path,proxy) # send the processing order to process slave
                #self.async_call = proxy.begin_processImage(path)
                print "Sended image ",path
                included = True
        if not included:
            print "Imagen includa ",path
            self.pending.append(path) #
        self.sem.release()
        if included:
            print "Waiting for sent ",path
            #self.async_call.waitForSent()
	return 0

    def processImage(self,path,prxPP):
        async_call=prxPP.begin_processImage(path)
        return async_call

    def levelProcessed(self,prxPP,path,level,current=None):
        self.sem.acquire()
        if prxPP  not in self.busy_proxies_pp:
            print "PRX not included"
        if level ==6:
            None
	print scenario
        self.sem.release()

    def imageProcessed(self,path,prxPP,current=None):
        self.sem.acquire()
	print "Stop Scenario"

        included =False
        #avisar a broker log
        self.busy_proxies_pp.delete(prxPP) #remove proxy of the busy proxy list
        self.stages_pp.delete(prxPP) # remove the current stage for proxy
        if not self.pending.empty():
            for proxy in self.proxies_pp:# for all proxies running into cloud
                if proxy  not in self.busy_proxies_pp: #if any proxy is free
                    self.busy_proxies_pp[proxy]=path # add the proxy to busy with its file
                    self.stages_pp[proxy] = "L0" # add proxy with its corresponding stage
                    async_call= self.processImage(path,proxy) # send the processing order to process slave
                    print "Sended image ",path
                    included = True
                if included:
                    async_call.waitForSent()

        self.sem.release()

    def cleanQueue(self,current=None):
        self.sem.acquire()
	print "Clean orchestrator"
        self.sem.release()

    def stop(self,current=None):
        print "StopPP"
	self.sem.acquire()
        self.busy_proxies_pp.clear()
        self.stages_pp.clear()
        self.pending.clear()
        
        for proxy in self.busy_proxies_pp:
            proxy.stop()
        #send the stop order for each chain processing
        self.sem.release()

class Orchestrator(Ice.Application):
    def run(self,args):
        try:
            com = self.communicator()
            servant = OrchestratorI(com)
            adapter = com.createObjectAdapter('OrchestratorOA')
            prx = adapter.add(servant, com.stringToIdentity('orchestrator'))
            print prx
            print "Orchestrator ready!"
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

