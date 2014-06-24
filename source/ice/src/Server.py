import sys, traceback, Ice
import time

Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
import geocloud

class BrokerI(geocloud.Broker):
    def appendLog(self,newLog,current=None):
	print "Log %s"%(newLog)
	#self.log.append(newLog)

    def startScenario(self,scenario,scen,current=None):
	print scenario
	while(1):
		print "Dentrobucle"
		
    def stopScenario(self,scen,current=None):
	print "Stop Scenario"

    def cleanOrchestrator(self,current=None):
	print "Clean orchestrator"
	while(1):
		print "Dentrobucle"

    def stopProcessors(self,current=None):
	print "Stop processors"



status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    adapter = ic.createObjectAdapterWithEndpoints('BrokerAdapter', 'tcp -h * -p 10001')
    object = BrokerI()
    adapter.add(object, ic.stringToIdentity("Broker"))
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

