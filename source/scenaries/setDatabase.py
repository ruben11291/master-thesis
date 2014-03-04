
#!/usr/bin/env python

import MySQLdb as mdb
import sys
import pdb


def initGroundStations():
    gs = [("Chetuval",0),("Cordoba",1),("Dubai",2),("Irkutsk",3),("Korou",4),("Krugersdorp",5),("Malysia",6),("Prince_Albert",7),("Puertollano",8),("Svalbard",9),("Sydney",10),("Troll",11)]

    try:
        con = mdb.connect('localhost', 'root','','Scenarios')
        cur = con.cursor()
        with con:
            cur.execute('delete  from GroundStations')
            for ground in gs:
                cur.execute('insert into GroundStations values ('+str(ground[1])+',\''+ground[0]+'\')')
        con.close()
            
    except Exception as e:
        print "Exception ",e


print "GroundStations imported"

def initScenaries():
    
#initGroundStations()

args = sys.argv[1:]
for doc in args:
    scenarie = ("".join(doc.split("_")[2:])).split(".")[0]
    print scenarie
    lines = []
    f = open(doc,"r")
    for line in f:
        if line != "\n":
           # pdb.set_trace()
            lines.append(line)
    
   # pdb.set_trace()
    for line in lines:
        if(line.find("GEO") != -1):
            sat = line[line.index("_")+1:line.index("_")+4]
            gs = line.split("-")[3]
            print sat, gs
        else:
            line = line.split(",")
            start = line[1]
            end = line[3]
            time = line[5]
            print start, end, time
