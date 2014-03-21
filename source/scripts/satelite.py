
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
      
        try:
            self.id = id
            self.scenario = scenario
            self.host = host
            self.total_desviation = 0
            #pdb.set_trace()
            ##realise the connection with the ground station

            con = mdb.connect(host,'root','','Scenarios')
            cur = con.cursor()
            satellite_info = 'select * from Satellites where idSatellite=%s and Scenario=%s ORDER BY timeInStation;'%(self.id,self.scenario)
            scenario_times = 'select timeIni,timeEnd from Scenarios where Name=%s;'%(self.scenario)
            #############################
            #Must obtain the ip directions from database

            self.groundIP = socket.gethostbyname(socket.gethostname())

            with con:
                cur.execute(satellite_info)
                self.rows= cur.fetchall()#Getting the Satellite events and its times
                cur.execute(scenario_times)
                s_times= cur.fetchall()[0]#Getting when the scenario starts and finishes
                
                
            con.close()
            self.scenario_times = [float(i)/10000 for i in s_times]
                #Convers the time into seconds 

            
        except socket.error as e:
            print "[Satellite %s] Error creating the socket!"%(self.id)
            exit(-1)
        except Exception as e:
            print "Exception ", e
            exit(-1)


    def scheduleBehaviours(self):
        if self.rows and self.scenario_times:
            s = sched.scheduler(time.time, time.sleep)
            reductionRate = 10
            reference_time = 5 # added 5 seconds for the sched can be produced without impairments and have enough time for program this.
            init_time = time.time()
            print "Init Time ",init_time
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
                interesting_zone_start = abs_int_zone_start/10000 if float(seq[-2]) > -1 else -1 #time in which the satellite starts to cacht the interesting zone
                interesting_zone_end= abs_int_zone_end/10000 if float(seq[-1]) > -1 else -1  #time in which the satellite stops to cacht the interesting zone. 
                #pdb.set_trace()

                #If this visibility cone hasn't got any interesting area
                if interesting_zone_start == -1:
                    s.enter(reference_time + zone_in_time,self.useless_priority,self.notInteresting , argument=(reference_time+zone_in_time,((abs_zone_out_time-abs_zone_in_time)/ reductionRate ),ground_station,))
                    
                   

                #If this visibility cone has got any interesting area
                else:

                    #First case: 
                    if abs_int_zone_start < abs_zone_in_time:
                        # If the interesting area starts before the visibility area starts, we must to calculate the area of interest cachted by the satellite
                        time_offset_before =  ((abs_zone_in_time - abs_int_zone_start)/reductionRate)  #difference between the times in which the satellite goes into the cone and the time in which the satellite goes into the interesting zone
                        abs_int_zone_start = abs_zone_in_time

                    else: 
                        size_offset_before = 0
                        
                    #Second case:
                    if abs_int_zone_end > abs_zone_out_time: 
                        
                        abs_int_zone_end = abs_zone_out_time
                        
                    #Scheduling the tasks
                        
                    if abs_int_zone_start != abs_zone_in_time:
                        
                        s.enter(reference_time + zone_in_time, self.usefull_priority, self.notInteresting, argument=(reference_time+zone_in_time,((abs_int_zone_start-abs_zone_in_time)/ reductionRate) ,ground_station,))
                        s.enter(reference_time + interesting_zone_start, self.usefull_priority, self.Interesting, argument = (reference_time + interesting_zone_start, ((abs_int_zone_end-abs_int_zone_start) / reductionRate ), ground_station,0,))
                    else:
                        s.enter(reference_time + zone_in_time, self.usefull_priority, self.Interesting, argument=(reference_time+zone_in_time, ((abs_int_zone_end-abs_int_zone_start) / reductionRate) ,ground_station,time_offset_before,))

                    if abs_int_zone_end < abs_zone_out_time:
                        s.enter(reference_time + interesting_zone_end , self.useless_priority, self.notInteresting, argument = (reference_time+interesting_zone_end, ((abs_zone_out_time - abs_int_zone_end) / reductionRate), ground_station, ))
                    

                #Also, we are going to schedule the area between two visibility cones
                if initial_time_next_element != -1:
                    s.enter(reference_time + zone_out_time, self.without_priority, self.outOfVisibility, argument =(reference_time+zone_out_time, ((initial_time_next_element - abs_zone_out_time)/ reductionRate),))

            try:
                s.run()
                print "End time ",time.time()-init_time
                print "Total Desviation: %f Total Penalty: %f"%(self.total_desviation,self.time_penality*self.penalty_times)
            except socket.error:
                print "[Sat%s] Error with ground station connection!\nExiting"%(self.id)
                exit(-1)

        else:
            print "[Behaviours] Nothing to schedule"
            exit(-1)

    def notInteresting(self,time_start, time_end, gs):
        offset= penal_times =0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.groundIP,5000))
        t_temp = time.time() # save the current time in t_temp
        final_time = t_temp+time_end
        begin_time = t_temp
        print "[Sat%s] In not interesting zone : GroundStation: %s Start: %f TimeEnd: %f ActualPenality: %f " %(self.id,gs,time_start,time_end,self.penalty_times*self.time_penality)
        while(t_temp < final_time+offset):# while current time is less that time_end+offset
          
            print "Enviado " ,self.socket.send('I')
            print "[Sat%s] Sended package with noise data: StartTime: %f CurrentTime: %f ApproximatedFinalTime: %f" %(self.id,begin_time, t_temp-begin_time,(final_time+offset)-begin_time)
            penal_times += 1
            offset = self.time_penality*penal_times 
            time.sleep(1-(time.time()-t_temp))
            t_temp = time.time()
        self.penalty_times += penal_times
        self.socket.shutdown(1)
        self.socket.close()
        local_desviation = t_temp-final_time
        self.total_desviation += local_desviation
        print "Desviation of normal behaviour : %f TotalTime : %f" %(local_desviation,t_temp-begin_time) #real final time minus the corresponding final_time

    def Interesting(self,time_start, time_end, gs, offset_time):
        offset = penal_times = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.groundIP,5000))
        t_temp = time.time() # save the current time in t_temp
        final_time = t_temp+time_end
        intermediate_time = t_temp + offset_time
        begin_time = t_temp
        
        print "[Sat%s] In interesting zone : GroundStation: %s Start: %f TimeEnd: %f ActualPenality: %f " %(self.id,gs,time_start,time_end,self.penalty_times*self.time_penality)

        while(t_temp < intermediate_time+offset):# while current time is less that time_end+offset
            self.socket.send('B')
            print "[Sat%s] Sended package with all data usefull: StartTime: %f CurrentTime: %f ApproximatedFinalTime: %f" %(self.id,begin_time, t_temp-begin_time,(final_time+offset)-begin_time)
            penal_times += 1
            offset = self.time_penality*penal_times 
            time.sleep(1-(time.time()-t_temp))
            t_temp = time.time()

        while(t_temp < final_time+offset):# while current time is less that time_end+offset
            self.socket.send('U')
            print "[Sat%s] Sended package with usefull data: StartTime: %f CurrentTime: %f ApproximatedFinalTime: %f" %(self.id,begin_time, t_temp-begin_time,(final_time+offset)-begin_time)
            penal_times += 1
            offset = self.time_penality*penal_times 
            time.sleep(1-(time.time()-t_temp))
            t_temp = time.time()
        self.penalty_times += penal_times
        self.socket.shutdown(1)
        self.socket.close()
        local_desviation = t_temp-final_time
        self.total_desviation += local_desviation
        print "Desviation of normal behaviour : %f TotalTime : %f" %(local_desviation,t_temp-begin_time) #real final time minus the corresponding final_time
            
    def outOfVisibility(self,time_start,time_end):
        offset  = penal_times = 0
        t_temp = time.time()
        begin_time = t_temp
        final_time = t_temp+time_end
        print "[Sat%s] Between visibility cones :Start: %f TimeEnd: %f ActualPenality: %f " % (self.id,time_start,time_end, self.penalty_times*self.time_penality)
        while (t_temp < final_time + offset):
            print "[Sat%s] Getting images : StartTime: %f CurrentTime: %f ApproximatedFinalTime: %f" %(self.id,begin_time, t_temp-begin_time,(final_time+offset)-begin_time)
            penal_times += 1
            offset = self.time_penality*penal_times 
            time.sleep(1-(time.time()-t_temp))
            t_temp = time.time()
        self.penalty_times +=penal_times
        local_desviation = t_temp-final_time
        self.total_desviation += local_desviation
        print "Desviation of normal behaviour : %f TotalTime : %f" %(local_desviation,t_temp-begin_time) #real final time minus the corresponding final_time


                                
if __name__=="__main__":
    if(len(sys.argv) != 4):
        print "Error with arguments. Must introduce the satellite's id, scenario and host in which database is located"
        exit(-1)

    id = sys.argv[1]
    scenario = sys.argv[2]
    host = sys.argv[3]
    sat = Satellite(id,scenario,host)
    sat.scheduleBehaviours()

