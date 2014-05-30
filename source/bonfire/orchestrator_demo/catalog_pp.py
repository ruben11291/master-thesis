 #!/usr/bin/env python


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

from geoserver.catalog import Catalog
from geoserver.workspace import Workspace
from geoserver.store import DataStore
from geoserver.store import CoverageStore
from AyC import catalog
import sys

geoserver_path = "http://localhost:8080/geoserver/rest"

def sendToCatalog(catalog, path):
	 name = path.split("/")[-1]
         wksp = None
         #pdb.set_trace()
         while True:
             try:
                 wksp = catalog.createWkspace(name)
                 break
             except Exception:
                 
	 print path
         catalog.addImage(name,wksp,path)

catalog = catalog.catalog(geoserver_path)
sendToCatalog(catalog,sys.argv[1])
