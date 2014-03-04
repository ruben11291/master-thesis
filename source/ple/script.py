#!/usr/bin/env python
import pdb
from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState

import os

username = "wa8il8im88ge"
hosts ={"China":"planetlab1.buaa.edu.cn","Spain":"planetlab1.uc3m.es","Chile":"planetlab1-santiago.lan.redclara.net","PuertoRico":"planetlab-01.ece.uprm.edu","Argentina":"planet-lab1.itba.edu.ar","Israel":"planet1.cs.huji.ac.il","Brazil":"planetlab1.pop-pa.rnp.br","ReunionIsland":"lim-planetlab-1.univ-reunion.fr","Malaysia":"planetlab1.comp.nus.edu.sg","Canada":"planetlab-1.usask.ca","Australia":"planetlab1.research.nicta.com.au"}

host = "planetlab1.u-strasbg.fr"
slic = "ple"
key ="/home/deimos/.ssh/id_rsa"
nodes=[]

def create_node(ec, user, id_key, hostname):

    node = ec.register_resource("PlanetlabNode")
    ec.set(node, "username", user)
    ec.set(node, "identity", id_key)
    ec.set(node, "hostname", hostname)
    ec.set(node, "cleanHome", True)
    ec.set(node, "cleanProcesses", True)
    ec.set(node, "cleanExperiment",True)

    return node

#pdb.set_trace()

# Create the entity Experiment Controller:
ec = ExperimentController("PLE test")

# for n in hosts:
#     nodes.append(create_node(ec,username+"_"+slic,key,n[1])

node = create_node(ec, username+"_"+slic, key, host)

file = "script.py"

app = ec.register_resource("LinuxApplication")
ec.set(app,"command","ping -c3 nepi.inria.fr")
ec.register_connection(app,node)

app2 = ec.register_resource("LinuxApplication")
ec.set(app2,"sources",file)
ec.set(app2,"command","cat script.py")
ec.register_connection(app2,node)


ec.deploy()
ec.wait_finished(app)
ec.wait_finished(app2)
# Wait until the applications are finish to retrive the traces:
print ec.trace(app,"stdout")
print ec.trace(app2,"stdout")


ec.shutdown()

# END
