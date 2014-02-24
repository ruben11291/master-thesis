import sys
sys.path.append("..")


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
        self.cat.save(vk)
        return vk

    def addImage(self,name,workspace,data):
        self.cat.create_coveragestore("Imagen","/usr/share/tomcat/webapps/geoserver/data/data/DE2_MS__L1CT___20140220T104454.tif",vk)

        inf = CoverageStore(self.cat,workspace,name)

        inf.fetch()

        self.cat.save(inf)
