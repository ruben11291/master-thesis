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
import subprocess


import geocloud

class ProcessorI(geocloud.Processor):

    def __init__(self,com,name):
        self.name=name
        self.thread=None
        if not com:
            raise RuntimeError("Not communicator")
        self.com=com
        q = com.stringToProxy('IceGrid/Query')
        self.query = IceGrid.QueryPrx.checkedCast(q)
        if not self.query:
           raise RuntimeError("Invalid proxy")
       


    def setOrchestrator(self, orch,current=None):
        self.orchestrator = orch

    def processImage(self,path,current=None):
        i=0
        print "Processing image...",path
        t = time.time()
        while (time.time()-t < 5.0):
            time.sleep(1.0)
            print "aa"

        print "Sending image..."
        self.orchestrator = geocloud.OrchestratorPrx.uncheckedCast(self.com.stringToProxy("orchestrator"))
        if self.orchestrator:
            left=self.orchestrator.begin_imageProcessed(path)
            print "Sent"

    def shutdown(self,current=None):
        print (self.name+ " shutting down...")
        current.adapter.getCommunicator().shutdown()
        if self.thread:
            self.thread.kill()
            self.thread=None


class Processor(Ice.Application):
    def run(self,args):
        com = self.communicator()
        if not com:
            raise RuntimeError("Not communicator")

        else:
            properties = com.getProperties()
            adapter = com.createObjectAdapter("ChainProcessingOA")
            id = com.stringToIdentity(properties.getProperty("Identity"))
            adapter.add(ProcessorI(com,properties.getProperty("Ice.ProgramName")),id)
            print "Processor%s ready!"%(sys.argv[1])
            adapter.activate()
            #self.shutdownOnInterrupt()
            com.waitForShutdown()


if __name__=="__main__":
    app = Processor()
    sys.exit(app.main(sys.argv))
