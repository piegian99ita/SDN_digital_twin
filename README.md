# SDN_digital_twin

Creating a digital twin of an SDN network by using mininet, RYU and REST APIs.

(add the method to include comnetsemu)

## CLONE THE REPOSITORY
```bash
  cd comnetsemu
  git clone https://github.com/piegian99ita/SDN_digital_twin
```

## HOW TO USE

### START THE NETWORK

Start the VM with multipass or vagrant. Open 3 terminal windows.
In the first terminal window start the topology:
```bash
  cd comnetsemu/SDN_digital_twin
  sudo python3 topology.py
```
### START THE CONTROLLER

In order to start the RYU controller type in the second window:

```bash
  ryu-manager ryu.app.simple_switch_13 rest_topology
```

### START THE MONITOR

(There's a problem with the third host:it's not detected idk why)
In order to start the monitor we can type in the third window: 

```bash
  cd comnetsemu/SDN_digital_twin
  python3 monitor.py
```

(This will retrieve the information about the topology every 10 seconds and print in the terminal the informations retrieved)
