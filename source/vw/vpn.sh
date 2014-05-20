#Bash script to install the openvpn service and to configure it for 
#accesing BonFIRE WAN through a tunnel

#!/bin/bash
apt-get install openvpn

wget --no-check-certificate http://doc.bonfire-project.eu/R4.0.5/_static/openvpn/bonfireca.cert -O /etc/openvpn/bonfireca.cert"/>
wget --no-check-certificate http://doc.bonfire-project.eu/R4.0.5/_static/openvpn/bonfire-openvpn-user-cert.pem -O /etc/openvpn/bonfire-openvpn-user-cert.pem
wget --no-check-certificate http://doc.bonfire-project.eu/R4.0.5/_static/openvpn/bonfire-openvpn-user-key.pem -O /etc/openvpn/bonfire-openvpn-user-key.pem
wget --no-check-certificate http://doc.bonfire-project.eu/R4.0.5/_static/openvpn/client.conf -O /etc/openvpn/client.conf

/etc/init.d/openvpn restart
