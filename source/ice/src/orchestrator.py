import sys, traceback, Ice
import time

Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
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


status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    adapter = ic.createObjectAdapterWithEndpoints('OrchestratorAdapter', 'tcp -h * -p 10001')
    object = OrchestratorI()
    adapter.add(object, ic.stringToIdentity("Orchestrator"))
    adapter.activate()
    ic.waitForShutdown()
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

