#!/bin/sh
echo "*********************************************************"
echo "Conexion con registry, carga de xml y despliegue de la "
echo "aplicación"
echo "*********************************************************"

echo "........................................................"
icegridadmin --Ice.Config=icegrid/locator.cfg -uuser -ppass -e "application add ./icegrid/CannonAppDist.xml"
echo "aplicacion desplegada correctamente"
sleep 3s
echo ""
echo ""


