#!/bin/sh
echo "*********************************************************"
echo " Lanzamiento de los nodos"
echo "*********************************************************"

echo "........................................................"
VBoxManage startvm "jagi-node1" --type headless &
echo "nodo1 lanzado"
sleep 1s

echo "........................................................"
VBoxManage startvm "jagi-node2" --type headless &
echo "nodo2 lanzado"
sleep 1s

echo "........................................................"
VBoxManage startvm "jagi-node3" --type headless &
echo "nodo3 lanzado"
sleep 1s
echo "Esperando 30 segundos a que arranque los tres nodos ....."
sleep 30s 
echo ""
echo ""


