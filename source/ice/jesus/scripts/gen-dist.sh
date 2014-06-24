#!/bin/sh
echo "*********************************************************"
echo "Creacion de carpeta con binarios a desplegar"
echo "*********************************************************"

echo "........................................................"
sshpass -p "admin" ssh -o StrictHostKeyChecking=no root@jagi-node1.local -C "mkdir /etc/dist"
echo "carpeta creada correctamente ..."
sleep 3s


echo "........................................................"
sshpass -p "admin" scp -o StrictHostKeyChecking=no -r /tmp/DistributedSystem_grid/src/dist/*.ice root@jagi-node1.local:/etc/dist
sshpass -p "admin" scp -o StrictHostKeyChecking=no -r /tmp/DistributedSystem_grid/src/dist/*.py root@jagi-node1.local:/etc/dist
sshpass -p "admin" ssh -o StrictHostKeyChecking=no root@jagi-node1.local -C "chmod 777 /etc/dist/*"
echo "binarios copiados correctamente ..."	
sshpass -p "admin" ssh -o StrictHostKeyChecking=no root@jagi-node1.local -C "chown -R ice /etc/dist && icepatch2calc /etc/dist"
echo "directorio de binarios preparados para el despliegue"
sleep 3s
echo ""
echo ""
