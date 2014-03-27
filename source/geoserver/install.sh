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

