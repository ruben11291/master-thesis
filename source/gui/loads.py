
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



class Loads():

    def __init__(self,host,experimentController,time,threadLock):
        self.host = host
        self.experimentController = experimentController;
        self.time=time
        self.threadLock=threadLock
        self.timer = 

    def stop(self):
        self.stop()

    def run(self):
        print self.host
        out =os.system("ssh -A -o StrictHostKeyChecking=no -i /home/deimos/.ssh/id_rsa jbecedas@%s"%(self.host)+" -oPort=22 -oProxyCommand='ssh -o StrictHostKeyChecking=no -e none -i /home/deimos/Descargas/emulabcert.pem -oPort=22 jbecedas@bastion.test.iminds.be nc -w 5 %h %p' "+self.order)
        self.threadLock.acquire()
        self.experimentController.log(str(self.msg) +" "+str(self.id)+ " ha acabado su ejecucion")
        self.threadLock.release()
        print "Out ",out
        if out != 0:
            self.experimentController.error(self)
       
