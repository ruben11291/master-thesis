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

#Host where the ground stations will be allocated
hosts ={"China":"planetlab1.buaa.edu.cn","Spain":"planetlab2.dit.upm.es","Uruguay":"planetlab1-santiago.lan.redclara.net","PuertoRico":"planetlab-01.ece.uprm.edu","Argentina":"planet-lab1.itba.edu.ar","Israel":"planet1.cs.huji.ac.il","Brazil":"planetlab1.pop-pa.rnp.br","ReunionIsland":"lim-planetlab-1.univ-reunion.fr","Malaysia":"planetlab1.comp.nus.edu.sg","Canada":"planetlab-1.usask.ca","Australia":"plnode01.cs.mu.oz.au"}
#Host where the BonFIRE cloud will be
bonfire_host = ("France","ple6.ipv6.lip6.fr")

ec = ExperimentController("test_ple")

# The username in this case is the slice name, the one to use for login in 
# via ssh into PlanetLab nodes. Replace with your own slice name.

slice = "ibbtple_geocloud"
pleuser="jonathan.becedas@elecnor-deimos.com"
plepass="deimos_space14"
ssh_key = "/home/deimos/.ssh/id_rsa"
source_file = "E2E_0Gerardo.bin" #file that client will send
port = 20000 #port in which the iperf will run

#node1 = create_node(ec,slice,pleuser,plepass,hostname="planetlab1.u-strasbg.fr")
#node2 = create_node(ec,slice,pleuser,plepass,hostname="planetlab2.dit.upm.es")
nodes = [] 
apps = []

bonfire = create_node(ec,slice,pleuser,plepass,hostname=bonfire_host[1],country=bonfire_host[0])
command="iperf -s -p %d -f m"%(port)
app_bf = create_app(ec,command,dependencies="iperf")
ec.register_connection(app_bf,bonfire)


for host in hosts:
	node = create_node(ec,slice,pleuser,plepass,hostname=hosts[host],country=host)	
	command="iperf -f m -F $SRC/%s -p %d -o %s -c %s"%(source_file, port, target_file, bonfire.ip())
	app = create_app(ec,command,dependencies="iperf",source=source_file)
	ec.register_connection(app,node)
	#The app will be started once the app_bf application is running
	ec.register_condition(app,ResourceAction.START, app_bf, ResourceState.STARTED)
	apps.append(app)
	nodes.append(node)

# Deploy the experiment:
ec.deploy()
ec.wait_finished(apps)

print ec.trace(app1,"stdout")
# Do the experiment controller shutdown:
ec.shutdown()

# END
