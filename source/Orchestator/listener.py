 #!/usr/bin/env python
import orchestator
import ftplib import FTP

# ftp = FTP('localhost')
# ftp.login('deimos','deimos')


class listener:
   def __init__(self, orchesta):
       Gstations =[]
       ftpconex = []
       orchestator = orchesta;
       for i in range(0,12):
           Gstations.append(["localhost",2000+i])
       
       self.connect()
       print "Listener ready"

   def connect():
       for i in Gstations:
           #ftpconex[i] = FTP(i[0],i[1])
           ftpconex[i] = FTP(i[0])

   
