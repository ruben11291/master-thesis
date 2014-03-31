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


This directory contains all necesary files to create the data base and fills it.
The files will be explained as follows:

-- All_Scenarios.csv : contains the data of the interesting area for each satellite within scenarios.

-- Scenario_<NUM>_<NAME>: that files contains the Scenario's exported data from STK (Systems Tool Kit).

-- setDatabase.py : python script that fills the data base processing all the scenario files and all scenarios file.
   The execution of this script must be made (as root) as follows:
   -- python setDatabase <IP_DATA_BASE> <ALL_SCENARIOS_DATA> <SCENARIO_1> <SCENARIO_2> ...<SCENARIO_N>

-- makefile : bash script that  insert into the data base all scenario data automatically.
   The execution of this script must be made (as root) as follows:
   -- make 
