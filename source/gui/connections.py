
#!/usr/bin/env python

#
#    Copyright (C) 2014 DEIMOS
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Ruben Perez <ruben.perez@deimos-space.com>

import os
import paramiko
from paramiko import SSHClient
import threading

class VWConnection():

    def __init__(self,id,host,username,key,proxy_hostname,proxy_username,proxy_port,proxy_key):
        self.id=id
        self.proxy_client = SSHClient()
        self.proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.proxy_client.connect(
            proxy_hostname,
            port=proxy_port,
            username=proxy_username,
            password="deimos-space",
            key_filename=key
            )
        self.transport = self.proxy_client.get_transport()
        dest_addr = (host, 22)
        local_addr = ('127.0.0.1', 22)
        self.channel = self.transport.open_channel("direct-tcpip", dest_addr, local_addr)
        
        # # Create a NEW client and pass this channel to it as the `sock` (along with
        # # whatever credentials you need to auth into your REMOTE box
        self.remote_client = SSHClient()
        self.remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.remote_client.connect(host, password="deimos-space",port=22, username='jbecedas', key_filename=proxy_key,sock=self.channel)
    
    def close(self):
        self.stop()
        self.proxy_client.close()
        self.remote_client.close()
        
    def getId(self):
        return self.id

    def execute(self,command):
        self.thread = Command(self.remote_client,command)
        self.thread.start()
        #stdin,stdout,stderr=self.remote_client.exec_command(command)
        #return stdout

    def stop(self):
        print "Stopping"
        print self.thread.isAlive()
        if self.thread.isAlive():
            try:
                self.thread._Thread__stop()
                print self.thread.isAlive()
            except:
                print(str(self.thread.getId()) + ' could not be terminated')

class Command(threading.Thread):
    def __init__(self,remote_client,command):
        threading.Thread.__init__(self)
        self.command = command
        self.client = remote_client

    def run(self):
        print "Starting command"
        stdin,stdout,stderr=self.client.exec_command(self.command)
        #print stderr.readlines()
        #print stdout.readlines()
        
if __name__=="__main__":
    a = VWConnection(1,"n144-07b.wall1.ilabt.iminds.be",'jbecedas','/home/deimos/.ssh/id_rsa.pub','bastion.test.iminds.be','jbecedas',22,'/home/deimos/Descargas/emulabcert.pem')
    out = a.execute("tail -f a.txt")
    a.stop()
    print "caca"
    #print out.readlines()
