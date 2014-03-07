
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

def initGroundStations():
    gs = [("Chetuval",0),("Cordoba",1),("Dubai",2),("Irkutsk",3),("Korou",4),("Krugersdorp",5),("Malysia",6),("Prince_Albert",7),("Puertollano",8),("Svalbard",9),("Sydney",10),("Troll",11)]
  #  pdb.set_trace()
    try:
        con = mdb.connect(host, 'root','','Scenarios')
        cur = con.cursor()
        with con:
            for ground in gs:
                cur.execute('insert into GroundStations values (%s, %s)',(str(ground[1]),ground[0]))
 
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
    try:
        con = mdb.connect(host,'root','','Scenarios')
        cur = con.cursor()
        data_scenarios = getAllData(args[0][0])

        for doc in args[0][1:]:
    #Format of the file name must be "Scenario_NUM_NAME.csv"
    #where NUM is a interger and NAME can be a undefined string
            scenarie = ("".join(doc.split("_")[2:])).split(".")[0] 
            print scenarie
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
                
                    for line in lines:
        #The missing format is like "GEO-Cloud_005-To-Troll" where 005 is the number
        #of the satellite, Troll is the ground station
                        if(line.find("GEO") != -1):
                            sat = line[line.index("_")+1:line.index("_")+4]
                            gs = line.split("-")[3]
                            print sat, gs
                        else:
            #Whether we are not looking for the Gs or Number of satellite, we are in
            #data line, in which are been the usefull time, the leave time and the total
            #time into the area
                            line = line.split(",")
                            start = line[1]
                            end = line[3]
                            time = line[5]
                            print start, end, time

    except IOException:
        print "[InitSatellites] Error with file!"
    except(mdb.IntegrityError,mdb.DatabaseError,mdb.InterfaceError,mdb.Error):
        print "[InitSatellites] DataBaseError ocurred!"
    finally:
        if f:
            f.close()
        if con:
            con.close()
    
def getAllData(file):
    res ={}
    f = open(args[0][0],"r")
    for lines in f:
        line = lines.split(",")
        if(line[0]!="Scenario" and len(line[0]) != 0):#into the first state
            


def dropDatabase():
    try:
        con = mdb.connect(host, 'root','','Scenarios')
        cur = con.cursor()
        with con:
            cur.execute('delete from GroundStations')
            cur.execute('delete from Scenarios')
            cur.execute('delete from Satellites')
        con.commit()
    except (mdb.DatabaseError,mdb.Error,mdb.InterfaceError):
        if con:
            con.rollback()
            print "[DropDataBase] DatabaseError ocurred!"
    finally:
        if con:
            con.close()
            
dropDatabase()
initGroundStations()
initScenaries(allscenarios)
initSatellites(sys.argv[2:])

