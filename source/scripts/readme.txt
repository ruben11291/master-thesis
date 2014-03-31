
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


This directory contains the scripts will be executed in Virtual Wall nodes.
This files are depicted as follows:

-- groundstation.py : This script simulate the behaviour of a ground station. It needs some parameters as the simulated scenario , the id of the ground station and the ip where the data base is running.

-- satellite.py : This script simulate the behavior of a satellite. It needs some parameters as the simulated scenario, the id of the ground station and the ip where the data base is running.

-- runGS.sh : bash script for testing. This script executes all the ground stations in a specific scenario (taken as parameter). 
   The execution is made as root as follows:
   -- $ ./runGS.sh <NUM_SCENARIO> <DATA_BASE_IP> [LEVEL_LOG] 
   -- where NUM_SCENARIO is the simulated scenario id, data base ip is the IP where the data	 base is allocated and level log is the level that you are able to get in the standard output. 	This values can be INFO, DEBUG, ERROR.

-- runSat.sh : bash script for testing. This script executes all satellites in a specific scenario (taken as parameter).
   The execution is made as root as follows:
   -- $ ./runSat.sh <NUM_SCENARIO> <DATA_BASE_IP> [LEVEL_LOG] 
   -- where NUM_SCENARIO is the simulated scenario id, data base ip is the IP where the data	 base is allocated and level log is the level that you are able to get in the standard output. 	This values can be INFO, DEBUG, ERROR.

-- clean.sh : bash script that cleans all temporaly files and log files
