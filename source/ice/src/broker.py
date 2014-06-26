#!/usr/bin/env python
import sys, traceback, Ice,IceGrid
import time

Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
import geocloud

class BrokerI(geocloud.Broker):
    clean = False #if True, is necessary to clean the Orchestrator Queue and stop all processors

    def __init__(self,com):
        if not com:
            raise RuntimeError("Not communicator")
        q = com.stringToProxy('IceGrid/Query')
        self.query = IceGrid.QueryPrx.checkedCast(q)
        if not self.query:
            raise RuntimeError("Invalid proxy")
        self.clean = False
        self.file=open("broker.log","w")

    def appendLog(self,newLog,current=None):
	print "Log %s"%(newLog)
        #lock
        self.file.write(newLog)
        self.lastlogs.append(newLog)
        #unlock
	#self.log.append(newLog)
    
    def getLastLogs(self,current=None):
        #lock
        tmp =list(self.lastlogs)
        #unlock
        ret=""
        for part in tmp:
            ret+=str(part)
        return ret

    def startScenario(self,scenario,scen,current=None):
	print "Starting ",scenario
        try:
            orchestrator=self.query.findObjectById("orchestrator")
            if self.clean:
                clean_orch= orchestrator.begin_cleanQueue()
                finish_pp = orchestrator.begin_stopPP()
                clean_orch.waitToBeCompleted()
                finish_pp.waitToBeCompleted()
            
            #starts the satellites and the ground stations
            #To use NEPI or to implement ICE also
            self.clean = True


        except ObjectNotExistException:
            print "Object not found!"
            sys.exit(-1)
        except Exception as e:
            print e
            sys.exit(-1)

            		
    def stopScenario(self,scen,current=None):
	print "Stop Scenario"
        try:
            orchestrator=self.query.findObjectById("orchestrator")
            if self.clean:
                clean_orch= orchestrator.begin_cleanQueue()
                finish_pp = orchestrator.begin_stopPP()
                clean_orch.waitToBeCompleted()
                finish_pp.waitToBeCompleted()
            
            #stops the satellites and the ground stations
            #To use NEPI or to implement ICE also
            self.clean = False
            
        except ObjectNotExistException:
            print "Object not found!"
            sys.exit(-1)
        except Exception as e:
            print e
            sys.exit(-1)



class Broker(Ice.Application):
    def run(self,args):
        try:
            com = self.communicator()
            servant = BrokerI(com)
            adapter = com.createObjectAdapter('BrokerOA')
            adapter.add(servant, com.stringToIdentity('broker'))
            print "Broker ready!"
            adapter.activate()
            self.shutdownOnInterrupt()
            com.waitForShutdown()
        except RuntimeError as e:
            print "RuntimeException %s"%(e)
        except Exception as e:
            print "Unrecognized exception has occurred!",e

            
     


if __name__=="__main__":
    app = Broker()
    sys.exit(app.main(sys.argv))
