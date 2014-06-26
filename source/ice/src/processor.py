#!/usr/bin/env python
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


class Processor(Ice.Application):
    def run(self,args):
        com = self.communicator()
        servant = ProcessorI()
        if not com:
            raise RuntimeError("Not communicator")

        else:
            adapter = com.createObjectAdapter('ChainProcessingOA')
            adapter.add(servant, com.stringToIdentity('Processor%s'%(sys.argv[1])))
            print "Processor%s ready!"%(sys.argv[1])
            adapter.activate()
            self.shutdownOnInterrupt()
            com.waitForShutdown()
            

if __name__=="__main__":
    app = Processor()
    sys.exit(app.main(sys.argv))
