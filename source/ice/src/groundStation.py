import sys, traceback, Ice
Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
import geocloud
import sys

status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    orch_str = ic.stringToProxy('Orchestrator')
    orchestrator = geocloud.OrchestratorPrx.checkedCast(orch_str)

    if not orchestrator:
        raise RuntimeError("Invalid proxy")

    r = orchestrator.begin_downloadedImage("Imagen")
    print "Despues de la primera invocacion remota"
    a = orchestrator.begin_downloadedImage("Imagen")

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
