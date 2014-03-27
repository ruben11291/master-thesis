#!/usr/bin/env python
import pdb
from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState
import os

def create_node(ec,username,pl_user, pl_password, hostname=None,country=None):
    
    node = ec.register_resource("PlanetlabNode")
    
    if username:
        ec.set(node,"username",username)
    if pl_user:
        ec.set(node,"pluser",pl_user)
    if pl_password:
        ec.

ec = ExperimentController("testple")

# The username in this case is the slice name, the one to use for login in 
# via ssh into PlanetLab no1des. Replace with your own slice name.
hostname1 = "planetlab1.u-strasbg.fr"
hostname2 = "planetlab1.dit.upm.es"
slice = "ibbtple_geocloud"


name1= "wa8il8im88ge"

ssh_key = "/home/deimos/.ssh/id_rsa"
node1 = ec.register_resource("LinuxNode")
ec.set(node1,"hostname",hostname1)
ec.set(node1,"username",name1+"_"+slice1)
ec.set(node1,"identity",ssh_key)

node2 = ec.register_resource("LinuxNode")
ec.set(node2,"hostname",hostname2)
ec.set(node2,"username",name1+"_"+slice2)
ec.set(node2,"identity",ssh_key)

app = ec.register_resource("LinuxApplication")
ec.set(app,"command","ping -c5"+hostname2)
ec.register_connection(app,node1)

app2 = ec.register_resource("LinuxApplication")
ec.set(app2,"command","ping -c5"+hostname1)
ec.register_connection(app2,node2)

# Deploy the experiment:
ec.deploy()
ec.trace(app,"stdout")
ec.trace(app2,"stdout")
ec.wait_finished(app)
ec.wait_finished(app2)
# Do the experiment controller shutdown:
ec.shutdown()

# END
