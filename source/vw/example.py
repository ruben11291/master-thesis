#!/usr/bin/env python
import pdb
from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState

import os

def add_node(ec,hostname,username,ssh_key):

    node = ec.register_resource("LinuxNode")
    ec.set(node, "hostname", hostname)
    ec.set(node, "username", username)
    ec.set(node, "identity", ssh_key)
    ec.set(node, "cleanHome", True)
    ec.set(node, "cleanProcesses", True)
    return node

def add_app(ec, command, node):
    app = ec.register_resource("LinuxApplication")
    ec.set(app,"command",command)
    ec.register_connection(app, node)
    return app

hostname = "planetlab2.fri.uni-lj.si"
username = "jbecedas"
identity = "</home/deimos/.ssh/id_rsa.pub>"

pdb.set_trace()
exp_id = "geocloud"

# Create the entity Experiment Controller:
ec = ExperimentController(exp_id)

pl_user = "jonathan.becedas@elecnor-deimos.es"

node = add_node(ec,hostname,username,identity)
app = add_app(ec,"ping -c3 nepi.inria.fr",node)


# Deploy the experiment:
ec.deploy()

# Wait until the applications are finish to retrive the traces:
ec.wait_finished(apps)
