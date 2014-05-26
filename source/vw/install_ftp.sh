#!/bin/bash

sudo apt-get update
sudo apt-get install mysql-client ftp ftplib3 vsftpd
sudo sed -i "s/listen=YES/listen=NO/b" /etc/vsftpd.conf
sudo sed -i "s/#listen_ipv6=NO/listen_ipv6=YES/b" /etc/vsftpd.conf
sudo sed -i "s/anonymous_enable=YES/anonymous_enable=NO/b" /etc/vsftpd.conf
sudo sed -i "s/#local_enable=NO/local_enable=YES/b" /etc/vsftpd.conf
sudo sed -i "s/#write_enable=NO/write_enable=YES/b" /etc/vsftpd.conf
sudo sed -i "s/#local_umask/local_umask/b" /etc/vsftpd.conf
sudo sed -i "s/#chroot_list_file/chroot_list_file/b" /etc/vsftpd.conf
sudo mkdir -p /home/ftp/deimos
sudo mkdir /home/deimos
sudo useradd -d /home/deimos -g ftp deimos

chmod 777 -R /home
sudo touch /etc/vsftpd.chroot_list
sudo echo "deimos" > /etc/vsftpd.chroot_list

sudo service vsftpd restart