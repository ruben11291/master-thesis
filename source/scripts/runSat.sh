#!/bin/bash


if [ $# -lt '1' ] 
then
	echo "Error with arguments. Must introduce the id scenario to simulate it!"
	exit
fi
scenario=$1
level=$2

for num in {0..16};
do
	python satelite.py $num $scenario localhost $2&
done

