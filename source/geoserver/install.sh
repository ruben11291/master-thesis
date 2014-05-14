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
VERSIONGS=2.5
VERSIONT=7.0.53
PLUGIN=geoserver-${VERSIONGS}-csw-plugin.zip
WAR=geoserver-${VERSIONGS}-war.zip
APACHE=apache-tomcat-${VERSIONT}

apt-get update && apt-get upgrade -y
apt-get install unzip wget openjdk-6-jdk openjdk-6-jre -y
cd /tmp
rm -rf /tmp/geo* /tmp/apache* /usr/share/tomcat* /tmp/*.jar
wget --tries=10 downloads.sourceforge.net/project/geoserver/GeoServer/${VERSIONGS}/$WAR&& unzip ${WAR} && rm ${WAR}
wget --tries=10 apache.rediris.es/tomcat/tomcat-7/v${VERSIONT}/bin/${APACHE}.tar.gz && tar xvzf  ${APACHE}.tar.gz 
wget --tries=10 http://sourceforge.net/projects/geoserver/files/"GeoServer Extensions"/${VERSIONGS}/${PLUGIN} && unzip ${PLUGIN} && rm ${PLUGIN}
#http://downloads.sourceforge.net/project/geoserver/GeoServer%20Extensions/${VERSIONGS}/${PLUGIN}?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fgeoserver%2Ffiles%2FGeoServer%2520Extensions%2F2.5%2F&ts=1399541643&use_mirror=kent
export CATALINA_HOME=/usr/share/tomcat7/${APACHE}/
export JAVA_OPTS="-Xms1024m -Xmx10246m -XX:NewSize=256m -XX:MaxNewSize=356m -XX:PermSize=256m -XX:MaxPermSize=356m"


JAVA_HOME=/usr/lib/jvm/java-1.6.0-openjdk
JRE_HOME=/usr/lib/jvm/java-1.6.0-openjdk/jre
#export JAVA_HOME
#export JRE_HOME
PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
export PATH

mkdir /usr/share/tomcat7
mv /tmp/${APACHE} /usr/share/tomcat7

sed -i 's/"8080"/"80"/g' /usr/share/tomcat7/${APACHE}/conf/server.xml

mv /tmp/geoserver.war /usr/share/tomcat7/${APACHE}/webapps
sleep 2s

/usr/share/tomcat7/${APACHE}/bin/startup.sh
#/usr/share/tomcat7/${APACHE}/bin/startup.sh

sleep 2s

mv /tmp/*.jar /usr/share/tomcat7/apache-tomcat-7.0.53/webapps/geoserver/WEB-INF/lib/

#/usr/share/tomcat7/${APACHE}/bin/stop.sh
/usr/share/tomcat7/${APACHE}/bin/startup.sh


