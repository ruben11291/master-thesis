import sys
sys.path.append("..")

import pdb
from geoserver.catalog import Catalog
from geoserver.workspace import Workspace
from geoserver.store import DataStore
from geoserver.store import CoverageStore

class catalog:
    def __init__(self,path):
        self.cat = Catalog(path)
    
    def createWkspace(self,name):
        vk = self.cat.create_workspace(name,name)
        vk.enabled = True
        return vk

    def addImage(self,name,workspace,data):
        pdb.set_trace()
        self.cat.create_coveragestore(name,"/usr/share/tomcat/webapps/geoserver/data/data/DE2_MS__L1CT___20140220T104454.tif",workspace)

        inf = CoverageStore(self.cat,workspace,name)

        inf.fetch()

        self.cat.save(inf)
