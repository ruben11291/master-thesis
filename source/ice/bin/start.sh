#!/bin/bash

. bin/common.sh

start "$@"

echo "Starting application..."
icegridadmin --Ice.Config=cfg/locator.cfg -e "application add app/GeoCloudApp.xml" 

