
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

"""Script to import the scenarios files into a MySQL database named 'Scenarios'.
First, imports the ground stations.
Then, imports all data from files passed as arguments
The input must be:
>>First argument: The host where the database is allocated
>>Second argument: File that contains the generic information about all scenarios 
>>More arguments, one by scenario, could be passed for processing
"""

import MySQLdb as mdb
import sys
import pdb


host = sys.argv[1]
allscenarios = sys.argv[2]

gs = {"Chetumal":0,"Cordoba":1,"Dubai":2,"Irkutsk":3,"Kourou":4,"Krugersdorp":5,"Malaysia":6,"Prince_Albert":7,"Puertollano":8,"Svalbard":9,"Sydney":10,"Troll":11}

def initGroundStations():
  #  pdb.set_trace()
    try:
        con = mdb.connect(host, 'root','','Scenarios')
        cur = con.cursor()
        with con:
            for ground in gs:
                cur.execute('insert into GroundStations values (%s, %s)',(str(gs[ground]),ground))
 
        con.commit()
        print "[GroundStations] Success!"
    except mdb.IntegrityError:
        if con:
            con.rollback()
        print "[GroundStations] IntegrityError ocurred!"
    except mdb.DatabaseError:
        if con:
            con.rollback()
        print "[GroundStations] DatabaseError ocurred!"
    except mdb.InterfaceError:
        if con:
            con.rollback()
        print "[GroundStations] Not be able to located the database!"
    except mdb.Error:
        if con:
            con.rollback()
        print "[GroundStations] Error in database"
    except Exception as e:
        print "[GroundStations] Unexpected Error ",e
    finally:
        if con:
            con.close()
   

def initScenaries(file):
    
    try:
        f = open(file,"r")
        con = mdb.connect(host,'root','','Scenarios')
        cur = con.cursor()

       # pdb.set_trace()
        for line in f:
          
            try:
               
                l = line.split(",")
                
                if(len(l[0]) != 0 and l[0] != "Scenario"):
                    scenario = int(l[0])
                    scenarioIni=float(l[1])
                    scenarioEnd=float(l[2])
                    
                    with con:
                        cur.execute("insert into Scenarios values (%s, %s,%s)",(scenario,scenarioIni,scenarioEnd))

            except(mdb.IntegrityError,mdb.DatabaseError,mdb.InterfaceError,mdb.Error):
                if con:
                    con.rollback()
                print "[InitScenaries] DataBaseError ocurred!"
            except ValueError :
                None 
            except Exception as e:
                if con:
                    con.rollback()
                print "[InitScenaries] Unexpected Error!"
            
        con.commit()
        print "[Init Scenaries] Success!"

    except(mdb.IntegrityError,mdb.DatabaseError,mdb.InterfaceError,mdb.Error):
            print "[InitScenaries] DataBaseError ocurred!"
    except IOError:
        print "[InitScenaries] Error opening file!"
    finally:
        if con:
            con.close()
        if f:
            f.close()
            
        
def initSatellites(*args):
    """This functions consists in the initialitation of satellites. This is made by iterating the lines of scenarios files. Once the usefull time of data adquisition of each satellite in each scenario, it will be comparated with each action got from the orbital data by the scenario files.
The scenario file must be named like "Scenario_NUM_NAMESCENARIO.csv" """
    try:
        con = mdb.connect(host,'root','','Scenarios')
        cur = con.cursor()
        data_scenarios = getAllData(args[0][0])
     
        try:
            for doc in args[0][1:]:
    #Format of the file name must be "Scenario_NUM_NAME.csv"
    #where NUM is a interger and NAME can be a undefined string
                scenarie = doc.split("_")[1]
                lines = []
                f = open(doc,"r")
                for line in f:
                    if line != "\n":
                        # pdb.set_trace()
                        lines.append(line)
    
        #pdb.set_trace()
    #Now, we are going to find the num of satellite, the ground station, and the time
    #when the satellite is in the action area of ground station and when it goes out 
    #from the area
                #pdb.set_trace()
                for l in lines:
                   
        #The missing format is like "GEO-Cloud_005-To-Troll" where 005 is the number
        #of the satellite, Troll is the ground station
                    if(l.find("GEO") != -1):
                        sat = int(l[l.index("_")+1:l.index("_")+4])
                        groundStation = l.split("-")[3]
                       
                    
                    else:
            #Whether we are not looking for the Gs or Number of satellite, we are in
            #data line, in which are been the usefull time for us, the leave time and the total
            #time into the area
                        l = l.split(",")
                        start = l[1]
                        end = l[3]
                        time = l[5]
                        #print groundStation, sat
                        # print scenarie, data_scenarios[scenarie]
                        if data_scenarios.has_key(scenarie) and data_scenarios[scenarie].has_key(str(sat)):#if this satellite has usefull time for this scenario
                            #compare times
                            for i in data_scenarios[scenarie][str(sat)]:
                             
                                if(float(i[0]) >= float(start) and float(i[0]) < float(end)):
                                    #print i
                            #times = data_scenarios[scenarie][str(sat)]
                           # print times
                         
                            #print start,end,time, sat, gs[groundStation[:-1]]
                            #print data_scenarios[scenarie][str(sat)], sat, groundStation
                            #insert into the database with usefull times
                                    with con:
                                        cur.execute("insert into Satellites values(%s,%s,%s,%s,%s,%s,%s)",(sat,scenarie,gs[groundStation[:-1]],start, end,data_scenarios[scenarie][str(sat)][0][0],data_scenarios[scenarie][str(sat)][0][1]))
                                    con.commit()

                            #     print iteration, sat, scenarie
                            #     print len(data_scenarios[scenarie][str(sat)])
                        else:
                            #inser into the database without usefull times
                            with con:
                                cur.execute("insert into Satellites values(%s,%s,%s,%s,%s,%s,%s)",(sat,scenarie,gs[groundStation[:-1]],start, end,-1,-1))
                            con.commit()
              
                    

           # print data_scenarios
        except IOError:
            print "[InitSatellites] Error with file!"
        finally:
            if f:
                f.close()

        print "[InitSatellites] Success!"
    except(mdb.IntegrityError,mdb.DatabaseError,mdb.InterfaceError,mdb.Error):
        print "[InitSatellites] DataBaseError ocurred!"
    finally:
        if con:
            con.close()
    
def getAllData(file):
    """This function gets the important data for scenarios that are when the satellites
    came into the interesting area and when they go out of that.
    For this, we are going to create a dictonary names scenarios that will contains, 
    ordered by id scenario, all those interactions the satellites will realize
    The format of scenarios is the next:
    {scenario:{sat:[(num,num),...], sat:[(num,num),...]}, scenario:{sat:{[(num,num),...], sat:[(num,num),...]}} """

    scenarios ={}
    try:
       # pdb.set_trace()
        f = open(file,"r")
        for lines in f:
            line = lines.split(",")
         #storage in scenario the time in which the satellite came into the zone, which is the satellite and when it comes out the zone
    
            if(line[0]!="Scenario"):
                if(len(line[0]) != 0):#into the first state, contains the first satellite action
                    idscenario = line[0]
                    scenarios [idscenario] = {line[3]:[(line[4],line[5])]}
                    # print (scenarios[idscenario])[line[3]]
                elif(len(line[3]) != 0):#into the second state that contains a satellite action
                    if(scenarios[idscenario].has_key(line[3])):
                        scenarios[idscenario][line[3]].append((line[4],line[5]))
                    else:
                        scenarios[idscenario][line[3]] = [(line[4],line[5])]
    except IOError:
        print "[GetData] Error with file!"

    return scenarios

def dropDatabase():
    con=""
    try:
        con = mdb.connect(host, 'root','','Scenarios')
        cur = con.cursor()
        with con:
            cur.execute('delete from Satellites')
            cur.execute('delete from GroundStations')
            cur.execute('delete from Scenarios')
        con.commit()
    except (mdb.DatabaseError,mdb.Error,mdb.InterfaceError) as e:
        if con:
            con.rollback()
            con.close()
        print "[DropDataBase] DatabaseError ocurred!",e
 
dropDatabase()
initGroundStations()
initScenaries(allscenarios)
initSatellites(sys.argv[2:])

