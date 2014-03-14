
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
    acquisition_rate = 1395 #Mbps
    ###Calculation of time penality
    t = time.time()
    time.time()
    time_penality=time.time()-t 
    #############################
    penalty_times = 0
    
    def __init__(self,id,scenario,host):
        
        try:
            #pdb.set_trace()
            con = mdb.connect(host,'root','','Scenarios')
            cur = con.cursor()
            satellite_info = 'select * from Satellites where idSatellite=%s and Scenario=%s ORDER BY timeInStation;'%(id,scenario)
            scenario_times = 'select timeIni,timeEnd from Scenarios where Name=%s;'%(scenario)
            with con:
                cur.execute(satellite_info)
                self.rows= cur.fetchall()#Getting the Satellite events and its times
                cur.execute(scenario_times)
                s_times= cur.fetchall()[0]#Getting when the scenario starts and finishes
                
                
            con.close()
            self.scenario_times = [float(i)/10000 for i in s_times]
                #Convers the time into seconds 

        except Exception as e:
            print "Exception ", e

    def scheduleBehaviours(self):
        if self.rows and self.scenario_times:
            s = sched.scheduler(time.time, time.sleep)
            print "Scenario times are ",self.scenario_times,type(self.scenario_times[0])

            reference_time = 5 # added 5 seconds for the sched can be produced without impairments and have enough time for program this.
            
            for seq in self.rows:
                zone_in_time= float(seq[3])/10000 #time in which the satellite goes into the visibility cone
                zone_out_time=float(seq[4])/10000# time in which the satellite goes out the visibility cone
                ground_station = int(seq[2])
                interesting_zone_start = float(seq[-2])/10000 if float(seq[-2]) > -1 else -1 #time in which the satellite starts to cacht the interesting zone
                interesting_zone_end= float(seq[-1])/10000 if float(seq[-1]) > -1 else -1  #time in which the satellite stops to cacht the interesting zone. 
                #pdb.set_trace()
                if interesting_zone_start == -1:
                    s.enter(reference_time + zone_in_time,self.useless_priority,self.notInteresting , argument=(reference_time+zone_in_time,reference_time+zone_out_time,ground_station,))
                else:

                    #First case: 
                    if interesting_zone_start < zone_in_time:
                        
                        size_offset_before =  (zone_in_time - interesting_zone_start) * self.acquisition_rate  #difference between the times in which the satellite goes into the cone and the time in which the satellite goes into the interesting zone
                        interesting_zone_start = zone_in_time
                    else: 
                        size_offset_before = 0
                        
                    #Second case:
                    if interesting_zone_end > zone_out_time: 
                        
                        interesting_zone_end = zone_out_time
                        
                    #Scheduling the tasks
                        
                    if interesting_zone_start != zone_in_time:
                        
                        s.enter(reference_time + zone_in_time, self.usefull_priority, self.notInteresting, argument=(reference_time+zone_in_time, reference_time + interesting_zone_start,ground_station,))
                        s.enter(reference_time + interesting_zone_start, self.usefull_priority, self.Interesting, argument = (reference_time + interesting_zone_start, reference_time+interesting_zone_end, ground_station,0,))
                    else:
                        s.enter(reference_time + zone_in_time, self.usefull_priority, self.Interesting, argument=(reference_time+zone_in_time, reference_time + interesting_zone_end ,ground_station,size_offset_before,))
                    if interesting_zone_end < zone_out_time:
                        s.enter(reference_time + interesting_zone_end , self.useless_priority, self.notInteresting, argument = (reference_time+interesting_zone_end, reference_time+ zone_out_time, ground_station, ))
                    
                print seq," Scheduled" 

            s.run()


        else:
            print "[Behaviours] Nothing to schedule"
            exit(-1)

    def notInteresting(self,time_start, time_end, gs):
        offset= 0
        t_temp = time.time() # save the current time in t_temp
        print "Not interesting GS:",gs, "time_start :",time_start," time_end :",time_end
        while(t_temp < time_end+offset):# while current time is less that time_end+offset
            print "Una vez", t_temp, time_end+offset, time_start
            d = time.time()-t_temp # save the lose time realising the send
            self.penalty_times +=1
            time.sleep(1-d)
            offset += self.time_penality*self.penalty_times 
            t_temp = time.time()#update the time

    def Interesting(self,time_start, time_end, gs, offsetbytes):
        offset= 0
        t_temp = time.time() # save the current time in t_temp
        print "Interesting GS:",gs, "time_start :",time_start," time_end :",time_end
        while(t_temp < time_end+offset):# while current time is less that time_end+offset
            print "Una vez", t_temp, time_end+offset
            d = time.time()-t_temp # save the lose time realising the send
            self.penalty_times += 1
            time.sleep(1-d)
            offset += self.time_penality*self.penalty_times 
            t_temp = time.time()#update the time
            
if __name__=="__main__":
    if(len(sys.argv) != 4):
        print "Error with arguments. Must introduce the satellite's id, scenario and host in which database is located"
        exit(-1)

    id = sys.argv[1]
    scenario = sys.argv[2]
    host = sys.argv[3]
    sat = Satellite(id,scenario,host)
    sat.scheduleBehaviours()

#f = FTP('localhost','deimos','deimos')
