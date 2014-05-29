#!/bin/bash

sudo apt-get update
sudo apt-get install mysql-client ftp ftplib3 vsftpd -y
sudo sed -i "s/listen=YES/listen=NO/" /etc/vsftpd.conf
sudo sed -i "s/#listen_ipv6=NO/listen_ipv6=YES/" /etc/vsftpd.conf
sudo sed -i "s/#listen_ipv6=YES/listen_ipv6=YES/" /etc/vsftpd.conf
sudo sed -i "s/anonymous_enable=YES/anonymous_enable=NO/" /etc/vsftpd.conf
sudo sed -i "s/#local_enable=NO/local_enable=YES/" /etc/vsftpd.conf
sudo sed -i "s/#local_enable=YES/local_enable=YES/" /etc/vsftpd.conf
sudo sed -i "s/#write_enable=NO/write_enable=YES/" /etc/vsftpd.conf
sudo sed -i "s/#write_enable=YES/write_enable=YES/" /etc/vsftpd.conf
sudo sed -i "s/#local_umask/local_umask/" /etc/vsftpd.conf
sudo sed -i "s/#chroot_list_file/chroot_list_file/" /etc/vsftpd.conf
sudo mkdir -p /home/ftp/deimos
sudo mkdir /home/deimos
sudo useradd -d /home/deimos -g ftp  deimos
sudo chmod 777 -R /home
sudo touch /etc/vsftpd.chroot_list
sudo su
echo "deimos:deimos"|chpasswd
echo "deimos" >> /etc/vsftpd.chroot_list
sudo service vsftpd restart