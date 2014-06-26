#!/usr/bin/env python
import sys, traceback, Ice
import time

#Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
Ice.loadSlice('-I'+Ice.getSliceDir()+' Geocloud.ice')
import geocloud

class OrchestratorI(geocloud.Orchestrator):
    def downloadedImage(self,path,current=None):
	print "Path %s %s"%(path,current)
	return 0

    def levelProcessed(self,path,level,current=None):
	print scenario
		
    def imageProcessed(self,path,current=None):
	print "Stop Scenario"

    def cleanQueue(self,current=None):
	print "Clean orchestrator"

class Orchestrator(Ice.Application):
    def run(self,args):
	print "Ready"
        com = self.communicator()
        servant = OrchestratorI()
        if not com:
            raise RuntimeError("Not communicator")

        else:
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

