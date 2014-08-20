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
from geoserver.catalog import Catalog
from geoserver.workspace import Workspace
from geoserver.store import DataStore
from geoserver.store import CoverageStore
from geoserver.catalog import Catalog, ConflictingDataError, UploadError, \
    FailedRequestError
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
        self.broker=geocloud.BrokerPrx.checkedCast(com.stringToProxy("broker"))
        self.sem = Ice.threading.RLock() #Lock for managing the data structures
        geoserver_path = "http://localhost:80/geoserver/rest"
        self.catalog = Catalog(geoserver_path)
        self.workspace=None

    def setBroker(self,broker,current=None):
        self.broker =broker

    def log(self,log):
        if self.broker:
            self.broker.begin_appendLog("<ArchiveAndCatalogue> "+str(log))
        else:
            print log

    def createScenario(self,scenario,current=None):
        self.sem.acquire()
        try:
            if self.catalog ==None:
                self.log("Catalog")
                raise geocloud.CreationScenarioException()
            try:
                self.workspace = self.catalog.create_workspace(scenario,scenario)
                self.workspace.enabled =True
                self.log("Created Scenario %s"%(scenario))
            except Exception:
                print ("workspace does not created")
                self.log("Workspace does not created")
        except FailedRequestError:
            self.log("Request failed")
            raise geocloud.CreationScenarioException();
        finally:
            self.sem.release()
                

    def catalogue(self,path,store,scenario,current=None):
  
        if self.workspace ==None:
            raise geocloud.CataloguingException()
        else:
            try:
                if self.catalog==None:
                    raise geocloud.CataloguingException()
               # store = path.split('/')[-1]
                self.sem.acquire()
                cv = self.catalog.create_coveragestore(store,path,self.workspace)
                self.log("%s Catalogued!"%(path))
            except ConflictingDataError as e:
                self.log(e)
            except UploadError as e:
                self.log(e)
            except FailedRequestError  as e:
		None
            except Exception as e:
                self.log(e)
            finally:
                self.sem.release()
                

    def deleteScenario(self,scenario,current=None):
        self.sem.acquire()
        try:
            for layer in self.catalog.get_layers():
                self.catalog.delete(layer)
            for coverage in self.catalog.get_stores():
                for resource in coverage.get_resources():
                    catalog.delete(resource)
                catalog.delete(coverage)
            for vk in catalog.get_workspaces():
                catalog.delete(wk)
        except Exception:
            self.log("Exception while cleanning scenario")

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
