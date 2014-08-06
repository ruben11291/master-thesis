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
    
    def __init__(self,name):
        self.name = name
        # q = self.com.stringToProxy('IceGrid/Query')
        # self.query = IceGrid.QueryPrx.checkedCast(q)
        # if not self.query:
        #     raise RuntimeError("Invalid proxy")
        # orchest = self.query.findObjectById(self.com.stringToIdentity('orchestrator'))
        # self.orchestrator = geocloud.OrchestratorPrx.checkedCast(orchest)


    def processImage(self,path,current=None):
        i=0  
        print "Applied name:",self.name
        print "Processing image...",path
        
        if self.orchestrator:
            print "Sending image..."
            #left=self.orchestrator.begin_imageProcessed(path,(ProcessorI)self)
            print "Sent"

    def shutdown(self,current=None):
        print (self.name+ " shutting down...")
        current.adapter.getCommunicator().shutdown()
       


class Processor(Ice.Application):
    def run(self,args):
        com = self.communicator()
        servant = ProcessorI(com)
        if not com:
            raise RuntimeError("Not communicator")

        else:
            properties = com.getProperties()
            adapter = com.createObjectAdapter("ChainProcessingOA")
            id = com.stringToIdentity(properties.getProperty("Identity"))
            adapter.add(ProcessorI(properties.getProperty("Ice.ProgramName")),id)
            print "Processor%s ready!"%(sys.argv[1])
            adapter.activate()
            self.shutdownOnInterrupt()
            com.waitForShutdown()
            

if __name__=="__main__":
    app = Processor()
    sys.exit(app.main(sys.argv))
