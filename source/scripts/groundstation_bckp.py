
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
import asyncore
import socket
import time
import signal
import pdb

"""This script simulates the behaviour of a GroundStation
Must be executed by "python <id> <scenario> <hostDatabase>"

The arguments above are:
id: is the identity of the ground station
scenario: is the scenario that will be simulated
hostDatabase: is the host where the MySQL database is located
"""


class GroundStation(asyncore.dispatcher):
    ###########Values############ 
    image_size = 44 #MBytes
    acquisition_rate = 1395 #Mbps

    ###Calculation of time penality
    t = time.time()
    time.time()
    time_penality=time.time()-t 
    #############################
    max_connections = 20
    
    def __init__(self,id,scenario,hostdb):
        
        asyncore.dispatcher.__init__(self)
        self.handlerClass = ConnectionHandler

        try:
            self.id = id
            self.scenario = scenario
            self.hostdb = hostdb

            self.host = 'localhost'
            self.port = 5002 #port in which the server will be listenning for in connections
            #pdb.set_trace()
            con = mdb.connect(host,'root','','Scenarios')
            cur = con.cursor()
            satellite_info = 'select * from GroundStations where idGrounStations=%s;'%(self.id)
            self.pids = [] # will get the pids of forks
           
            with con:
                cur.execute(satellite_info)
                self.rows= cur.fetchall()#Getting the Satellite events and its times
              
                
            con.close()

            signal.signal(signal.SIGINT, self.sighandler)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.set_reuse_addr()
            self.bind((self.host, self.port))
            self.listen(self.max_connections)

            print "Listening"

        except Exception as e:
            print "Exception ", e

        
    def sighandler(self, signum, frame):
        print "Closing the Ground Station"
        self.close()
        exit(0)
    

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s:%s' % (repr(addr),sock)
            #pdb.set_trace()
            self.pids.append(os.fork())
            if os.getpid() > 0:
                self.handlerClass(sock,addr,self)
            print os.getpid()
    

class ConnectionHandler(asyncore.dispatcher):
    
    def __init__(self,conn_sock, client_address, server):
        self.server = server
        self.client_address = client_address
        self.buffer = ""
        
        self.is_writable = False
        asyncore.dispatcher.__init__(self, conn_sock)

    def readable(self):
        return True

    def handle_read(self):
        print "Conection Handl"
        data = self.recv(1024)
        if data:
            
            print data
            print self
            time.sleep(2)

    def handle_close(self):
        print "conn_closed: client_address=%s:%s" % \
                     (self.client_address[0],
                      self.client_address[1])
        self.close()




if __name__=="__main__":
    if(len(sys.argv) != 4):
        print "Error with arguments. Must introduce the satellite's id, scenario and host in which database is located"
        exit(-1)

    id = sys.argv[1]
    scenario = sys.argv[2]
    host = sys.argv[3]
    if os.getpid() > 0:
        gs = GroundStation(id,scenario,host)
        asyncore.loop()
    else :
        print "I'm a fork"

#f = FTP('localhost','deimos','deimos')
