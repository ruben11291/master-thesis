#!/usr/bin/env python
#
#    NEPI, a framework to manage network experiments
#    Copyright (C) 2013 INRIA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Lucia Guevgeozian <lucia.guevgeozian_odizzio@inria.fr>

from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState
import os

# Create the EC
exp_id = "example_geo"
ec = ExperimentController(exp_id)

pl_user = "lucia.guevgeozian_odizzio@inria.fr"
pl_password =  os.environ.get("PL_PASS")
slicename = "inria_sfatest"


node1 = ec.register_resource("PlanetlabNode")
ec.set(node1, "hostname", "planetlab2.dit.upm.es")
minBandwidth = X
ec.set(node1, "minBandwidth", minBandwidth)
ec.set(node1, "username", slicename)
ec.set(node1, "pluser", pl_user)
ec.set(node1, "plpassword", pl_password)
ec.set(node1, "cleanHome", True)
ec.set(node1, "cleanProcesses", True)

node2 = ec.register_resource("PlanetlabNode")
ec.set(node2, "country", "Spain")
ec.set(node2, "username", slicename)
ec.set(node2, "pluser", pl_user)
ec.set(node2, "plpassword", pl_password)
ec.set(node2, "cleanHome", True)
ec.set(node2, "cleanProcesses", True)

remote_hostname = ec.get_attribute(node1, "hostname")
destination = "%s@%s" % (slicename, remote_hostname)

app1 = ec.register_resource("LinuxApplication")
file = "../big_file.geo"
ec.set(app1, "sources", file)
command = "scp $SRC/big_file.geo %s" % destination 
ec.set(app1, "command", command)
ec.register_connection(app1, node1)

app2 = ec.register_resource("LinuxApplication")
ec.set(app, "sudo", sudo)
ec.set(app, "depends", "ifstat")
command = "ifstat -b eth0 > ifstat.txt"
command = "iperf ..." 
ec.set(app2, "command", command)
ec.register_connection(app2, node1)

ec.register_condition(app2, ResourceAction.START, app1, ResourceState.STARTED)


# Deploy
ec.deploy()

ec.wait_finished([app1, app2])

trace_file = "examples/planetlab/ifstat.txt"
trace = ec.trace(app2, "ifstat.txt")
f = open(trace_file, "w")
f.write(trace)
f.close()

ec.shutdown()

# End
