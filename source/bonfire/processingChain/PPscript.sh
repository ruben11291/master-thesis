#Bash script for processing chain. Must be executed as d2pp user.

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
l0 /mnt/disco/job_orders/${jobOrder}$L0.$exten 2>&1 | tee l0.output
#rm -rf /mnt/disco/l0/output/*_[^C4DC]*
l0r /mnt/disco/job_orders/${jobOrder}$L0R.$exten
#rm -rf /mnt/disco/l0r/output/*_[^7851]*
l1a /mnt/disco/job_orders/${jobOrder}$L1A.$exten
#set +x
#l1a/output/DE2_L1A_000000_20130711T100120_20130711T100123_DE2_269_B4D4/DE2_MS1_L1A__1_20140602T165057.tif
scp /mnt/disco/l1a/output/DE2_L1A_000000_20130711T100120_20130711T100123_DE2_269_B4D4/DE2_MS1_L1A__1_20140602T165057.ti$
ssh root@${IP_GEOSERVER} "python /root/catalog_pp.py $path/DE2_MS1_L1A__1_20140602T165057.tif"

#rm -rf /mnt/disco/l1a/output/*_[^C555]*
#l1br /mnt/disco/job\ orders/${jobOrder}$LBR.$exten
#l1cr /mnt/disco/job\ orders/${jobOrder}$L1CR.$exten
#l1ct /mnt/disco/job\ orders/${jobOrder}$L1CT.$exten
#falta enviar a archive and catalog


