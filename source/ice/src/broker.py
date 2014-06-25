#!/usr/bin/env python
import sys, traceback, Ice
import time

Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
import geocloud

class BrokerI(geocloud.Broker):
    def appendLog(self,newLog,current=None):
	print "Log %s"%(newLog)
	#self.log.append(newLog)

    def startScenario(self,scenario,scen,current=None):
	print "Starting ",scenario
        try:
            query = com.stringToProxy('IceGrid/Query')
            q = IceGrid.QueryPrx.checkedCast(query)
            if not q:
                raise RuntimeError("Invalid proxy")
            self.orchestrator=q.findObjectByType("::GeoCloud::Orchestrator")
            if not q:
                raise RuntimeError("Invalid proxy")

        except ObjectNotExistException:
            print "Object not found!"
            sys.exit(-1)
        except Exception as e:
            print e
            sys.exit(-1)

	print "Quering to Orchestrator..."
        self.orchestrator.begin_downloadedImage("path")
		
    def stopScenario(self,scen,current=None):
	print "Stop Scenario"

    def cleanOrchestrator(self,current=None):
	print "Clean orchestrator"
	while(1):
		print "Dentrobucle"

    def stopProcessors(self,current=None):
	print "Stop processors"



class Broker(Ice.Application):
    def run(self,args):
        com = self.communicator()
        servant = BrokerI()
        if not com:
            raise RuntimeError("Not communicator")

        else:
            adapter = com.createObjectAdapter('BrokerAdapter')
            adapter.add(servant, com.stringToIdentity('Broker'))
            print "Broker ready!"
            adapter.activate()
            self.shutdownOnInterrupt()
            com.waitForShutdown()


if __name__=="__main__":
    app = Broker()
    sys.exit(app.main(sys.argv))
