#!/usr/bin/env python
import sys, traceback, Ice
import time

#Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
Ice.loadSlice('-I'+Ice.getSliceDir()+' Geocloud.ice')
import geocloud

class OrchestratorI(geocloud.Orchestrator):
    self.proxies_pp=[]
    self.busy_proxies_pp=dict()
    self.stages_pp = dict()
    self.pending = []
    def __init__(self,com):
        if not com:
            raise RuntimeError("Not communicator")
        q = com.stringToProxy('IceGrid/Query')
        self.query = IceGrid.QueryPrx.checkedCast(q)
        if not query:
            raise RuntimeError("Invalid proxy")
        self.proxies_pp = self.query.findAllObjectsByType("::GeoCloud::Processor")
        if not self.proxies_pp:
            raise RuntimeError("Not able to fecht processor proxies")

    def downloadedImage(self,path,current=None):
        #lock
	print "Path %s %s"%(path,current)
        for proxy in self.proxies_pp:
            if proxy is not in self.busy_proxies_pp:
                self.busy_proxies_pp[proxy]=path
                self.stages_pp[proxy] = "L0"
                included = True
        if not included:
            self.pending.append(path)
        #unlock
	return 0

    def levelProcessed(self,prxPP,path,level,current=None):
        #lock
        if prxPP is not in self.busy_proxies_pp:
            print "PRX not included"
        if level ==6:
            self.
	print scenario
        #unlock

    def imageProcessed(self,path,current=None):
        #lock
	print "Stop Scenario"
        #unlock

    def cleanQueue(self,current=None):
        #lock
	print "Clean orchestrator"
        #unlock

class Orchestrator(Ice.Application):
    def run(self,args):
        try:
            com = self.communicator()
            servant = OrchestratorI(com)
        except RuntimeError as e:
            print "RuntimeException %s"%(e)
        except Exception:
            print "Unrecognized exception has occurred!"

        
        adapter = com.createObjectAdapter('OrchestratorOA')
        prx = adapter.add(servant, com.stringToIdentity('orchestrator'))
        print prx
        print "Orchestrator ready!"
        adapter.activate()
        self.shutdownOnInterrupt()
        com.waitForShutdown()
	
if __name__=="__main__":
    app = Orchestrator()
    sys.exit(app.main(sys.argv))

