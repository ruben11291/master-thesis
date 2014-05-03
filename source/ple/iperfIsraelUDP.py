#!/usr/bin/env python
import pdb
from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState
import os


def create_node(ec,slice,pluser,plpass,hostname=None):
	node = ec.register_resource("PlanetlabNode")

	ec.set(node,"username",slice)
	ec.set(node,"pluser",pluser)
	ec.set(node,"plpassword",plpass)
	ec.set(node,"hostname",hostname)

	ec.set(node, "cleanHome", True)
	ec.set(node, "cleanProcesses", True)

	return node
def create_node2(ec,slice,pluser,plpass,country):
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


# The username in this case is the slice name, the one to use for login in
# via ssh into PlanetLab nodes. Replace with your own slice name.
ec = ExperimentController("test_ple")
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

# for host in nodes_customers:
# 	print host
# 	node= create_node(ec,slice,pleuser,plepass,host)
# 	nodes.append(node)
# 	command_client = "ping %s -w %d  > node%d.out " % ("ple6.ipv6.lip6.fr",seconds,node)
# 	app=create_app(ec,command_client)
# 	ec.register_connection(app,node)
# 	apps.append(app)
# 	node_app[node] =app
#print "NODE under APP :" ,node_app
#No: Austria,Cyprus*,Denmark,Egypt*,Ecuador*,Iceland,India,Jordan,Mexico,Korea, Republic of, Pakistan,Puerto Rico,Romania,Slovenia,Sri Lanka,Tunisia,Turkey,Thailand,Venezuela,Uruguay,Taiwan.
nodes_customers=("Argentina","Australia","Belgium","Brazil","Canada","China","Czech Republic","Finland","France","Greece","Germany","Hong Kong","Hungary","Korea, Republic of","Ireland","Israel","Italy","Japan","Netherlands","New Zealand","Norway","Portugal","Poland","Russian Federation","Singapore","Spain","Sweden","Switzerland","Thailand","United Kingdom","United States")
# node= create_node(ec,slice,pleuser,plepass,"Taiwan")
# nodes.append(node)
# command_client = "ping %s -w %d  > node%d.out " % ("ple6.ipv6.lip6.fr",seconds,node)
# app=create_app(ec,command_client)
# ec.register_connection(app,node)
# apps.append(app)
# node_app[node] =app


target_file = "data.txt"
port = 20004
seconds = 43200
seconds = 3600 #5 h
nodes = []
apps = []


command_server = "timeout %dm iperf -s -f m -i 1 -p %d -u" %((seconds/60)+2,port)#the timeout takes in advantage to 5 minutes
bonfire_host = ("France","ple6.ipv6.lip6.fr")

#Creates the BonFIRE node and the application is added
bonfire_node = create_node(ec,slice,pleuser,plepass,hostname=bonfire_host[1])
app_bonfire = create_app(ec,command_server,dependencies="iperf")
ec.register_connection(app_bonfire,bonfire_node)
apps.append(app_bonfire)
node_app=dict()



node= create_node2(ec,slice,pleuser,plepass,"Israel")
nodes.append(node)
command_client = "iperf  -i 1 -f m -c %s -t %d -p %d   -u> node%d.out " % (bonfire_host[1],seconds,port,node)
app = create_app(ec,command_client,dependencies="iperf")
ec.register_connection(app,node)
node_app[node] =app
ec.register_condition(app,ResourceAction.START, app_bonfire, ResourceState.STARTED)

#pdb.set_trace()
ec.deploy()

ec.wait_finished(apps)


trace=ec.trace(app,"node%d.out"%(node))
f = open(ec.get(node,"country")+":"+ec.get(node,"ip")+":"+"node%d_IPERF.out"%(node),"w")
f.write(trace)
f.close()
#print ec.trace(app1,"stdout")
# Do the experiment controller shutdown:
ec.shutdown()

# END
