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

def create_node2(ec,slice,pluser,plpass,country=None):
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

hosts={"New Zealand":"planetlab1.cs.otago.ac.nz"}
#Host where the BonFIRE cloud will be
bonfire_host = ("France","ple6.ipv6.lip6.fr")
ec = ExperimentController("test_ple")
slice = "ibbtple_geocloud"
pleuser= os.environ["PL_USER"]
plepass= os.environ["PL_PASS"]
ssh_key = "~/.ssh/id_rsa"
seconds = 3600 #1 h
nodes = []
apps = []

node = create_node(ec,slice,pleuser,plepass,hostname="ple6.ipv6.lip6.fr")

#node_nz1=planetlab1.cs.otago.ac.nz
node_nz2="planetlab-1.cs.auckland.ac.nz" #customer
nodes.append(node)
command_client = "ping %s -w %d  > node%d.out " % (node_nz2,seconds,node)
app = create_app(ec,command_client)
ec.register_connection(app,node)

ec.deploy()

ec.wait_finished(app)


trace=ec.trace(app,"node%d.out"%(node))
f = open("NZ:"+":"+"node%d_PING.out"%(node),"w")
f.write(trace)
f.close()
#print ec.trace(app1,"stdout")
# Do the experiment controller shutdown:
ec.shutdown()

# END
