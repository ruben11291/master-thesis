Files of this directory

> iperfClients.py: experiments for measuring the bandwidth in the client nodes
> iperfClientsUDP.py:experiment for measuring the loss-rate in the client nodes
> pingClients.py: experiment for measuring the delay in the client nodes
> pingPLE.py: experiment for measuring the delay in the ground stations nodes
> pPLE.py: experiment for measuring the bandwidth in the ground stations nodes
> pPLEUDP.py: experiment for measuring the loss-rate in the ground stations node


> bandwith_plotting_per_ground.py: plotting the bandwidth in the inputs files nodes. With the results1Bandwith_GS_TCP directory
  - it is executed as follows:
      >> python bandwithd_plotting_per_ground.py dir ...
> bandwith_plotting_nodes.py: plotting the bandwith in nodes: With the results4Bandwidth_GS_TCP and results7IPERFCustomersTCP.
--------python bandwidth_plotting_nodes.py results4Bandwidth_GS_TCP results7IPERFCustomersTCP

> loss-rate_plotting_nodes_customers.py: plotting the loss-rate for the customer nodes. With the results8IPERFCustomersUDP.LossRateCustomers.png as result.

> loss-rate_plotting_nodes.py : plotting the loss-rate for the ground stations nodes. With the results1BandwidthUDP. LossRateGS.png as result.

> loss-rate_all.py : it plots the loss-rate of all nodes. The inputs for this script are results1BandwidthUDP and results8IPERFCustomersUDP , respectively.

> bandwith_plotting_per_ground.py: plotting the every ground station bandwidth in histrograms using subplots. The input is the results4Bandwidth_GS_TCP directory.

> delay_plotting_per_ground.py : plotting the delay in hist for the ground station nodes. With the results5PING. Output is DelayHistGS.png

> delay_plotting_nodes.py : plotting the delay in

> bandwidth_plotting_nodes_sin_ordenar.py : not used
