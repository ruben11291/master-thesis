
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
import socket
import select
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


class GroundStation():
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
        
       # asyncore.dispatcher.__init__(self)
       # self.handlerClass = ConnectionHandler

        try:
            self.id = id
            self.scenario = scenario
            self.hostdb = hostdb

            self.host = 'localhost'
            self.port = 5000 #port in which the server will be listenning for in connections
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

            self.created_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.set_reuse_addr()
            self.created_socket.bind((self.host, self.port))
            self.created_socket.listen(self.max_connections)
            #pdb.set_trace()

            print "[GroundStation%s] The ground station has started!"%(self.id
)
            self.serverFunction()

        except socket.error as msg:
            print "Exception" , msg
            self.created_socket.close()
            
        except Exception as e:
            print "Exception ", e

        
    def sighandler(self, signum, frame):
        print "[GroundStation%s] Closing the Ground Station" %(self.id)
        for pid in self.pids:
            os.kill(pid,signal.SIGINT)
        self.created_socket.close()
        exit(0)
   
    def sonSighandler(self, signum, frame):
        print "[DownloadWorker%s]Closing the downloading process"%(self.pid)
        self.socket.close()
        exit(0)

    def serverFunction(self):
        readList = [self.created_socket]

        while True:
            (sread, swrite, sex) = select.select(readList,[],[]);
        
            for sock in sread:
                if sock == self.created_socket:
                    (newsock,address) = self.created_socket.accept()
                    print "[GroundStation%s] New connection from %s:%s!" %(self.id,newsock,address)
                    self.pid = os.fork()
                    if self.pid == 0:          
                        print "I'm the son"
                        self.Download(sock)
                    else:
                        self.pids.append(self.pid)
                        print "I'm the father"
            

            
    def Download(self,sock):
        self.socket = sock
        signal.signal(signal.SIGINT, self.sonSighandler)
        t = time.time()
        final_time = t+20
        while t < final_time :
            print "Downloading %s" %(os.getpid())
            time.sleep(1)
            t = time.time()


if __name__=="__main__":
    if(len(sys.argv) != 4):
        print "Error with arguments. Must introduce the satellite's id, scenario and host in which database is located"
        exit(-1)

    id = sys.argv[1]
    scenario = sys.argv[2]
    host = sys.argv[3]
    gs = GroundStation(id,scenario,host)
    


#f = FTP('localhost','deimos','deimos')
