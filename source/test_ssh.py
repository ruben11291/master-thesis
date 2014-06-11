#!/bin/bash --
# -*- coding:utf-8; tab-width:4; mode:shell-script -*-
import paramiko
from paramiko import SSHClient
# Set up the proxy (forwarding server) credentials
proxy_hostname = 'ssh.fr-inria.bonfire-project.eu'
proxy_username = 'geo-user'
proxy_port = 22

#Instantiate a client and connect to the proxy server
proxy_client = SSHClient()
proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
proxy_client.connect(
    proxy_hostname,
    port=proxy_port,
    username=proxy_username,
    key_filename='/home/ruben/.ssh/id_rsa.pub'
)

stdin, stdout, stderr = proxy_client.exec_command('ls -l')
print stdout.readlines()
# Get the client's transport and open a `direct-tcpip` channel passing
# the destination hostname:port and the local hostname:port
transport = proxy_client.get_transport()
dest_addr = ('172.18.240.209', 22)
local_addr = ('127.0.0.1', 22)
channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

# # Create a NEW client and pass this channel to it as the `sock` (along with
# # whatever credentials you need to auth into your REMOTE box
remote_client = SSHClient()
remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_client.connect('172.18.240.209', port=22, username='root', key_filename='/home/ruben/.ssh/id_rsa.pub',sock=channel)

# # `remote_client` should now be able to issue commands to the REMOTE box
stdin,stdout,stderr=remote_client.exec_command('tail -f a.txt')
print stdout.readlines()
