
import paramiko
import time
from paramiko import SSHClient
# Set up the proxy (forwarding server) credentials
proxy_hostname = 'ssh.fr-inria.bonfire-project.eu'
proxy_username = 'geo-user'
proxy_port = 22

#Instantiate a client and connect to the proxy server
proxy_client = SSHClient()
proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
time1=time.time()
proxy_client.connect(
    proxy_hostname,
    port=proxy_port,
    username=proxy_username,
    key_filename='/home/deimos/.ssh/id_rsa.pub'
)
time2=time.time()
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
time3=time.time()
remote_client.connect('172.18.240.209', port=22, username='root', key_filename='/home/deimos/.ssh/id_rsa.pub',sock=channel)
time4=time.time()
print "Time first connection ", time2-time1
print "Time second connection ", time4-time3

while(True):
    time5=time.time()
# # `remote_client` should now be able to issue commands to the REMOTE box
    stdin,stdout,stderr=remote_client.exec_command('ls')
    time6=time.time()
    print "Time  command ", time6-time5


