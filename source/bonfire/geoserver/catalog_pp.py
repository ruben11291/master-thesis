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

geoserver_path = "http://localhost:80/geoserver/rest"


if __name__ == "__main__":
        if (len(sys.argv) != 2):
                print "Error with arguments. Must enter almost two"
                sys.exit(-1)
        print sys.argv[1]
        name_file=sys.argv[1].split("/")[-1]
        scenario="Scenario1"
        cat = Catalog(geoserver_path)
        #pdb.set_trace()

        try:
                print name_file,sys.argv[1]
                vk = cat.get_workspace(scenario)
                if vk ==None:
                        vk=cat.create_workspace(scenario,scenario)
                vk.enabled=True
                cv = cat.create_coveragestore("test",sys.argv[1],vk)
                inf=CoverageStore(cat,vk,scenario)
                #inf.fetch()
                cat.save(inf)
                f.write("Processed")
        except ConflictingDataError as e:
                print "Exception ",e
        except UploadError as e:
                print "Exception ",e
        except FailedRequestError  as e:
                print "Exception ",e


