#!/bin/bash

apt-get update
apt-get upgrade -y
apt-get install mysql-server -y
apt-get install build-essential python-dev libmysqlclient-dev -y
apt-get install python-mysqldb

