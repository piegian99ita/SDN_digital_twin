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

Start the VM with multipass or vagrant. Open 4 terminal windows.
In the first terminal window start the topology(everytime we start the network we need to clean the previous mininet instance):
```bash
  cd comnetsemu/SDN_digital_twin
  sudo mn -c 
  sudo python3 topology.py
```
### START THE PHYSICAL CONTROLLER

In order to start the RYU controller type in the second window:

```bash
  cd comnetsemu/SDN_digital_twin
  ryu-manager --observe-links controller.py
```

### START THE DIGITAL TWIN CONTROLLER
In the third window type:
```bash
  ryu-manager --ofp-tcp-listen-port 5544 ryu.app.simple_switch_13
```

### START THE MONITOR

(There's a problem with the linkage of the host: every time we )
In order to start the monitor we can type in the fourth window: 

```bash
  cd comnetsemu/SDN_digital_twin
  sudo python3 monitor.py
```

(This will retrieve the information about the topology and opens up the CLI of Mininet inside the fourth terminal window, if we want to update the network type quit in mininet terminal: in the digital twin one )
