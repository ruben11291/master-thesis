import sys, traceback, Ice
import time

Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
import geocloud

class ProcessorI(geocloud.Processor):

    def l0(self,path,current=None):
	print "Processing l0..."

    def l0r(self,path,current=None):
	print "Processing l0r..."

    def l1a(self,path,current=None):
	print "Processing l1a..."



status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    adapter = ic.createObjectAdapterWithEndpoints('ProcessorAdapter', 'tcp -h * -p 10001')
    object = ProcessorI()
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

