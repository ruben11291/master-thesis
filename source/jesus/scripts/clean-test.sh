#!/bin/sh
echo "*********************************************************"
echo "Borrado de archivos generados"
echo "*********************************************************"

echo "........................................................"
rm -f src/*~ 
rm -f src/*.pyc
rm -f test/*pyc
rm -f test/*~
echo "archivos eliminados correctamente ..."
sleep 3s
echo ""
echo ""
