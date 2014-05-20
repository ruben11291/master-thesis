#!/bin/bash

# **********
# This script is used to assign an IP address from the BonFIRE WAN range to the control interface
# BonFIRE WAN is available on VLAN 2040 ; IP requests via DHCP
# Questions: vwall-ops@atlantis.ugent.be
# Tested with Debian 6
# Execute as ROOT or with sudo 
# **********

#Only execute script if not executed already
if [ ! -f /var/emulab/boot/controlif_bonfire ]; then
  #Init...
  BONFIRE_VLAN=2040

  #Install package for VLAN support
  apt-get install --yes vlan

  #Load module
  modprobe 8021q

  #Find out what interface is the control-interface:
  CONTROL_IF=`cat /var/emulab/boot/controlif`

  #Add vlan 2040 to control interface:
  vconfig add $CONTROL_IF $BONFIRE_VLAN

  #Request IP via DHCP
  dhclient ${CONTROL_IF}.${BONFIRE_VLAN}

  #Add a route to Bonfire WAN range
  ip route add 172.18.0.0/16 via 172.18.4.254

  #Write status file
  echo ${CONTROL_IF}.${BONFIRE_VLAN} > /var/emulab/boot/controlif_bonfire

fi
