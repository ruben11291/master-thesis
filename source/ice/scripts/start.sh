#!/bin/bash    

echo "Creating directories..."
mkdir -p ../data/nodo1 ../data/nodo2 ../data/nodo3 ../data/registry
echo "Deploying Node1..."
icegridnode --Ice.Config=../config/nodo1.cfg --daemon --nochdir
sleep 1

echo "Deploying Node2..."
icegridnode --Ice.Config=../config/nodo2.cfg --daemon --nochdir
sleep 1 
echo "Deploying Node3..."
icegridnode --Ice.Config=../config/nodo3.cfg --daemon --nochdir
sleep 1
echo "Starting application..."
icegridadmin --Ice.Config=../config/locator.cfg -e "application add ../src/GeocloudApp.xml"
sleep 1