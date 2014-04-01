#!/usr/bin/env python
import pdb
from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState
import os


def create_node(ec,slice,pluser,plpass,hostname=None,country=None):
	node = ec.register_resource("PlanetlabNode")
	
	ec.set(node,"username",slice)
	ec.set(node,"pluser",pluser)
	ec.set(node,"plpassword",plpass)
	if hostname:
		ec.set(node,"hostname",hostname)
	if country:
		ec.set(node,"country",country)
	
	ec.set(node, "cleanHome", True)
	ec.set(node, "cleanProcesses", True)

	return node

def create_app(ec,command,sudo=None,dependencies=None,source=None):
	app = ec.register_resource("LinuxApplication")
	if sudo:
		ec.set(app,"sudo",sudo)
	if dependencies:
		ec.set(app,"depends",dependencies)
	if source:
		ec.set(app,"sources",source)

	ec.set(app,"command",command)
	return app



ec = ExperimentController("test_ple")

# The username in this case is the slice name, the one to use for login in 
# via ssh into PlanetLab nodes. Replace with your own slice name.

slice = "ibbtple_geocloud"
pleuser="jonathan.becedas@elecnor-deimos.com"
plepass="******" #Enter the password
ssh_key = "/home/deimos/.ssh/id_rsa"
source_file = "/home/deimos/GeoCloudResources/E2E_0Gerardo.bin" #file that client will send
target_file = "iperfOut.txt"





#Host where the BonFIRE cloud will be
bonfire_host = ("France","ple6.ipv6.lip6.fr")

#Creates the BonFIRE node and the application is added
bonfire = create_node(ec,slice,pleuser,plepass,hostname=bonfire_host[1],country=bonfire_host[0])
command="iperf -s -f m -t 30 -D"
#command = "ping -c 5 planetlab2.utt.fr"
print "Server command ",command
app_bf = create_app(ec,command,dependencies="iperf")
ec.register_connection(app_bf,bonfire)

node1 = create_node(ec,slice,pleuser,plepass,hostname="planetlab2.utt.fr")
command="iperf -f m -F $SRC%s -o $SRC/%s -c %s -t 30"%(source_file, target_file, bonfire_host[1])
#command="ping -c 5 "+bonfire_host[1]
print "Client command ",command
app = create_app(ec,command,dependencies="iperf",source=source_file)
ec.register_connection(app,node1)

#The app will be started once the app_bf application is running

ec.register_condition(node1, ResourceAction.DEPLOY, bonfire, ResourceState.PROVISIONED)
ec.register_condition(bonfire, ResourceAction.START , node1,ResourceState.READY)
ec.register_condition(node1, ResourceAction.START, bonfire, ResourceState.STARTED)
#ec.register_condition(app, ResourceAction.START, app_bf, ResourceState.STARTED)
#ec.register_condition(app,ResourceAction.START, app_bf, ResourceState.STARTED)


# Deploy the experiment:
ec.deploy()
pdb.set_trace()
ec.wait_finished([app,app_bf])


trace=ec.trace(app,"$SRC/"+target_file)
f = open("output.txt","w")
f.write(trace)
f.close()

#print ec.trace(app1,"stdout")
# Do the experiment controller shutdown:
ec.shutdown()

# END
