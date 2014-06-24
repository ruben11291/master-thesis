#!/bin/sh
echo "*********************************************************"
echo "Cambiamos los archivos de configuracion para el despliegue"
echo "*********************************************************"

echo "........................................................"
sshpass -p "admin" scp -o StrictHostKeyChecking=no -r /tmp/DistributedSystem_grid/icegrid/icegridnode-jagi-node1.cfg root@jagi-node1.local:/etc/icegridnode.conf
sshpass -p "admin" ssh -o StrictHostKeyChecking=no root@jagi-node1.local -C "service icegridnode restart"
echo "Configuración nodo1 cambiada"
sleep 5
echo "........................................................"
sshpass -p "admin" scp -o StrictHostKeyChecking=no -r /tmp/DistributedSystem_grid/icegrid/icegridnode-jagi-node2.cfg root@jagi-node2.local:/etc/icegridnode.conf
sshpass -p "admin" ssh -o StrictHostKeyChecking=no root@jagi-node2.local -C "service icegridnode restart"
echo "Configuración nodo2 cambiada"
sleep 5
echo "........................................................"
sshpass -p "admin" scp -o StrictHostKeyChecking=no -r /tmp/DistributedSystem_grid/icegrid/icegridnode-jagi-node3.cfg root@jagi-node3.local:/etc/icegridnode.conf
sshpass -p "admin" ssh -o StrictHostKeyChecking=no root@jagi-node3.local -C "service icegridnode restart"
echo "Configuración nodo3 cambiada"
sleep 3s
echo ""
echo ""
