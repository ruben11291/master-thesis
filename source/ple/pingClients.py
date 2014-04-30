#!/usr/bin/env python
import pdb
from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState
import os


def create_node(ec,slice,pluser,plpass,country):
	node = ec.register_resource("PlanetlabNode")

	ec.set(node,"username",slice)
	ec.set(node,"pluser",pluser)
	ec.set(node,"plpassword",plpass)
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


#################
nodes_customers=("Argentina","Australia")
#"Austria","Belgium","Brazil")
#"Canada","China","Cyprus","CzechRepublic","Denmark","Ecuador","Egypt","Findland","France","Germany","Greece","HongKong","Hungary","Iceland","India","Ireland","Israel","Italy","Japan","Jordan","Korea","Mexico","Netherlands","NewZealand","Norway","Pakistan","Poland","Portugal","PuertoRico", "Romania","RussianFederation","Singapore","Slovenia","Spain","SriLanca", "Sweeden","Switzerland","Taiwan","Thailand","Tunisia","Turkey","UnitedKingdom","UnitedStates","Uruguay","Venezuela"]

ec = ExperimentController("test_ple")

# The username in this case is the slice name, the one to use for login in
# via ssh into PlanetLab nodes. Replace with your own slice name.

slice = "ibbtple_geocloud"
pleuser= os.environ["PL_USER"]
plepass= os.environ["PL_PASS"]
ssh_key = "~/.ssh/id_rsa"
#source_file = "/home/deimos/GeoCloudResources/E2E_0Gerardo.bin" #file that client will send
target_file = "data.txt"
port = 20004
seconds = 43200
seconds = 3600 #1 h
nodes = []
apps = []

node_app=dict()

for host in nodes_customers:
	print host
	node= create_node(ec,slice,pleuser,plepass,host)
	nodes.append(node)
	command_client = "ping %s -w %d  > node%d.out " % ("ple6.ipv6.lip6.fr",seconds,node)
	app=create_app(ec,command_client)
	ec.register_connection(app,node)
	apps.append(app)
	node_app[node] =app
#print "NODE under APP :" ,node_app	

# Deploy the experiment:

#pdb.set_trace()
ec.deploy()

ec.wait_finished(apps)


for node, app in node_app.iteritems():
#	print "iteration :",node,app
	trace=ec.trace(app,"node%d.out"%(node))
	f = open(ec.get(node,"country")+":"+ec.get(node,"ip")+":"+"node%d_PING.out"%(node),"w")
	f.write(trace)
	f.close()
#print ec.trace(app1,"stdout")
# Do the experiment controller shutdown:
ec.shutdown()

# END
