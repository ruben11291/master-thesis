#!/bin/bash

icegridadmin --Ice.Config=../config/locator.cfg -e "application remove GeoCloudApp"

sleep 1
echo "Shutting down the nodes..."
icegridadmin --Ice.Config=../config/locator.cfg -e "node shutdown Nodo3"
sleep 1
icegridadmin --Ice.Config=../config/locator.cfg -e "node shutdown Nodo2"
sleep 1
icegridadmin --Ice.Config=../config/locator.cfg -e "node shutdown Nodo1"
