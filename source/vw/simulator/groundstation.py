
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
import logging
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
    try:
        f = open("/etc/hosts","rw")
        lines = f.readlines()
        f.close()
        ifconfig=os.popen("ifconfig")
        ip = ""
    
        logger.info("Start modifing the file /etc/hosts")
        for line in ifconfig:
            if line.find("eth0") != -1: 
               ip = ifconfig.next().split(":")[1].split(" ")[0]
               logging.debug("Eth0 is encountered")
               break
            
            elif line.find("wlan0") != -1:
                ip = ifconfig.next().split(":")[1].split(" ")[0]
                logging.debug("Wlan0 is encountered")
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
        logger.info("File /etc/hosts modified")
        logger.debug("File /etc/hosts modified")
    except IOError as e:
        logger.error("[GroundStation%s] Error with file!"%(self.id),exc_info=True)
        exit(-1)
    except Exception as e:
        logger.error("[GroundStation%s] Unexpected Exception!"%(self.id),exc_info=True)
    

class GroundStation():
    ###########Values############ 
    bits_rate = 160 #MBps
    acquisition_rate = 1395 #Mbps
    compresion_rate = 14.15
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
        logger.info("Starting the initialitation")
        try:
            self.id = id
            self.scenario = scenario
            self.hostdb = hostdb
            self.pids = [] # will get the pids of forks
            #self.host = socket.gethostbyname(socket.gethostname())
            self.host = socket.gethostbyname_ex(socket.gethostname())[1][0]
            self.port = 5000 #port in which the server will be listenning for in connections. May can be changed.
            #pdb.set_trace()
          
           
            self.port = self.create_socket(self.port)
	    #pdb.set_trace()
            update_ip = 'UPDATE GroundStations SET ip=\'%s\',port =\'%s\' WHERE idGroundStation=%s' %(self.host,self.port,self.id); #mysql sentence for update GroundStations table
            #update the data base with the current ip and host where the gs is running
            self.updateDB(update_ip)

            #Set the handler for SIGINT signal
            signal.signal(signal.SIGINT, self.sighandler)

            logger.info("[GroundStation%s] The ground station has started!",(self.id
))
            logger.debug("[GroundStation%s] The ground station has started!",(self.id
))
            self.serverFunction()

        except socket.error as msg:
            logger.error("[GroundStation%s] Error with socket connection!",self.id)
        except Exception as e:
            logger.error("[GroundStation%s] Exception Unexpected",(self.id),exc_info=True)

    def updateDB(self,sentence):
        try:
            logger.info("[GroundStation%s] Connecting with the data base",self.id)
            con = mdb.connect(host,'root','','Scenarios')
            cur = con.cursor()
        
            with con:
                cur.execute(sentence)
                self.rows= cur.fetchall()#Getting the Satellite events and its times
                logger.info("[GroundStation%s] Fetching records of database",self.id)
                logger.debug("[GroundStation%s] Send: \n %s"%(self.id,sentence))
                
            con.close()
        except (mdb.DataError,mdb.DatabaseError,mdb.Error,mdb.InterfaceError) as e:
            logger.error("[GroundStation%s] Error with database: %s!"%(self.id),exc_info=True)
            exit(-1)

    def create_socket(self,port):
        nosocket = True
        logger.debug("[GroundStation%s] Creating the socket",self.id)
        while nosocket:
            try:
                self.created_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.created_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                self.created_socket.bind((self.host, port))
                self.created_socket.listen(self.max_connections)
                nosocket =False

            except socket.error:
                port +=1
            except socket.herror:
                logger.debug("[GroundStation%s] Error creating the socket!"%(self.id))
                exit(-1)
            except Exception as e:
                logger.debug("[GroundStation%s] Error creating the socket!"%(self.id))
                exit(-1)
        logger.debug("[GroundStation%s] Socket created in port %d"%(self.id,port))
        logger.info("[GroundStation%s] Socket created in port %d"%(self.id,port))
        return port
        
    def sighandler(self, signum, frame):
        logger.debug("[GroundStation%s] Closing the Ground Station" %(self.id))
        for pid in self.pids:
            os.kill(pid,signal.SIGINT)
            logger.debug("Killed process %d",pid)
        self.created_socket.close()
        exit(0)
   
    def sonSighandler(self, signum, frame):
        logger.info("[DownloadWorker%s]Closing the downloading process"%(self.pid))
        self.socket.close()
        exit(0)

    def serverFunction(self):
        readList = [self.created_socket]

        while True:
            (sread, swrite, sex) = select.select(readList,[],[]);
        
            for sock in sread:
                if sock == self.created_socket:
                    (newsock,address) = self.created_socket.accept()
                    logger.info("[GroundStation%s] New connection from %s!" %(self.id,address))
                    self.pid = os.fork()
                    if self.pid == 0:          
                        self.Download(newsock)
                    else:
                        self.pids.append(self.pid)
            

            
    def Download(self,sock):
        try:
            self.socket = sock
            signal.signal(signal.SIGINT, self.sonSighandler) #set the handler for SIGINT signal
            usefull_info = useless_info = 0
            buff_naoi=buff_aoi= naoi=aoi =0
	    reduction_rate=10
            satellite=-1
            while True :
                data = self.socket.recv(1024)
                if data != "":
                    satellite = data.split(":")[1]
                    data=data.split(":")[0]
                    logger.info("[GroundStation%s] Fork %s Receiving data from %s :%s"%(data,self.id,os.getpid(),self.socket.getsockname()))                              
                    if data == 'I': #not interesting data
                        #useless_info += float(self.bits_rate)*reduction_rate
                        buff_naoi+=(self.bits_rate - (float(self.acquisition_rate )/float(self.compresion_rate)))*reduction_rate
                        naoi +=(float(self.acquisition_rate)/float(self.compresion_rate))*reduction_rate
                        logger.info("[GroundStation%s] Received I packet",self.id)
                    elif data == 'B': #interesting data with interesting data adcquired before
                        buff_aoi +=(self.bits_rate - (float(self.acquisition_rate )/float(self.compresion_rate)))*reduction_rate
                        aoi += (float(self.acquisition_rate)/float(self.compresion_rate))*reduction_rate
                        #usefull_info += float(self.bits_rate)*reduction_rate
                        logger.info("[GroundStation%s] Received B packet",self.id)
                    elif data =='U': #interesting data
                        buff_naoi+=(self.bits_rate - (float(self.acquisition_rate )/float(self.compresion_rate)))*reduction_rate
                        aoi+=(float(self.acquisition_rate)/float(self.compresion_rate))*reduction_rate
                        #useless_info += (self.bits_rate - (float(self.acquisition_rate )/float(self.compresion_rate)))*reduction_rate
                        #usefull_info += (float(self.acquisition_rate)/float(self.compresion_rate))*reduction_rate
                        logger.debug("[GroundStation%s] Received U packet",self.id)
                else:
                    logger.info("[GroundStation%s_Sat%s] Total info = %d Mbits"%(self.id,satellite, buff_naoi/5.0 + naoi/5.0 + buff_aoi/5.0 + aoi/5.0))
                    #self.createFile((int(useless_info/5.0)/(self.img_size*8)), int((usefull_info/5.0)/(self.img_size*8)))
                    self.createFile(satellite,(int(buff_naoi/5.0)/(self.img_size*8))+(int(naoi/5.0)/(self.img_size*8)), int((buff_aoi/5.0)/(self.img_size*8))+  int((aoi/5.0)/(self.img_size*8)))
                    break
           
        except socket.error as e:
            logger.error("[GroundStation%s] Error with the socket!"%(self.id))
        except Exception as e:
            logger.error("[GroundStation%s] %s "%(self.id, e))
        finally:
            logger.info("[GroundStation%s] Socket %s closed"%(self.id,self.socket.getsockname()))
            self.socket.close()
            exit(0)

    def createFile(self,satellite, useless_images, usefull_images):
        for _ in xrange(useless_images):
            nano = str(time.time()).split('.')[1]
            name = "W_GS%d_SAT%s_%d_USELESS_%s" %(int(self.id),satellite,int(self.scenario),datetime.datetime.now().strftime("%H:%M:%S:"+nano+"_%d-%m-%y"))
            os.system("cp /tmp/original.bin /tmp/"+name+".bin")
	    os.system("sudo chmod 777  /tmp/"+name+".bin")
            os.system("sudo chown deimos:ftp  /tmp/"+name+".bin")
            logger.info("[GroundStation%s] ImageUseless %s created!"%(self.id,name))
            time.sleep(0.2)

        for _ in xrange(usefull_images):
            nano = str(time.time()).split('.')[1]
            name = "W_GS%d_SAT%s_%d_USEFULL_%s" %(int(self.id),satellite,int(self.scenario),datetime.datetime.now().strftime("%H:%M:%S:"+nano+"_%d-%m-%y"))
            os.system("cp /tmp/original.bin /tmp/"+name+".bin")
	    os.system("sudo chmod 777  /tmp/"+name+".bin")
            os.system("sudo chown deimos:ftp  /tmp/"+name+".bin")
            logger.info("[GroundStation%s] ImageUseful %s created!"%(self.id,name))
            time.sleep(0.2)



if __name__=="__main__":
    """Ground Station behaviour simulation.
    This software realises the simulation of the GEO-Cloud 'grounds stations individually.
    The parameters are:
    id: id ground station
    scenario : scenario in which the ground station will simulate
    host: IP of data base host
    level_loggin: Level for the log
    """

    if(len(sys.argv) < 4):
        print "Error with arguments. Must introduce the satellite's id, scenario and host in which database is located"
        exit(-1)

    loglevel = "INFO"
    if(len(sys.argv) > 4):
        loglevel = sys.argv[4]
        if loglevel.find("log")!= -1:
            loglevel = loglevel[loglevel.index("g")+2:]

  
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)


    logging.basicConfig(level=numeric_level)
    logger = logging.getLogger()

    handler = logging.FileHandler("gs%s.log"%(sys.argv[1]),mode="w")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    modHostsFile()
    id = sys.argv[1]
    scenario = sys.argv[2]
    host = sys.argv[3]
    gs = GroundStation(id,scenario,host)
    


