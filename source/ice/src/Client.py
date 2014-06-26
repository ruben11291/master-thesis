import sys, traceback, Ice,IceGrid
Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
import geocloud
import sys


class Client(Ice.Application):
    def run(self,args):
        com = self.communicator()
        if not com:
            raise RuntimeError("Not communicator")

        else:
            query = com.stringToProxy('IceGrid/Query')
            q = IceGrid.QueryPrx.checkedCast(query)
            try:
                broker=q.findAllObjectsByType("::GeoCloud::Broker")
                orch = q.findAllObjectsByType("::GeoCloud::Orchestrator")
                print orch[0].ice_getIdentity()
                #orchestrator = geocloud.OrchestratorPrx.checkedCast(orch[0])
            except Exception as e:
                print e
                sys.exit(-1)
            
            
           
            print broker
            print orch[0]
           # start=broker.begin_startScenario("Scenario1",1)
            #print "Applying for"
            #start.waitForCompleted()
#base = com.stringToProxy('orchestrator1')
            #orchestrator = geocloud.OrchestratorPrx.checkedCast(orch[0])
            # if not orchestrator:
            #     raise RuntimeError("Invalid proxy")
    #if not orch:
	#raise RuntimeError("Invalid proxy")
            # r = orchestrator.begin_downladedImage("aa")
            # print "Despues de la primera invocacion remota"
            # a = orchestrator.begin_cleanQueue()
            
            # print r.isCompleted()
            # print a.isCompleted()
            # r.waitForCompleted()
            # a.waitForCompleted()
            # print r.isCompleted()
            # print a.isCompleted()

if __name__=="__main__":
    c = Client()
    sys.exit(c.main(sys.argv))
