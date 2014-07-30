#!/usr/bin/env python

#
#    Copyright (C) 2014 DEIMOS
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Ruben Perez <ruben.perez@deimos-space.com>

import sys, traceback, Ice,IceGrid
import time

Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
import geocloud

class ProcessorI(geocloud.Processor):
    
    def __init__(self,com):
        if not com:
            raise RuntimeError("Communication is not available")
        self.com = com
        


    def processImage(self,path,current=None):
        i=0  
        q = self.com.stringToProxy('IceGrid/Query')
        self.query = IceGrid.QueryPrx.checkedCast(q)
        if not self.query:
            raise RuntimeError("Invalid proxy")
        orchest = self.query.findObjectById(self.com.stringToIdentity('orchestrator'))
        self.orchestrator = geocloud.OrchestratorPrx.checkedCast(orchest)

        print "Processing image...",path
        
        if self.orchestrator:
            print "Sending image..."
            self.orchestrator.imageProcessed(path,self)
        
       


class Processor(Ice.Application):
    def run(self,args):
        com = self.communicator()
        servant = ProcessorI(com)
        if not com:
            raise RuntimeError("Not communicator")

        else:
            adapter = com.createObjectAdapter('ChainProcessingOA')
            adapter.add(servant, com.stringToIdentity('ProcessingChain%s'%(sys.argv[1])))
            print "Processor%s ready!"%(sys.argv[1])
            adapter.activate()
            self.shutdownOnInterrupt()
            com.waitForShutdown()
            

if __name__=="__main__":
    app = Processor()
    sys.exit(app.main(sys.argv))
