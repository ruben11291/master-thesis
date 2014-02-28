#!/usr/bin/env python
import pdb
from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState

import os

def add_PLEnode(ec,hostname,username,ssh_key):

    node = ec.register_resource("PlanetlabNode")
    ec.set(node, "hostname", hostname)
    ec.set(node, "username", username)
    ec.set(node, "identity", ssh_key)
    return node

def add_app(ec, command, node):
    app = ec.register_resource("LinuxApplication")
    ec.set(app,"command",command)
    ec.register_connection(app, node)
    return app

ec = ExperimentController("geocloud")

identity = "/home/deimos/.ssh/id_rsa"

exp_id = "geocloud"

hosts=["planetlab1.u-strasbg.fr","planetlab1.tlm.unavarra.es","ops.ii.uam.es"]
nodes=[]
for i in hosts:
	nod=ec.register_resource("PlanetlabNode")
	ec.set(nod,"hostname",i)
	ec.set(nod,"username","jbecedas")
	ec.set(nod,"identity",identity)
	nodes.append(nod)

# Create the entity Experiment Controller:
apps = []
#for i in nodes:
#	app = add_app(ec,"ping -c3 nepi.inria.fr",i)
#	apps.append(app)

# Deploy the experiment:
ec.deploy()
ec.trace(nodes[0],"stoudt")
#ec.wait_finished(apps[0])
ec.shutdown()
# Wait until the applications are finish to retrive the traces:
#ec.wait_finished(apps)