#!/bin/bash

## BEGIN INIT INFO
# Provides: getip
# Required-Start: $mysql
# Short-Description: Update the /etc/hosts file
### END INIT INFO

sed "2i$(hostname -I |cut -f 1 -d ' ') $(hostname)" /etc/hosts

