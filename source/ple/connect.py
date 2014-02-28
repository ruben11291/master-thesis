#!/usr/bin/env python
import pdb
from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState
import os

ec = ExperimentController("testple")

# The username in this case is the slice name, the one to use for login in 
# via ssh into PlanetLab nodes. Replace with your own slice name.
hostname = "planetlab1.u-strasbg.fr"
username="wal8il8im88ge_pletest"
ssh_key = "/home/deimos/.ssh/id_rsa"
hostname2=""
username2=""

node = ec.register_resource("PlanetlabNode")
ec.set(node,"hostname",hostname)
ec.set(node,"username",username)
ec.set(node,"identity",ssh_key)

node2 = ec.register_resource("PlanetlabNode")
ec.set(node2,"hostname",hostname2)
ec.set(node2,"username",username2)
ec.set(node,"identity",ssh_key)

ec.register_connection(node2,node)


# Deploy the experiment:
ec.deploy()
ec.trace(node,"stdout")
# Do the experiment controller shutdown:
ec.shutdown()

# END
