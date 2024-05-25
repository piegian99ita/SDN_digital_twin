## DIGITAL TWINS IN SDN NETWORKS
 This project explores the application of machine learning for traffic prediction in Software-Defined Networking (SDN) environments. It leverages the following technologies:

 Mininet: A Python library for emulating network topologies, enabling the creation and experimentation with virtual networks.
 Ryu: A popular open-source SDN controller framework, providing the foundation for constructing your custom traffic management and data collection logic.

### START THE NETWORK
 To start our system you need to open 4 terminal windows:
 In the first terminal window start the topology "topo.py"(everytime we start the network we need to clean the previous mininet instance):
 ```bash
   cd comnetsemu/SDN_digital_twin
   sudo mn -c 
   sudo python3 topo.py
 ```
 This will create our main network, where we will get the data and share them with the second network (his digital twin)
 ### START THE PHYSICAL CONTROLLER

 In order to start the RYU controller type in the second window:

 ```bash
   ryu-manager --observe-links controller.py
 ```

 This will enable the devices in the first network to communicate, it will also enable other functionality for the network.
 ### START THE DIGITAL TWIN CONTROLLER
 Start the ryu manager for the second network, the digital twin.
 In the third window type:
 ```bash
   ryu-manager --ofp-tcp-listen-port 5544 ryu.app.simple_switch_13
 ```

 ### START THE MONITOR
 Start the second network.
 (There is a problem if we try to disconnect a link between devices, since the commands don't work and the API doesn't properly work) (working in progress) 
 
 In order to start the monitor we can type in the fourth window: 

 ```bash
   cd comnetsemu/SDN_digital_twin
   sudo python3 monitor2.py
 ```

 (This will retrieve the information about the topology and opens up the CLI of Mininet inside the fourth terminal window, if we want to update the network type quit in mininet terminal: in the digital twin one )
