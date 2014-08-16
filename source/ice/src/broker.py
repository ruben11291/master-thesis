#!/usr/bin/env python
import sys, traceback, Ice,IceGrid
import time,datetime

Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
import geocloud

class BrokerI(geocloud.Broker):
    lastlogs = []

    def __init__(self,com):
        if not com:
            raise RuntimeError("Not communicator")
        q = com.stringToProxy('IceGrid/Query')
        self.query = IceGrid.QueryPrx.checkedCast(q)
        if not self.query:
            raise RuntimeError("Invalid proxy")
        self.clean = False
        # cat = self.query.findObjectById(com.stringToIdentity('ayc'))
        # self.catalogue = geocloud.ArchiveAndCataloguePrx.checkedCast(cat)
        self.orchestrator = geocloud.OrchestratorPrx.checkedCast(com.stringToProxy("orchestrator"))
        self.sem = Ice.threading.RLock() #Lock for managing the data structures


    def appendLog(self,newLog,current=None):
        self.sem.acquire()
        self.lastlogs.append(str(datetime.datetime.now())+" "+newLog)
        self.sem.release()

    def getLastLogs(self,current=None):
        self.sem.acquire()
        tmp =list(self.lastlogs)
        self.lastlogs=[]
        self.sem.release()
        ret=""
        for part in tmp: #introduces the lines in a string var
            ret+=str(part+"\n")
        return ret

    def startScenario(self,scenario,current=None):
        self.sem.acquire()
        #self.lastlogs=[]
        self.sem.release()
        self.appendLog("<Broker> Initializing Scenario %d"%(scenario))
        try:
            if self.orchestrator:
                ami=self.orchestrator.begin_initScenario(scenario)
                ami.waitForSent()
            #starts the satellites and the ground stations
            #To use NEPI or to implement ICE also
        except Exception as e:
            self.appendLog("Exception %s"%(e))
            sys.exit(-1)
        print self.lastlogs


    def stopScenario(self,scen,current=None):
        self.sem.acquire()
        self.appendLog("<Broker> Stopping scenario %d"%(scen))
        self.sem.release()
        try:
            if self.orchestrator:
                ami=self.orchestrator.begin_stopScenario()
                ami.waitForSent()
            #stops the satellites and the ground stations
            #To use NEPI or to implement ICE also
            self.sem.acquire()
            self.appendLog("<Broker> Stopping space simulator")
            self.sem.release()
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
