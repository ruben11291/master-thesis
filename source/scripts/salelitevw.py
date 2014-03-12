
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

"""This script simulates the behaviour of a satellite
Must be executed by "python <id> <scenario> <hostDatabase>"

The arguments above are:
id: is the identity of the satellite
scenario: is the scenario that will be simulated
hostDatabase: is the host where the MySQL database is located
"""


class Satellite:
    usefull_priority = 4
    useless_priority = 2

    def __init__(self,id,scenario,host):
        
        try:
            con = mdb.connect(host,'root','','Scenarios')
            cur = con.cursor()
            satellite_info = 'select * from Satellites where idSatellite=%s and Scenario=%s ORDER BY ;'%(id,scenario)
            scenario_times = 'select timeIni,timeEnd from Scenarios where Name=%s'%(scenario)
            with con:
                cur.execute(satellite_info)
                self.rows= cur.fetchall()#Getting the Satellite events and its times
                cur.execute(scenario_times)
                s_times= cur.fetchall()[0]#Getting when the scenario starts and finishes
                self.scenario_times = [float(i)/1000 for i in s_times]
                #Convers the time into seconds 
                
            con.close()
        except Exception as e:
            print "Exception ", e

    def scheduleBehaviours(self):
        if self.rows and self.scenario_times:
            s = sched.scheduler(time.time, time.sleep)
            print "Scenario times are ",self.scenario_times,type(self.scenario_times[0])

            for seq in self.rows:
                zone_in_time= float(seq[3])
                zone_out_time=float(seq[4])
                ground_station = int(seq[2])
                if seq[-1] == -1:
                    s.enter(10,self.useless_priority,self.f1, argument=(str(seq[-2]),))
                    #I can access to the event
                    #Maybe could be interesting to create a queue or a reference containing the last running event
                else:
                    s.enter(3,self.usefull_priority,self.f1,argument=(str(seq[-1]),))
                print seq," Scheduled" 
            s.run()
            print "after"
        else:
            print "[Behaviours] Nothing to schedule"
            exit(-1)

    def f1(self,time):
        print "Im the f1 function and print %s" %(time)
        while(1):
            None


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
