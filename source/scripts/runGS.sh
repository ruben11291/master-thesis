#!/bin/bash


if [ $# -lt '1' ] 
then
	echo "Error with arguments. Must introduce the id scenario to simulate it!"
	exit
fi
scenario=$1
level=$2

for num in {0..11};
do
	python groundstation.py $num $scenario localhost $2&
	sleep 1
done

