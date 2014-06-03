#!/bin/bash

jobOrder=job_order_DCM_
exten=xml
L0=L0
LOR=L0R
L1A=L1A
L1BG=L1BG
L1BR=L1BR
L1CR=L1CR
L1CT=L1CT
outfile=$1

su - d2pp
. ~/.bashrc
l0 /mnt/disco/job_orders/${jobOrder}$L0.$exten
#rm -rf /mnt/disco/l0/output/*_[^C4DC]*
l0r /mnt/disco/job_orders/${jobOrder}$L0R.$exten
#rm -rf /mnt/disco/l0r/output/*_[^7851]*
l1a /mnt/disco/job_orders/${jobOrder}$LBG.$exten

scp /mnt/disco/imagefull root@${IP_GEOSERVER}:/usr/share/tomcat7/apache-tomcat-7.0.53/webapps/geoserver/data/data/$1
ssh root@${IP_GEOSERVER} "python add_image.py $1"

#rm -rf /mnt/disco/l1a/output/*_[^C555]*
#l1br /mnt/disco/job\ orders/${jobOrder}$LBR.$exten
#l1cr /mnt/disco/job\ orders/${jobOrder}$L1CR.$exten
#l1ct /mnt/disco/job\ orders/${jobOrder}$L1CT.$exten
#falta enviar a archive and catalog
