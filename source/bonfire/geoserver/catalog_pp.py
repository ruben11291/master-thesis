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
import pdb
from geoserver.catalog import Catalog
from geoserver.workspace import Workspace
from geoserver.store import DataStore
from geoserver.store import CoverageStore
from geoserver.catalog import Catalog, ConflictingDataError, UploadError, \
    FailedRequestError
#from AyC import catalog
import sys
import os
geoserver_path = "http://localhost:80/geoserver/rest"

def sendToCatalog(catalog, path):
	 name = path.split("/")[-1]
         wksp = None
         pdb.set_trace()
         while True:
             try:
                 wksp = catalog.createWkspace(name)
                 break
             except Exception:
		 None                 
	 print path
         catalog.addImage(name,wksp,path)
#pdb.set_trace()
#catalog = catalog.catalog(geoserver_path)
#sendToCatalog(catalog,sys.argv[1])

if __name__ == "__main__":
	if (len(sys.argv) != 4):
		print "Error with arguments. Must enter almost three"
		sys.exit(-1)
	print sys.argv[1]
	name_file=sys.argv[1].split("/")[-1]
	scenario=sys.argv[2]
	nameStore=sys.argv[3]
	cat = Catalog(geoserver_path)
	#pdb.set_trace()
		
	try:
		print name_file,sys.argv[1]
		vk = cat.get_workspace(scenario)
		if vk ==None:
			vk=cat.create_workspace(scenario,scenario)
		vk.enabled=True
		try:
			cv = cat.create_coveragestore(nameStore,sys.argv[1],vk)
			inf=CoverageStore(cat,vk,scenario)
			inf.fetch()
			cat.save(inf)
			f.write("Processed %s"%(name_file))
		except Exception:
			print "Catalogued %s!"%(name_file)
		print nameStore,name_file,scenario
		comman ='curl -i --data "layerName=%s&coverageStore=%s&imageurl=ftp://131.254.204.143:21/../../usr/share/tomcat7/apache-tomcat-7.0.53/webapps/geoserver/data/data/%s/%s/%s.geotiff" http://172.18.242.41:8043/IDV'%(name_file,nameStore,scenario,nameStore,nameStore)
		print comman
		print "Sending to IDV module!"
		#os.system(comman)

	except ConflictingDataError as e:
		print "Exception ",e
	except UploadError as e:
		print "Exception ",e
	except FailedRequestError  as e:
		print "Exception ",e
	
