 # Digital Twins in SDN Networks
 
 This project explores the creation of a real-time digital twin for network management in Software-Defined Networking (SDN) environments. It leverages the following technologies:

 - **Mininet**: A Python library for emulating network topologies, enabling the creation and experimentation with virtual networks.
 - **Ryu**: A popular open-source SDN controller framework, providing the foundation for constructing custom traffic management and data collection logic.

 ## Getting Started

 To start our system, you need to open 4 terminal windows. We recommend using `tmux` to parallelize the environment effectively.

 ### Terminal 1: Start the Topology

 In the first terminal window, start the topology `topo.py` (every time we start the network, we need to clean the previous Mininet instance):

 ```bash
 cd comnetsemu/SDN_digital_twin
 sudo mn -c 
 sudo python3 topo.py
 ```

 This will create our main network, where we will get the data and share them with the second network (his digital twin)
 ### Terminal 2: start the physical controller

 In order to start the RYU controller type in the second window:

 ```bash
   ryu-manager --observe-links controller.py
 ```

 This will enable the devices in the first network to communicate, it will also enable other functionality for the network.
 ### Terminal 3: start the digital twin's controller
 Start the ryu manager for the second network, the digital twin.
 In the third window type:
 ```bash
   ryu-manager --ofp-tcp-listen-port 5544 ryu.app.simple_switch_13
 ```

 ### Terminal 4: start the monitor(digital twin)
 Start the second network.
 (There is a problem if we try to disconnect a link between devices, since the commands don't work and the API doesn't properly work) (working in progress) 
 
 In order to start the monitor we can type in the fourth window: 

 ```bash
   cd comnetsemu/SDN_digital_twin
   sudo python3 monitor2.py
 ```

 (This will retrieve the information about the topology and opens up the CLI of Mininet inside the fourth terminal window, if we want to update the network type quit in mininet terminal: in the digital twin one )
