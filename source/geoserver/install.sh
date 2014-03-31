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

apt-get update && apt-get upgrade -y
apt-get install unzip wget openjdk-6-jdk openjdk-6-jre -y
cd /tmp
rm -rf /tmp/geo* /tmp/apache* /usr/share/tomcat*
wget --tries=10 downloads.sourceforge.net/project/geoserver/GeoServer/2.5/geoserver-2.5-war.zip&& unzip geoserver-2.5-war.zip && rm geoserver-2.5-war.zip
wget --tries=10 apache.rediris.es/tomcat/tomcat-7/v7.0.52/bin/apache-tomcat-7.0.52.tar.gz && tar xvzf  apache-tomcat-7.0.52.tar.gz 

export CATALINA_HOME=/usr/share/tomcat7/apache-tomcat-7.0.52/
export JAVA_OPTS="-Xms1024m -Xmx10246m -XX:NewSize=256m -XX:MaxNewSize=356m -XX:PermSize=256m -XX:MaxPermSize=356m"

JAVA_HOME=/usr/lib/jvm/java-1.6.0-openjdk
JRE_HOME=/usr/lib/jvm/java-1.6.0-openjdk/jre
export JAVA_HOME
export JRE_HOME
PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
export PATH

mkdir /usr/share/tomcat7
mv /tmp/apache-tomcat-7.0.52 /usr/share/tomcat7

mv /tmp/geoserver.war /usr/share/tomcat7/apache-tomcat-7.0.52/webapps

/usr/share/tomcat7/apache-tomcat-7.0.52/bin/startup.sh

