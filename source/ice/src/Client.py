import sys, traceback, Ice
Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
import geocloud
import sys

status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    base = ic.stringToProxy('Broker:tcp -h localhost -p 10001')
    #orch_str = ic.stringToProxy('Orchestrator:tcp -h localhost -p 10001')
    broker = geocloud.BrokerPrx.checkedCast(base)
    #orch = geocloud.OrchestratorPrx.checkedCast(orch_str)
    if not broker:
        raise RuntimeError("Invalid proxy")
    #if not orch:
	#raise RuntimeError("Invalid proxy")
    r = broker.begin_cleanOrchestrator()
    print "Despues de la primera invocacion remota"
    a = broker.begin_cleanOrchestrator()

    print r.isCompleted()
    print a.isCompleted()
    r.waitForCompleted()
    a.waitForCompleted()
    print r.isCompleted()
    print a.isCompleted()

    
	
except:
    traceback.print_exc()
    status = 1

if ic:
    # Clean up
    try:
        ic.destroy()
    except:
        traceback.print_exc()
        status = 1

sys.exit(status)
