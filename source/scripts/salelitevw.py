
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

import sys
import os
from ftplib import FTP
import MySQLdb as mdb

"""This script simulates the behaviour of a satellite
Must be executed by "python <id> <scenario> <hostDatabase>"

The arguments above are:
id: is the identity of the satellite
scenario: is the scenario that will be simulated
hostDatabase: is the host where the MySQL database is located
"""

if(len(sys.argv) != 4):
    print "Error with arguments. Must introduce the satellite's id, scenario and host to ftp"
    exit(-1)

id = sys.argv[1]
scenario = sys.argv[2]
host = sys.argv[3]

try:
    con = mdb.connect(host,'root','','Scenarios')
    cur = con.cursor()
    with con:
        res = cur.execute('select idGrounStation,timeInStation,timeOutStation from Satellites where idSatellite = '+id+' and Scenarie = "'+scenario+'"')
        print res
    con.close()
except Exception as e:
    print "Exception ", e


f = FTP('localhost','deimos','deimos')
