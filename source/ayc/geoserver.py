import sys
sys.path.append("..")

from geoserver.catalog import Catalog
from geoserver.workspace import Workspace
from geoserver.store import DataStore
from geoserver.store import CoverageStore

cat = Catalog("http://localhost:8080/geoserver/rest")

vk = cat.create_workspace("workspace","wokspace")
vk.enabled = True

cat.create_coveragestore("Imagen","/usr/share/tomcat/webapps/geoserver/data/data/DE2_MS__L1CT___20140220T104454.tif",vk)

inf = CoverageStore(cat,vk,"Imagen")

inf.fetch()

cat.save(inf)
