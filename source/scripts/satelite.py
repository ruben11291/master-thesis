
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
import sched,time
import socket
import logging
import pdb

"""This script simulates the behaviour of a satellite
Must be executed by "python <id> <scenario> <hostDatabase>"

The arguments above are:
id: is the identity of the satellite
scenario: is the scenario that will be simulated
hostDatabase: is the host where the MySQL database is located
"""


class Satellite:
    ###########Values############ 
    usefull_priority = 4
    useless_priority = 2
    without_priority = 0
    compression_rate = 14.1
    acquisition_rate = 1395 #Mbps
    time_image_acquisition = 23.4 #seconds
    time_image_download = 14.4 #seconds

    ###Calculation of time penality
    t = time.time()
    time.time()
    time_penality=time.time()-t 
    #############################

    penalty_times = 0 # This variable will contain the times that penalty times will be acumulated

  
    
    def __init__(self,id,scenario,host):
        logger.info("[Satellite%s] Initializing!"%(id))
        try:
            self.id = id
            self.scenario = scenario
            self.host = host
            self.total_desviation = 0
            ##realise the connection with the ground station
            
            satellite_info = 'select * from Satellites where idSatellite=%s and scenario=%s ORDER BY timeInStation;'%(self.id,self.scenario)
            
            scenario_times = 'select timeIni,timeEnd from Scenarios where name=%s;'%(self.scenario)
            logger.debug("[Satellite%s] Scenario times query: %s!"%(self.id,scenario_times))

            ips_groundstations = 'select ip,port from GroundStations order by idGroundStation;'            
            #############################
            #Must obtain the ip directions from database and all the info
            self.getDataFromDB(ips_groundstations,satellite_info,scenario_times)

        except socket.error as e:
            logger.error("[Satellite%s] Error creating the socket!"%(self.id))
            exit(-1)
        except Exception as e:
            logger.error("[Satellite%s] Error Unexpected!"%(self.id),exc_info=True)
            exit(-1)

    def getDataFromDB(self, ips_groundstations,satellite_info,scenario_times):
        logger.debug("[Satellite%s] Connecting with data base!"%(self.id))
        con = None
        try:
            con = mdb.connect(host,'root','','Scenarios')
            cur = con.cursor()
            with con:
                cur.execute(ips_groundstations)
                self.ips = cur.fetchall() #Getting the ips from ground stations
                cur.execute(satellite_info)
                self.rows= cur.fetchall()#Getting the Satellite events and its times
                cur.execute(scenario_times)
                s_times= cur.fetchall()[0]#Getting when the scenario starts and finishes
                self.scenario_times = [float(i)/10000 for i in s_times]
                #Convers the time into seconds 
                logger.debug("[Satellite%s] Converting times!"%(self.id))
                logger.debug("[Satellite%s] Queries to data base done!"%(self.id))
                logger.debug("[Satellite%s] Closed data base!"%(self.id))
            con.close()
        except (mdb.DataError,mdb.DatabaseError,mdb.Error,mdb.InterfaceError) as e:
            logger.error("[Satellite%s] Error with database: %s!"%(self.id),exc_info=True)
            exit(-1)

    def scheduleBehaviours(self):
        if self.rows and self.scenario_times:
            logger.info("[Satellite%s] Scheduling the tasks!"%(self.id))

            s = sched.scheduler(time.time, time.sleep)
            reductionRate = 10
            reference_time = 5 # added 5 seconds for the sched can be produced without impairments and have enough time for program this.
            init_time = time.time()
            logger.info("[Satellite%s] Init time %s!"%(self.id,str(init_time)))

            for seq in self.rows:
                #Get the time in which the next visibility cone starts. If the actual zone is the last, initial time will be -1, else it will acquire the initial time value.
                initial_time_next_element = -1 if len(self.rows)-1 == self.rows.index(seq) else self.rows[self.rows.index(seq)+1][3] 

                abs_zone_in_time = float(seq[3])
                abs_zone_out_time = float(seq[4])
                abs_int_zone_start = float(seq[-2])
                abs_int_zone_end = float(seq[-1])
                zone_in_time= abs_zone_in_time/10000 #time in which the satellite goes into the visibility cone
                zone_out_time= abs_zone_out_time/10000# time in which the satellite goes out the visibility cone
                ground_station = int(seq[2])
               
                ip_groundstation = (self.ips[ground_station][0], int(self.ips[ground_station][1])) #the host,ip of the ground station
                interesting_zone_start = abs_int_zone_start/10000 if float(seq[-2]) > -1 else -1 #time in which the satellite starts to cacht the interesting zone
                interesting_zone_end= abs_int_zone_end/10000 if float(seq[-1]) > -1 else -1  #time in which the satellite stops to cacht the interesting zone. 
                #pdb.set_trace()
                
                logger.debug("[Satellite%s] Abs_zone_in_time %f\t Abs_zone_out_time %f\nAbs_int_zone_start %f\tAbs_int_zone_end %f\nGroundStation %d: IP %s"%(self.id,abs_zone_in_time,abs_zone_out_time,abs_int_zone_start,abs_int_zone_end, ground_station, ip_groundstation))

                #If this visibility cone hasn't got any interesting area
                if interesting_zone_start == -1:
                    s.enter(reference_time + zone_in_time,self.useless_priority,self.notInteresting , argument=(reference_time+zone_in_time,((abs_zone_out_time-abs_zone_in_time)/ reductionRate ),ground_station,ip_groundstation))
                    logger.debug("[Satellite%s] Schedule not interesting area!"%(self.id))

                   

                #If this visibility cone has got any interesting area
                else:

                    #First case: 
                    if abs_int_zone_start < abs_zone_in_time:
                        # If the interesting area starts before the visibility area starts, we must to calculate the area of interest cachted by the satellite
                        time_offset_before =  ((abs_zone_in_time - abs_int_zone_start)/reductionRate)  #difference between the times in which the satellite goes into the cone and the time in which the satellite goes into the interesting zone
                        abs_int_zone_start = abs_zone_in_time
                        logger.debug("[Satellite%s] The interesting area starts before the visibility cone !"%(self.id))
                                                
                    else: 
                        time_offset_before = 0
                        
                    #Second case:
                    if abs_int_zone_end > abs_zone_out_time: 
                        
                        abs_int_zone_end = abs_zone_out_time
                        
                    #Scheduling the tasks
                        
                    if abs_int_zone_start != abs_zone_in_time:
                        logger.debug("[Satellite%s] Schedule interesting zone starting after visibility cone : 2 task!"%(self.id))
                                            
                        s.enter(reference_time + zone_in_time, self.usefull_priority, self.notInteresting, argument=(reference_time+zone_in_time,((abs_int_zone_start-abs_zone_in_time)/ reductionRate) ,ground_station,ip_groundstation))
                        s.enter(reference_time + interesting_zone_start, self.usefull_priority, self.Interesting, argument = (reference_time + interesting_zone_start, ((abs_int_zone_end-abs_int_zone_start) / reductionRate ), ground_station,ip_groundstation,0,))
                    else:
                        logger.debug("[Satellite%s] Schedule interesting zone starting before or equal into visibility cone : 1 task!"%(self.id))
                        s.enter(reference_time + zone_in_time, self.usefull_priority, self.Interesting, argument=(reference_time+zone_in_time, ((abs_int_zone_end-abs_int_zone_start) / reductionRate) ,ground_station,ip_groundstation,time_offset_before,))

                    if abs_int_zone_end < abs_zone_out_time:
                        logger.debug("[Satellite%s] Schedule interesting zone ending before goes out visibility cone : 1 task!"%(self.id))
                        s.enter(reference_time + interesting_zone_end , self.useless_priority, self.notInteresting, argument = (reference_time+interesting_zone_end, ((abs_zone_out_time - abs_int_zone_end) / reductionRate), ground_station,ip_groundstation, ))
                    

                #Also, we are going to schedule the area between two visibility cones
                if initial_time_next_element != -1:
                    logger.debug("[Satellite%s] Schedule the area between two visibility cones : 1 task!"%(self.id))
                    s.enter(reference_time + zone_out_time, self.without_priority, self.outOfVisibility, argument =(reference_time+zone_out_time, ((initial_time_next_element - abs_zone_out_time)/ reductionRate),))

            try:
                logger.info("[Satellite%s] Starting the simulation!!"%(self.id))
                s.run()
                logger.info("[Satellite%s] End time ",(self.id,time.time()-init_time))
                logger.info("[Satellite%s] Total Desviation: %f Total Penalty: %f"%(self.id,self.total_desviation,self.time_penality*self.penalty_times))
            except socket.error:
                logger.error("[Satellite%s] Error with ground station connection!\nExiting"%(self.id))
                exit(-1)

        else:
            print "[Satellite%s] Nothing to schedule"%(self.id)
            exit(-1)

    def notInteresting(self,time_start, time_end, gs,ipGs):
        offset= penal_times =0
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(ipGs)
            t_temp = time.time() # save the current time in t_temp
            final_time = t_temp+time_end
            begin_time = t_temp
            logger.info("[Satellite%s] In not interesting zone : GroundStation: %s:%s Start: %f TimeEnd: %f ActualPenality: %f " %(self.id,gs,ipGs,time_start,time_end,self.penalty_times*self.time_penality))
            while(t_temp < final_time+offset):# while current time is less that time_end+offset
          
                self.socket.send('I')
                logger.info("[Satellite%s] Sended package with noise data: StartTime: %f CurrentTime: %f ApproximatedFinalTime: %f" %(self.id,begin_time, t_temp-begin_time,(final_time+offset)-begin_time))
                penal_times += 1
                offset = self.time_penality*penal_times 
                time.sleep(1-(time.time()-t_temp))
                t_temp = time.time()
            self.penalty_times += penal_times
            self.socket.shutdown(1)
            self.socket.close()
            local_desviation = t_temp-final_time
            self.total_desviation += local_desviation
            logger.info("[Satellite%s] Desviation of normal behaviour : %f TotalTime : %f" %(self.id,local_desviation,t_temp-begin_time)) #real final time minus the corresponding final_time

        except socket.error:
            logger.error("[Satellite%s] Ground Station %d unreachable!" %(self.id,gs))
            
    def Interesting(self,time_start, time_end, gs,ipGs, offset_time):
        offset = penal_times = 0
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(ipGs)
            t_temp = time.time() # save the current time in t_temp
            final_time = t_temp+time_end
            intermediate_time = t_temp + offset_time
            begin_time = t_temp
        
            logger.info("[Satellite%s] In interesting zone : GroundStation: %s:%s Start: %f TimeEnd: %f ActualPenality: %f " %(self.id,gs,ipGs,time_start,time_end,self.penalty_times*self.time_penality))
            
            while(t_temp < intermediate_time+offset):# while current time is less that time_end+offset
                self.socket.send('B')
                logger.info("[Satellite%s] Sended package with all data usefull: StartTime: %f CurrentTime: %f ApproximatedFinalTime: %f" %(self.id,begin_time, t_temp-begin_time,(final_time+offset)-begin_time))
                penal_times += 1
                offset = self.time_penality*penal_times 
                time.sleep(1-(time.time()-t_temp))
                t_temp = time.time()

            while(t_temp < final_time+offset):# while current time is less that time_end+offset
                self.socket.send('U')
                logger.info("[Satellite%s] Sended package with usefull data: StartTime: %f CurrentTime: %f ApproximatedFinalTime: %f" %(self.id,begin_time, t_temp-begin_time,(final_time+offset)-begin_time))
                penal_times += 1
                offset = self.time_penality*penal_times 
                time.sleep(1-(time.time()-t_temp))
                t_temp = time.time()
            self.penalty_times += penal_times
            self.socket.shutdown(1)
            self.socket.close()
            local_desviation = t_temp-final_time
            self.total_desviation += local_desviation
            logger.info("[Satellite%s] Desviation of normal behaviour : %f TotalTime : %f" %(self.id,local_desviation,t_temp-begin_time)) #real final time minus the corresponding final_time
        except socket.error:
             logger.error("[Satellite%s] Ground Station %d unreachable!" %(self.id,gs))
            
    def outOfVisibility(self,time_start,time_end):
        offset  = penal_times = 0
        t_temp = time.time()
        begin_time = t_temp
        final_time = t_temp+time_end
        logger.info("[Satellite%s] Between visibility cones :Start: %f TimeEnd: %f ActualPenality: %f " % (self.id,time_start,time_end, self.penalty_times*self.time_penality))
        while (t_temp < final_time + offset):
            logger.info("[Satellite%s] Getting images : StartTime: %f CurrentTime: %f ApproximatedFinalTime: %f" %(self.id,begin_time, t_temp-begin_time,(final_time+offset)-begin_time))
            penal_times += 1
            offset = self.time_penality*penal_times 
            time.sleep(1-(time.time()-t_temp))
            t_temp = time.time()
        self.penalty_times +=penal_times
        local_desviation = t_temp-final_time
        self.total_desviation += local_desviation
        logger.info("[Satellite%s] Desviation of normal behaviour : %f TotalTime : %f" %(self.id,local_desviation,t_temp-begin_time)) #real final time minus the corresponding final_time

                             
                                
if __name__=="__main__":
    if(len(sys.argv) != 4):
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

    handler = logging.FileHandler("satellite%s.log"%(sys.argv[1]),mode="w")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    id = sys.argv[1]
    scenario = sys.argv[2]
    host = sys.argv[3]
    sat = Satellite(id,scenario,host)
    sat.scheduleBehaviours()

