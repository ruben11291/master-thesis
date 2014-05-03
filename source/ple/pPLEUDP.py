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
hosts ={"Argentina":"planetlab1.pop-rs.rnp.br","China":"planetlab1.buaa.edu.cn","Spain":"planetlab2.dit.upm.es","Norway":"planetlab1.cs.uit.no","New Zealand":"planetlab1.cs.otago.ac.nz","Florida":"planetlab1.csee.usf.edu","Israel":"planetlab2.mta.ac.il","Brazil":"planetlab1.pop-pa.rnp.br","Reunion Island":"lim-planetlab-1.univ-reunion.fr","Malaysia":"planetlab1.comp.nus.edu.sg","Canada":"planetlab-2.usask.ca","Australia":"pl1.eng.monash.edu.au"}
#hosts={"New Zealand":"planetlab1.cs.otago.ac.nz"}
#Host where the BonFIRE cloud will be
bonfire_host = ("France","ple6.ipv6.lip6.fr")

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


command_server = "timeout %dm iperf -s -f m -i 1 -p %d -u" %((seconds/60)+2,port)#the timeout takes in advantage to 5 minutes

#Creates the BonFIRE node and the application is added
bonfire_node = create_node(ec,slice,pleuser,plepass,hostname=bonfire_host[1])
app_bonfire = create_app(ec,command_server,dependencies="iperf")
ec.register_connection(app_bonfire,bonfire_node)
apps.append(app_bonfire)
node_app=dict()

#print "Deployed nodes: ",nodes


for host in hosts:
	node = create_node(ec,slice,pleuser,plepass,hostname=hosts[host],country=host)
	nodes.append(node)
	command_client = "iperf  -i 1 -f m -c %s -t %d -p %d  -y c -u > node%d.out " % (bonfire_host[1],seconds,port,node)
	app = create_app(ec,command_client,dependencies="iperf")
	ec.register_connection(app,node)
	#The app will be started once the app_bf application is running
	apps.append(app)
	node_app[node] = app
	ec.register_condition(app,ResourceAction.START, app_bonfire, ResourceState.STARTED)

#print "NODE under APP :" ,node_app	

# Deploy the experiment:

#pdb.set_trace()
ec.deploy()

ec.wait_finished(apps)


for node, app in node_app.iteritems():
#	print "iteration :",node,app
	trace=ec.trace(app,"node%d.out"%(node))
	f = open(ec.get(node,"country")+":"+ec.get(node,"ip")+":"+"node%d.out"%(node),"w")
	f.write(trace)
	f.close()
#print ec.trace(app1,"stdout")
# Do the experiment controller shutdown:
ec.shutdown()

# END
