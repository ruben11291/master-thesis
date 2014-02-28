#!/usr/bin/env python
import pdb
from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState
import os

ec = ExperimentController("testple")

# The username in this case is the slice name, the one to use for login in 
# via ssh into PlanetLab nodes. Replace with your own slice name.
hostname = "planetlab1.u-strasbg.fr"
username="wal8il8im88ge_as"
ssh_key = "/home/deimos/.ssh/id_rsa"
node = ec.register_resource("LinuxNode")
ec.set(node,"hostname",hostname)
ec.set(node,"username",username)
ec.set(node,"identity",ssh_key)

app = ec.register_resource("LinuxApplication")
ec.set(app,"command","ping www.google.es")
ec.register_connection(app,node)


# Deploy the experiment:
ec.deploy()
ec.trace(app,"stdout")
# Do the experiment controller shutdown:
ec.shutdown()

# END
