
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

class Loads():

    def __init__(self,host,username,key,proxy_hostname,proxy_username,proxy_port,proxy_key):
        self.results=[0,0,0,0,0,0,0]
        self.proxy_client = SSHClient()
        self.proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.proxy_client.connect(
            proxy_hostname,
            port=proxy_port,
            username=proxy_username,
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
        self.remote_client.connect(host, port=22, username='root', key_filename=proxy_key,sock=self.channel)
        self.timer_thread= threading.Timer(0.2,self.__get_load)
        self.timer_thread.start()

    def __get_load(self):
        stdin,stdout,stderr=self.remote_client.exec_command('python getload.py')
        tmp = stdout.readlines()[0].rstrip()[1:-1].split(',')
        self.results = [float(p) for p in tmp]
        self.timer_thread = threading.Timer(0.2,self.__get_load)
        self.timer_thread.start()
        

    def stop(self):
        self.timer_thread.cancel()
        self.proxy_client.close()
        self.remote_client.close()

    def get_load(self):
        #b=shlex.split("ssh -A -o StrictHostKeyChecking=no -i /home/deimos/.ssh/id_rsa root@%s"%(self.host)+" -oPort=22 -oProxyCommand='ssh -o StrictHostKeyChecking=no  -oPort=22 geo-user@ssh.fr-inria.bonfire-project.eu nc -w 5 %h %p' "+"python getload.py")
        #print b
        #out = subprocess.check_output(b)
        return self.results
       

if __name__=="__main__":
    a = Loads("172.18.240.209",'root','/home/deimos/.ssh/id_rsa.pub','ssh.fr-inria.bonfire-project.eu','geo-user',22,'/home/deimos/.ssh/id_rsa.pub')
    out = a.get_load()
    print out
