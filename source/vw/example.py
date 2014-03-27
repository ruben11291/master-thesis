#!/usr/bin/env python
import pdb
from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState

import os

def add_node(ec,hostname,username,passwd,ssh_key):

    node = ec.register_resource("LinuxNode")
    ec.set(node, "hostname", hostname)
    ec.set(node, "username", username)
    ec.set(node, "identity", ssh_key)
    ec.set(node, "password", passwd)
    ec.set(node, "cleanHome", True)
    ec.set(node, "cleanProcesses", True)
    return node

def add_app(ec, command, node):
    app = ec.register_resource("LinuxApplication")
    ec.set(app,"command",command)
    ec.register_connection(app, node)
    return app

hostname = "172.18.4.89"
username = "geo-user"
identity = "/home/deimos/.ssh/id_rsa"
password = "deimos_space14"
#pdb.set_trace()
exp_id = "geocloud"

# Create the entity Experiment Controller:
ec = ExperimentController(exp_id)


node = add_node(ec,hostname,username,password,identity)
app = add_app(ec,"ping -c3 google.es",node)


# Deploy the experiment:
ec.deploy()
ec.trace(app,"stdout")
# Wait until the applications are finish to retrive the traces:
ec.wait_finished(apps)
ec.shutdown()
