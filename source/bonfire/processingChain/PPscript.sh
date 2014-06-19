#!/bin/bash

jobOrder=job_order_DCM_
exten=xml
L0=L0
L0R=L0R
L1A=L1A
L1BG=L1BG
L1BR=L1BR
L1CR=L1CR
L1CT=L1CT
outfile=$1
export IP_GEOSERVER=172.18.249.22
#set -x
path=/usr/share/tomcat7/apache-tomcat-7.0.53/webapps/geoserver/data/data
#su - d2pp
. ~/.bashrc
l0 /mnt/disco/job_orders/${jobOrder}$L0.$exten &> l0.output #2>&1 | tee l0.output
#rm -rf /mnt/disco/l0/output/*_[^C4DC]*
echo "L0 processed!"
l0r /mnt/disco/job_orders/${jobOrder}$L0R.$exten &> lor.output
echo "L0R processed!"
#rm -rf /mnt/disco/l0r/output/*_[^7851]*
l1a /mnt/disco/job_orders/${jobOrder}$L1A.$exten  &> l1a.output
echo "L1A processed!"
order=python" "/root/catalog_pp.py 
image=$path/LC81990332014075LGN00_RGB.tif #
scenario=Scenario1
scenario=$2 
execute=$order" "$image" "$scenario" "${outfile}
#set +x
#echo $execute
echo "Sending to catalog module ..."
#l1a/output/DE2_L1A_000000_20130711T100120_20130711T100123_DE2_269_B4D4/DE2_MS1_L1A__1_20140602T165057.tif
scp /mnt/disco/LC81990332014075LGN00_RGB.tif root@${IP_GEOSERVER}:$path
ssh root@${IP_GEOSERVER} $execute

#rm -rf /mnt/disco/l1a/output/*_[^C555]*
#l1br /mnt/disco/job\ orders/${jobOrder}$LBR.$exten
#l1cr /mnt/disco/job\ orders/${jobOrder}$L1CR.$exten
#l1ct /mnt/disco/job\ orders/${jobOrder}$L1CT.$exten
#falta enviar a archive and catalog


