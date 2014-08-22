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
import xml.dom.minidom
import MySQLdb as mdb
import pdb

class LoadData():
	
	def __init__(self):
	    #pdb.set_trace()
	    file = xml.dom.minidom.parse("orchestrator.conf.xml")
	    nodes=file.childNodes
	    self.ftp_user = nodes[0].getElementsByTagName("ftp")[0].getElementsByTagName("user")[0].firstChild.toxml()
	    self.ftp_passwd = nodes[0].getElementsByTagName("ftp")[0].getElementsByTagName("passwd")[0].firstChild.toxml()
	   
	    self.database_ip = nodes[0].getElementsByTagName("address")[0].getElementsByTagName("database")[0].firstChild.toxml()
	    
	def getData(self):
	    subject = "select ip,port from GroundStations ORDER BY idGroundStation";
	    try:
		con = mdb.connect(database_ip, 'root','','Scenarios')
		cur = con.cursor()
		with con:
		    cur.execute(subject)
		    ground_stations_address=  cur.fetchall()
		con.close()
	    except (mdb.DataError,mdb.DatabaseError,mdb.Error,mdb.InterfaceError) as e:
		print e
		exit(-1)
	    return ftp_user,ftp_passwd,ground_stations_address

