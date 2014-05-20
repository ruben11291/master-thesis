#!/bin/bash

## BEGIN INIT INFO
# Provides: getip
# Required-Start: $mysql
# Short-Description: Update the /etc/hosts file
### END INIT INFO

ip=`hostname -i`
name=`hostname`
l = "2i$ip $name"
sed -i $l /etc/hosts

l="2i$ip\(.\{1})$name/\1 \2"
deimos@deimos-virtual-machine:~$ sed -e $l /etc/hosts

