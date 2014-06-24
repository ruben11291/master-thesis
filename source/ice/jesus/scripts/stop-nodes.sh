#!/bin/sh
echo "*********************************************************"
echo "Paramos los nodos en ejecución"
echo "*********************************************************"

echo "........................................................"
VBoxManage controlvm "jagi-node3" poweroff
echo "nodo3 parado"
echo "........................................................"
VBoxManage controlvm "jagi-node2" poweroff
echo "nodo2 parado"
echo "........................................................"
VBoxManage controlvm "jagi-node1" poweroff
echo "nodo1 parado"
sleep 3s
echo ""
echo ""
