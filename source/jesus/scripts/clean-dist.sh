#!/bin/sh
echo "*********************************************************"
echo "Borrado de archivos generados en el despliegue"
echo "*********************************************************"

echo "........................................................"
sshpass -p "admin" ssh -o StrictHostKeyChecking=no root@jagi-node1.local -C "rm -Rf /etc/dist"
sshpass -p "admin" ssh -o StrictHostKeyChecking=no root@jagi-node1.local -C "rm -Rf /var/lib/ice/icegrid/node1/* && rm -Rf /var/lib/ice/icegrid/registry/*"
sshpass -p "admin" ssh -o StrictHostKeyChecking=no root@jagi-node2.local -C "rm -Rf /var/lib/ice/icegrid/node1/*"
sshpass -p "admin" ssh -o StrictHostKeyChecking=no root@jagi-node3.local -C "rm -Rf /var/lib/ice/icegrid/node1/*"
echo "archivos eliminados correctamente ..."
sleep 5s
echo ""
echo ""
