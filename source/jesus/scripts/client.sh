#!/bin/sh
echo "*********************************************************"
echo "Ejecucion del cliente"
echo "*********************************************************"

echo "........................................................"
echo "cliente ejecutandose ..."
python src/client.py --Ice.Config=icegrid/locator.cfg "loader1 -t -e 1.1 @ LoaderServer.LoaderAdapter" "4"
echo "ejecucion del cliente terminada ..."
sleep 3s
echo ""
echo ""



