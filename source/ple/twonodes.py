from nepi.execution.ec import ExperimentController
from nepi.execution.resource import ResourceAction, ResourceState
import os


def create_node(ec, username, pluser, plpass, hostname=None, country=None):

    node = ec.register_resource("PlanetlabNode")

    ec.set(node,"username", username)
    ec.set(node,"pluser", pluser)
    ec.set(node,"plpassword", plpass)
    if hostname:
        ec.set(node,"hostname", hostname)
    if country:
        ec.set(node,"country", country)

    ec.set(node, "cleanHome", True)
    ec.set(node, "cleanProcesses", True)

    return node

def create_app(ec, command, sudo=None, dependencies=None, source=None):

    app = ec.register_resource("LinuxApplication")
    if sudo:
        ec.set(app,"sudo",sudo)
    if dependencies:
        ec.set(app,"depends",dependencies)
    if source:
        ec.set(app,"sources",source)

    ec.set(app,"command",command)
    return app


ec = ExperimentController("test_ple")

username = "ibbtple_geocloud"
pl_user = "jonathan.becedas@elecnor-deimos.com"
pl_password =  "deimos_space14"

source_file = "/user/lguevgeo/home/desarrollo/nepi_3dev/examples/big_buck_bunny_240p_mpeg4_lq.ts"
target_file = "output.txt"

#Host where the BonFIRE cloud will be
host1 = "ple6.ipv6.lip6.fr"
host2 = "planetlab2.utt.fr"


port = 20000
#Creates the BonFIRE node and the application is added
node_server = create_node(ec, username, pl_user, pl_password, hostname=host1)
node_client = create_node(ec, username, pl_user, pl_password, hostname=host2)

command_server = "iperf -s -f m -t 30 -i 1 -p %d -u" %(port)
command_client = "iperf -f m  -c %s  -t 10 -p %d -i 1 -u > %s" % ( host1,port,target_file)

app_server = create_app(ec, command_server, dependencies="iperf")
ec.register_connection(node_server, app_server)

app_client = create_app(ec, command_client, dependencies="iperf", source=source_file)
ec.register_connection(node_client, app_client)

ec.register_condition(app_client, ResourceAction.START, app_server, ResourceState.STARTED)


# Deploy the experiment:
ec.deploy()

ec.wait_finished([app_client])

trace = ec.trace(app_client, target_file)
print trace
f = open("hostout.txt","w")
f.write(trace)
f.close()

ec.shutdown()

