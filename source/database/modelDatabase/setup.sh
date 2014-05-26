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


#!/bin/bash
model=modelDataBase

apt-get update
apt-get upgrade -y
apt-get install mysql-server -y
apt-get install build-essential python-dev libmysqlclient-dev -y
apt-get install python-mysqldb

service mysql restart
mysql -u root -p < modelDataBase
sed "s/bind-address/bind-address $(hostname -I | cut -f 1 -d ' ') #/g" /etc/mysql/my.cnf
service mysql restart 

#GRANT ALL PRIVILEGES ON Scenaries.* TO "root"@"%";


