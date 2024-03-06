# SDN_digital_twin

Creating a digital twin of an SDN network by using mininet, RYU and REST APIs.

(add the method to include comnetsemu)

## CLONE THE REPOSITORY
```bash
  cd comnetsemu
  git clone https://github.com/Fundamentals-of-robotics/ur5.git
```

## HOW TO USE

Start the VM with multipass or vagrant. Open 3 terminal windows.
In the first terminal window start the topology:
```bash
  cd comnetsemu/SDN_digital_twin
  sudo python3 topology.py
```
In order to start the RYU controller type in the second window:

```bash
  cd comnetsemu/SDN_digital_twin
  ryu-manager controller.py
```

(This script doesn't work because we have to change the controller in order to receive an http request by using the RYU REST APIs: it doen't receive an HTTP response and it remains "blocked")
In order to start the monitor we can type in the third window:

```bash
  cd comnetsemu/SDN_digital_twin
  python3 monitor.py
```
