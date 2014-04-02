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

#Argentina is missing ,"Argentina":"planet-lab2.itba.edu.ar"
#Host where the ground stations will be allocated
hosts ={"Argentina":"planetlab1.pop-rs.rnp.br","China":"planetlab1.buaa.edu.cn","Spain":"planetlab2.dit.upm.es","Norway":"planetlab1.cs.uit.no","New Zealand":"planetlab1.cs.otago.ac.nz","EEUU":"planetlab1.csee.usf.edu","Israel":"planetlab2.mta.ac.il","Brazil":"planetlab1.pop-pa.rnp.br","Reunion Island":"lim-planetlab-1.univ-reunion.fr","Malaysia":"planetlab1.comp.nus.edu.sg","Canada":"planetlab-2.usask.ca","Australia":"pl1.eng.monash.edu.au"}

#Host where the BonFIRE cloud will be
bonfire_host = ("France","ple6.ipv6.lip6.fr")

ec = ExperimentController("test_ple")

# The username in this case is the slice name, the one to use for login in 
# via ssh into PlanetLab nodes. Replace with your own slice name.

slice = "ibbtple_geocloud"
pleuser="jonathan.becedas@elecnor-deimos.com"
plepass= os.environ["PL_PASS"]
ssh_key = "~/.ssh/id_rsa"
source_file = "/home/deimos/GeoCloudResources/E2E_0Gerardo.bin" #file that client will send
target_file = "data.txt"
port = 20000

#node1 = create_node(ec,slice,pleuser,plepass,hostname="planetlab1.u-strasbg.fr")
#node2 = create_node(ec,slice,pleuser,plepass,hostname="planetlab2.dit.upm.es")
nodes = [] 
apps = []


command_server = "iperf -s -f m -t 30 -i 1 -p %d -u" %(port)

#Creates the BonFIRE node and the application is added
bonfire_node = create_node(ec,slice,pleuser,plepass,hostname=bonfire_host[1],country=bonfire_host[0])
app_bonfire = create_app(ec,command_server,dependencies="iperf")
ec.register_connection(app_bonfire,bonfire_node)

node_app=dict()

for host in hosts:
	node = create_node(ec,slice,pleuser,plepass,country=host)
	command_client = "iperf -f m  -c %s  -t 3600 -p %d -i 1 -u > %d%s" % ( bonfire_host[1],port,node,target_file)	
	app = create_app(ec,command_client,dependencies="iperf",source=source_file)
	ec.register_connection(app,node)
	#The app will be started once the app_bf application is running
	apps.append(app)
	node_app[node] = app
	nodes.append(node)
	ec.register_condition(app,ResourceAction.START, app_bonfire, ResourceState.STARTED)


# Deploy the experiment:
ec.deploy()
ec.wait_finished(apps)

for node, app in node_app.iteritems():
	trace=ec.trace(node,str(node)+target_file)
	f = open(str(node)+"output.txt","w")
	f.write(trace)
	f.close()
#print ec.trace(app1,"stdout")
# Do the experiment controller shutdown:
ec.shutdown()

# END
