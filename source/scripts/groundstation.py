
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
import MySQLdb as mdb
import socket
import select
import time
import signal
import pdb
from struct import *


"""This script simulates the behaviour of a GroundStation
Must be executed by "python <id> <scenario> <hostDatabase>"

The arguments above are:
id: is the identity of the ground station
scenario: is the scenario that will be simulated
hostDatabase: is the host where the MySQL database is located
"""


def modHostsFile():
    """This method solves the bug in the Unix based systems. This bug is based on
    a wrong line in /etc/hosts. The second line that must contain the IP of the phisical interface, is shown as 127.0.1.1, so it is wrong."""
    f = open("/etc/hosts","rw")
    lines = f.readlines()
    f.close()
    ifconfig=os.popen("ifconfig")
    ip = ""

    for line in ifconfig:
        if line.find("eth0") != -1:
            ip = ifconfig.next().split(":")[1].split(" ")[0]
            break
            
        elif line.find("wlan0") != -1:
            ip = ifconfig.next().split(":")[1].split(" ")[0]
            break
    f = open("/tmp/hosts","w")
    for line in lines:
        if line.find(socket.gethostname()) != -1:
            to_add = ip +" "+socket.gethostname()+"\n"
            f.write(to_add)
        else:
            f.write(line)
    f.close()

    os.system("sudo mv /tmp/hosts /etc/hosts")


    

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
    SIZE_PACKET = 204800 #Bytes
    FORMAT = '!c204800s'

    def __init__(self,id,scenario,hostdb):
        
       # asyncore.dispatcher.__init__(self)
       # self.handlerClass = ConnectionHandler

        try:
            self.id = id
            self.scenario = scenario
            self.hostdb = hostdb

            self.host = socket.gethostbyname(socket.gethostname())
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
            self.created_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
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
                    print "[GroundStation%s] New connection from %s!" %(self.id,address)
                    self.pid = os.fork()
                    if self.pid == 0:          
                        self.Download(newsock)
                    else:
                        self.pids.append(self.pid)
            

            
    def Download(self,sock):
        try:
            self.socket = sock
            signal.signal(signal.SIGINT, self.sonSighandler)
            while True :
                data = self.socket.recv(self.SIZE_PACKET)
                if data != "":
                    type, padding = unpack(self.FORMAT,data)
                    print "Downloading %s Len %d" %(os.getpid(), len(padding))
                    print type
                else:
                    print "No recibo nada"
                    break
           
        except socket.error as e:
            print "[DownloadingException]",e
        except Exception as e:
            print e
        finally:
            self.socket.close()
            print "Socket closed"
            exit(0)

if __name__=="__main__":
    if(len(sys.argv) != 4):
        print "Error with arguments. Must introduce the satellite's id, scenario and host in which database is located"
        exit(-1)
        
    modHostsFile()
    id = sys.argv[1]
    scenario = sys.argv[2]
    host = sys.argv[3]
    gs = GroundStation(id,scenario,host)
    


