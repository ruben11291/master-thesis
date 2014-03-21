
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

import sys,os,socket,select,time,datetime,signal
import MySQLdb as mdb
import pdb

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
    bits_rate = 160 #Mbps
    acquisition_rate = 1395 #Mbps
    compresion_rate = 14.1 
    img_size = 288 #MBytes
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

            self.host = socket.gethostbyname(socket.gethostname())
            self.port = 5000 #port in which the server will be listenning for in connections
            #pdb.set_trace()
            con = mdb.connect(host,'root','','Scenarios')
            cur = con.cursor()
            #satellite_info = 'select * from GroundStations where idGrounStations=%s;'%(self.id)
            self.pids = [] # will get the pids of forks
            update_ip = 'UPDATE GroundStations SET IP=\'%s\' WHERE idGrounStations=%s' %(self.host,self.id);
            
            with con:
                #cur.execute(satellite_info)
                cur.execute(update_ip)
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
            usefull_info = useless_info = 0
            while True :
                data = self.socket.recv(1024)
                if data != "":
                    if data == 'I': #not interesting data
                        useless_info += self.bits_rate
                    elif data == 'B': #interesting data with interesting data adcquired before
                        usefull_info += self.bits_rate
                    elif data =='U': #interesting data
                        useless_info += self.bits_rate - (self.acquisition_rate /self.compresion_rate)
                        usefull_info += self.acquisition_rate/self.compresion_rate

                    print "Reciving %s from %s " %(data,os.getpid())
                else:
                    print "useless info = %d usefull info = %d"%(useless_info,usefull_info)
                    self.createFile(int(useless_info/self.img_size), int(usefull_info/self.img_size))
                    break
           
        except socket.error as e:
            print "[DownloadingException]",e
        except Exception as e:
            print e
        finally:
            self.socket.close()
            print "Socket closed"
            exit(0)

    def createFile(self, useless_images, usefull_images):
        for _ in xrange(useless_images):
            nano = str(time.time()).split('.')[1]
            name = "W_GS%d_%d_USELESS_%s" %(int(self.id),int(self.scenario),datetime.datetime.now().strftime("%H:%M:%S:"+nano+"_%d-%m-%y"))
            os.system("cp /tmp/original.bin /tmp/"+name+".bin")
            print "Image %s created!"%(name)
            time.sleep(0.2)

        for _ in xrange(usefull_images):
            nano = str(time.time()).split('.')[1]
            name = "W_GS%d_%d_USEFULL_%s" %(int(self.id),int(self.scenario),datetime.datetime.now().strftime("%H:%M:%S:"+nano+"_%d-%m-%y"))
            os.system("cp /tmp/original.bin /tmp/"+name+".bin")
            print "Image %s created!"%(name)
            time.sleep(0.2)



if __name__=="__main__":
    if(len(sys.argv) != 4):
        print "Error with arguments. Must introduce the satellite's id, scenario and host in which database is located"
        exit(-1)
        
    modHostsFile()
    id = sys.argv[1]
    scenario = sys.argv[2]
    host = sys.argv[3]
    gs = GroundStation(id,scenario,host)
    


