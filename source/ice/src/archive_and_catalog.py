#!/usr/bin/python
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
import threading
import pdb
#from AyC import catalog
import MySQLdb as mdb
from collections import deque
#Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
Ice.loadSlice('-I'+Ice.getSliceDir()+' Geocloud.ice')
import geocloud


class ArchiveAndCatalogueI(geocloud.ArchiveAndCatalogue):

    def __init__(self,com):
        if not com:
            raise RuntimeError("Not communicator")
        self.com=com
        q = com.stringToProxy('IceGrid/Query')
        self.query = IceGrid.QueryPrx.checkedCast(q)
        if not self.query:
            raise RuntimeError("Invalid proxy")
        self.broker=None


    def setBroker(self,broker,current=None):
        self.broker =broker

    def log(self,log):
        if self.broker:
            self.broker.begin_appendLog("<ArchiveAndCatalogue> "+log)
        else:
            print "Created",scenario

    def createScenario(self,scenario,current=None):
        self.log("Created Scenario %s"%(scenario))
        return 1

    def catalogue(self,path,scenario,current=None):
        if scenario: #si existe escenario
            print "Catalogada",path
        return 1

    def deleteScenario(self,scenario,current=None):
        if scenario:#si existe scenario
            print  "Deleted ",scenario
        return 1


class ArchiveAndCatalogue(Ice.Application):
    def run(self,args):
        try:
            com = self.communicator()
            if not com:
                raise RuntimeError("Not communicator")

            else:
                adapter = com.createObjectAdapter("AyCOA")
                adapter.add(ArchiveAndCatalogueI(com),com.stringToIdentity("ayc"))
                print "ArchiveAndCatalogue Module ready!"
                adapter.activate()
            #self.shutdownOnInterrupt()
                com.waitForShutdown()
        except RuntimeError as e:
            print "RuntimeException %s"%(e)
        except Exception as e:
            print "Unrecognized exception has occurred!",e

if __name__=="__main__":
    app = ArchiveAndCatalogue()
    sys.exit(app.main(sys.argv))
