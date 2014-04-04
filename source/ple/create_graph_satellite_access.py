import  MySQLdb as mdb
import logging
import matplotlib.pyplot as plt
import numpy as np


logging.basicConfig("INFO")
logger = logging.getLogger()

def get_sat_access_data(scenario,id_sat):
    
    try:
        con= mdb.connect(host,"root","","Scenarios")
        cur = con.cursor()
        with con:
            cur.execute("select timeInStation,timeOutStation from Satellites where idGroundStation=%d and scenario=%d;"%(id_sat,scenario))
            rows = cur.fetchall()
        con.close()
        return rows

    except (mdb.DataError,mdb.DatabaseError,mdb.Error,mdb.InterfaceError) as e:
        logger.info("[GET_SAT_ACCES] Error with database: %s!",exc_info=True)
        exit(-1)

def get_sat_AOI_data(scenario,id_sat):
     try:
        con= mdb.connect(host,"root","","Scenarios")
        cur = con.cursor()
        with con:
            cur.execute("select timeInStation,timeOutStation,interestZoneIni,interestZoneEnd from Satellites where idGroundStation=%d and scenario=%d and interestZoneIni!=-1 and interestZoneEnd!=-1;"%(id_sat,scenario))

            rows = cur.fetchall()
        con.close()
        return rows

    except (mdb.DataError,mdb.DatabaseError,mdb.Error,mdb.InterfaceError) as e:
        logger.info("[GET_SAT_ACCES] Error with database: %s!",exc_info=True)
        exit(-1)


def plot_sat_access(id_sat,data):
    None

def plot_sat_AOI(id_sat,data):
    None
